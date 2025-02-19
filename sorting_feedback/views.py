
from .evaluation import evaluate_code
import json

from django.contrib.auth.decorators import login_required
from .models import Submission, Evaluation
from django.shortcuts import render
import logging
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import EvaluationCriteria, Evaluation
import ast
import subprocess
from django.contrib.auth.models import User  # Ensure the User model is imported
import logging
from difflib import SequenceMatcher
from django.db.models import Q
import os
import chardet  # For detecting file encoding
from .utils import *
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.contrib import messages
from .models import DeadlineExtensionLog  
from django.core.mail import send_mail
from django.utils.timezone import localtime

from .forms import SubmissionDeadlineForm

logger = logging.getLogger(__name__)

def home(request):
    user = request.user
    is_logged_in = user.is_authenticated
    return render(request, 'home.html', {'is_logged_in': is_logged_in, 'user': user})
    


def assessmentchoice(request):
    return render(request, 'assessment_choice.html')



def calculate_similarity(code1, code2):
    """Calculate similarity using SequenceMatcher (Levenshtein-like)."""
    return SequenceMatcher(None, code1, code2).ratio() * 100  # Convert to percentage

def check_plagiarism(new_code, student):
    """Check plagiarism by comparing new submission with previous ones."""
    existing_submissions = Evaluation.objects.exclude(student=student)  # Exclude current student's own work
    max_similarity = 0  # Store the highest similarity score

    for submission in existing_submissions:
        similarity = calculate_similarity(new_code, submission.student_code)
        if similarity > max_similarity:
            max_similarity = similarity

    return max_similarity  # Return highest similarity score



def evaluate_code_with_criteria(code, criteria):
    feedback = []
    correctness = True  # Default to True, adjust based on conditions

    try:
        tree = ast.parse(code)
    except SyntaxError as syntax_error:
        feedback.append(f"Syntax error: {syntax_error}")
        return {
            "feedback": "\n".join(feedback),
            "correctness": False,
            "time_complexity": "Not Applicable",
            "strengths": {},
            "weaknesses": {},
            "detected_constructs": [],  
            "missing_constructs": [],   
        }

    strengths = {}
    weaknesses = {}

    # ✅ Syntax Check
    if criteria.check_syntax:
        try:
            compile(code, "<string>", "exec")
            feedback.append("✅ Syntax is correct!")
            strengths["Syntax"] = "Great job! Your syntax is correct and well-structured. Keep up the good work! 🎯"
        except Exception as exec_error:
            feedback.append(f"⚠️ Syntax error: {exec_error}")
            weaknesses["Syntax"] = "Your code contains syntax errors. Please check and fix them."
            correctness = False  # If syntax is incorrect, mark correctness as False

    # ✅ Indentation Check
    if criteria.check_indentation:
        lines = code.split("\n")
        for line_no, line in enumerate(lines, start=1):
            stripped = line.lstrip()
            if not stripped or stripped.startswith("#"):
                continue  # Skip blank lines and comments
            
            leading_spaces = len(line) - len(stripped)
            if leading_spaces % 4 != 0:
                feedback.append(f"⚠️ Line {line_no}: Indentation should be a multiple of 4 spaces.")
                weaknesses["Indentation"] = "Your code has incorrect indentation. Ensure you use multiples of 4 spaces."
                correctness = False  # Incorrect indentation affects correctness

    # ✅ Comment Check
    if criteria.check_comments:
        comment_count = sum(1 for line in code.split("\n") if line.strip().startswith("#"))
        if comment_count < criteria.min_comments:
            feedback.append(f"⚠️ Insufficient comments. Found {comment_count}, but at least {criteria.min_comments} required.")
            weaknesses["Comments"] = "Your code lacks sufficient comments. Aim for more explanations."
        else:
            feedback.append(f"✅ Comments are sufficient: {comment_count} comment(s).")
            strengths["Comments"] = "Great job! Your code is well-commented, making it easier to understand. 💡"

    # ✅ Construct Validation
    detected_constructs = detect_constructs(code)  # Detect constructs
    missing_constructs = []

    for required_construct in criteria.required_constructs:
        if required_construct.lower() not in detected_constructs:
            missing_constructs.append(required_construct)

    if missing_constructs:
        feedback.append(f"⚠️ Required constructs missing: {', '.join(missing_constructs)}.")
        for construct in missing_constructs:
            weaknesses[construct] = f"The required construct '{construct}' is missing. Please include it."
        correctness = False  # Missing constructs make correctness False
    else:
        feedback.append("✅ All required constructs are present.")
        strengths["Constructs"] = "Well done! You've included all necessary constructs. 🏆"

    return {
        "feedback": "\n".join(feedback),
        "correctness": correctness,  # Correctness now considers missing constructs
        "time_complexity": "Not Applicable",
        "strengths": strengths,
        "weaknesses": weaknesses,
        "detected_constructs": detected_constructs,  
        "missing_constructs": missing_constructs,  
    }


@login_required
def submit_code(request):
    if request.method == "POST":
        submission_file = request.FILES.get("submission_file")
        student = request.user

        if not submission_file:
            return render(request, "feedback_result.html", {
                "success": False,
                "error": "Submission file is required."
            })

        # Detect file encoding and read content
        raw_data = submission_file.read()
        encoding = chardet.detect(raw_data)["encoding"]
        file_content = raw_data.decode(encoding or "utf-8").strip()

        # Get evaluation criteria
        criteria = EvaluationCriteria.objects.first()

        if not criteria:
            return render(request, "feedback_result.html", {
                "success": False,
                "error": "No evaluation criteria set by the tutor."
            })
        
        # Check submission deadline
        if criteria.submission_deadline and now() > criteria.submission_deadline:
            return render(request, "feedback_result.html", {
                "success": False,
                "error": "The submission deadline has passed. You can no longer submit."
            })

        required_constructs = criteria.required_constructs  # Fetch required constructs dynamically
        title = ", ".join(required_constructs)  # Use required constructs as title

        # Check if the student has already submitted for this set of constructs
        existing_submission = Evaluation.objects.filter(student=student, title=title).exists()
        if existing_submission:
            return render(request, "feedback_result.html", {
                "success": False,
                "error": "You have already submitted for these required constructs."
            })

        # Check plagiarism: Flag if another student has submitted the same code
        similar_submission = Evaluation.objects.filter(~Q(student=student), student_code=file_content).exists()
        plagiarism_score = 100.0 if similar_submission else check_plagiarism(file_content, student)
        is_plagiarized = plagiarism_score > 50  # Mark as plagiarized if similarity > 50%

        # Evaluate the code
        raw_feedback = evaluate_code_with_criteria(file_content, criteria)
        print("DEBUG: Raw Feedback from Evaluation ->", raw_feedback)

        # Ensure feedback is a dictionary
        try:
            feedback = json.loads(raw_feedback) if isinstance(raw_feedback, str) else raw_feedback
        except json.JSONDecodeError:
            print("ERROR: Could not parse feedback as JSON. Defaulting to plain text.")
            feedback = {"feedback": raw_feedback, "strengths": {}, "weaknesses": {}}
        
 
        missing_constructs = feedback.get("missing_constructs", [])
        # Automatically assign grading based on evaluation
        grade = assign_grade(feedback.get("correctness", 0) * 100, plagiarism_score, missing_constructs)

        # Save evaluation to the database
        evaluation = Evaluation.objects.create(
            title=title,
            student=student,
            student_code=file_content,
            submission_file=submission_file,
            feedback=feedback["feedback"],
            correctness=feedback.get("correctness", 0),
            time_complexity=feedback.get("time_complexity", 0),
            plagiarism_score=plagiarism_score,
            is_plagiarized=is_plagiarized,
            grade=grade,
            status='submitted'
        )

        # Update Student Performance
        student_performance, created = StudentPerformance.objects.get_or_create(student=student)
        student_performance.update_performance(evaluation)
        
        return render(request, "feedback_result.html", {
            "success": True,
            "feedback": feedback["feedback"],
            "plagiarism_score": plagiarism_score,
            "is_plagiarized": is_plagiarized,
            "evaluation": evaluation
        })

    return redirect('submit_assignment')


@login_required
def dashboard(request):
    submissions = Submission.objects.filter(user=request.user).select_related('evaluation')
    return render(request, 'dashboard.html', {"submissions": submissions})



@login_required
def analytics(request):
    user = request.user
    submissions = Submission.objects.filter(user=user)
    evaluations = Evaluation.objects.filter(submission__in=submissions)

    total_submissions = submissions.count()
    correct_submissions = evaluations.filter(correctness=True).count()
    incorrect_submissions = total_submissions - correct_submissions

    return render(request, "analytics.html", {
        "total_submissions": total_submissions,
        "correct_submissions": correct_submissions,
        "incorrect_submissions": incorrect_submissions,
    })


def evaluations_list(request):
    evaluations = Evaluation.objects.all()
    context = {
        'evaluations': evaluations
    }
    return render(request, 'evaluations_list.html', context)


@login_required
def student_submitted_assignment(request):
    # Get the currently logged-in user
    current_user = request.user

    # Fetch evaluations submitted by the current user
    evaluations = Evaluation.objects.filter(student=current_user)

    return render(request, 'accounts/student_submitted_assignment.html', {'evaluations': evaluations})



@login_required
def extend_deadline(request, criteria_id):



    total_students = User.objects.filter(profile__role='student').count()
    evaluations = Evaluation.objects.all().count()
    pending_evaluations = Evaluation.objects.filter(status='pending').count()

    criteria = get_object_or_404(EvaluationCriteria, id=criteria_id)

    # evaluation = get_object_or_404(EvaluationCriteria, id=evaluation_id)

     # Your logic to extend the deadline
    # evaluation.deadline += timedelta(days=7)  # Example: Extend by 7 days
    # evaluation.save()

    # Ensure only the tutor who created the criteria can update it
    if request.user != criteria.created_by:
        messages.error(request, "You are not authorized to extend this deadline.")
        return redirect("dashboard_t")  # Change to the appropriate redirect

    if request.method == "POST":
        form = SubmissionDeadlineForm(request.POST, instance=criteria)
        if form.is_valid():
            old_deadline = criteria.submission_deadline  # Store old deadline
            form.save()
            new_deadline = criteria.submission_deadline  # Get new deadline

          
            # Log the deadline change
            DeadlineExtensionLog.objects.create(
                tutor=request.user,
                criteria=criteria,
                old_deadline=old_deadline,
                new_deadline=new_deadline
            )

            # Send notification email (as implemented earlier)
            students = User.objects.filter(groups__name="Students")
            # print(stu)
            student_emails = [student.email for student in students if student.email]

            

            if student_emails:
                formatted_deadline = new_deadline.strftime("%B %d, %Y %I:%M %p")
                send_mail(
                    subject="Submission Deadline Changed",
                    message=f"Dear Student,\n\nThe deadline for '{criteria.title}' has been extended to {formatted_deadline}. "
                            f"Please ensure your submission is completed before this deadline.\n\n"
                            f"Best regards,\nFeedback Generator Team",
                    from_email='ochinell@outlook.com',
                    recipient_list=student_emails,
                    fail_silently=True,
                )
            # print("DEFAULT_FROM_EMAIL", DEFAULT_FROM_EMAIL)
            # print("formatted_deadline", formatted_deadline)

            messages.success(request, "Submission deadline updated and students notified.")
            return redirect("extend_deadline", criteria_id=criteria.id)

    else:
        form = SubmissionDeadlineForm(instance=criteria)
    
    context = {
        "total_students": total_students,
        "assignments_submitted": evaluations,
        "pending_evaluations": pending_evaluations,
        "criteria" : criteria,
        "form" : form
    }

    return render(request, "accounts/extend_deadline.html", context)

    


    return render(request, "accounts/extend_deadline.html", context)


def custom_404_view(request, exception):
    return render(request, 'errors/404.html', status=404)

def custom_500_view(request):
    return render(request, 'errors/500.html', status=500)


    
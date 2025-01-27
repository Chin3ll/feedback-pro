import cohere
from .evaluation import evaluate_code
from .gpt_feedback import generate_feedback

from django.contrib.auth.decorators import login_required
from .models import Submission, Evaluation
from django.shortcuts import render
import logging
from django.http import JsonResponse
from .utils import generate_feedback
from django.shortcuts import get_object_or_404
from .models import EvaluationCriteria, Evaluation
import ast
import subprocess
from django.contrib.auth.models import User  # Ensure the User model is imported

# Initialize Cohere client
co = cohere.Client('ZIFDjiIznKChVeU5Q1v2z25sKYTI8nQFTV5Q4MYL')  # Replace with your API key


def home(request):
    user = request.user
    is_logged_in = user.is_authenticated
    return render(request, 'home.html', {'is_logged_in': is_logged_in, 'user': user})
    


def assessmentchoice(request):
    return render(request, 'assessment_choice.html')


@login_required
def generate_feedback(prompt):
    try:
        response = co.generate(
            model='xlarge',
            prompt=prompt,
            max_tokens=100
        )
        return response.generations[0].text
    except AttributeError as e:
        # Log the error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error in generate_feedback: {e}")
        raise e
    except Exception as e:
        # Catch all other exceptions
        raise e

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
@login_required



def evaluate_code(submission_code):
    feedback = {
        "feedback": [],
        "correctness": True
    }

    # Fetch active criteria
    active_criteria = EvaluationCriteria.objects.filter(is_active=True).values_list('name', flat=True)

    # Syntax Check
    if "Syntax Check" in active_criteria:
        try:
            ast.parse(submission_code)  # Parse the code to check syntax
            feedback["feedback"].append("Code has valid syntax.")
        except SyntaxError as e:
            feedback["feedback"].append(f"Syntax error: {e.msg} at line {e.lineno}.")
            feedback["correctness"] = False

    # Indentation Check
    if "Indentation Check" in active_criteria:
        lines = submission_code.split("\n")
        for i, line in enumerate(lines):
            if line and not line.startswith(" ") and line != line.lstrip():
                feedback["feedback"].append(f"Improper indentation at line {i + 1}: Use multiples of 4 spaces.")
                feedback["correctness"] = False
                break

    # Comment Check
    if "Comment Check" in active_criteria:
        if "#" not in submission_code:
            feedback["feedback"].append("Code lacks comments. Consider adding comments for clarity.")

    return feedback

def evaluate_code_with_criteria(code, criteria):
    import ast
    feedback = []
    correctness = True

    # Check Syntax
    if criteria.check_syntax:
        try:
            ast.parse(code)  # Parse the code for syntax errors
            feedback.append("Syntax is correct.")
            
            # Additional Compilation Check
            try:
                compile(code, "<string>", "exec")
            except Exception as exec_error:
                feedback.append(f"Code compilation error: {exec_error}")
                correctness = False
        except SyntaxError as syntax_error:
            feedback.append(f"Syntax error: {syntax_error}")
            correctness = False

    # Check Indentation
    if criteria.check_indentation:
        lines = code.split("\n")
        indentation_stack = [0]
        for line_no, line in enumerate(lines, start=1):
            stripped = line.lstrip()
            if not stripped or stripped.startswith("#"):
                continue  # Skip blank lines and comments
            
            leading_spaces = len(line) - len(stripped)

            if leading_spaces % 4 != 0:
                feedback.append(f"Line {line_no}: Indentation should be a multiple of 4 spaces.")
                correctness = False

            if stripped.endswith(":"):
                if leading_spaces > indentation_stack[-1]:
                    indentation_stack.append(leading_spaces)
                else:
                    feedback.append(f"Line {line_no}: Expected increased indentation for a block after ':'.")
                    correctness = False
            else:
                while indentation_stack and leading_spaces < indentation_stack[-1]:
                    indentation_stack.pop()

                if leading_spaces != indentation_stack[-1] and len(indentation_stack) > 1:
                    feedback.append(f"Line {line_no}: Misaligned indentation.")
                    correctness = False

    # Check Comments
    if criteria.check_comments:
        comment_count = sum(1 for line in code.split("\n") if line.strip().startswith("#"))
        if comment_count < criteria.min_comments:
            feedback.append(f"Insufficient comments. Found {comment_count}, but at least {criteria.min_comments} required.")
            correctness = False
        else:
            feedback.append(f"Comments are sufficient: {comment_count} comment(s).")

    return {
        "feedback": "\n".join(feedback),
        "correctness": correctness,
        "time_complexity": "Not Applicable"
    }


@login_required
def submit_code(request):
    if request.method == "POST":
        try:
            title = request.POST.get('title', '').strip()
            submission_code = request.POST.get('submission_code', '').strip()
            student = request.user

            if not title:
                return JsonResponse({"success": False, "error": "Title is required."})
            if not submission_code:
                return JsonResponse({"success": False, "error": "Submission code is required."})

            # Get evaluation criteria
            criteria = get_object_or_404(EvaluationCriteria, pk=1)  # Assuming a single criteria instance

            # Evaluate the code
            feedback = evaluate_code_with_criteria(submission_code, criteria)

            # Save evaluation to the database
            evaluation = Evaluation.objects.create(
                title=title,
                student=student,
                student_code=submission_code,
                feedback=feedback["feedback"],
                correctness=feedback["correctness"],
                time_complexity=feedback["time_complexity"],
                status='submitted'
            )

            return render(request, "feedback_result.html", {
                "success": True,
                "feedback": feedback["feedback"],
                "evaluation": evaluation
            })

        except Exception as e:
            logger.error(f"Error during code submission: {e}")
            return render(request, "feedback_result.html", {"success": False, "error": str(e)})

    return render(request, "submit_code_form.html")

# @login_required
# def submit_code(request):
#     if request.method == "POST":
#         try:
#             # Retrieve POST data
#             title = request.POST.get('title', '').strip()
#             submission_code = request.POST.get('submission_code', '').strip()
#             student = request.user  # Current logged-in user
            
#             if not title:
#                 return JsonResponse({"success": False, "error": "Title is required."})
#             if not submission_code:
#                 return JsonResponse({"success": False, "error": "Submission code is required."})

#             logger.debug(f"Submission Title: {title}")
#             logger.debug(f"Submission Code: {submission_code}")

#             # Evaluate the code
#             feedback = evaluate_code(submission_code)
#             feedback_message = feedback.get('feedback', 'No feedback available.')
#             correctness = feedback.get('correctness', False)
#             time_complexity = feedback.get('time_complexity', "Unknown")

#             # Generate GPT-style feedback
#             gpt_feedback = "No GPT feedback available."
#             try:
#                 prompt = f"Evaluate the following sorting algorithm implementation:\n{submission_code}"
#                 gpt_feedback = generate_feedback(prompt)
#             except Exception as e:
#                 gpt_feedback = f"An error occurred while generating GPT feedback: {str(e)}"
#                 logger.error(f"GPT feedback generation error: {e}")

#             # Save evaluation to the database
#             evaluation = Evaluation.objects.create(
#                 title=title,
#                 student=student,
#                 student_code=submission_code,
#                 feedback=feedback_message,
#                 gpt_feedback=gpt_feedback,
#                 correctness=correctness,
#                 time_complexity=time_complexity,
#                 status='submitted'  # Default status on submission
#             )

#             logger.debug(f"Evaluation saved: {evaluation}")

#             # Render feedback result page
#             return render(request, "feedback_result.html", {
#                 "success": True,
#                 "feedback": feedback_message,
#                 "gpt_feedback": gpt_feedback,
#                 "evaluation": evaluation
#             })

#         except Exception as e:
#             logger.error(f"Error during code submission: {e}")
#             return render(request, "feedback_result.html", {
#                 "success": False,
#                 "error": str(e)
#             })
#     else:
#         # Render the code submission form
#         return render(request, "feedback_result.html")




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
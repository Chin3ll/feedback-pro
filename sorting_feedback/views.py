
from .evaluation import evaluate_code

from django.contrib.auth.decorators import login_required
from .models import Submission, Evaluation
from django.shortcuts import render
import logging
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import EvaluationCriteria, Evaluation
import ast
import subprocess
from django.contrib.auth.models import User  # Ensure the User model is imported
import logging
logger = logging.getLogger(__name__)

def home(request):
    user = request.user
    is_logged_in = user.is_authenticated
    return render(request, 'home.html', {'is_logged_in': is_logged_in, 'user': user})
    


def assessmentchoice(request):
    return render(request, 'assessment_choice.html')


# @login_required
# def generate_feedback(prompt):
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

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# @login_required



# def evaluate_code(submission_code):
#     feedback = {
#         "feedback": [],
#         "correctness": True
#     }

#     # Fetch active criteria
#     active_criteria = EvaluationCriteria.objects.filter(is_active=True).values_list('name', flat=True)

#     # Syntax Check
#     if "Syntax Check" in active_criteria:
#         try:
#             ast.parse(submission_code)  # Parse the code to check syntax
#             feedback["feedback"].append("Code has valid syntax.")
#         except SyntaxError as e:
#             feedback["feedback"].append(f"Syntax error: {e.msg} at line {e.lineno}.")
#             feedback["correctness"] = False

#     # Indentation Check
#     if "Indentation Check" in active_criteria:
#         lines = submission_code.split("\n")
#         for i, line in enumerate(lines):
#             if line and not line.startswith(" ") and line != line.lstrip():
#                 feedback["feedback"].append(f"Improper indentation at line {i + 1}: Use multiples of 4 spaces.")
#                 feedback["correctness"] = False
#                 break

#     # Comment Check
#     if "Comment Check" in active_criteria:
#         if "#" not in submission_code:
#             feedback["feedback"].append("Code lacks comments. Consider adding comments for clarity.")

#     return feedback

# import ast

def evaluate_code_with_criteria(code, criteria):
    feedback = []
    correctness = True

    try:
        tree = ast.parse(code)  # Parse the code for syntax errors
    except SyntaxError as syntax_error:
        feedback.append(f"Syntax error: {syntax_error}")
        return {
            "feedback": "\n".join(feedback),
            "correctness": False,
            "time_complexity": "Not Applicable"
        }

    # Syntax Check
    if criteria.check_syntax:
        try:
            compile(code, "<string>", "exec")
            feedback.append("Code has valid syntax.")
        except Exception as exec_error:
            feedback.append(f"Code compilation error: {exec_error}")
            correctness = False

    # Indentation Check
    if criteria.check_indentation:
        lines = code.split("\n")
        for line_no, line in enumerate(lines, start=1):
            stripped = line.lstrip()
            if not stripped or stripped.startswith("#"):
                continue  # Skip blank lines and comments
            
            leading_spaces = len(line) - len(stripped)

            if leading_spaces % 4 != 0:
                feedback.append(f"Line {line_no}: Indentation should be a multiple of 4 spaces.")
                correctness = False

    # Comment Check
    if criteria.check_comments:
        comment_count = sum(1 for line in code.split("\n") if line.strip().startswith("#"))
        if comment_count < criteria.min_comments:
            feedback.append(f"Insufficient comments. Found {comment_count}, but at least {criteria.min_comments} required.")
            correctness = False
        else:
            feedback.append(f"Comments are sufficient: {comment_count} comment(s).")

    # **Construct Validation: Ensure Required Constructs Exist**
    construct_mapping = {
        "while loop": ast.While,
        "for loop": ast.For,
        "function": ast.FunctionDef,
        "lambda function": ast.Lambda,
        "list comprehension": ast.ListComp,
        "dictionary comprehension": ast.DictComp,
        "set comprehension": ast.SetComp,
        "try-except": ast.Try,
        "class": ast.ClassDef,
        "assignment": ast.Assign,
        "return statement": ast.Return,
        "if statement": ast.If,
        "import statement": ast.Import,
        "import from": ast.ImportFrom,
        "dictionary": ast.Dict,
        "list": ast.List,
        "tuple": ast.Tuple,
        "set": ast.Set
    }

    missing_constructs = []
    
    for required_construct in criteria.required_constructs:
        construct_node = construct_mapping.get(required_construct.lower())

        if construct_node:
            if not any(isinstance(node, construct_node) for node in ast.walk(tree)):
                missing_constructs.append(required_construct)
        else:
            feedback.append(f"Warning: '{required_construct}' is not a recognized construct.")

    if missing_constructs:
        feedback.append(f"Error: The code must contain the following construct(s): {', '.join(missing_constructs)}.")
        correctness = False

    if correctness:
        feedback.append("Code evaluation successful.")

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

            # Get the latest evaluation criteria set by the tutor
            criteria = EvaluationCriteria.objects.order_by('-last_updated').first()
            if not criteria:
                return JsonResponse({"success": False, "error": "No evaluation criteria set."})

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
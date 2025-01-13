import cohere
from .evaluation import evaluate_code
from .gpt_feedback import generate_feedback

from django.contrib.auth.decorators import login_required
from .models import Submission, Evaluation
from django.shortcuts import render
import logging
from django.http import JsonResponse
from .utils import generate_feedback
from .models import Evaluation


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


@login_required
def submit_code(request):
    if request.method == "POST":
        try:
            # Retrieve POST data
            title = request.POST.get('title', '').strip()
            submission_code = request.POST.get('submission_code', '').strip()
            student = request.user  # Current logged-in user
            
            if not title:
                return JsonResponse({"success": False, "error": "Title is required."})
            if not submission_code:
                return JsonResponse({"success": False, "error": "Submission code is required."})

            logger.debug(f"Submission Title: {title}")
            logger.debug(f"Submission Code: {submission_code}")

            # Evaluate the code
            feedback = evaluate_code(submission_code)
            feedback_message = feedback.get('feedback', 'No feedback available.')
            correctness = feedback.get('correctness', False)
            time_complexity = feedback.get('time_complexity', "Unknown")

            # Generate GPT-style feedback
            gpt_feedback = "No GPT feedback available."
            try:
                prompt = f"Evaluate the following sorting algorithm implementation:\n{submission_code}"
                gpt_feedback = generate_feedback(prompt)
            except Exception as e:
                gpt_feedback = f"An error occurred while generating GPT feedback: {str(e)}"
                logger.error(f"GPT feedback generation error: {e}")

            # Save evaluation to the database
            evaluation = Evaluation.objects.create(
                title=title,
                student=student,
                student_code=submission_code,
                feedback=feedback_message,
                gpt_feedback=gpt_feedback,
                correctness=correctness,
                time_complexity=time_complexity,
                status='submitted'  # Default status on submission
            )

            logger.debug(f"Evaluation saved: {evaluation}")

            # Render feedback result page
            return render(request, "feedback_result.html", {
                "success": True,
                "feedback": feedback_message,
                "gpt_feedback": gpt_feedback,
                "evaluation": evaluation
            })

        except Exception as e:
            logger.error(f"Error during code submission: {e}")
            return render(request, "feedback_result.html", {
                "success": False,
                "error": str(e)
            })
    else:
        # Render the code submission form
        return render(request, "feedback_result.html")




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
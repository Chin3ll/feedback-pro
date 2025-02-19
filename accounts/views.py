from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()
from .forms import ChangeUsernamePasswordForm
from sorting_feedback.models import Evaluation, EvaluationCriteria
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from .utils import execute_code_safely  # Import the execution function
from sorting_feedback.models import StudentPerformance, Evaluation



def logout_required(view_func):
    return user_passes_test(lambda user: not user.is_authenticated, login_url='home')(view_func)




@login_required
def change_credentials(request):
    user = request.user

    if request.method == "POST":
        form = ChangeUsernamePasswordForm(request.POST, instance=user)
        if form.is_valid():
            new_username = form.cleaned_data.get("username")
            new_password = form.cleaned_data.get("password")

            # Update username across all models if changed
            if new_username and new_username != user.username:
                # Update all models where the username is stored
                Evaluation.objects.filter(student__username=user.username).update(student__username=new_username)
                # Add other models as needed

                user.username = new_username

            # Update password if provided
            if new_password:
                user.set_password(new_password)

            user.save()
            update_session_auth_hash(request, user)  # Keep user logged in after password change

            messages.success(request, "Your credentials have been updated successfully.")
            return redirect("profile")  # Redirect to the profile page

    else:
        form = ChangeUsernamePasswordForm(instance=user)

    return render(request, "accounts/change_credentials.html", {"form": form})



def submit_assignment(request):
    # Fetch the latest evaluation criteria
    criteria = EvaluationCriteria.objects.order_by('-last_updated').first()

    return render(request, 'dashboard-submit-assignment.html', {
        'criteria': criteria
    })

def manage_users(request):
    return render(request, 'manage_users.html')

@login_required
def check_student_assignments(request):
    # Fetch all submitted evaluations
    evaluations = Evaluation.objects.filter(status='submitted')

    return render(request, 'evaluations_list.html', {'evaluations': evaluations})




@login_required
def dashboard_a(request):
   

    total_students = User.objects.filter(profile__role='student').count()
    evaluations = Evaluation.objects.all().count()
    pending_evaluations = Evaluation.objects.filter(status='pending').count()
    
    context = {
        "total_students": total_students,
        "assignments_submitted": evaluations,
        "pending_evaluations": pending_evaluations
    }
    
   
    return render(request, "accounts/dashboard-a.html", context)



@login_required
def dashboard_student_assignment_submission(request):
    # Dummy data for demonstration
    # stats = {
    #     "total_students": 120,
    #     "assignments_submitted": 75,
    #     "pending_approvals": 18,
    # }
    
    # recent_submissions = [
    #     {"id": 1, "student_name": "John Doe", "assignment": "Sorting Algorithm", "submitted_on": "2025-01-01", "status": "Approved"},
    #     {"id": 2, "student_name": "Jane Smith", "assignment": "Bubble Sort", "submitted_on": "2025-01-02", "status": "Pending"},
    #     {"id": 3, "student_name": "Mike Brown", "assignment": "Merge Sort", "submitted_on": "2025-01-03", "status": "Rejected"},
    # ]
    
    # context = {
    #     "stats": stats,
    #     "recent_submissions": recent_submissions,
    # }
    
    return render(request, "dashboard-submit-assignment.html")    

@login_required
def dashboard_t(request):
  
  
    total_students = User.objects.filter(profile__role='student').count()
    evaluations = Evaluation.objects.all().count()
    pending_evaluations = Evaluation.objects.filter(status='pending').count()

    # Fetch the latest evaluation criteria
    criteria = EvaluationCriteria.objects.order_by('-last_updated').first()

   
    
    context = {
        "total_students": total_students,
        "assignments_submitted": evaluations,
        "pending_evaluations": pending_evaluations,
        "criteria" : criteria
    }
    
    
    return render(request, "accounts/dashboard-t.html", context)


@login_required
def dashboard_s(request):
    # Dummy data for demonstration
    # stats = {
    #     "total_students": 120,
    #     "assignments_submitted": 75,
    #     "pending_approvals": 18,
    # }
    
    # recent_submissions = [
    #     {"id": 1, "student_name": "John Doe", "assignment": "Sorting Algorithm", "submitted_on": "2025-01-01", "status": "Approved"},
    #     {"id": 2, "student_name": "Jane Smith", "assignment": "Bubble Sort", "submitted_on": "2025-01-02", "status": "Pending"},
    #     {"id": 3, "student_name": "Mike Brown", "assignment": "Merge Sort", "submitted_on": "2025-01-03", "status": "Rejected"},
    # ]
    
    total_students = User.objects.filter(profile__role='student').count()
    
    current_user = request.user

    # Fetch evaluations submitted by the current user
    evaluations = Evaluation.objects.filter(student=current_user)

    context = {
        "total_students": total_students,
        # "stats": stats,
        # "recent_submissions": recent_submissions,
    }
    
    return render(request, 'accounts/student_submitted_assignment.html', {'evaluations': evaluations})   

@logout_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Redirect to the profile page
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile(request):
    user = request.user
    is_logged_in = user.is_authenticated
    return render(request, 'accounts/profile.html', {'is_logged_in': is_logged_in, 'user': user})




def students_list(request):
    # Get all students
    students = User.objects.filter(profile__role='student')
    return render(request, 'accounts/students_list.html', {'students': students})


def users_list(request):
    # Get all users
    users = User.objects.all()
    return render(request, 'accounts/users_list.html', {'users': users})


def evaluation_report(request, evaluation_id):
    # Fetch evaluation object by ID for the logged-in student
    evaluation = get_object_or_404(Evaluation, id=evaluation_id, student=request.user)

    # Get student performance for this evaluation
    # student_performance = StudentPerformance.objects.filter(evaluation=evaluation).first()

    # Run the submitted code and get output
    execution_result = execute_code_safely(evaluation.student_code)


    return render(request, 'student-assignment-report.html', {
        'execution_result': execution_result,  # Include execution output in context
        'evaluation': evaluation,
        "strengths": student_performance.strengths if student_performance else {},
        "weaknesses": student_performance.weaknesses if student_performance else {},
        "overall_performance": student_performance.overall_performance if student_performance else "No data available",
    })


@login_required
def pending_evaluations_list(request):
    # Fetch all pending evaluations
    evaluations = Evaluation.objects.filter(status='pending')

    return render(request, 'pending_evaluations_list.html', {'evaluations': evaluations})


class CustomPasswordResetView(PasswordResetView):
    template_name = "resetPassword/password_reset.html"  # Ensure this template exists
    email_template_name = "resetPassword/password_reset_email.html"  # Ensure this template exists
    subject_template_name = "resetPassword/password_reset_subject.txt"  # Ensure this template exists
    success_url = reverse_lazy("password_reset_done")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        context["protocol"] = "https" if request.is_secure() else "http"
        context["domain"] = get_current_site(request).domain
        return context
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
User = get_user_model()
from sorting_feedback.models import Evaluation


def submit_assignment(request):
    return render(request, 'dashboard-submit-assignment.html')

def manage_users(request):
    return render(request, 'manage_users.html')

@login_required
def check_student_assignments(request):
    # Fetch all submitted evaluations
    evaluations = Evaluation.objects.filter(status='submitted')

    return render(request, 'evaluations_list.html', {'evaluations': evaluations})


from django.contrib.auth.decorators import login_required

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
    stats = {
        "total_students": 120,
        "assignments_submitted": 75,
        "pending_approvals": 18,
    }
    
    recent_submissions = [
        {"id": 1, "student_name": "John Doe", "assignment": "Sorting Algorithm", "submitted_on": "2025-01-01", "status": "Approved"},
        {"id": 2, "student_name": "Jane Smith", "assignment": "Bubble Sort", "submitted_on": "2025-01-02", "status": "Pending"},
        {"id": 3, "student_name": "Mike Brown", "assignment": "Merge Sort", "submitted_on": "2025-01-03", "status": "Rejected"},
    ]
    
    context = {
        "stats": stats,
        "recent_submissions": recent_submissions,
    }
    
    return render(request, "dashboard-submit-assignment.html", context)    

@login_required
def dashboard_t(request):
  
  
    total_students = User.objects.filter(profile__role='student').count()
    evaluations = Evaluation.objects.all().count()
    pending_evaluations = Evaluation.objects.filter(status='pending').count()
    
    context = {
        "total_students": total_students,
        "assignments_submitted": evaluations,
        "pending_evaluations": pending_evaluations
    }
    
    
    return render(request, "accounts/dashboard-t.html", context)


@login_required
def dashboard_s(request):
    # Dummy data for demonstration
    stats = {
        "total_students": 120,
        "assignments_submitted": 75,
        "pending_approvals": 18,
    }
    
    recent_submissions = [
        {"id": 1, "student_name": "John Doe", "assignment": "Sorting Algorithm", "submitted_on": "2025-01-01", "status": "Approved"},
        {"id": 2, "student_name": "Jane Smith", "assignment": "Bubble Sort", "submitted_on": "2025-01-02", "status": "Pending"},
        {"id": 3, "student_name": "Mike Brown", "assignment": "Merge Sort", "submitted_on": "2025-01-03", "status": "Rejected"},
    ]
    
    total_students = User.objects.filter(profile__role='student').count()

    context = {
        "total_students": total_students,
        "stats": stats,
        "recent_submissions": recent_submissions,
    }
    
    return render(request, "accounts/dashboard-s.html", context)    

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

# Registration View
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        role = request.POST['role']

        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('register')

        # Create user with role
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.profile.role = role  # Set the role (assumes profile extension)
        user.save()
        messages.success(request, "Account created successfully!")
        return redirect('login')

    return render(request, 'accounts/register.html')


def students_list(request):
    # Get all students
    students = User.objects.filter(profile__role='student')
    return render(request, 'accounts/students_list.html', {'students': students})


def users_list(request):
    # Get all users
    users = User.objects.all()
    return render(request, 'accounts/users_list.html', {'users': users})
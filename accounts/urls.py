from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),  # Profile page
    path('submit-assignment/', views.submit_assignment, name='submit_assignment'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('all-users/', views.users_list, name='users_list'),
    path('check-assignments/', views.check_student_assignments, name='check_student_assignments'),
    path('dashboard-a/', views.dashboard_a, name='dashboard_a'),
    path('dashboard-t/', views.dashboard_t, name='dashboard_t'),
    path('dashboard-s/', views.dashboard_s, name='dashboard_s'),
    path('dashboard-student-assignment-submission/', views.dashboard_student_assignment_submission, name='dashboard_student_assignment_submission'),
    path('students-list/', views.students_list, name='students_list'),
    path('evaluation/<int:evaluation_id>/', views.evaluation_report, name='evaluation_report'),
    path('pending-evaluation-list/', views.pending_evaluations_list, name='pending_evaluations_list'),
]

from django.urls import path
from . import views
from .views import CustomPasswordResetView

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),  # Profile page
    path('change-credentials/', views.change_credentials, name='change_credentials'),
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
    path('reviewed-evaluation-list/', views.reviewed_evaluations_list, name='reviewed_evaluations_list'),

    # Forgot password
    path("password-reset/", auth_views.PasswordResetView.as_view(template_name="resetPassword/password_reset.html"), name="password_reset"),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='resetPassword/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='resetPassword/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='resetPassword/password_reset_complete.html'), name='password_reset_complete'),
]

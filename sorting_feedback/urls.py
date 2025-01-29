from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('assessmentchoice/', assessmentchoice, name='assessmentchoice'),
    path('submit/', submit_code, name='submit_code'),
    path('dashboard/', dashboard, name='dashboard'),
    path('analytics/', analytics, name='analytics'), 
    path('evaluation-list/', evaluations_list, name='evaluations_list'),
    
    path('student-submitted-assignment/', student_submitted_assignment, name='student_submitted_assignment'),
]

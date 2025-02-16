from django.contrib import admin
from .models import *

@admin.register(EvaluationCriteria)
class EvaluationCriteriaAdmin(admin.ModelAdmin):
    list_display = ("check_syntax", "check_indentation", "check_comments", "min_comments", "last_updated")


@admin.register(DeadlineExtensionLog)
class DeadlineExtensionLogAdmin(admin.ModelAdmin):
    list_display = ("tutor", "old_deadline", "new_deadline", "timestamp")
    list_filter = ("tutor",)
    # search_fields = ("criteria__title", "tutor__username")

@admin.register(StudentPerformance)
class StudentPerformanceAdmin(admin.ModelAdmin):
    list_display = ("student", "total_submissions", "accuracy")  # Display fields
    search_fields = ("student__username",)  # Enable search by student username
    list_filter = ("accuracy",)  # Add filter option

# admin.site.register(StudentPerformance, StudentPerformanceAdmin)
admin.site.register(Submission)
admin.site.register(Evaluation)


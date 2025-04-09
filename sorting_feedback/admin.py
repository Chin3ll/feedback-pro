from django.contrib import admin
from .models import *
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse

@admin.register(EvaluationCriteria)
class EvaluationCriteriaAdmin(admin.ModelAdmin):
    list_display = ("check_syntax", "check_indentation", "check_comments", "min_comments", "last_updated")
    
    def has_add_permission(self, request):
        # Prevent add if one exists
        return not EvaluationCriteria.objects.exists()

    def changelist_view(self, request, extra_context=None):
        obj = EvaluationCriteria.objects.first()
        if obj:
            return HttpResponseRedirect(reverse('admin:sorting_feedback_evaluationcriteria_change', args=[obj.id]))
        return super().changelist_view(request, extra_context)


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "created_by":
            kwargs["queryset"] = User.objects.filter(profile__role="tutor")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# @admin.register(DeadlineExtensionLog)
# class DeadlineExtensionLogAdmin(admin.ModelAdmin):
#     list_display = ("tutor", "old_deadline", "new_deadline", "timestamp")
#     list_filter = ("tutor",)
#     # search_fields = ("criteria__title", "tutor__username")

@admin.register(StudentPerformance)
class StudentPerformanceAdmin(admin.ModelAdmin):
    list_display = ("student", "total_submissions", "accuracy")  # Display fields
    search_fields = ("student__username",)  # Enable search by student username
    list_filter = ("accuracy",)  # Add filter option

# admin.site.register(StudentPerformance, StudentPerformanceAdmin)
# admin.site.register(Submission)
admin.site.register(Evaluation)


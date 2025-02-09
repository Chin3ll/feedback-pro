from django.contrib import admin
from .models import Submission, Evaluation
from .models import EvaluationCriteria

from .models import DeadlineExtensionLog

@admin.register(EvaluationCriteria)
class EvaluationCriteriaAdmin(admin.ModelAdmin):
    list_display = ("check_syntax", "check_indentation", "check_comments", "min_comments", "last_updated")


@admin.register(DeadlineExtensionLog)
class DeadlineExtensionLogAdmin(admin.ModelAdmin):
    list_display = ("tutor", "old_deadline", "new_deadline", "timestamp")
    list_filter = ("tutor",)
    # search_fields = ("criteria__title", "tutor__username")




admin.site.register(Submission)
admin.site.register(Evaluation)


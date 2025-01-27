from django.contrib import admin
from .models import Submission, Evaluation
from .models import EvaluationCriteria


@admin.register(EvaluationCriteria)
class EvaluationCriteriaAdmin(admin.ModelAdmin):
    list_display = ("check_syntax", "check_indentation", "check_comments", "min_comments", "last_updated")


admin.site.register(Submission)
admin.site.register(Evaluation)


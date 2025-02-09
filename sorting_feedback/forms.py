from django import forms
from .models import EvaluationCriteria

class SubmissionDeadlineForm(forms.ModelForm):
    class Meta:
        model = EvaluationCriteria
        fields = ["submission_deadline"]
        widgets = {
            "submission_deadline": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"})
        }

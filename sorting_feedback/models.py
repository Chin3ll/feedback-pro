from django.db import models
# from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.models import User, Group


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    algorithm = models.CharField(max_length=50)
    code = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

class Evaluation(models.Model):
    title = models.CharField(max_length=255)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations')
    student_code = models.TextField(blank=True, null=True)  # Store code as text
    submission_file = models.FileField(upload_to='submissions/', blank=True, null=True)  # Store file uploads
    feedback = models.TextField()
    tutor_feedback = models.TextField(
        null=True, 
        blank=True, 
        help_text="Tutor specific feedback for the submission."
    )
    correctness = models.BooleanField(default=False)
    time_complexity = models.CharField(max_length=50, default="Unknown")
    grade = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[('submitted', 'Submitted'), ('reviewed', 'Reviewed')], default='submitted')
    plagiarism_score = models.FloatField(default=0.0, help_text="Plagiarism percentage score.")
    is_plagiarized = models.BooleanField(default=False, help_text="Indicates if plagiarism is detected.")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.student.username}"



class EvaluationCriteria(models.Model):
    title = models.CharField(max_length=255)
    check_syntax = models.BooleanField(default=True, help_text="Check for syntactic accuracy.")
    check_indentation = models.BooleanField(default=True, help_text="Check for correct indentation.")
    check_comments = models.BooleanField(default=True, help_text="Check for good comments.")
    min_comments = models.PositiveIntegerField(default=1, help_text="Minimum required comments in the code.")
    required_constructs = models.JSONField(default=list, help_text="List of required constructs (e.g., ['while loop', 'function']).")
    submission_deadline = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)

    # def save(self, *args, **kwargs):
    #     if self.created_by.role != "tutor":  # Prevent students/admins from setting criteria
    #         raise PermissionDenied("Only tutors can create evaluation criteria.")
    #     super().save(*args, **kwargs)
  

    def __str__(self):
        return "Evaluation Criteria"

class DeadlineExtensionLog(models.Model):
    tutor = models.ForeignKey(User, on_delete=models.CASCADE)
    criteria = models.ForeignKey(EvaluationCriteria, on_delete=models.CASCADE)
    old_deadline = models.DateTimeField()
    new_deadline = models.DateTimeField()
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"Extension for {self.evaluation_criteria}"  
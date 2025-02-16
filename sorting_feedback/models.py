from django.db import models
# from django.contrib.auth.models import User
from django.utils.timezone import now
from django.contrib.auth.models import User, Group
import re
import json  # Import JSON for parsing feedback if needed



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

class StudentPerformance(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    total_submissions = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0.0)
    strength_areas = models.JSONField(default=dict)  # Use JSON for flexibility
    weakness_areas = models.JSONField(default=dict)
    last_updated = models.DateTimeField(auto_now=True)

   

    def update_performance(self, evaluation):
        print("DEBUG: Updating performance for student ->", self.student.username)

        feedback = evaluation.feedback  # Should already contain evaluation text
        print("DEBUG: Received feedback ->", feedback)

        if not feedback:
            print("ERROR: Feedback is empty! Skipping update.")
            return

        # Extract strengths and weaknesses if available
        strength_start = feedback.find("Strengths:")
        weakness_start = feedback.find("Weaknesses:")

        strengths = feedback[strength_start + 10:weakness_start].strip() if strength_start != -1 else ""
        weaknesses = feedback[weakness_start + 11:].strip() if weakness_start != -1 else ""

        # Generate human-readable feedback
        if strengths:
            strength_message = f"Great job! {strengths} Keep up the good work!"
        else:
            strength_message = "You're making progress! Try to apply best practices consistently."

        if weaknesses:
            weakness_message = f"Here's where you can improve: {weaknesses}. Focus on these areas next time!"
        else:
            weakness_message = "No major weaknesses detected, but always strive to refine your skills!"

        print(f"DEBUG: Generated Strength Message -> {strength_message}")
        print(f"DEBUG: Generated Weakness Message -> {weakness_message}")

        # Save extracted text as JSON-like dictionaries
        self.strength_areas = {"description": strength_message}
        self.weakness_areas = {"description": weakness_message}

        # Update total submissions
        self.total_submissions += 1

        # Save changes
        self.save(update_fields=["strength_areas", "weakness_areas", "total_submissions"])
        print("✅ Student performance updated with friendly feedback!")

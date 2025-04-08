from django.test import TestCase
from django.contrib.auth.models import User
from collections import Counter

from sorting_feedback.models import Evaluation, StudentPerformance
from sorting_feedback.utils import analyze_student_performance


def analyze_student_performance(student):
    """
    Analyzes a student's strengths and weaknesses based on their evaluation history.
    """
    evaluations = Evaluation.objects.filter(student=student)
    total_submissions = evaluations.count()

    if total_submissions == 0:
        # Ensure StudentPerformance record exists even if no evaluations exist
        StudentPerformance.objects.get_or_create(
            student=student,
            defaults={
                "total_submissions": 0,
                "accuracy": 0,
                "strength_areas": {},
                "weakness_areas": {},
            }
        )
        return

    # Count occurrences of constructs and errors
    construct_counts = Counter()
    error_counts = Counter()
    total_correct_submissions = 0

    for eval in evaluations:
        if eval.correctness:
            total_correct_submissions += 1

        # Extract constructs from feedback (assuming constructs are mentioned)
        feedback_lines = eval.feedback.split("\n")
        for line in feedback_lines:
            if "Error:" in line:
                error_counts[line] += 1
            elif "✅" in line:  # Assuming strengths are marked with a checkmark
                construct_counts[line] += 1

    # Determine strengths (most frequently correct constructs)
    strengths = {construct: count for construct, count in construct_counts.most_common(3)}
    
    # Determine weaknesses (most frequent errors)
    weaknesses = {error: count for error, count in error_counts.most_common(3)}

    # Calculate accuracy percentage
    accuracy = (total_correct_submissions / total_submissions) * 100 if total_submissions else 0

    # Save or update the student's performance record
    performance, created = StudentPerformance.objects.get_or_create(student=student)
    performance.total_submissions = total_submissions
    performance.accuracy = accuracy
    performance.strength_areas = strengths  # Store as a dict
    performance.weakness_areas = weaknesses  # Store as a dict
    performance.save()



    

class StudentPerformanceTests(TestCase):
    def setUp(self):
        """Set up a test user for performance evaluation."""
        self.student = User.objects.create(username="student1")

    def test_initial_performance(self):
        """Ensure new students start with no evaluations."""
        analyze_student_performance(self.student)

        # Ensure StudentPerformance record is created
        performance = StudentPerformance.objects.get(student=self.student)

        self.assertEqual(performance.total_submissions, 0)
        self.assertEqual(performance.accuracy, 0)
        self.assertEqual(performance.strength_areas, {})  # JSONField default is an empty dict
        self.assertEqual(performance.weakness_areas, {})

    def test_multiple_submissions(self):
        """Ensure multiple submissions affect performance correctly."""
        Evaluation.objects.create(student=self.student, correctness=True, feedback="✅ Syntax is correct.\nError: Missing return statement.")
        Evaluation.objects.create(student=self.student, correctness=False, feedback="Error: Incorrect loop syntax.\nError: Missing comments.")

        analyze_student_performance(self.student)
        performance = StudentPerformance.objects.get(student=self.student)

        self.assertEqual(performance.total_submissions, 2)
        self.assertGreaterEqual(performance.accuracy, 50)
        self.assertIn("✅ Syntax is correct.", performance.strength_areas.keys())
        self.assertIn("Error: Missing return statement.", performance.weakness_areas.keys())

    def test_update_performance(self):
        """Ensure performance updates correctly after evaluations."""
        Evaluation.objects.create(student=self.student, correctness=True, feedback="✅ Well-indented.\n✅ Good variable names.")
        Evaluation.objects.create(student=self.student, correctness=False, feedback="Error: Missing comments.\nError: Unused variable.")

        analyze_student_performance(self.student)
        performance = StudentPerformance.objects.get(student=self.student)

        self.assertEqual(performance.total_submissions, 2)
        self.assertIn("✅ Well-indented.", performance.strength_areas.keys())
        self.assertIn("Error: Missing comments.", performance.weakness_areas.keys())
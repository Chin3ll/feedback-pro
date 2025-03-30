# from django.test import TestCase
# from django.contrib.auth.models import User
# from sorting_feedback.models import Evaluation, StudentPerformance
# from sorting_feedback.utils import analyze_student_performance

# class StudentPerformanceTests(TestCase):
#     def setUp(self):
#         """Set up a test user for performance evaluation."""
#         self.student = User.objects.create(username="student1")

#     def test_initial_performance(self):
#         """Ensure new students start with no evaluations."""
#         analyze_student_performance(self.student)

#         # Ensure StudentPerformance record is created
#         performance = StudentPerformance.objects.get(student=self.student)

#         self.assertEqual(performance.total_submissions, 0)
#         self.assertEqual(performance.accuracy, 0)
#         self.assertEqual(performance.strength_areas, {})  # JSONField default is an empty dict
#         self.assertEqual(performance.weakness_areas, {})

#     def test_multiple_submissions(self):
#         """Ensure multiple submissions affect performance correctly."""
#         Evaluation.objects.create(student=self.student, correctness=True, feedback="✅ Syntax is correct.\nError: Missing return statement.")
#         Evaluation.objects.create(student=self.student, correctness=False, feedback="Error: Incorrect loop syntax.\nError: Missing comments.")

#         analyze_student_performance(self.student)
#         performance = StudentPerformance.objects.get(student=self.student)

#         self.assertEqual(performance.total_submissions, 2)
#         self.assertGreaterEqual(performance.accuracy, 50)
#         self.assertIn("✅ Syntax is correct.", performance.strength_areas.keys())
#         self.assertIn("Error: Missing return statement.", performance.weakness_areas.keys())

#     def test_update_performance(self):
#         """Ensure performance updates correctly after evaluations."""
#         Evaluation.objects.create(student=self.student, correctness=True, feedback="✅ Well-indented.\n✅ Good variable names.")
#         Evaluation.objects.create(student=self.student, correctness=False, feedback="Error: Missing comments.\nError: Unused variable.")

#         analyze_student_performance(self.student)
#         performance = StudentPerformance.objects.get(student=self.student)

#         self.assertEqual(performance.total_submissions, 2)
#         self.assertIn("✅ Well-indented.", performance.strength_areas.keys())
#         self.assertIn("Error: Missing comments.", performance.weakness_areas.keys())
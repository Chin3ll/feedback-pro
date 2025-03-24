from django.test import TestCase
from sorting_feedback.models import StudentPerformance, Evaluation

class StudentPerformanceTests(TestCase):
    def setUp(self):
        """Set up mock student and evaluation records"""
        self.student = Student.objects.create(username="student1")

    def test_initial_performance(self):
        """Ensure new students start with no evaluations"""
        performance = StudentPerformance.objects.create(student=self.student)
        self.assertEqual(performance.total_submissions, 0)

    def test_update_performance(self):
        """Ensure performance updates correctly after evaluations"""
        performance = StudentPerformance.objects.create(student=self.student)
        evaluation = Evaluation.objects.create(
            student=self.student,
            grade="A",
            correctness=True
        )

        performance.update_performance(evaluation)
        self.assertEqual(performance.total_submissions, 1)
        self.assertEqual(performance.success_rate, 100)  # 1 success out of 1

    def test_multiple_submissions(self):
        """Ensure multiple submissions affect performance correctly"""
        performance = StudentPerformance.objects.create(student=self.student)
        Evaluation.objects.create(student=self.student, grade="A", correctness=True)
        Evaluation.objects.create(student=self.student, grade="F", correctness=False)

        performance.update_performance()
        self.assertEqual(performance.total_submissions, 2)
        self.assertEqual(performance.success_rate, 50)  # 1 success out of 2

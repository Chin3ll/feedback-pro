from django.test import TestCase
from sorting_feedback.utils import assign_grade

class GradingTests(TestCase):
    def test_perfect_score(self):
        """Ensure 100% correctness with no plagiarism gets an A"""
        grade = assign_grade(correctness=100, plagiarism_score=0, missing_constructs=[])
        self.assertEqual(grade, 80)

    def test_partial_score(self):
        """Ensure missing constructs lower the grade"""
        grade = assign_grade(correctness=80, plagiarism_score=0, missing_constructs=["if"])
        self.assertEqual(grade, 15)  # 75 - (1 * 60) = 15

    def test_high_plagiarism(self):
        """Ensure high plagiarism results in a failing grade"""
        grade = assign_grade(correctness=90, plagiarism_score=80, missing_constructs=[])
        self.assertEqual(grade, 0)  # Plagiarized submissions get 0

    def test_low_correctness(self):
        """Ensure low correctness results in failure"""
        grade = assign_grade(correctness=40, plagiarism_score=0, missing_constructs=["if", "for"])
        self.assertEqual(grade, 0)  # 40 - (2 * 60) = 0 (minimum is 0)

    def test_edge_case(self):
        """Ensure borderline grades are correctly classified"""
        grade = assign_grade(correctness=50, plagiarism_score=49, missing_constructs=["for"])
        self.assertEqual(grade, 0)  # 50 - (1 * 60) = 0 (minimum is 0)
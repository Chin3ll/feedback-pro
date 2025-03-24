from django.test import TestCase
from sorting_feedback.views import evaluate_code_with_criteria
from sorting_feedback.models import EvaluationCriteria

class CodeEvaluationTests(TestCase):
    def setUp(self):
        """Set up mock evaluation criteria"""
        self.criteria = EvaluationCriteria.objects.create(
            check_syntax=True,
            check_indentation=True,
            check_comments=True,
            min_comments=2,
            required_constructs=["for", "if"]
        )

    def test_correct_syntax_code(self):
        """Ensure valid syntax is detected correctly"""
        code = "for i in range(5): print(i)"
        result = evaluate_code_with_criteria(code, self.criteria)
        self.assertTrue(result["correctness"])
        self.assertIn("✅ Syntax is correct!", result["feedback"])

    def test_syntax_error(self):
        """Ensure syntax errors are detected"""
        code = "for i in range(5 print(i)"
        result = evaluate_code_with_criteria(code, self.criteria)
        self.assertFalse(result["correctness"])
        self.assertIn("Syntax error", result["feedback"])

    def test_indentation_check(self):
        """Ensure incorrect indentation is flagged"""
        code = "for i in range(5):\nprint(i)"
        result = evaluate_code_with_criteria(code, self.criteria)
        self.assertIn("Indentation should be a multiple of 4 spaces", result["feedback"])

    def test_comment_check(self):
        """Ensure insufficient comments are flagged"""
        code = "# loop\nfor i in range(5): print(i)"
        result = evaluate_code_with_criteria(code, self.criteria)
        self.assertIn("❌ Insufficient comments", result["feedback"])

    def test_construct_check(self):
        """Ensure missing constructs are detected"""
        code = "print('Hello')"
        result = evaluate_code_with_criteria(code, self.criteria)
        self.assertIn("❌ Required constructs missing: for, if.", result["feedback"])

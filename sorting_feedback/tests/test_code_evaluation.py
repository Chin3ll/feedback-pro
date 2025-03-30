# from django.test import TestCase
# from sorting_feedback.views import evaluate_code_with_criteria  # Use separate module
# from sorting_feedback.models import EvaluationCriteria
# from django.contrib.auth import get_user_model

# User = get_user_model()

# class TestCodeEvaluation(TestCase):
#     def setUp(self):
#         """Set up a basic evaluation criteria."""
#         self.user = User.objects.create(username="test_tutor")
#         self.criteria = EvaluationCriteria.objects.create(
#             title="Basic Evaluation",
#             check_syntax=True,
#             check_indentation=True,
#             check_comments=True,
#             min_comments=1,
#             required_constructs=["function"],
#             created_by=self.user
#         )

#     def test_correct_syntax(self):
#         """Test if correct Python syntax passes evaluation."""
#         code = "def add(a, b):\n    return a + b"
#         result = evaluate_code_with_criteria(code, self.criteria)
#         self.assertTrue(result["correctness"])
#         self.assertIn("✅ Syntax is correct!", result["feedback"])

#     def test_syntax_error(self):
#         """Test if syntax errors are caught."""
#         code = "def add(a, b):\nreturn a + b"  # Indentation missing
#         result = evaluate_code_with_criteria(code, self.criteria)
#         self.assertFalse(result["correctness"])
#         self.assertIn("Syntax error", result["feedback"])

#     def test_incorrect_indentation(self):
#         """Test if incorrect indentation is detected."""
#         code = "def add(a, b):\n return a + b"  # Indentation not multiple of 4
#         result = evaluate_code_with_criteria(code, self.criteria)
#         self.assertFalse(result["correctness"])
#         self.assertIn("❌ Line", result["feedback"])

#     def test_detects_required_constructs(self):
#         """Test if required constructs are detected."""
#         code = "def multiply(x, y):\n    return x * y"
#         result = evaluate_code_with_criteria(code, self.criteria)
#         self.assertTrue(result["correctness"])
#         self.assertNotIn("❌ Required constructs missing", result["feedback"])

#     def test_missing_required_constructs(self):
#         """Test if missing constructs are flagged."""
#         code = "x = 5 + 3"  # No function definition
#         result = evaluate_code_with_criteria(code, self.criteria)
#         self.assertFalse(result["correctness"])
#         self.assertIn("❌ Required constructs missing", result["feedback"])

#     def test_sufficient_comments(self):
#         """Test if sufficient comments pass."""
#         code = "# This is a function\n\ndef add(a, b):\n    return a + b"
#         result = evaluate_code_with_criteria(code, self.criteria)
#         self.assertTrue(result["correctness"])
#         self.assertIn("✅ Comments are sufficient", result["feedback"])

#     def test_insufficient_comments(self):
#         """Test if insufficient comments are flagged."""
#         code = "def add(a, b):\n    return a + b"
#         result = evaluate_code_with_criteria(code, self.criteria)
#         self.assertFalse(result["correctness"])
#         self.assertIn("❌ Insufficient comments", result["feedback"])
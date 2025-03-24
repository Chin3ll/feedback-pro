from django.test import TestCase
# from .evaluation import evaluate_code

# from django.test import TestCase
# from unittest.mock import patch
# from .gpt_feedback import generate_feedback_with_gpt

# class GPTFeedbackTests(TestCase):
#     @patch("openai.ChatCompletion.create")
#     def test_gpt_feedback(self, mock_openai):
#         # Mock OpenAI response
#         mock_openai.return_value = {
#             'choices': [{
#                 'message': {'content': "This is a test feedback from GPT."}
#             }]
#         }

#         feedback = generate_feedback_with_gpt("def bubble_sort(arr): pass", [2, 3, 4, 5, 8])
#         self.assertIn("test feedback", feedback)


# class EvaluationTests(TestCase):
#     def test_correct_bubble_sort(self):
#         submission_code = """
#         def bubble_sort(arr):
#             for i in range(len(arr)):
#                 for j in range(0, len(arr)-i-1):
#                     if arr[j] > arr[j+1]:
#                         arr[j], arr[j+1] = arr[j+1], arr[j]
#             return arr
#         """
#         feedback = evaluate_code(submission_code)
#         self.assertTrue(feedback['correctness'])
#         self.assertIn("Your implementation is correct", feedback['feedback'])

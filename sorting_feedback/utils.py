# # sorting_feedback/utils.py

# import cohere
# from decouple import config

# COHERE_API_KEY = config('COHERE_API_KEY')

# # def generate_feedback(prompt):
# #     response = co.generate(
# #         model='xlarge',
# #         prompt=prompt,
# #         max_tokens=100
# #     )
# #     return response.generations[0].text



# def generate_feedback(prompt):
#     """
#     Generate feedback using the Cohere API.
#     :param prompt: str - The input prompt for Cohere
#     :return: str - Generated feedback
#     """
#     try:
#         response = co.generate(
#             model='xlarge',
#             prompt=prompt,
#             max_tokens=100
#         )
#         return response.generations[0].text.strip()
#     except Exception as e:
#         return f"An error occurred while generating feedback: {str(e)}"

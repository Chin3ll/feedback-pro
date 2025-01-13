import cohere

# Initialize Cohere Client
co = cohere.Client('YOUR_COHERE_API_KEY')  # Replace with your actual API key

def generate_feedback(prompt):
    """
    Generate feedback using Cohere's language model.
    :param prompt: A string containing the prompt for Cohere's API
    :return: Generated feedback as a string
    """
    try:
        response = co.generate(
            model='xlarge',
            prompt=prompt,
            max_tokens=100
        )
        return response.generations[0].text
    except Exception as e:
        return f"An error occurred while generating feedback: {str(e)}"

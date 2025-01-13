import time

def evaluate_code(submission_code):
    """
    Evaluate the sorting algorithm submitted by a student.
    :param submission_code: str - Python code submitted by the student
    :return: dict - Feedback details
    """
    feedback = {}
    try:
        # Test input and expected output
        test_input = [5, 3, 8, 4, 2]
        expected_output = sorted(test_input)

        # Execute submitted code
        exec(submission_code, globals())  # Executes the code submitted by the student

        # Ensure the student defined the bubble_sort function
        if 'bubble_sort' not in globals():
            feedback['feedback'] = "The function 'bubble_sort' is not defined in your code."
            feedback['correctness'] = False
            feedback['time_complexity'] = "Unknown"
            return feedback

        # Start measuring the execution time
        start_time = time.time()  # Define start_time here before using it
        result = bubble_sort(test_input.copy())  # Execute the sorting algorithm
        execution_time = time.time() - start_time  # Measure execution time

        # Check correctness
        feedback['correctness'] = result == expected_output

        # Time complexity estimation (simplified for example purposes)
        feedback['time_complexity'] = "O(n^2)"  # Bubble sort time complexity

        # Correctness feedback
        if feedback['correctness']:
            feedback['feedback'] = "Your implementation is correct."
        else:
            feedback['feedback'] = "Your implementation is incorrect. Check your logic."

        # Time complexity feedback
        if feedback['time_complexity'] == "O(n^2)":
            feedback['feedback'] += " Consider optimizing your solution for better performance."

    except NameError as e:
        feedback['correctness'] = False
        feedback['feedback'] = f"Error in your code: {str(e)}"
    except Exception as e:
        feedback['correctness'] = False
        feedback['feedback'] = f"Error in your code: {str(e)}"

    return feedback

import ast

from collections import Counter
from .models import *

class ConstructDetector(ast.NodeVisitor):
    """
    Dynamically detects constructs in Python code using AST.
    """
    def __init__(self):
        self.found_constructs = set()

    def visit_While(self, node):
        self.found_constructs.add("while loop")
        self.generic_visit(node)

    def visit_For(self, node):
        self.found_constructs.add("for loop")
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.found_constructs.add("function")
        self.generic_visit(node)

    def visit_Lambda(self, node):
        self.found_constructs.add("lambda function")
        self.generic_visit(node)

    def visit_ListComp(self, node):
        self.found_constructs.add("list comprehension")
        self.generic_visit(node)

    def visit_DictComp(self, node):
        self.found_constructs.add("dictionary comprehension")
        self.generic_visit(node)

    def visit_SetComp(self, node):
        self.found_constructs.add("set comprehension")
        self.generic_visit(node)

    def visit_Try(self, node):
        self.found_constructs.add("try-except")
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.found_constructs.add("class")
        self.generic_visit(node)

    def visit_Assign(self, node):
        """
        Detects variable assignment.
        Example: x = 10
        """
        self.found_constructs.add("variable assignment")

        # Check if the assignment uses tuple/list unpacking
        if isinstance(node.targets[0], (ast.Tuple, ast.List)):
            self.found_constructs.add("tuple/list unpacking")

        self.generic_visit(node)

    def visit_Return(self, node):
        self.found_constructs.add("return statement")
        self.generic_visit(node)

    def visit_If(self, node):
        self.found_constructs.add("if statement")
        self.generic_visit(node)

    def visit_Import(self, node):
        self.found_constructs.add("import statement")
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.found_constructs.add("import from")
        self.generic_visit(node)

    def visit_Dict(self, node):
        self.found_constructs.add("dictionary")
        self.generic_visit(node)

    def visit_List(self, node):
        self.found_constructs.add("list")
        self.generic_visit(node)

    def visit_Tuple(self, node):
        self.found_constructs.add("tuple")
        self.generic_visit(node)

    def visit_Set(self, node):
        self.found_constructs.add("set")
        self.generic_visit(node)

    def visit_Call(self, node):
        """
        Detects higher-order functions dynamically.
        A function is considered 'higher-order' if:
        - It takes another function as an argument
        - It returns another function
        """
        if isinstance(node.func, ast.Name):  # Function call like my_function()
            for arg in node.args:
                if isinstance(arg, ast.Lambda) or isinstance(arg, ast.Call):
                    self.found_constructs.add("higher-order function")
        self.generic_visit(node)


def detect_constructs(code):
    """
    Dynamically detects constructs present in the given code.
    Returns a set of detected constructs.
    """
    try:
        tree = ast.parse(code)
        detector = ConstructDetector()
        detector.visit(tree)
        return detector.found_constructs
    except SyntaxError:
        return set()  # If there's a syntax error, return an empty set


def assign_grade(correctness, plagiarism_score):
    """
    Assigns a preliminary grade based on correctness and plagiarism score.
    Max system grading is 80, final grading beyond that is left to the tutor.
    """
    if plagiarism_score > 50:
        grade = 0  # Plagiarized submissions get 0
    elif correctness >= 90:
        grade = 80  # System assigns max 80; tutor decides final score
    elif correctness >= 80:
        grade = 75
    elif correctness >= 70:
        grade = 65
    elif correctness >= 50:
        grade = 50
    else:
        grade = 40  # Failed submission

    print(f"System-Assigned Grade: {grade}")  # Debugging print
    return grade  # Tutor will review and adjust if necessary



def analyze_student_performance(student):
    """
    Analyzes a student's strengths and weaknesses based on their evaluation history.
    """
    evaluations = Evaluation.objects.filter(student=student)
    total_submissions = evaluations.count()

    if total_submissions == 0:
        return  # No need to analyze if there are no submissions

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
            elif "construct" in line.lower():
                construct_counts[line] += 1

    # Determine strengths (most frequently correct constructs)
    strengths = [construct for construct, count in construct_counts.most_common(3)]
    
    # Determine weaknesses (most frequent errors)
    weaknesses = [error for error, count in error_counts.most_common(3)]

    # Calculate accuracy percentage
    accuracy = (total_correct_submissions / total_submissions) * 100 if total_submissions else 0

    # Save or update the student's performance record
    performance, created = StudentPerformance.objects.get_or_create(student=student)
    performance.total_submissions = total_submissions
    performance.accuracy = accuracy
    performance.strengths = ", ".join(strengths)
    performance.weaknesses = ", ".join(weaknesses)
    performance.save()

import io
import sys

def execute_code_safely(code):
    """ Executes student code in a restricted environment and captures output. """
    output_buffer = io.StringIO()
    sys.stdout = output_buffer  # Redirect stdout to capture print statements

    safe_builtins = {
        "print": print,
        "range": range,
        "len": len,
        "int": int,
        "float": float,
        "str": str,
        "bool": bool,
        "list": list,
        "dict": dict,
        "tuple": tuple,
        "set": set,
        "enumerate": enumerate,
        "zip": zip,
    }

    try:
        exec(code, {"__builtins__": safe_builtins})  # Allow only safe built-ins
        result = output_buffer.getvalue()  # Get printed output
    except Exception as e:
        result = f"Execution Error: {e}"

    sys.stdout = sys.__stdout__  # Restore original stdout
    return result.strip()  # Remove trailing spaces

from langchain_core.tools import Tool


def email_criteria(input: str) -> str:
    """Email Address Lookup Tool. Input should be an email address."""
    return """
    Criteria:
    - The email address must contain a @ symbol.
    - The email address must contain a . symbol.
    - The email address must not contain any spaces.
    """
def state_criteria(input: str) -> str:
    """State Lookup Tool. Input should be a state."""
    return """
    Criteria:
    - The state must a two letter abbreviation.
    - The state must be in the set of US state abbreviations.
    - If the state is not in the set of US state abbreviations, return a nearest best guess that is a valid state abbreviation.'
    - Do not return any other text than a US state abbreviation.
"""
def tool_two(input: str) -> str:
    """Alternative addition tool. Input should be two space-separated numbers."""
    try:
        # Split input into two numbers
        parts = input.strip().split()
        if len(parts) != 2:
            return "Error: Please provide exactly two numbers separated by a space."
        
        num1 = float(parts[0])
        num2 = float(parts[1])
        result = num1 + num2
        
        return str(result)
    except ValueError:
        return "Error: Please provide valid numbers."
    except Exception as e:
        return f"Error: {str(e)}"

TOOL_LIST = [
    Tool(
        name="EmailCriteria",
        func=email_criteria,
        description="Email Address Lookup Tool. Validates email address format. Input should be an email address."
    ),
    Tool(
        name="StateCriteria",
        func=state_criteria,
        description="State Lookup Tool. Validates US state format. Input should be a state (two letter abbreviation)."
    ),
    Tool(
        name="ToolTwo", 
        func=tool_two,
        description="Alternative addition tool. Adds two numbers together. Input should be two space-separated numbers (e.g., '5 3')."
    ),
]
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
]
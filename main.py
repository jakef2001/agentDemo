from agent.agent import CustomPromptAgent
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def call_agent(field1: str, field2: str, system_instructions: str = None) -> str:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    llm = ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-2.0-flash")
    system_instructions = system_instructions or (
        "You are a data postprocessing agent. You are given a field type and a value. "
        "Follow this process:\n"
        "1. First, use a tool to lookup any criteria for that field type. Format: 'Thought:' (reasoning), 'Action:' (tool name), 'Action Input:' (field type)\n"
        "2. After the tool returns the result, use this criteria, context about the field type, and the value to format and error correct the value. Format: 'Thought:' (reasoning)"
        "3. Provide the final answer. Format: 'Thought:' (reasoning), 'Final Answer:' (result)\n"
        "Do NOT combine tool usage and final answer in the same response. Use the tool first, then provide the final answer."
        "If the field type is not found, return 'No criteria found for this field type.'"
    )
    agent = CustomPromptAgent(llm, system_instructions)
    return agent.run(field1, field2)

def instantiate_agent(system_instructions: str = None):
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    llm = ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-2.0-flash")
    system_instructions = system_instructions or (
        "You are a data postprocessing agent. You are given a field type and a value. "
        "Follow this process:\n"
        "1. First, use a tool to lookup any criteria for that field type. Format: 'Thought:' (reasoning), 'Action:' (tool name), 'Action Input:' (field type)\n"
        "2. After the tool returns the result, use this criteria, context about the field type, and the value to format and error correct the value. Format: 'Thought:' (reasoning)"
        "3. Provide the final answer. Format: 'Thought:' (reasoning), 'Final Answer:' (result)\n"
        "Do NOT combine tool usage and final answer in the same response. Use the tool first, then provide the final answer."
        "If the field type is not found, return 'No criteria found for this field type.'"
    )
    agent = CustomPromptAgent(llm, system_instructions)
    return agent

def main():
    agent = instantiate_agent()
    response = agent.run("Email Address", "pleaseformatme @gmail..com")
    print("Agent response:", response) 

if __name__ == "__main__":
    # Example usage
    main()

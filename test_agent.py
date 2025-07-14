from agent.agent import CustomPromptAgent
from langchain_google_genai import ChatGoogleGenerativeAI
import os

def test_agent_output():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("GOOGLE_API_KEY not set")
        return
    
    llm = ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-2.0-flash")
    system_instructions = (
        "You are a data postprocessing agent. You are given a field type and a value. "
        "Follow this process:\n"
        "1. First, use a tool to lookup any criteria for that field type. Format: 'Thought:' (reasoning), 'Action:' (tool name), 'Action Input:' (field type)\n"
        "2. After the tool returns the result, use this criteria, context about the field type, and the value to format and error correct the value. Format: 'Thought:' (reasoning)"
        "3. Provide the final answer. Format: 'Thought:' (reasoning), 'Final Answer:' (result)\n"
        "Do NOT combine tool usage and final answer in the same response. Use the tool first, then provide the final answer."
        "If the field type is not found, return 'No criteria found for this field type.'"
    )
    
    agent = CustomPromptAgent(llm, system_instructions)
    
    # Test with a simple case
    result = agent.run("Email Address", "test@example.com")
    
    print("Type of result:", type(result))
    print("Result:", result)
    print("Result repr:", repr(result))
    
    if isinstance(result, dict):
        print("Result keys:", result.keys())
        if "output" in result:
            print("Output value:", result["output"])
            print("Output type:", type(result["output"]))

if __name__ == "__main__":
    test_agent_output() 
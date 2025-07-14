from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from .tools import TOOL_LIST

class CustomPromptAgent:
    def __init__(self, llm, system_instructions: str):
        # Build a custom prompt template
        tool_descriptions = "\n".join(
            [f"{tool.name}: {tool.description}" for tool in TOOL_LIST]
        )
        template = (
            f"{system_instructions}\n\n"
            "You have access to the following tools:\n"
            "{tools}\n\n"
            "Tool names: {tool_names}\n\n"
            "When given an input, decide which tool to use and respond accordingly.\n"
            "Input: {input}\n"
            "{agent_scratchpad}"
        )
        prompt = PromptTemplate(
            input_variables=["input", "tools", "tool_names", "agent_scratchpad"],
            template=template
        )

        # Create the agent
        agent = create_react_agent(
            llm=llm,
            tools=TOOL_LIST,
            prompt=prompt
        )

        # Set up the executor
        self.executor = AgentExecutor(
            agent=agent,
            tools=TOOL_LIST,
            verbose=True,
            handle_parsing_errors=True
        )
        self.tool_descriptions = tool_descriptions

    def run(self, field1: str, field2: str) -> str:
        user_input = f"{field1} {field2}"
        result = self.executor.invoke({
            "input": user_input
        })
        # Extract the output string from the result dictionary
        return result.get("output", str(result)) 
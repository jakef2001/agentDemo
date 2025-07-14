from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from agent.agent import CustomPromptAgent
from langchain_google_genai import ChatGoogleGenerativeAI

app = FastAPI(
    title="Agentic Agent API",
    description="API for interacting with the custom agent for data postprocessing",
    version="1.0.0"
)

class AgentRequest(BaseModel):
    field_type: str
    value: str
    system_instructions: Optional[str] = None

class AgentResponse(BaseModel):
    result: str
    field_type: str
    value: str

def get_agent(system_instructions: Optional[str] = None) -> CustomPromptAgent:
    """Create and return an agent instance"""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GOOGLE_API_KEY environment variable not set")
    
    llm = ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-2.0-flash")
    
    default_instructions = (
        "You are a data postprocessing agent. You are given a field type and a value and have the goal of formatting and error correcting the value. "
        "Follow this process:\n"
        "1. First, use a tool to lookup any criteria for that field type. Format: 'Thought:' (reasoning), 'Action:' (tool name), 'Action Input:' (field type)\n"
        "2. After the tool returns the result, take in the criteria and use it as context for guiding your error correction. Format: 'Thought:' (reasoning)"
        "3. Use the value and tool result to perform the error correction. Format: 'Thought:' (reasoning)"
        "4. Error correct only if error correction is needed. If you know a field is incorrect but cannot with confidence correct the error, give a best guess."
        "5. Provide the final answer. Format: 'Thought:' (reasoning), 'Final Answer:' (result)\n"
        "Do NOT combine tool usage and final answer in the same response. Use the tool first, then provide the final answer."
        "If the field type is not found, return 'No criteria found for this field type.'"
    )
    
    instructions = system_instructions or default_instructions
    return CustomPromptAgent(llm, instructions)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Agentic Agent API is running"}

@app.post("/process", response_model=AgentResponse)
async def process_field(request: AgentRequest):
    """
    Process a field type and value using the agent
    
    - **field_type**: The type of field (e.g., "Email Address", "State")
    - **value**: The value to be processed
    - **system_instructions**: Optional custom system instructions
    """
    try:
        agent = get_agent(request.system_instructions)
        result = agent.run(request.field_type, request.value)
        
        # Ensure result is a string
        if not isinstance(result, str):
            result = str(result)
        
        # Create response object
        response = AgentResponse(
            result=result,
            field_type=request.field_type,
            value=request.value
        )
        
        return response
    except Exception as e:
        import traceback
        print(f"Error details: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Agent processing failed: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint to verify API and agent availability"""
    try:
        # Test if we can create an agent
        agent = get_agent()
        return {
            "status": "healthy",
            "message": "API and agent are ready to process requests"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
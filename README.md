# Agentic LLM Skeleton Project

This project provides a skeleton for building an agentic LLM using LangChain with Google's Gemini model. It is designed to accept field types and values, use an agent with tools to validate and format data, and return a response. The project includes both a direct Python interface and a REST API.

## Setup

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Google API key:
   ```bash
   export GOOGLE_API_KEY="your_google_api_key_here"
   ```

## Usage

### Direct Python Interface

Edit `main.py` to provide your input fields. Run:

```bash
python main.py
```

### REST API Interface

1. Start the API server:
   ```bash
   python api.py
   ```

2. The API will be available at `http://localhost:8000`

3. API Endpoints:
   - `GET /` - Health check
   - `GET /health` - Detailed health check
   - `POST /process` - Process a field type and value

4. Example API usage:
   ```bash
   # Test the client example
   python client_example.py
   ```

5. API Documentation:
   - Interactive docs: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Example API Request

```bash
curl -X POST "http://localhost:8000/process" \
     -H "Content-Type: application/json" \
     -d '{
       "field_type": "Email Address",
       "value": "pleaseformatme @gmail..com"
     }'
```

## Available Tools

- **EmailCriteria**: Validates email address format
- **StateCriteria**: Validates US state format (two letter abbreviation)
- **ToolTwo**: Adds two numbers together

## Extending

- Add or modify tools in `agentic_agent/tools.py`.
- Implement your logic in the tool functions.
- Adjust the agent's behavior in `agentic_agent/agent.py`.
- Extend the API in `api.py` with additional endpoints.

## Requirements
- Python 3.8+
- Google API key (set `GOOGLE_API_KEY` in your environment) 
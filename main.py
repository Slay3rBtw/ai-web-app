from fastapi import FastAPI
from pydantic import BaseModel

# 1. Initialize our FastAPI app setup
app = FastAPI()

# 2. An in-memory list acting as a temporary database for now
incidents = []

# 3. Define the rules for what an "Incident" data packet must look like
class Incident(BaseModel):
    title: str
    description: str
    severity: str # "low" | "medium" | "high"

# --- THE MENU (ENDPOINTS) ---

# Endpoint 1: A simple health check to make sure the server is alive
@app.get("/health")
def health():
    return {"status": "ok"}

# Endpoint 2: Take incoming data from a user and save it
@app.post("/incidents")
def create_incident(incident: Incident):
    record = incident.model_dump()
    record["id"] = len(incidents) + 1
    incidents.append(record)
    return record

# Endpoint 3: Return the entire list of saved incidents
@app.get("/incidents")
def list_incidents():
    return incidents
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# (Your existing app, Incident class, and endpoints remain up here)

class AIRequest(BaseModel):
    user_query: str

@app.post("/ask-ai")
def ask_ai_agent(request: AIRequest):
    # This is an architectural mock of an external LLM text completion endpoint
    external_llm_url = "https://api.live-ai-model-provider.com/v1/completions"
    
    # We construct the exact structured payload the AI expects
    payload = {
        "model": "advanced-text-model",
        "prompt": f"Answer this question like a senior systems engineer: {request.user_query}",
        "max_tokens": 150
    }
    
    headers = {
        "Authorization": "Bearer MOCK_SECRET_API_KEY_HERE",
        "Content-Type": "application/json"
    }
    
    try:
        # In a real setup, this sends the data packet over the web to the AI brain
        # For our local sandbox testing, we will mock the response structure:
        mock_response = {
            "choices": [{
                "text": f"AI Agent Response: Internal analysis complete for query '{request.user_query}'."
            }]
        }
        return {"response": mock_response["choices"][0]["text"]}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="The AI brain connection timed out.")
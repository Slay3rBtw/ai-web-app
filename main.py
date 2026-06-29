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
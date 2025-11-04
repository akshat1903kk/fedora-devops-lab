from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

# Make sure this file is in the same 'app' directory
from .log_analyzer import analyze_logs

app = FastAPI(
    title="DevOps Lab API", 
    version="0.0.1"
)

# -- Pydantic Models (Data validation)--

class ServiceBase(BaseModel):
    name: str
    status: str

class Service(ServiceBase):
    id: int

# -- Init DB --

db: List[Service] = [
    Service(id=1, name="Nginx-Prod", status="Running"),
    Service(id=2, name="FastAPI-Prod", status="Running"),
    Service(id=3, name="Fedora-VM-Lab", status="Offline"),
]

#-- API ENDPOINTS --

@app.get("/api/v1/status")
async def get_status():
    return {"status": "API is live"}

@app.get("/api/v1/analytics") # Log analyzer
async def get_analytics():
    return analyze_logs()

# --- FIXED URL ---
@app.post("/api/v1/services", response_model=Service) # Create a new service
async def create_service(service: ServiceBase):
    
    new_id = max(s.id for s in db) + 1 if db else 1
    new_service = Service(id=new_id, **service.model_dump())
    db.append(new_service)
    
    # --- FIXED RESPONSE ---
    # Must return the Service object, not a dict, to match response_model
    return new_service

@app.get("/api/v1/services", response_model=List[Service]) # returns a list of all services.
async def get_services():
    return db

@app.get("/api/v1/services/{service_id}", response_model=Service) # returns service by id
async def get_sepcific_service(service_id: int):
    for service in db:
        if service.id == service_id:
            return service
    
    # --- FIXED INDENTATION ---
    # This must be OUTSIDE the loop, otherwise it stops on the first miss.
    raise HTTPException(status_code=404, detail="Service not found")

# --- FIXED URL (standard REST practice) ---
@app.put("/api/v1/services/{service_id}", response_model=Service) # update service name/status
async def update_service(service_id: int, updated_service: ServiceBase): 
    
    # --- FIXED VARIABLE NAME (service, not Service) ---
    for i, service in enumerate(db):
        if service.id == service_id:
            # This is a safer way to update
            db[i] = Service(id=service_id, **updated_service.model_dump())
            return db[i]
            
    raise HTTPException(status_code=404, detail="Service not found")

# --- FIXED URL (standard REST practice) ---
@app.delete("/api/v1/services/{service_id}") # delete service by id
async def delete_service(service_id: int):
    
    # --- FIXED VARIABLE NAME (service, not Service) ---
    for i, service in enumerate(db):
        if service.id == service_id:
            del db[i]
            return {"message": "Service deleted"}
            
    # --- FIXED LOGIC ---
    # Added the missing error check
    raise HTTPException(status_code=404, detail="Service not found")
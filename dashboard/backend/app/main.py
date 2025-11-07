#!/usr/bin/env python3
"""
main.py
--------
FastAPI application for the DevOps Lab project.

Provides:
- Health & status endpoints
- Service CRUD operations (in-memory mock DB)
- Log analytics endpoint (Nginx access log parser)

Author: Akshat Kushwaha
"""

from pathlib import Path
from typing import List

from app.log_analyzer import analyze_logs
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="DevOps Lab API",
    version="1.0.0",
    description="A lightweight FastAPI-based DevOps monitoring and analytics service.",
)

# =========================================================
#                     MODELS
# =========================================================


class ServiceBase(BaseModel):
    name: str
    status: str


class Service(ServiceBase):
    id: int


# =========================================================
#                     MOCK DATABASE
# =========================================================

db: List[Service] = [
    Service(id=1, name="Nginx-Prod", status="Running"),
    Service(id=2, name="FastAPI-Prod", status="Running"),
    Service(id=3, name="API-Gateway", status="Offline"),
]

# =========================================================
#                     ENDPOINTS
# =========================================================


@app.get("/api/v1/status", tags=["Health"])
async def get_status():
    """Check if the API is running."""
    return {"status": "API is live", "services_count": len(db)}


@app.get("/api/v1/analytics", tags=["Analytics"])
async def get_analytics(log_path: str | None = None):
    """
    Analyze Nginx access logs and return traffic stats.
    Optional query param: log_path (custom log location).
    """
    path = log_path or "/var/log/nginx/access.log"
    result = analyze_logs(path)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# =========================================================
#                     SERVICES CRUD
# =========================================================


@app.get("/api/v1/services", response_model=List[Service], tags=["Services"])
async def get_services():
    """Return list of all services."""
    return db


@app.get("/api/v1/services/{service_id}", response_model=Service, tags=["Services"])
async def get_service(service_id: int):
    """Return a single service by ID."""
    for service in db:
        if service.id == service_id:
            return service
    raise HTTPException(status_code=404, detail="Service not found")


@app.post("/api/v1/services", response_model=Service, tags=["Services"])
async def create_service(service: ServiceBase):
    """Create a new service entry."""
    new_id = max((s.id for s in db), default=0) + 1
    new_service = Service(id=new_id, **service.model_dump())
    db.append(new_service)
    return new_service


@app.put("/api/v1/services/{service_id}", response_model=Service, tags=["Services"])
async def update_service(service_id: int, updated_service: ServiceBase):
    """Update an existing service."""
    for i, service in enumerate(db):
        if service.id == service_id:
            db[i] = Service(id=service_id, **updated_service.model_dump())
            return db[i]
    raise HTTPException(status_code=404, detail="Service not found")


@app.delete("/api/v1/services/{service_id}", tags=["Services"])
async def delete_service(service_id: int):
    """Delete a service by ID."""
    for i, service in enumerate(db):
        if service.id == service_id:
            del db[i]
            return {"message": f"Service '{service.name}' deleted successfully."}
    raise HTTPException(status_code=404, detail="Service not found")


# =========================================================
#                     ROOT ROUTE
# =========================================================


@app.get("/", include_in_schema=False)
async def root():
    """Redirect to the interactive API docs."""
    return {"message": "Welcome to the DevOps Lab API", "docs_url": "/docs"}


# =========================================================
#                     ENTRYPOINT
# =========================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(Path(__file__).stem == "main" and 8000),
        reload=True,
    )

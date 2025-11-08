#!/usr/bin/env python3
"""
main.py
--------
FastAPI backend for the DevOps Lab project.

Provides:
- Health and analytics endpoints
- Full CRUD API for monitored services
- Integration with PostgreSQL via SQLAlchemy
- Efficient, stateless DB access and log analytics

Author: Akshat Kushwaha
"""

from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.log_analyzer import analyze_logs
from app.models.service_model import Service

# =========================================================
#                  FASTAPI APP CONFIG
# =========================================================

app = FastAPI(
    title="DevOps Lab API",
    version="2.1.0",
    description="A FastAPI-based DevOps monitoring and analytics backend powered by PostgreSQL.",
)

# =========================================================
#                  SCHEMAS
# =========================================================


class ServiceBase(BaseModel):
    name: str
    status: str


class ServiceCreate(ServiceBase):
    """Schema for creating a new service."""


class ServiceUpdate(ServiceBase):
    """Schema for updating a service."""


class ServiceOut(ServiceBase):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        orm_mode = True


# =========================================================
#                  HEALTH & ANALYTICS
# =========================================================


@app.get("/api/v1/status", tags=["Health"])
async def get_status():
    """Basic health check."""
    return {"status": "API is operational", "version": "2.1.0"}


@app.get("/api/v1/analytics", tags=["Analytics"])
async def get_analytics(log_path: str | None = None):
    """Analyze access logs and return summarized stats."""
    path = log_path or "/var/log/nginx/access.log"
    result = analyze_logs(path)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


# =========================================================
#                  SERVICES CRUD
# =========================================================


@app.get("/api/v1/services", response_model=List[ServiceOut], tags=["Services"])
async def get_services(db: Session = Depends(get_db)):
    """Fetch all registered services."""
    # Use yield-based sessions for memory safety
    return db.query(Service).all()


@app.get("/api/v1/services/{service_id}", response_model=ServiceOut, tags=["Services"])
async def get_service(service_id: int, db: Session = Depends(get_db)):
    """Fetch a service by ID."""
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")
    return service


@app.post(
    "/api/v1/services",
    response_model=ServiceOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Services"],
)
async def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    """Register a new service."""
    new_service = Service(
        name=service.name,
        status=service.status,
        created_at=datetime.utcnow(),
    )
    db.add(new_service)
    try:
        db.commit()
        db.refresh(new_service)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database commit failed.")
    return new_service


@app.put("/api/v1/services/{service_id}", response_model=ServiceOut, tags=["Services"])
async def update_service(
    service_id: int, updated: ServiceUpdate, db: Session = Depends(get_db)
):
    """Update an existing service entry."""
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    for key, value in updated.model_dump().items():
        setattr(service, key, value)
    service.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(service)
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update record.")

    return service


@app.delete("/api/v1/services/{service_id}", tags=["Services"])
async def delete_service(service_id: int, db: Session = Depends(get_db)):
    """Remove a service record."""
    service = db.get(Service, service_id)
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    try:
        db.delete(service)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete record.")

    return {"message": f"Service '{service.name}' deleted successfully."}


# =========================================================
#                  ROOT ROUTE
# =========================================================


@app.get("/", include_in_schema=False)
async def root():
    """API root."""
    return {"message": "Welcome to DevOps Lab API!", "docs_url": "/docs"}


# =========================================================
#                  ENTRYPOINT
# =========================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )

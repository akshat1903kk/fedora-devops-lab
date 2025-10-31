from fastapi import FastAPI

# Create the FastAPI app instance
app = FastAPI(title="Fedora DevOps Lab API")

@app.get("/")
def read_root():
    """
    Root endpoint for the API.
    """
    return {"message": "Hello, Fedora DevOps Lab!"}

@app.get("/health")
def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "ok"}
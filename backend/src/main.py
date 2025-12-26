from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

# Create FastAPI app instance
app = FastAPI(
    title="My FastAPI Server",
    description="A simple FastAPI server running locally",
    version="1.0.0"
)

# Root endpoint
@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}


# Run the server if this file is executed directly
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",  # Localhost
        port=8000,         # Default port
        reload=True        # Auto-reload on code changes
    )
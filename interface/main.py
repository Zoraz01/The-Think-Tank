from fastapi import FastAPI
from interface.api import video
from interface.websocket import handlers 
import asyncio

# Initialize the main FastAPI application
app = FastAPI(title="The Think Tank Server")

# Include routers
app.include_router(video.router)
app.include_router(handlers.router) 

@app.on_event("startup")
async def startup_event():
    """
    Starts background tasks when the server starts.
    """
    print("Starting background task for periodic updates...")
    asyncio.create_task(handlers.send_periodic_updates())

@app.get("/", tags=["Status"])
async def root():
    """
    Root endpoint that provides a simple status message.
    """
    return {"status": "ok", "message": "Welcome to The Think Tank Server!"}
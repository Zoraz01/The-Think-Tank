# In interface/websocket/manager.py

from fastapi import WebSocket
from typing import List
import asyncio

class ConnectionManager:
    """
    Manages active WebSocket connections.
    Allows for broadcasting messages to all connected clients.
    """
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accepts and stores a new WebSocket connection."""
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"New client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Removes a WebSocket connection."""
        self.active_connections.remove(websocket)
        print(f"Client disconnected. Total clients: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        """Sends a message to all active connections."""
        for connection in self.active_connections:
            await connection.send_text(message)

# Create a single instance of the manager to be used across the application
manager = ConnectionManager()
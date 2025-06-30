from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from interface.websocket.manager import manager
import asyncio
import json
import random

# Create a new router for WebSocket-related endpoints
router = APIRouter(
    prefix="/ws",
    tags=["WebSocket"]
)

@router.websocket("/controller")
async def websocket_endpoint(websocket: WebSocket):
    """
    The main WebSocket endpoint for real-time control and telemetry.
    """
    await manager.connect(websocket)
    try:
        # This loop listens for incoming commands from the app
        while True:
            data = await websocket.receive_json() # Awaits JSON messages

            if data.get('type') == 'command':
                payload = data.get('payload', {})
                command = payload.get('command_name')
                
                print(f"Received command: {command} with payload: {payload}")

                # --- COMMAND HANDLING LOGIC GOES HERE ---
                if command == 'select_target':
                    # TODO: Implement aiming logic
                    target_id = payload.get('target_id')
                    print(f"Server logic to aim at {target_id} would run here.")
                
                elif command == 'fire':
                    # TODO: Implement firing logic
                    print("Server logic to fire the turret would run here.")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"An error occurred in the WebSocket: {e}")
        manager.disconnect(websocket)

# --- PRANK ZONE: REALISTIC DUMMY DATA GENERATION ---

# Define the "screen" boundaries
WIDTH, HEIGHT = 640, 480

# Create a list of dummy objects to "track"
tracked_objects = [
    {
        "id": "obj-001", "label": "person", "box": [100, 150, 50, 80],
        "velocity": [random.randint(-3, 3), random.randint(-3, 3)]
    },
    {
        "id": "obj-002", "label": "car", "box": [400, 300, 120, 60],
        "velocity": [random.randint(-3, 3), random.randint(-3, 3)]
    },
    {
        "id": "obj-003", "label": "dog", "box": [200, 50, 60, 45],
        "velocity": [random.randint(-3, 3), random.randint(-3, 3)]
    },
    {
        "id": "obj-004", "label": "cat", "box": [500, 100, 55, 50],
        "velocity": [random.randint(-3, 3), random.randint(-3, 3)]
    }
]

def update_object_positions():
    """Updates the position of each object and makes them bounce off the walls."""
    for obj in tracked_objects:
        box = obj["box"]
        vel = obj["velocity"]

        # Update position
        box[0] += vel[0]
        box[1] += vel[1]

        # Bounce off walls
        if box[0] <= 0 or (box[0] + box[2]) >= WIDTH:
            vel[0] *= -1 # Reverse X velocity
        if box[1] <= 0 or (box[1] + box[3]) >= HEIGHT:
            vel[1] *= -1 # Reverse Y velocity
            
        # Add slight random wobble to velocity to make it less robotic
        vel[0] += random.uniform(-0.2, 0.2)
        vel[1] += random.uniform(-0.2, 0.2)


async def send_periodic_updates():
    """
    A background task that sends realistically moving object detection data.
    """
    while True:
        # Update the positions of our dummy objects
        update_object_positions()
        
        # Format the data into the correct JSON structure
        data_to_send = {
          "type": "object_update",
          "payload": {
            "timestamp": asyncio.get_event_loop().time(),
            "objects": [
                # Create a clean copy of each object for the payload
                {"id": o["id"], "label": o["label"], "box": [int(p) for p in o["box"]]} 
                for o in tracked_objects
            ]
          }
        }
        
        await manager.broadcast(json.dumps(data_to_send))
        await asyncio.sleep(0.03) # Send updates ~33 times per second for smooth motion
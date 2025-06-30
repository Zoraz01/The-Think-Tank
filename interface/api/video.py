from fastapi import APIRouter
from starlette.responses import StreamingResponse
import asyncio
import cv2
import numpy as np

# Create a new router to handle video-related endpoints
router = APIRouter(
    prefix="/video",
    tags=["Video Streaming"]
)

def get_processed_frame():
    """
    This is the core function where you'll integrate your vision processing.
    
    - Captures a frame from the camera.
    - Runs the YOLOv8 model on the frame.
    - Draws bounding boxes and labels on the frame.
    - Returns the annotated frame.
    """
    # --- Placeholder: Replace with your actual vision logic ---
    # For now, we create a simple black frame with a timestamp.
    height, width = 480, 640
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Add some text to simulate annotations
    timestamp = asyncio.get_event_loop().time()
    text = f"Frame @ {timestamp:.2f}"
    cv2.putText(frame, text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    
    return frame

async def video_stream_generator():
    """
    A generator function that continuously yields JPEG encoded frames.
    This is what creates the MJPEG stream.
    """
    while True:
        # Get the latest processed frame from your vision system
        frame = get_processed_frame()
        
        # Encode the frame as a JPEG image
        (flag, encodedImage) = cv2.imencode(".jpg", frame)
        
        # If encoding fails, skip this frame
        if not flag:
            continue
            
        # Yield the binary JPEG data with the correct HTTP headers
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
               bytearray(encodedImage) + b'\r\n')
        
        # Control the frame rate (e.g., ~30 FPS)
        await asyncio.sleep(0.03)

@router.get("/feed")
async def video_feed():
    """
    The main video feed endpoint. The iOS app will connect to this URL.
    It returns a streaming response that uses our generator.
    """
    return StreamingResponse(video_stream_generator(),
                             media_type="multipart/x-mixed-replace; boundary=frame")
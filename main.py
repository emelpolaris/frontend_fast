import base64
from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from http.server import HTTPServer, SimpleHTTPRequestHandler, test

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Unused CORSRequestHandler removed

@app.get('/')
async def read_root():
    return {"Message": "Detect Object!"}

@app.get('/detect/')
async def detect_objects():
    video_path = 'bus.jpg'
    cap = cv2.VideoCapture(video_path)

    width = int(cap.get(3))
    height = int(cap.get(4))

    if not cap.isOpened():
        print("Error opening video stream or file")
        return {"error": "Error opening video stream or file"}

    frame_count = 0
    while cap.isOpened():
        detections = np.empty((0, 5))
        ret, frame = cap.read()

        if not ret:
            print("Error reading frames")
            break

        frame = cv2.resize(frame, (640, 480))
        # Perform object detection on the frame here if needed

        # Encode the frame to base64
        _, buffer = cv2.imencode('.jpg', frame)
        frame_base64 = base64.b64encode(buffer).decode('utf-8')

        # You may want to store or process detections here

        return {"frame": frame_base64}

    cap.release()
    return {"message": "Video processing completed"}

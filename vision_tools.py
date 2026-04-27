import cv2
import numpy as np
import os
from datetime import datetime

def analyze_image(image_path):
    """Analyze an image and return basic metadata and properties."""
    if not os.path.exists(image_path):
        return f"❌ Error: Image file not found at {image_path}"
    
    try:
        img = cv2.imread(image_path)
        if img is None:
            return "❌ Error: Could not decode image."
        
        height, width, channels = img.shape
        size_kb = os.path.getsize(image_path) / 1024
        
        # Basic color analysis
        avg_color_per_row = np.average(img, axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        # BGR to RGB
        avg_color_rgb = [round(c) for c in avg_color[::-1]]
        
        return {
            "status": "success",
            "dimensions": f"{width}x{height}",
            "channels": channels,
            "size_kb": round(size_kb, 2),
            "average_color_rgb": avg_color_rgb,
            "message": f"🖼️ Image analyzed: {width}x{height} pixels, {channels} channels."
        }
    except Exception as e:
        return f"❌ Error during image analysis: {str(e)}"

def detect_faces(image_path):
    """Detect faces in an image using Haar Cascades."""
    if not os.path.exists(image_path):
        return f"❌ Error: Image file not found at {image_path}"
    
    try:
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Load pre-trained face detector
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        count = len(faces)
        if count > 0:
            return f"👤 Found {count} face(s) in the image."
        return "😶 No faces detected in the image."
    except Exception as e:
        return f"❌ Error during face detection: {str(e)}"

def take_snapshot(output_path="snapshot.jpg"):
    """Capture a frame from the default camera."""
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "❌ Error: Could not open camera."
        
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(output_path, frame)
            cap.release()
            return f"📸 Snapshot saved to {output_path}"
        
        cap.release()
        return "❌ Error: Could not read frame from camera."
    except Exception as e:
        return f"❌ Error during camera capture: {str(e)}"

def get_edge_detection(image_path, output_path="edges.jpg"):
    """Perform Canny edge detection on an image."""
    if not os.path.exists(image_path):
        return f"❌ Error: Image file not found at {image_path}"
    
    try:
        img = cv2.imread(image_path)
        edges = cv2.Canny(img, 100, 200)
        cv2.imwrite(output_path, edges)
        return f"⚡ Edge detection complete. Result saved to {output_path}"
    except Exception as e:
        return f"❌ Error during edge detection: {str(e)}"

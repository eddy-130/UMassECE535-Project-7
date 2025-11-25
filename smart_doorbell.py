import cv2
from picamera2 import Picamera2
from ultralytics import YOLO
import face_recognition
import pickle
import numpy as np
from datetime import datetime

# Load YOLO11n NCNN model for person detection
yolo_model = YOLO("yolo11n_ncnn_model")

# Load face encodings
print("Loading face encodings...")
with open("face_encodings.pickle", "rb") as f:
    data = pickle.load(f)
known_encodings = data["encodings"]
known_names = data["names"]

# Initialize Pi Camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

print("Smart Doorbell Active - Press 'q' to quit")

while True:
    # Capture frame from camera
    frame = picam2.capture_array()
    
    # Run YOLO person detection
    results = yolo_model(frame, imgsz=240, verbose=False)
    
    # Check if person detected (class 0 = person in COCO dataset)
    person_detected = False
    for result in results:
        for box in result.boxes:
            if int(box.cls[0]) == 0:  # Person class
                person_detected = True
                break
    
    # If person detected, run face recognition
    if person_detected:
        # Convert BGR to RGB for face_recognition library
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Find faces and encodings
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        
        # Check each face
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare with known faces
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
            name = "Unknown"
            
            # Find best match
            if True in matches:
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_names[best_match_index]
            
            # Draw box and label
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
            
            # Log detection
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Detected: {name}")
            
            # TODO: Add your alert/notification logic here
            # For example: send notification, ring doorbell, etc.
    
    # Display annotated frame
    annotated_frame = results[0].plot()
    cv2.imshow("Smart Doorbell", annotated_frame)
    
    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cv2.destroyAllWindows()
picam2.stop()
print("Doorbell stopped")

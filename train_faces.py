import face_recognition
import pickle
import cv2
import os

# Path to your dataset
dataset_path = "dataset"

# Lists to store encodings and names
known_encodings = []
known_names = []

# Loop through each person's folder
for person_name in os.listdir(dataset_path):
    person_folder = os.path.join(dataset_path, person_name)
    
    if not os.path.isdir(person_folder):
        continue
    
    print(f"Processing images for {person_name}...")
    
    # Process each image in the person's folder
    for image_file in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_file)
        
        # Load image and find face encodings
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)
        
        # Save encoding if face found
        if len(face_encodings) > 0:
            known_encodings.append(face_encodings[0])
            known_names.append(person_name)
            print(f"  Encoded {image_file}")
        else:
            print(f"  No face found in {image_file}")

# Save encodings to file
data = {"encodings": known_encodings, "names": known_names}
with open("face_encodings.pickle", "wb") as f:
    pickle.dump(data, f)

print(f"\nTraining complete! Saved {len(known_encodings)} face encodings.")

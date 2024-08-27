import cv2
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder



def mainModel():
        
    # Path to the directory containing training images
    dataset_path = "data"

    # Create the LBPH face recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Initialize the face detector (using Haar cascades)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Prepare training data
    faces = []
    labels = []

    # Iterate over the dataset directory
    for person_name in os.listdir(dataset_path):
        person_path = os.path.join(dataset_path, person_name)
        
        # Skip if not a directory
        if not os.path.isdir(person_path):
            continue
        
        for image_name in os.listdir(person_path):
            image_path = os.path.join(person_path, image_name)
            
            # Load the image in grayscale
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            
            # Detect face in the image
            faces_rects = face_cascade.detectMultiScale(image, scaleFactor=1.2, minNeighbors=5)
            
            for (x, y, w, h) in faces_rects:
                # Extract the face region of interest (ROI)
                face = image[y:y+w, x:x+h]
                
                # Append the face and label
                faces.append(face)
                labels.append(person_name)

    # Convert faces to have a consistent shape
    faces = [cv2.resize(face, (100, 100)) for face in faces]
    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(labels)

    # Convert faces and labels to numpy arrays
    faces = np.array(faces)
    labels = np.array(labels)
    labels = np.array(labels)

    # Train the recognizer
    recognizer.train(faces, labels)

    # Save the trained model
    recognizer.save("face_recognition_model.yml")
    np.save('label_encoder.npy', label_encoder.classes_)

    print("Model trained and saved as face_recognition_model.yml")





def CreateModel():
    if os.path.exists('face_recognition_model.yml'):
        os.remove('face_recognition_model.yml')
    if os.path.exists('label_encoder.npy'):
        os.remove('label_encoder.npy')

    mainModel()


if __name__ == "__main__":
    CreateModel()

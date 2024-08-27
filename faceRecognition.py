import cv2
import numpy as np

def recognizer():
    # Load the trained face recognition model
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("face_recognition_model.yml")
    label_encoder = np.load('label_encoder.npy')

    # Initialize the face detector (using Haar cascades)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Access the webcam (0 is the ID for the default camera)
    cap = cv2.VideoCapture(0)

    # Set the number of consecutive frames required to consider a person as unknown
    confidence_threshold = 80.0
    unknown_threshold = 30
    unknown_count = 0

    # Create a separate class for unknown persons
    unknown_class = "Unknown"

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces_rects = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.2, minNeighbors=5)

        for (x, y, w, h) in faces_rects:
            # Predict the face
            label, confidence = recognizer.predict(gray_frame[y:y+h, x:x+w])

            # If the confidence is below the threshold, map the label to the name
            if confidence < confidence_threshold:
                label_names = {i: label_encoder[i] for i in range(len(label_encoder))}
                name = label_names.get(label, unknown_class)
                unknown_count = 0  # Reset the unknown count
            else:
                name = unknown_class
                unknown_count += 1  # Increment the unknown count

            # Display the name and confidence on the frame
            cv2.putText(frame, f"{name}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # If no faces are detected, show "Unknown"
        if len(faces_rects) == 0:
            cv2.putText(frame, unknown_class, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        
        unknown_count += 1  # Increment the unknown count

        # If the unknown count exceeds the threshold, display "Unknown"
        if unknown_count >= unknown_threshold:
            cv2.putText(frame, unknown_class, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Show the frame
        cv2.imshow("Face Recognition", frame)

        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    recognizer()

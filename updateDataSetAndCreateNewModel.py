import cv2
import os
# import time
from model import CreateModel
import shutil

def TakeImage(name):
    # Initialize the camera (0 is usually the default camera)
    cap = cv2.VideoCapture(0)
   
    # Load the pre-trained Haar Cascade face detection model
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Failed to open the camera")
        return

    # Define the directory where you want to save the images
    save_dir = f"data/{name}"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Capture and save 20 images
    for i in range(20):
        ret, frame = cap.read()

        if ret:
            # Convert the frame to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Draw a rectangle around each detected face
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # Display the progress on the frame
            cv2.putText(frame, f"Image {i+1}/20", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

            # Display the frame in a window
            cv2.imshow('Camera', frame)

            # Define the image file name with an incremental index
            image_path = os.path.join(save_dir, f"image_{i+1}.jpg")

            # Save the image
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            cv2.imwrite(image_path, frame)
            print(f"Image {i+1} saved at: {image_path}")
        else:
            print(f"Failed to capture image {i+1}")

        # Wait for 1 seconds before taking the next image
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

    # Release the camera
    cap.release()

    # Close the camera window
    cv2.destroyAllWindows()

    # Create the new model
    CreateModel()


def remove_User(username):
    path = "data"
    user_found = False
    
    for item in os.listdir(path):
        if item == username:
            user_found = True
            print("User found")
            try:
                full_path = os.path.join(path, username)
                
                # Check if it's a file or directory
                if os.path.isfile(full_path):
                    os.remove(full_path)
                    print("User file removed")
                elif os.path.isdir(full_path):
                    shutil.rmtree(full_path)
                    print("User directory removed")
                
            except PermissionError:
                print("Access denied. Make sure you have the necessary permissions.")
            break
    
    if not user_found:
        print("User not found")
    CreateModel()   




if __name__ == "__main__":
    name = "Sayan Kumar Das"
    TakeImage(name)
    remove_User('Bill Gates')
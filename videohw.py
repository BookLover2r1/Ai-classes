import cv2

import numpy as np

from tensorflow.keras.models import load_model

from keras.preprocessing.image import img_to_array



# Load the pre-trained Haar Cascade Classifier for face detection

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')



# Load the emotion detection model (e.g., fer2013)

emotion_model = load_model('emotion_model.h5')  # Replace with your model path



# Define emotion labels

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']



# Start video capture from the default webcam

cap = cv2.VideoCapture(0)



if not cap.isOpened():

    print("Error: Could not open camera.")

    exit()



while True:

    ret, frame = cap.read()

    if not ret:

        print("Error: Failed to capture image")

        break



    # Convert frame to grayscale (Face detection works better on grayscale)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)



    # Detect faces in the grayscale image

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))



    # For each detected face, perform emotion recognition

    for (x, y, w, h) in faces:

        # Draw rectangle around the face

        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)



        # Extract the ROI for emotion detection

        roi_gray = gray[y:y + h, x:x + w]

        roi_color = frame[y:y + h, x:x + w]



        # Resize the face to match the input shape of the emotion model

        roi_resized = cv2.resize(roi_gray, (48, 48))

        roi_resized = roi_resized.astype('float32') / 255

        roi_resized = img_to_array(roi_resized)

        roi_resized = np.expand_dims(roi_resized, axis=0)

        

        # Predict emotion

        emotion_pred = emotion_model.predict(roi_resized)

        max_index = np.argmax(emotion_pred[0])

        predicted_emotion = emotion_labels[max_index]



        # Display the predicted emotion on the frame

        cv2.putText(frame, predicted_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)



    # Display the resulting frame

    cv2.imshow('Face and Emotion Detection', frame)



    # Exit on pressing the 'q' key

    if cv2.waitKey(1) & 0xFF == ord('q'):

        break



# Release the capture and close any open windows

cap.release()

cv2.destroyAllWindows()
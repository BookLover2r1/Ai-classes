import cv2
import mediapipe as mp
import time
import os
import numpy as np

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)


last_gesture_time = 0
debounce_delay = 1.0  
current_filter = "Normal"
feedback_message = ""
msg_expiry = 0


if not os.path.exists("captured_photos"):
    os.makedirs("captured_photos")

def apply_filter(img, filter_name):
    if filter_name == "Grayscale":
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    elif filter_name == "Sepia":
        kernel = np.array([[0.272, 0.534, 0.131],
                           [0.349, 0.686, 0.168],
                           [0.393, 0.769, 0.189]])
        sepia = cv2.transform(img, kernel)
        return np.clip(sepia, 0, 255).astype(np.uint8)
    elif filter_name == "Negative":
        return cv2.bitwise_not(img)
    elif filter_name == "Blur":
        return cv2.GaussianBlur(img, (15, 15), 0)
    return img

def get_distance(p1, p2):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    frame = cv2.flip(frame, 1) 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    current_time = time.time()
    

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_lms, mp_hands.HAND_CONNECTIONS)
            

            landmarks = hand_lms.landmark
            thumb_tip = landmarks[4]
            

            if current_time - last_gesture_time > debounce_delay:
                

                if get_distance(thumb_tip, landmarks[8]) < 0.05:
                    filtered_frame = apply_filter(frame.copy(), current_filter)
                    filename = f"captured_photos/photo_{int(time.time())}.jpg"
                    cv2.imwrite(filename, filtered_frame)
                    feedback_message = "PHOTO SAVED!"
                    msg_expiry = current_time + 2
                    last_gesture_time = current_time


                elif get_distance(thumb_tip, landmarks[12]) < 0.05:
                    current_filter = "Grayscale"
                    last_gesture_time = current_time
                elif get_distance(thumb_tip, landmarks[16]) < 0.05:
                    current_filter = "Sepia"
                    last_gesture_time = current_time
                elif get_distance(thumb_tip, landmarks[20]) < 0.05:
                    current_filter = "Negative"
                    last_gesture_time = current_time
                elif get_distance(thumb_tip, landmarks[17]) < 0.05:  
                    current_filter = "Blur"
                    last_gesture_time = current_time


    frame = apply_filter(frame, current_filter)


    cv2.putText(frame, f"Filter: {current_filter}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    if current_time < msg_expiry:
        cv2.putText(frame, feedback_message, (200, 250), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

    cv2.imshow("Gesture Photo App", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
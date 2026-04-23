import cv2
import mediapipe as mp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

# --- Setup MediaPipe ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# --- Setup Volume Control (Pycaw) ---
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
vol_range = volume.GetVolumeRange()  # (-65.25, 0.0)
min_vol, max_vol = vol_range[0], vol_range[1]

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, img = cap.read()
    if not success: break
    
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)
    
    vol_bar = 400 # Initial bar position
    bright_bar = 400

    if results.multi_hand_landmarks:
        for hand_lms in results.multi_hand_landmarks:
            # Get specific landmarks (Thumb tip: 4, Index tip: 8)
            lm_list = []
            for id, lm in enumerate(hand_lms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])

            if lm_list:
                x1, y1 = lm_list[4][1], lm_list[4][2] # Thumb
                x2, y2 = lm_list[8][1], lm_list[8][2] # Index
                
                # Draw circles and line
                cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # Calculate distance
                length = math.hypot(x2 - x1, y2 - y1)

                # --- CONTROL LOGIC ---
                # Map distance (approx 20 to 200 pixels) to volume/brightness
                # Adjust '20' and '200' based on how far you sit from the cam
                vol = np.interp(length, [20, 200], [min_vol, max_vol])
                bright = np.interp(length, [20, 200], [0, 100])
                
                vol_bar = np.interp(length, [20, 200], [400, 150])
                bright_bar = np.interp(length, [20, 200], [400, 150])

                # Apply changes
                volume.SetMasterVolumeLevel(vol, None)
                sbc.set_brightness(int(bright))

            mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS)

    # --- Visual Feedback (The Bars) ---
    # Volume Bar (Left)
    cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(img, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(img, 'VOL', (45, 430), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

    # Brightness Bar (Right)
    cv2.rectangle(img, (550, 150), (585, 400), (255, 0, 0), 3)
    cv2.rectangle(img, (550, int(bright_bar)), (585, 400), (255, 0, 0), cv2.FILLED)
    cv2.putText(img, 'BRIGHT', (520, 430), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.imshow("Gesture Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
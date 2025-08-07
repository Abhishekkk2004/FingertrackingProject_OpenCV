import cv2
import HandTrackingModule as htm
import time
import numpy as np
import math
import subprocess

# Set camera dimensions
wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

# FPS variables
pTime = 0

# Initialize hand detector
detector = htm.handDetector(detectionCon=0.8)

def set_volume_mac(vol_percent):
    vol_percent = int(np.clip(vol_percent, 0, 100))
    subprocess.call(["osascript", "-e", f"set volume output volume {vol_percent}"])

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Thumb tip and index tip
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        # Center point and distance
        cx, cy = (x1 + x2)//2, (y1 + y2)//2
        length = math.hypot(x2 - x1, y2 - y1)

        # Display the distance
        cv2.putText(img, f'Distance: {int(length)}', (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Map the length (20–200 px) to volume (0–100%)
        volume = np.interp(length, [20, 200], [0, 100])
        set_volume_mac(volume)

        # UI feedback
        cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
        cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)

        cv2.putText(img, f'Volume: {int(volume)}%', (40, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

         #Creating a volume bar
        cv2.rectangle(img, (50, 100), (90, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(400 - (volume * 3))), (90, 400), (0, 255, 0), cv2.FILLED)
    else:
        cv2.putText(img, 'No Hand Detected', (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # FPS display
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Show window
    cv2.imshow("Volume Control", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

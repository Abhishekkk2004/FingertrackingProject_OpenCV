import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
capture = cv2.VideoCapture(1)  # 0 for default webcam
    
detector = htm.handDetector()
pTime = 0
cTime = 0
    
while True:
    success, img = capture.read()
    if not success:
        break
    
    img = detector.findHands(img)
    
    lmList = detector.findPosition(img)
    if len(lmList) != 0:
        print(lmList[4])  # Print the position of the thumb tip (id=4)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
        
    cv2.putText(img, f'FPS: {int(fps)}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("Image", img)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
            
capture.release()
cv2.destroyAllWindows()

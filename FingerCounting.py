import cv2
import time
import os
import mediapipe as mp
import HandTrackingModule as htm
import numpy as np

# Set the width and height of the camera
wCam, hCam = 640, 480

capture = cv2.VideoCapture(1)  # 0 for default webcam

capture.set(3, wCam)  # Set width
capture.set(4, hCam)  # Set height

folderPath = '/Users/abhishek/Desktop/LLMS_Architecture/CV_Projects/Hand_Tracking/fingers'  # Path to the folder containing images
myList = os.listdir(folderPath)  # List of images in the directory

# Sort filenames numerically
myList.sort(key=lambda x: int(x.split('.')[0]))

print("Sorted filenames:", myList)



overLayList = []
for imgPath in myList:
    image = cv2.imread(f'{folderPath}/{imgPath}')  # Read each image
    overLayList.append(image)  # Append the image to the overlay list
#sort the overlay list based on the name of the image

print(overLayList)


pTime = 0  # Previous time for FPS calculation
cTime = 0  # Current time for FPS calculation

detector = htm.handDetector( detectionCon=0.75)  # Initialize the hand detector


tipIds = [4, 8, 12, 16, 20]  # List of tip IDs for fingers (thumb, index, middle, ring, pinky)


while True:
    success, img = capture.read()
    if not success:
        print("Failed to capture image")
        break
    img = detector.findHands(img)  # Detect hands in the imageq
    lmList = detector.findPosition(img,draw=False)  # Get the positions of the landmarks
    # print(lmList)  # Print the list of landmarks


    if len(lmList) != 0:
        fingers = []
        for id in range(1, 5):
             # Check if the tip of the finger is up
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)  # Finger is up
            else:
                fingers.append(0)  # Finger is down
        # print(fingers)  # Print the list of fingers

        #Special case for thumb for right hand
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)  # Thumb is up
        else:
            fingers.append(0) # Thumb is down
        
        # Count the number of fingers up
        totalFingers = fingers.count(1)



        # Display the count of fingers on the image
        
   
        overlay_resized = cv2.resize(overLayList[totalFingers-1], (200, 200))
        img[0:200, 0:200] = overlay_resized

        #Write the count of fingers on the image as "No of Fingers: X"
        cv2.putText(img, f'No of Fingers: {totalFingers}', (250, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 4)


    cTime = time.time()  # Current time
    fps = 1 / (cTime - pTime)
    pTime = cTime  # Update previous time
    cv2.putText(img, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)



    # Display the captured image
    cv2.imshow("Image", img)
    cv2.waitKey(1)  # Wait for a key press to continue
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
capture.release()  # Release the camera
cv2.destroyAllWindows()  # Close all OpenCV windows

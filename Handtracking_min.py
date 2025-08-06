import cv2
import mediapipe as mp
import time

capture = cv2.VideoCapture(1)


mpHandds = mp.solutions.hands
hands = mpHandds.Hands()
mpDraw = mp.solutions.drawing_utils # Drawing utilities for drawing landmarks on the image


#Frame rate calculation
pTime = 0
cTime = 0

# Main loop to capture video frames
while True:
    success, img = capture.read()

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #Convert BGR to RGB as hands module works with RGB
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks) #Prints the landmarks of detected hands 

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: # Iterate through each hand detected

            for id, lm in enumerate(handLms.landmark): # Iterate through each landmark in the hand
            #Each id corresponds to a specific landmark i.e # 0: Wrist, 1: Thumb CMC, 2: Thumb MCP, 3: Thumb IP, 4: Thumb Tip, etc.
                
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h) # Get the x and y coordinates of the landmark
                # print(id, cx, cy) # Print the id and coordinates of the landmark
                
                if id == 4: # If the landmark is the thumb tip
                    cv2.circle(img, (cx, cy), 30, (255, 0, 255), cv2.FILLED) # Draw a circle on the wrist landmark
            mpDraw.draw_landmarks(img, handLms, mpHandds.HAND_CONNECTIONS) # Draw landmarks and connections on the image


    cTime = time.time() # Current time
    fps = 1 / (cTime - pTime) # Calculate frames per second
    pTime = cTime # Update previous time

    cv2.putText(img, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("Image", img)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
capture.release()
cv2.destroyAllWindows()
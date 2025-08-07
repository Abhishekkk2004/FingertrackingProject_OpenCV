import cv2
import numpy as np
import os
import HandTrackingModule as htm

folderPath = "WithoutBg"
myList = os.listdir(folderPath)  # List of images in the directory
# Sort filenames numerically
myList.sort(key=lambda x: int(x.split('.')[0]))

##########
brushThickness = 15  # Thickness of the brush


overlayList = []
for imPath in myList:
    # Load with alpha channel
    image = cv2.imread(f'{folderPath}/{imPath}', cv2.IMREAD_UNCHANGED)
    overlayList.append(image)
print(len(overlayList))

# Function to get overlay components
# Returns the BGR image, alpha channel, height, and width of the overlay
# This function is used to overlay images with transparency
# on the main image in the PaintApp.py
def get_overlay_components(index):
    header_rgba = overlayList[index]
    bgr = header_rgba[:, :, :3]
    alpha = header_rgba[:, :, 3] / 255.0
    h, w = bgr.shape[:2]
    return bgr, alpha, h, w

bgr, alpha, h, w = get_overlay_components(0) #By default, we get the first overlay image

#Red Colour for the brush
brushColor = (0, 0, 255)

# Initialize the hand detector
detector = htm.handDetector(detectionCon=0.65,maxHands=1)
xp, yp = 0, 0


imgCanvas = np.zeros((720, 1280, 3), np.uint8)
cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)

while True:
    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)


    # 2. Find hand landmarks
    img = detector.findHands(img, draw=False)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        # Get the tip of the index finger
        x1, y1 = lmList[8][1], lmList[8][2]  # Index finger tip coordinates
        x2, y2 = lmList[12][1], lmList[12][2]  # Middle finger tip coordinates

        fingers = detector.fingersUp()  # Get the status of fingers

        # 3. If selection mode is active
        if fingers[0]  and fingers[1]:
            xp, yp = 0, 0  # Reset previous point
            # print("Selection Mode")
            #Drawing a rectangle around the selected area
            cv2.rectangle(img, (x1-30, y1 - 30), (x2+30, y2+30), brushColor, cv2.FILLED)

            #Checking for the click
            if y1 < 125:
                if 60 < x1 < 240:
                    bgr, alpha, h, w = get_overlay_components(0)
                    brushColor= (0, 0, 255)  # Red color for the brush
                elif 340 < x1 < 520:
                    bgr, alpha, h, w = get_overlay_components(1)
                    brushColor = (0, 255, 0)  # Green color for the brush
                elif 600 < x1 < 780:
                    bgr, alpha, h, w = get_overlay_components(2)
                    brushColor = (0, 255, 255)
                elif 840 < x1 < 970:
                    brushColor = (255, 0, 0)
                    bgr, alpha, h, w = get_overlay_components(3)
                elif 1020 < x1 < 1180:
                    brushColor = (0, 0, 0)
                    bgr, alpha, h, w = get_overlay_components(4)
            


        # 4. If drawing mode is active
        if fingers[0] and fingers[1]== 0:    
            # print("Drawing Mode")
            #Drawing a circle on the selected area
            

            if xp == 0 and yp == 0:  # If previous point is not set
                xp, yp = x1, y1  # Set previous point to current point

                #Custom condition for erasor
            if brushColor == (0, 0, 0):
                cv2.line(imgCanvas, (x1, y1), (xp, yp), brushColor, brushThickness + 45)
                cv2.circle(img, (x1, y1), 30 , brushColor, cv2.FILLED)
            else:
                # Draw a line from previous point to current point
                cv2.circle(img, (x1, y1), brushThickness, brushColor, cv2.FILLED)
                cv2.line(imgCanvas, (x1, y1), (xp, yp), brushColor, brushThickness)  # Draw on the canvas

            xp, yp = x1, y1  # Update previous point to current point


    # Overlay header with transparency

    for c in range(3):
        img[0:h, 0:w, c] = img[0:h, 0:w, c] * (1 - alpha) + bgr[:, :, c] * alpha


    # blending the canvas with the main image
    # img = cv2.addWeighted(img, 0.5, imgCanvas, 0.5, 0)

    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)  # Invert the grayscale image
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)  # Convert back to BGR

    img = cv2.bitwise_and(img, imgInv)  # Apply the inverted mask to the main image
    img = cv2.bitwise_or(img, imgCanvas)  # Combine the canvas with the main image

    # Display the images
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)

    cv2.waitKey(1)  # Wait for a key press to continue
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



cap.release()  # Release the camera
cv2.destroyAllWindows()  # Close all OpenCV windows


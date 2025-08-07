# Computer Vision Projects using MediaPipe and OpenCV

This repository contains three real-time computer vision applications built using **MediaPipe** and **OpenCV**, designed to demonstrate hand tracking and gesture-based interaction.

## 🛠️ Setup Instructions

Follow the steps below to set up your environment and run the applications.

### 1. Create a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

```
# Navigate to your desired project folder
cd /path/to/your/project

# Create a virtual environment named 'cv'
python3 -m venv cv

# Activate the virtual environment
# On macOS/Linux:
source cv/bin/activate

# On Windows:
cv\Scripts\activate

```
2. Install Dependencies
Make sure your virtual environment is activated, then run:

```
pip install opencv-python mediapipe
```
🧠 Application Descriptions
1. ✋ Finger Number Detector (Real-Time)
Description:
This application uses hand tracking to detect how many fingers are being held up in real-time using a webcam. It employs MediaPipe's hand landmarks to count extended fingers and displays the result on the video feed.

Features:

Real-time hand tracking

Finger state detection (open/closed)

Dynamic counting from 0 to 5 fingers

Use Case:
Useful in gesture-based control systems or touchless input interfaces.

2. 🎨 Paint Art - Draw on Screen
Description:
A virtual drawing app that allows users to draw on the screen using finger gestures. The index finger is used to draw, while specific gestures (like using two fingers) can switch modes or colors.

Features:

Draw with finger in air

Change brush color or thickness using gestures

Clear screen with a specific gesture

Use Case:
Great for creative expression, educational tools, or interactive whiteboards.

3. 🔊 Volume Controller
Description:
This app allows users to control the system volume using the distance between their thumb and index finger. As the fingers come closer or move apart, the system volume changes accordingly.

Features:

Real-time finger distance measurement

Smooth volume control interface

Visual volume feedback on screen

Use Case:
Ideal for hands-free media control systems or accessibility tools.

🚀 Run Any Application
Once dependencies are installed and your virtual environment is active:

```
python FingerCounting.py    # For Finger Number Detector
python PaintApp.py          # For Paint Art
python VolumeHandControl.py    # For Volume Controller
```

Make sure your webcam is enabled and accessible by OpenCV.

📎 Notes
These applications require a working webcam.
## Before using these applications, make sure to have the HandTrackingModule.py module within the same folder

Performance may vary based on lighting and background conditions.

For best results, use a plain background and keep your hand in the frame.


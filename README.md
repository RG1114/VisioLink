# VisioLink

This project provides a **low-cost virtual reality solution** that uses:
- A **smartphone** as a VR display (via a simple VR headset like Google Cardboard),
- A **laptop webcam** to track **head and hand motions** using **computer vision**, and
- **Real-time network communication** between the laptop and phone to drive the VR experience.

Inspired by existing tools like **OpenTrack**, **Webcam Motion Capture**, and **MediaPipe-based tracking**, this system replaces expensive VR hardware (like Oculus controllers or full-body trackers) with a software solution driven by **OpenCV**, **MediaPipe**, and **WebSockets**.

---

## 📱🖥️ System Overview

There are **two components**:

- **Laptop/Desktop** (Motion Tracker):
  - Captures webcam feed.
  - Uses machine vision (MediaPipe) to detect head pose and hand gestures.
  - Sends real-time control signals to the phone via WebSockets.

- **Smartphone** (VR Display):
  - Runs a Unity/WebXR-based app displaying a stereoscopic VR scene.
  - Receives and applies motion control signals from the laptop.

---

## 🔧 How to Run

### Prerequisites

- Python 3.7 or higher
- A smartphone with a simple VR headset (like Google Cardboard)
- A laptop with an HD webcam
- Both devices connected to the same local Wi-Fi network

### Setup Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Motion Tracking Server**

    ```bash
    python app.py
    ```
4. **Launch the VR App on Phone**

- Deploy your Unity/WebXR VR scene to your phone.

- Ensure the mobile app is set to receive WebSocket messages from the laptop's IP.

import React, { useState, useEffect } from "react";
import Connection from "./components/Connection";
import ControlPanel from "./components/ControlPanel";
import "./App.css";

function App() {
  const [serverIp, setServerIp] = useState("");
  const [connectionStatus, setConnectionStatus] = useState("Disconnected");
  const [gesture, setGesture] = useState("");
  const [isCameraActive, setIsCameraActive] = useState(false);

  // Fetch IP and continuously poll for connection status from forward.py
  useEffect(() => {
    // 1. Fetch the IP from forward.py (port 5001)
    fetch("http://localhost:5001/my-ip")
      .then((res) => res.json())
      .then((data) => setServerIp(data.ip || ""))
      .catch((err) => console.error("Error fetching IP:", err));

    // 2. Poll the connection status every 3 seconds
    const statusInterval = setInterval(() => {
      fetch("http://localhost:5001/connection-status")
        .then((res) => res.json())
        .then((data) => {
          if (data.connected) {
            setConnectionStatus("Connected");
          } else {
            setConnectionStatus("Disconnected");
          }
        })
        .catch((err) => console.error("Error checking connection status:", err));
    }, 3000);

    return () => clearInterval(statusInterval);
  }, []);

  // Start the ML camera script (via Node server on port 5000)
  const startCamera = () => {
    setIsCameraActive(true);
    fetch("http://localhost:5000/start-camera")
      .then(() => {
        console.log("Camera started");
        // (Optional) Simulate random gestures if you want to see UI updates
        // Or remove this entirely if your run_gesture_model.py handles sending real gestures
        const gestures = [
          "Open Hand",
          "Closed Fist",
          "Peace Sign",
          "Pointing",
          "Thumbs Up",
        ];
        const gestureInterval = setInterval(() => {
          const randomGesture =
            gestures[Math.floor(Math.random() * gestures.length)];
          setGesture(randomGesture);
        }, 3000);
        window.gestureInterval = gestureInterval;
      })
      .catch((err) => {
        console.error("Error starting camera:", err);
        setIsCameraActive(false);
      });
  };

  // Stop the ML camera script (via Node server)
  const stopCamera = () => {
    setIsCameraActive(false);
    setGesture("");
    if (window.gestureInterval) {
      clearInterval(window.gestureInterval);
    }
    fetch("http://localhost:5000/stop-camera")
      .then(() => console.log("Camera stopped"))
      .catch((err) => console.error("Error stopping camera:", err));
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>VR Gesture Control</h1>
      </header>

      <main className="app-content">
        <Connection ip={serverIp} status={connectionStatus} />

        <div className="camera-controls">
          <button
            className={`camera-btn ${isCameraActive ? "active" : ""}`}
            onClick={isCameraActive ? stopCamera : startCamera}
          >
            {isCameraActive ? "Stop Camera" : "Start Gesture Detection"}
          </button>
        </div>

        <ControlPanel detectedGesture={gesture} isActive={isCameraActive} />
      </main>

      <footer className="app-footer">
        <p>VR Gesture Control Interface &copy; {new Date().getFullYear()}</p>
      </footer>
    </div>
  );
}

export default App;

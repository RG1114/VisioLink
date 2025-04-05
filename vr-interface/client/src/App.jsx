import React, { useState, useEffect } from "react";
import Connection from "./components/Connection";
import ControlPanel from "./components/ControlPanel";
import "./App.css";

function App() {
  const [serverIp, setServerIp] = useState("");
  const [connectionStatus, setConnectionStatus] = useState("Disconnected");
  const [gesture, setGesture] = useState("");
  const [isCameraActive, setIsCameraActive] = useState(false);

  // Fetch the IP and poll the connection status from forward.py (port 5001)
  useEffect(() => {
    // Fetch the server IP from forward.py
    fetch("http://localhost:5001/my-ip")
      .then((res) => res.json())
      .then((data) => setServerIp(data.ip || ""))
      .catch((err) => console.error("Error fetching IP:", err));

    // Poll the connection status every 3 seconds
    const statusInterval = setInterval(() => {
      fetch("http://localhost:5001/connection-status")
        .then((res) => res.json())
        .then((data) => {
          setConnectionStatus(data.connected ? "Connected" : "Disconnected");
        })
        .catch((err) => console.error("Error checking connection status:", err));
    }, 3000);

    return () => clearInterval(statusInterval);
  }, []);

  // Start the ML camera script via Node server (port 5000) and begin polling for real gestures
  const startCamera = () => {
    setIsCameraActive(true);
    fetch("http://localhost:5000/start-camera")
      .then(() => {
        console.log("Camera started");
        // Start polling for gesture from forward.py every second
        const gesturePolling = setInterval(() => {
          fetch("http://localhost:5001/get-latest-gesture")
            .then((res) => res.json())
            .then((data) => {
              setGesture(data.gesture || "No gesture");
            })
            .catch((err) => console.error("Error fetching gesture:", err));
        }, 1000);
        window.gesturePollingInterval = gesturePolling;
      })
      .catch((err) => {
        console.error("Error starting camera:", err);
        setIsCameraActive(false);
      });
  };

  // Stop the ML camera script and stop gesture polling
  const stopCamera = () => {
    setIsCameraActive(false);
    setGesture("");
    if (window.gesturePollingInterval) {
      clearInterval(window.gesturePollingInterval);
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

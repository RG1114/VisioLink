import React, { useState, useEffect } from "react";
import Connection from "./components/Connection";
import ControlPanel from "./components/ControlPanel";
import "./App.css";

function App() {
    const [serverIp, setServerIp] = useState("");
    const [connectionStatus, setConnectionStatus] = useState("Disconnected");
    const [gesture, setGesture] = useState("");

    useEffect(() => {
        fetch("/get-ip")
            .then((res) => res.json())
            .then((data) => setServerIp(data.ip))
            .catch((err) => console.error("Error fetching IP:", err));
    }, []);

    const startCamera = () => {
        fetch("/start-camera")
            .then(() => console.log("Camera started"))
            .catch((err) => console.error("Error starting camera:", err));
    };

    return (
        <div className="app-container">
            <h1>VR Gesture Control Interface</h1>

            <Connection ip={serverIp} status={connectionStatus} />

            <button className="camera-btn" onClick={startCamera}>
                Open Camera for Gesture Detection
            </button>

            <ControlPanel detectedGesture={gesture} />
        </div>
    );
}

export default App;

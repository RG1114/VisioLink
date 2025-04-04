import React from "react";
import "./ControlPanel.css";

const ControlPanel = ({ detectedGesture }) => {
    return (
        <div className="gesture-box">
            <h3>Detected Gesture:</h3>
            <p className="gesture-text">{detectedGesture || "No gesture detected"}</p>
        </div>
    );
};

export default ControlPanel;

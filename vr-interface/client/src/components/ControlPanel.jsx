import React from "react";
import "./ControlPanel.css";

const ControlPanel = ({ detectedGesture, isActive }) => {
  return (
    <div className={`gesture-panel ${isActive ? "active" : "inactive"}`}>
      <h3>Detected Gesture</h3>
      <div className="gesture-display">
        {isActive ? (
          detectedGesture ? (
            <>
              <div className="gesture-icon">{getGestureIcon(detectedGesture)}</div>
              <p className="gesture-text">{detectedGesture}</p>
            </>
          ) : (
            <div className="waiting-animation">
              <div className="pulse"></div>
              <p>Waiting for gesture...</p>
            </div>
          )
        ) : (
          <p className="inactive-text">Camera inactive</p>
        )}
      </div>
      {detectedGesture && (
        <div className="gesture-description">
          {getGestureDescription(detectedGesture)}
        </div>
      )}
    </div>
  );
};

// Helper function to return gesture icon (can be replaced with actual icons)
const getGestureIcon = (gesture) => {
  switch (gesture.toLowerCase()) {
    case "open hand":
      return "✋";
    case "closed fist":
      return "✊";
    case "peace sign":
      return "✌️";
    case "pointing":
      return "👆";
    case "thumbs up":
      return "👍";
    default:
      return "🖐️";
  }
};

// Helper function to return gesture descriptions
const getGestureDescription = (gesture) => {
  switch (gesture.toLowerCase()) {
    case "open hand":
      return "Navigate menu / Select all";
    case "closed fist":
      return "Grab object / Confirm selection";
    case "peace sign":
      return "Split view / Create duplicate";
    case "pointing":
      return "Select item / Navigate UI";
    case "thumbs up":
      return "Approve / Confirm action";
    default:
      return "Action not assigned";
  }
};

export default ControlPanel;

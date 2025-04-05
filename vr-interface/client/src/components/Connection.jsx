import React, { useState } from "react";
import "./Connection.css";

const Connection = ({ ip, status }) => {
  const [copySuccess, setCopySuccess] = useState(false);

  const copyIpToClipboard = () => {
    navigator.clipboard.writeText(ip);
    setCopySuccess(true);
    setTimeout(() => {
      setCopySuccess(false);
    }, 2000);
  };

  return (
    <div className="connection-container">
      <div className="connection-card">
        <div className="ip-section">
          <h2>Server IP Address</h2>
          <div className="ip-display">
            <p className="ip-address">{ip || "Fetching..."}</p>
            <button
              className="copy-btn"
              onClick={copyIpToClipboard}
              aria-label="Copy IP address to clipboard"
            >
              {copySuccess ? "Copied!" : "Copy"}
            </button>
          </div>
        </div>

        <div className="status-section">
          <h2>Status</h2>
          <div className={`connection-status ${status.toLowerCase()}`}>
            <div className="status-indicator"></div>
            <p>{status}</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Connection;

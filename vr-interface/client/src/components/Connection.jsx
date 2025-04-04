import React from "react";
import "./Connection.css";

const Connection = ({ ip, status }) => {
    return (
        <div className="connection-container">
            <div className="ip-card">
                <h2>Your Server IP</h2>
                <p className="ip-address">{ip || "Fetching..."}</p>
                <button className="copy-btn" onClick={() => navigator.clipboard.writeText(ip)}>
                    Copy IP
                </button>
            </div>

            <div className={`connection-status ${status === 'Connected' ? 'connected' : 'disconnected'}`}>
                <p>{status}</p>
            </div>
        </div>
    );
};

export default Connection;

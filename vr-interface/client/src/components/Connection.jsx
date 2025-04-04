// src/components/Connection.jsx
import React, { useState, useEffect } from 'react';
import socket from '../socket';

const Connection = ({ onConnected }) => {
  const [ipAddress, setIpAddress] = useState('');
  const [status, setStatus] = useState('Not Connected');

  useEffect(() => {
    // Listen for connection confirmation from server
    socket.on('connect', () => {
      setStatus('Connected');
      // You might want to pass the socket id or IP info
      onConnected(socket.id);
    });

    socket.on('disconnect', () => {
      setStatus('Disconnected');
    });

    // Clean up listeners on unmount
    return () => {
      socket.off('connect');
      socket.off('disconnect');
    };
  }, [onConnected]);

  const handleConnect = () => {
    // In a real scenario, you might send the IP address to the server
    // For this prototype, we're just triggering the socket connection.
    if (ipAddress.trim() === '') {
      alert('Please enter an IP address');
      return;
    }
    // Emit an event to the backend to simulate connection
    socket.emit('message', `Attempting connection from ${ipAddress}`);
    setStatus('Connecting...');
  };

  return (
    <div style={styles.container}>
      <h2>Device Connection</h2>
      <div style={styles.inputGroup}>
        <input
          type="text"
          placeholder="Enter IP address"
          value={ipAddress}
          onChange={(e) => setIpAddress(e.target.value)}
          style={styles.input}
        />
        <button onClick={handleConnect} style={styles.button}>Connect</button>
      </div>
      <p>Status: {status}</p>
    </div>
  );
};

const styles = {
  container: {
    padding: '20px',
    background: '#1e1e1e',
    color: '#fff',
    borderRadius: '8px',
    textAlign: 'center',
    margin: '20px auto',
    maxWidth: '400px',
  },
  inputGroup: {
    display: 'flex',
    justifyContent: 'center',
    marginBottom: '10px',
  },
  input: {
    padding: '10px',
    fontSize: '1rem',
    borderRadius: '4px 0 0 4px',
    border: 'none',
    outline: 'none',
    width: '70%',
  },
  button: {
    padding: '10px',
    fontSize: '1rem',
    borderRadius: '0 4px 4px 0',
    border: 'none',
    cursor: 'pointer',
    background: '#007bff',
    color: '#fff',
  },
};

export default Connection;

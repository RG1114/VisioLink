// src/components/GameLauncher.jsx
import React from 'react';

const GameLauncher = ({ connectionInfo }) => {
  const handleLaunchGame = () => {
    // Redirect to Unity game URL or trigger Unity launch mechanism
    // For demonstration, we simply alert and simulate a redirect
    if (!connectionInfo) {
      alert('No connection established!');
      return;
    }
    alert(`Launching game with connection: ${connectionInfo}`);
    // For example, redirect to a URL
    window.location.href = 'http://localhost:5000'; // Replace with your Unity game's URL or launch mechanism
  };

  return (
    <div style={styles.container}>
      <h2>Game Launcher</h2>
      <div style={styles.card}>
        <h3>Awesome VR Game</h3>
        <p>A thrilling VR experience awaits you.</p>
        <button onClick={handleLaunchGame} style={styles.button}>Launch Game</button>
      </div>
    </div>
  );
};

const styles = {
  container: {
    padding: '20px',
    textAlign: 'center',
  },
  card: {
    background: '#2d2d2d',
    color: '#fff',
    padding: '20px',
    borderRadius: '8px',
    display: 'inline-block',
    margin: '10px',
  },
  button: {
    padding: '10px 20px',
    fontSize: '1rem',
    borderRadius: '4px',
    border: 'none',
    cursor: 'pointer',
    background: '#28a745',
    color: '#fff',
  },
};

export default GameLauncher;

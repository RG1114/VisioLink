// src/App.jsx
import React, { useState } from 'react';
import Connection from './components/Connection';
import GameLauncher from './components/GameLauncher';

const App = () => {
  const [connectionInfo, setConnectionInfo] = useState(null);

  return (
    <div style={styles.app}>
      <h1 style={styles.title}>InMotion VR Interface</h1>
      {!connectionInfo ? (
        <Connection onConnected={(info) => setConnectionInfo(info)} />
      ) : (
        <GameLauncher connectionInfo={connectionInfo} />
      )}
    </div>
  );
};

const styles = {
  app: {
    background: '#121212',
    minHeight: '100vh',
    color: '#fff',
    fontFamily: 'Arial, sans-serif',
    padding: '20px',
  },
  title: {
    textAlign: 'center',
  },
};

export default App;

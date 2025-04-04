// src/socket.js
import { io } from 'socket.io-client';

// Connect to your backend (adjust URL/port if needed)
const socket = io('http://localhost:4000', {
  transports: ['websocket'], // Use WebSocket for low latency
});

export default socket;

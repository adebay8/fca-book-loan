// src/config.js
// Central place to store app-wide config values

const backendUrl = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export default backendUrl;

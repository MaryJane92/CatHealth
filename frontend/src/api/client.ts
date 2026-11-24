/**
 * API-клиент для взаимодействия с backend.
 * Базовый URL — /api, проксируется через Vite на http://127.0.0.1:8000.
 */
import axios from "axios";

export const apiClient = axios.create({
  baseURL: "/api",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 30000,
});

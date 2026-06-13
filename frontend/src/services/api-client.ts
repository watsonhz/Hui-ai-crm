/** Typed HTTP client wrapping axios, reading base URL from Vite env vars. */

import axios, { type AxiosInstance, type AxiosRequestConfig } from 'axios';
import type { ApiResponse } from '@/types/customer';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1';

const client: AxiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 15000,
  headers: { 'Content-Type': 'application/json' },
});

// Response interceptor — unwrap the standard envelope
client.interceptors.response.use(
  (res) => {
    const body = res.data as ApiResponse<unknown>;
    if (body.code !== 200) {
      return Promise.reject(new Error(body.message || 'API error'));
    }
    return res;
  },
  (err) => {
    if (err.response) {
      const body = err.response.data as ApiResponse<unknown>;
      return Promise.reject(new Error(body?.message || `HTTP ${err.response.status}`));
    }
    return Promise.reject(err);
  },
);

/** GET helper — returns unwrapped data directly */
export async function get<T>(url: string, params?: Record<string, unknown>): Promise<T> {
  const res = await client.get<ApiResponse<T>>(url, { params });
  return res.data.data as T;
}

/** POST helper */
export async function post<T>(url: string, data?: unknown, config?: AxiosRequestConfig): Promise<T> {
  const res = await client.post<ApiResponse<T>>(url, data, config);
  return res.data.data as T;
}

/** PUT helper */
export async function put<T>(url: string, data?: unknown): Promise<T> {
  const res = await client.put<ApiResponse<T>>(url, data);
  return res.data.data as T;
}

/** DELETE helper */
export async function del<T>(url: string): Promise<T> {
  const res = await client.delete<ApiResponse<T>>(url);
  return res.data.data as T;
}

export { client };

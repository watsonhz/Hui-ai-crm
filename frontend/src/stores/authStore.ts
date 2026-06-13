import { create } from 'zustand';
import client from '../api/client';

interface User { id: number; username: string; role: string; full_name: string; }

interface AuthState {
  user: User | null;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (username: string, password: string, email?: string, fullName?: string) => Promise<void>;
  logout: () => void;
  fetchMe: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: localStorage.getItem('token'),
  login: async (username, password) => {
    const res: any = await client.post('/auth/login', { username, password });
    localStorage.setItem('token', res.data.access_token);
    set({ token: res.data.access_token, user: res.data.user });
  },
  register: async (username, password, email, fullName) => {
    await client.post('/auth/register', { username, password, email, full_name: fullName });
  },
  logout: () => {
    localStorage.removeItem('token');
    set({ token: null, user: null });
    window.location.href = '/login';
  },
  fetchMe: async () => {
    try {
      const res: any = await client.get('/auth/me');
      set({ user: res.data });
    } catch { set({ user: null, token: null }); }
  },
}));

import { useEffect, useState } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { Spin } from 'antd';
import { useAuthStore } from '../stores/authStore';

export default function AuthGuard() {
  const { user, token, fetchMe } = useAuthStore();
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    if (token && !user) fetchMe().finally(() => setChecking(false));
    else setChecking(false);
  }, []);

  useEffect(() => {
    const handler = () => setChecking(false);
    window.addEventListener('auth:logout', handler);
    return () => window.removeEventListener('auth:logout', handler);
  }, []);

  if (checking) return <Spin size="large" style={{ display: 'block', marginTop: 200 }} />;
  if (!token) return <Navigate to="/login" replace />;
  return <Outlet />;
}

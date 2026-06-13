import { Routes, Route, Navigate } from 'react-router-dom';

function Dashboard() {
  return (
    <div>
      <h1>AI-CRM 数据仪表盘</h1>
      <p>
        API Base: {import.meta.env.VITE_API_BASE_URL} | Mock:{' '}
        {import.meta.env.VITE_ENABLE_MOCK === 'true' ? 'ON' : 'OFF'}
      </p>
    </div>
  );
}

function NotFound() {
  return <h1>404 — 页面未找到</h1>;
}

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

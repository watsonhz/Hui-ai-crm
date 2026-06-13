import { createBrowserRouter, Navigate } from 'react-router-dom';
import MainLayout from '../layouts/MainLayout';
import LoginPage from '../pages/login';
import DashboardPage from '../pages/dashboard';
import CustomerList from '../pages/customers';
import ProjectKanban from '../pages/projects';
import BiddingList from '../pages/bidding';

const router = createBrowserRouter([
  { path: '/login', element: <LoginPage /> },
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { index: true, element: <Navigate to="/dashboard" replace /> },
      { path: 'dashboard', element: <DashboardPage /> },
      { path: 'customers', element: <CustomerList /> },
      { path: 'projects', element: <ProjectKanban /> },
      { path: 'bidding', element: <BiddingList /> },
    ],
  },
]);

export default router;

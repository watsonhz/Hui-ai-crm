import { createBrowserRouter, Navigate } from 'react-router-dom';
import MainLayout from '../layouts/MainLayout';
import AuthGuard from '../components/AuthGuard';
import LoginPage from '../pages/login';
import DashboardPage from '../pages/dashboard';
import CustomerList from '../pages/customers';
import ProjectKanban from '../pages/projects';
import BiddingList from '../pages/bidding';
import OrgTreePage from '../pages/organizations';
import KnowledgePage from '../pages/knowledge';
import SystemPage from '../pages/system';
import OpportunityKanban from '../pages/opportunities';
import ActivityList from '../pages/activities';
import TodoPage from '../pages/todos';

const router = createBrowserRouter([
  { path: '/login', element: <LoginPage /> },
  {
    element: <AuthGuard />,
    children: [
      {
        element: <MainLayout />,
        children: [
          { path: '/', element: <Navigate to="/dashboard" replace /> },
          { path: '/dashboard', element: <DashboardPage /> },
          { path: '/customers', element: <CustomerList /> },
          { path: '/projects', element: <ProjectKanban /> },
          { path: '/bidding', element: <BiddingList /> },
          { path: '/opportunities', element: <OpportunityKanban /> },
          { path: '/activities', element: <ActivityList /> },
          { path: '/todos', element: <TodoPage /> },
          { path: '/organizations', element: <OrgTreePage /> },
          { path: '/knowledge', element: <KnowledgePage /> },
          { path: '/system', element: <SystemPage /> },
        ],
      },
    ],
  },
]);

export default router;

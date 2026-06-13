import { useState } from 'react';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { Layout, Menu, Button, theme, Dropdown } from 'antd';
import {
  DashboardOutlined, TeamOutlined, ProjectOutlined, FileSearchOutlined,
  LogoutOutlined, UserOutlined, MenuFoldOutlined, MenuUnfoldOutlined,
  ApartmentOutlined, BookOutlined, SettingOutlined,
} from '@ant-design/icons';
import { useAuthStore } from '../stores/authStore';

const { Header, Sider, Content } = Layout;

export default function MainLayout() {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { user, logout } = useAuthStore();
  const { token: { colorBgContainer, borderRadiusLG } } = theme.useToken();

  const menuItems = [
    { key: '/dashboard', icon: <DashboardOutlined />, label: '工作台' },
    { key: '/customers', icon: <TeamOutlined />, label: '客户管理' },
    { key: '/projects', icon: <ProjectOutlined />, label: '项目管理' },
    { key: '/bidding', icon: <FileSearchOutlined />, label: '招投标管理' },
    { key: '/organizations', icon: <ApartmentOutlined />, label: '组织架构' },
    { key: '/knowledge', icon: <BookOutlined />, label: '知识库' },
    { key: '/system', icon: <SettingOutlined />, label: '系统管理' },
  ];

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider trigger={null} collapsible collapsed={collapsed}>
        <div style={{ height: 48, margin: 12, color: '#fff', fontSize: collapsed ? 14 : 18, fontWeight: 700, textAlign: 'center', lineHeight: '48px' }}>
          {collapsed ? 'CRM' : 'AI-CRM v4'}
        </div>
        <Menu theme="dark" mode="inline" selectedKeys={[location.pathname]} items={menuItems} onClick={({ key }) => navigate(key)} />
      </Sider>
      <Layout>
        <Header style={{ padding: '0 24px', background: colorBgContainer, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Button type="text" icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />} onClick={() => setCollapsed(!collapsed)} />
          <Dropdown menu={{ items: [{ key: 'logout', icon: <LogoutOutlined />, label: '退出登录', onClick: logout }] }}>
            <Button type="text" icon={<UserOutlined />}>{user?.full_name || user?.username || '未登录'}</Button>
          </Dropdown>
        </Header>
        <Content style={{ margin: 16, padding: 24, background: colorBgContainer, borderRadius: borderRadiusLG, overflow: 'auto' }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}

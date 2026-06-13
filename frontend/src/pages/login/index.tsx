import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Form, Input, Button, message, Tabs } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useAuthStore } from '../../stores/authStore';

export default function LoginPage() {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { login, register } = useAuthStore();

  const onLogin = async (values: any) => {
    setLoading(true);
    try {
      await login(values.username, values.password);
      message.success('登录成功');
      navigate('/dashboard');
    } catch { message.error('用户名或密码错误'); }
    finally { setLoading(false); }
  };

  const onRegister = async (values: any) => {
    setLoading(true);
    try {
      await register(values.username, values.password, values.email, values.fullName);
      message.success('注册成功，请登录');
    } catch { message.error('注册失败'); }
    finally { setLoading(false); }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', background: '#f0f2f5' }}>
      <Card style={{ width: 420 }}>
        <h2 style={{ textAlign: 'center', marginBottom: 24 }}>AI-CRM 企业管理系统</h2>
        <Tabs items={[
          {
            key: 'login', label: '登录',
            children: (
              <Form onFinish={onLogin} size="large">
                <Form.Item name="username" rules={[{ required: true, message: '请输入用户名' }]}>
                  <Input prefix={<UserOutlined />} placeholder="用户名" />
                </Form.Item>
                <Form.Item name="password" rules={[{ required: true, message: '请输入密码' }]}>
                  <Input.Password prefix={<LockOutlined />} placeholder="密码" />
                </Form.Item>
                <Form.Item><Button type="primary" htmlType="submit" loading={loading} block>登录</Button></Form.Item>
              </Form>
            ),
          },
          {
            key: 'register', label: '注册',
            children: (
              <Form onFinish={onRegister} size="large">
                <Form.Item name="username" rules={[{ required: true }]}><Input placeholder="用户名" /></Form.Item>
                <Form.Item name="fullName" rules={[{ required: true }]}><Input placeholder="姓名" /></Form.Item>
                <Form.Item name="email"><Input placeholder="邮箱" /></Form.Item>
                <Form.Item name="password" rules={[{ required: true, min: 4 }]}><Input.Password placeholder="密码" /></Form.Item>
                <Form.Item><Button type="primary" htmlType="submit" loading={loading} block>注册</Button></Form.Item>
              </Form>
            ),
          },
        ]} />
      </Card>
    </div>
  );
}

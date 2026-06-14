import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card, Row, Col, Statistic, Table } from 'antd';
import {
  TeamOutlined, ProjectOutlined, FileSearchOutlined,
  PhoneOutlined, ExclamationCircleOutlined, BookOutlined, SettingOutlined,
} from '@ant-design/icons';
import client from '../../api/client';

const CARD_STYLE: React.CSSProperties = { cursor: 'pointer', transition: 'box-shadow 0.2s' };

export default function DashboardPage() {
  const [stats, setStats] = useState<any>({});
  const navigate = useNavigate();

  useEffect(() => {
    client.get('/dashboard/stats').then((res: any) => setStats(res.data));
  }, []);

  const statCards = [
    { title: '客户总数', value: stats.customers?.total ?? '-', icon: <TeamOutlined />, color: '#1677ff', path: '/customers' },
    { title: '项目总数', value: stats.projects?.total ?? '-', icon: <ProjectOutlined />, color: '#52c41a', path: '/projects' },
    { title: '进行中投标', value: stats.bidding?.active ?? '-', icon: <FileSearchOutlined />, color: '#faad14', path: '/bidding' },
    { title: '本月拜访', value: stats.visits?.this_month ?? '-', icon: <PhoneOutlined />, color: '#722ed1', path: '/activities' },
    { title: '待处理工单', value: stats.actions?.pending ?? '-', icon: <ExclamationCircleOutlined />, color: '#ff4d4f', path: '/todos' },
    { title: '本月报告', value: stats.reports?.this_month ?? '-', icon: <BookOutlined />, color: '#13c2c2', path: '/knowledge' },
    { title: '系统角色', value: 6, icon: <SettingOutlined />, color: '#eb2f96', path: '/system' },
  ];

  const pipelineColumns = [
    { title: '阶段', dataIndex: 'stage_name', key: 'stage_name', width: 100 },
    { title: '项目数', dataIndex: 'count', key: 'count', width: 80,
      render: (v: number) => <span style={{ fontWeight: 700, color: v > 0 ? '#1677ff' : '#ccc' }}>{v}</span> },
  ];

  const quickLinks = [
    { title: '新增客户', path: '/customers', color: '#1677ff' },
    { title: '新增项目', path: '/projects', color: '#52c41a' },
    { title: '投标管理', path: '/bidding', color: '#faad14' },
    { title: '商机看板', path: '/opportunities', color: '#722ed1' },
    { title: '跟进记录', path: '/activities', color: '#13c2c2' },
    { title: '我的待办', path: '/todos', color: '#ff4d4f' },
    { title: '知识库', path: '/knowledge', color: '#eb2f96' },
    { title: '系统管理', path: '/system', color: '#666' },
  ];

  return (
    <div>
      <h2>工作台</h2>
      <Row gutter={16} style={{ marginBottom: 16 }}>
        {statCards.map((s, i) => (
          <Col span={6} key={i}>
            <Card hoverable style={CARD_STYLE} onClick={() => navigate(s.path)}>
              <Statistic title={s.title} value={s.value} prefix={s.icon} valueStyle={{ color: s.color }} />
            </Card>
          </Col>
        ))}
      </Row>
      <Row gutter={16}>
        <Col span={12}>
          <Card title="项目漏斗" extra={<a onClick={() => navigate('/projects')}>查看全部 →</a>}>
            <Table rowKey="stage" columns={pipelineColumns} dataSource={stats.pipeline || []} pagination={false} size="small"
              onRow={(_r) => ({ onClick: () => navigate('/projects'), style: { cursor: 'pointer' } })} />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="快捷入口">
            <Row gutter={[12, 12]}>
              {quickLinks.map((q, i) => (
                <Col span={6} key={i}>
                  <Card size="small" hoverable style={{ textAlign: 'center', cursor: 'pointer' }}
                    onClick={() => navigate(q.path)}>
                    <div style={{ color: q.color, fontWeight: 600, fontSize: 13 }}>{q.title}</div>
                  </Card>
                </Col>
              ))}
            </Row>
          </Card>
        </Col>
      </Row>
    </div>
  );
}

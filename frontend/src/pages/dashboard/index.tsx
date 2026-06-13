import { useEffect, useState } from 'react';
import { Card, Row, Col, Statistic, Table } from 'antd';
import { TeamOutlined, ProjectOutlined, FileSearchOutlined, CheckCircleOutlined } from '@ant-design/icons';
import client from '../../api/client';

export default function DashboardPage() {
  const [stats, setStats] = useState<any>({});

  useEffect(() => {
    client.get('/dashboard/stats').then((res: any) => setStats(res.data));
  }, []);

  const statCards = [
    { title: '客户总数', value: stats.customers?.total || 0, icon: <TeamOutlined />, color: '#1677ff' },
    { title: '项目总数', value: stats.projects?.total || 0, icon: <ProjectOutlined />, color: '#52c41a' },
    { title: '进行中投标', value: stats.bidding?.active || 0, icon: <FileSearchOutlined />, color: '#faad14' },
    { title: '本月拜访', value: stats.visits?.this_month || 0, icon: <CheckCircleOutlined />, color: '#722ed1' },
  ];

  const pipelineColumns = [
    { title: '阶段', dataIndex: 'stage_name', key: 'stage_name' },
    { title: '项目数', dataIndex: 'count', key: 'count' },
  ];

  return (
    <div>
      <h2>工作台</h2>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        {statCards.map((s, i) => (
          <Col span={6} key={i}>
            <Card><Statistic title={s.title} value={s.value} prefix={s.icon} valueStyle={{ color: s.color }} /></Card>
          </Col>
        ))}
      </Row>
      <Card title="项目漏斗">
        <Table rowKey="stage" columns={pipelineColumns} dataSource={stats.pipeline || []} pagination={false} size="small" />
      </Card>
    </div>
  );
}

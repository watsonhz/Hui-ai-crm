import { useEffect, useState } from 'react';
import { Card, Tag, Button, Modal, Form, Input, Select, InputNumber, message, Row, Col } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import client from '../../api/client';

const STAGES: Record<number, { name: string; color: string }> = {
  1: { name: '线索', color: '#d9d9d9' }, 2: { name: '商机', color: '#87d068' },
  3: { name: '需求', color: '#2db7f5' }, 4: { name: '方案', color: '#108ee9' },
  5: { name: '报价', color: '#722ed1' }, 6: { name: '谈判', color: '#fa8c16' },
  7: { name: '合同', color: '#52c41a' }, 8: { name: '交付', color: '#13c2c2' },
  9: { name: '验收', color: '#eb2f96' }, 10: { name: '回款', color: '#f5222d' },
  11: { name: '运维', color: '#faad14' }, 12: { name: '结项', color: '#d9d9d9' },
};

export default function OpportunityKanban() {
  const [projects, setProjects] = useState<any[]>([]);
  const [open, setOpen] = useState(false);
  const [form] = Form.useForm();

  const fetch = async () => {
    try {
      const res: any = await client.get('/projects/board/kanban');
      setProjects(res.data || []);
    } catch {}
  };

  useEffect(() => { fetch(); }, []);

  const onCreate = async (values: any) => {
    await client.post('/projects/', values);
    message.success('创建成功');
    setOpen(false); form.resetFields(); fetch();
  };

  return (
    <div>
      <Button type="primary" icon={<PlusOutlined />} onClick={() => setOpen(true)} style={{ marginBottom: 16 }}>新增商机</Button>
      <Row gutter={12} style={{ overflowX: 'auto', flexWrap: 'nowrap' }}>
        {Object.entries(STAGES).slice(0, 8).map(([s, info]) => {
          const items = projects.find((p: any) => p.stage === Number(s))?.items || [];
          return (
            <Col key={s} style={{ minWidth: 200, maxWidth: 260 }}>
              <Card title={<span style={{ fontSize: 14 }}>{info.name} <Tag>{items.length}</Tag></span>} size="small"
                style={{ background: '#f5f5f5', height: '100%' }}>
                {items.map((p: any) => (
                  <Card key={p.id} size="small" style={{ marginBottom: 8 }}>
                    <strong>{p.name}</strong>
                    <div style={{ fontSize: 12, color: '#888' }}>¥{p.budget ? Number(p.budget).toLocaleString() : '-'}</div>
                  </Card>
                ))}
              </Card>
            </Col>
          );
        })}
      </Row>
      <Modal open={open} onCancel={() => setOpen(false)} title="新增商机" onOk={() => form.submit()}>
        <Form form={form} layout="vertical" onFinish={onCreate}>
          <Form.Item name="name" label="名称" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="stage" label="阶段" initialValue={1}>
            <Select options={Object.entries(STAGES).map(([k, v]) => ({ label: v.name, value: Number(k) }))} />
          </Form.Item>
          <Form.Item name="budget" label="金额"><InputNumber style={{ width: '100%' }} min={0} /></Form.Item>
        </Form>
      </Modal>
    </div>
  );
}

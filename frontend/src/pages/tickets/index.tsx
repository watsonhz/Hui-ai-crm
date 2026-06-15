import { useEffect, useState } from 'react';
import { Table, Tag, Button, Modal, Form, Input, Select, InputNumber, message, Space } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import client from '../../api/client';

const STATUS_MAP: Record<number, { color: string; label: string }> = {
  1: { color: 'red', label: '待处理' },
  2: { color: 'orange', label: '处理中' },
  3: { color: 'green', label: '已解决' },
  4: { color: 'default', label: '已关闭' },
};

export default function TicketPage() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [form] = Form.useForm();

  const fetch = async () => {
    setLoading(true);
    try { const res: any = await client.get('/ai/service/tickets/'); setData(res.data?.items || []); }
    finally { setLoading(false); }
  };

  useEffect(() => { fetch(); }, []);

  const onSubmit = async (values: any) => {
    if (form.getFieldValue('id')) {
      await client.put(`/ai/service/tickets/${form.getFieldValue('id')}`, values);
      message.success('更新成功');
    } else {
      await client.post('/ai/service/tickets/', values);
      message.success('创建成功');
    }
    setOpen(false); form.resetFields(); fetch();
  };

  return (
    <div>
      <h2>工单管理</h2>
      <Space style={{ marginBottom: 16 }}>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => { form.resetFields(); setOpen(true); }}>新增工单</Button>
      </Space>
      <Table rowKey="id" loading={loading} dataSource={data} columns={[
        { title: '标题', dataIndex: 'title' },
        { title: '状态', dataIndex: 'status', render: (v: number) => <Tag color={STATUS_MAP[v]?.color}>{STATUS_MAP[v]?.label}</Tag> },
        { title: '优先级', dataIndex: 'priority', render: (v: number) => ['紧急','高','中','低'][v] || v },
        { title: 'SLA响应(h)', dataIndex: 'sla_response_hours' },
        { title: '超期', dataIndex: 'is_overdue', render: (v: boolean) => v ? <Tag color="red">超期</Tag> : <Tag color="green">正常</Tag> },
        { title: '操作', render: (_: any, r: any) => (
          <Button size="small" onClick={() => { form.setFieldsValue(r); setOpen(true); }}>处理</Button>
        )},
      ]} pagination={false} />
      <Modal open={open} onCancel={() => { setOpen(false); form.resetFields(); }}
        title={form.getFieldValue('id') ? '处理工单' : '新增工单'} onOk={() => form.submit()}>
        <Form form={form} layout="vertical" onFinish={onSubmit}>
          <Form.Item name="title" label="标题" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="customer_id" label="客户ID" rules={[{ required: true }]}><InputNumber style={{ width: '100%' }} /></Form.Item>
          <Space>
            <Form.Item name="priority" label="优先级" initialValue={2}>
              <Select options={[{ label: '紧急', value: 0 }, { label: '高', value: 1 }, { label: '中', value: 2 }, { label: '低', value: 3 }]} style={{ width: 100 }} />
            </Form.Item>
            <Form.Item name="customer_level" label="客户等级" initialValue="normal">
              <Select options={[{ label: 'VIP', value: 'vip' }, { label: '重点', value: 'key' }, { label: '普通', value: 'normal' }]} style={{ width: 100 }} />
            </Form.Item>
          </Space>
          <Form.Item name="description" label="描述"><Input.TextArea rows={4} /></Form.Item>
          {form.getFieldValue('id') && (
            <Space>
              <Form.Item name="status" label="状态"><Select options={Object.entries(STATUS_MAP).map(([k, v]) => ({ label: v.label, value: Number(k) }))} style={{ width: 120 }} /></Form.Item>
              <Form.Item name="resolution" label="解决说明"><Input /></Form.Item>
            </Space>
          )}
        </Form>
      </Modal>
    </div>
  );
}

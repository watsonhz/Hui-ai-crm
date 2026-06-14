import { useEffect, useState } from 'react';
import { Table, Tag, Button, Modal, Form, Input, Select, DatePicker, message, Space } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import client from '../../api/client';
import dayjs from 'dayjs';

const VISIT_TYPES: Record<number, string> = { 1: '电话', 2: '拜访', 3: '会议', 4: '邮件', 5: '微信' };

export default function ActivityList() {
  const [data, setData] = useState<any[]>([]);
  const [open, setOpen] = useState(false);
  const [form] = Form.useForm();

  const fetch = async () => {
    try {
      const res: any = await client.get('/projects/?page=1&page_size=100');
      setData(res.data?.items || []);
    } catch {}
  };

  useEffect(() => { fetch(); }, []);

  const onCreate = async (values: any) => {
    await client.post('/relationships/', {
      customer_id: values.customer_id,
      contact_name: values.contact_name,
      contact_role: values.contact_role || '联系人',
      last_contact_date: values.visit_date?.toISOString(),
      notes: values.content,
      warmth: values.warmth || 0,
    });
    message.success('记录成功');
    setOpen(false); form.resetFields(); fetch();
  };

  return (
    <div>
      <Space style={{ marginBottom: 16 }}>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setOpen(true)}>新增拜访</Button>
      </Space>
      <Table rowKey="id" dataSource={data} columns={[
        { title: '名称', dataIndex: 'name' },
        { title: '阶段', dataIndex: 'stage', render: (v: number) => <Tag>{v}</Tag> },
        { title: '更新时间', dataIndex: 'updated_at', render: (v: string) => dayjs(v).format('YYYY-MM-DD HH:mm') },
      ]} pagination={false} />
      <Modal open={open} onCancel={() => setOpen(false)} title="新增拜访记录" onOk={() => form.submit()}>
        <Form form={form} layout="vertical" onFinish={onCreate}>
          <Form.Item name="customer_id" label="客户ID" rules={[{ required: true }]}><Input type="number" /></Form.Item>
          <Form.Item name="contact_name" label="联系人" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="visit_date" label="拜访时间"><DatePicker showTime style={{ width: '100%' }} /></Form.Item>
          <Form.Item name="visit_type" label="方式" initialValue={2}>
            <Select options={Object.entries(VISIT_TYPES).map(([k, v]) => ({ label: v, value: Number(k) }))} />
          </Form.Item>
          <Form.Item name="content" label="内容"><Input.TextArea rows={4} /></Form.Item>
        </Form>
      </Modal>
    </div>
  );
}

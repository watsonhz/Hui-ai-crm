import { useEffect, useState } from 'react';
import { Table, Button, Modal, Form, Input, Select, message, Space } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import client from '../../api/client';

export default function KnowledgePage() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [detail, setDetail] = useState<any>(null);
  const [form] = Form.useForm();

  const fetch = async () => {
    setLoading(true);
    try { const res: any = await client.get('/knowledge/'); setData(res.data?.items || []); }
    finally { setLoading(false); }
  };

  useEffect(() => { fetch(); }, []);

  const onCreate = async (values: any) => {
    await client.post('/knowledge/', values);
    message.success('创建成功');
    setOpen(false); form.resetFields(); fetch();
  };

  const categories = ['产品', '技术', '销售', '市场', '服务', '管理'];

  return (
    <div>
      <Space style={{ marginBottom: 16 }}>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setOpen(true)}>新增知识</Button>
      </Space>
      <Table rowKey="id" loading={loading} dataSource={data} onRow={(r) => ({ onClick: () => setDetail(r), style: { cursor: 'pointer' } })}
        columns={[
          { title: '标题', dataIndex: 'title' },
          { title: '分类', dataIndex: 'category' },
          { title: '标签', dataIndex: 'tags' },
          { title: '创建时间', dataIndex: 'created_at', render: (v: string) => new Date(v).toLocaleDateString() },
        ]} pagination={false} />
      <Modal open={open} onCancel={() => setOpen(false)} title="新增知识" onOk={() => form.submit()}>
        <Form form={form} layout="vertical" onFinish={onCreate}>
          <Form.Item name="title" label="标题" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="category" label="分类" rules={[{ required: true }]}>
            <Select options={categories.map(c => ({ label: c, value: c }))} />
          </Form.Item>
          <Form.Item name="tags" label="标签"><Input placeholder="用逗号分隔" /></Form.Item>
          <Form.Item name="content" label="内容" rules={[{ required: true }]}><Input.TextArea rows={6} /></Form.Item>
        </Form>
      </Modal>
      <Modal open={!!detail} onCancel={() => setDetail(null)} footer={null} title={detail?.title} width={700}>
        <div style={{ whiteSpace: 'pre-wrap' }}>{detail?.content}</div>
      </Modal>
    </div>
  );
}

import { useEffect, useState } from 'react';
import { Table, Button, Modal, Form, Input, Select, message, Space, Tag } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import client from '../../api/client';

export default function CustomerList() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [form] = Form.useForm();

  const fetch = async () => {
    setLoading(true);
    try {
      const res: any = await client.get('/organizations/tree');
      setData(res.data || []);
    } finally { setLoading(false); }
  };

  useEffect(() => { fetch(); }, []);

  const onCreate = async (values: any) => {
    await client.post('/organizations/', values);
    message.success('创建成功');
    setOpen(false);
    form.resetFields();
    fetch();
  };

  return (
    <div>
      <Space style={{ marginBottom: 16 }}>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setOpen(true)}>新增客户</Button>
      </Space>
      <Table rowKey="id" loading={loading} dataSource={data} columns={[
        { title: '名称', dataIndex: 'name' },
        { title: '类型', dataIndex: 'org_type', render: (v: string) => <Tag>{v === 'company' ? '公司' : v === 'dept' ? '部门' : '团队'}</Tag> },
        { title: '排序', dataIndex: 'sort_order' },
      ]} pagination={false} />
      <Modal open={open} onCancel={() => setOpen(false)} title="新增客户" onOk={() => form.submit()}>
        <Form form={form} layout="vertical" onFinish={onCreate}>
          <Form.Item name="name" label="名称" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="org_type" label="类型" initialValue="company">
            <Select options={[{ label: '公司', value: 'company' }, { label: '部门', value: 'dept' }, { label: '团队', value: 'team' }]} />
          </Form.Item>
          <Form.Item name="parent_id" label="上级ID"><Input type="number" /></Form.Item>
        </Form>
      </Modal>
    </div>
  );
}

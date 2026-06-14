import { useEffect, useState } from 'react';
import { Button, Modal, Form, Input, Select, InputNumber, message, Space, Tag, Tree } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import client from '../../api/client';

export default function OrgTreePage() {
  const [data, setData] = useState<any[]>([]);
  const [open, setOpen] = useState(false);
  const [form] = Form.useForm();

  const fetch = async () => {
    const res: any = await client.get('/organizations/tree');
    setData(res.data || []);
  };

  useEffect(() => { fetch(); }, []);

  const treeData = data.map((node: any) => ({
    title: <span>{node.name} <Tag>{node.org_type === 'company' ? '公司' : node.org_type === 'dept' ? '部门' : '团队'}</Tag></span>,
    key: node.id,
    children: node.children?.length ? node.children.map((c: any) => ({ title: c.name, key: c.id, children: c.children?.map((cc: any) => ({ title: cc.name, key: cc.id })) })) : [],
  }));

  const onCreate = async (values: any) => {
    await client.post('/organizations/', values);
    message.success('创建成功');
    setOpen(false); form.resetFields(); fetch();
  };

  return (
    <div>
      <Space style={{ marginBottom: 16 }}>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setOpen(true)}>新增组织</Button>
      </Space>
      <Tree treeData={treeData} defaultExpandAll showLine />
      <Modal open={open} onCancel={() => setOpen(false)} title="新增组织" onOk={() => form.submit()}>
        <Form form={form} layout="vertical" onFinish={onCreate}>
          <Form.Item name="name" label="名称" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="org_type" label="类型" initialValue="dept">
            <Select options={[{ label: '公司', value: 'company' }, { label: '部门', value: 'dept' }, { label: '团队', value: 'team' }]} />
          </Form.Item>
          <Form.Item name="parent_id" label="上级ID"><Input type="number" /></Form.Item>
          <Form.Item name="sort_order" label="排序"><InputNumber min={0} /></Form.Item>
        </Form>
      </Modal>
    </div>
  );
}

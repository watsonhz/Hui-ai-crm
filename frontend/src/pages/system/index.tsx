import { useEffect, useState } from 'react';
import { Table, Button, Modal, Form, Input, InputNumber, message, Space, Tabs } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import client from '../../api/client';

export default function SystemPage() {
  const [types, setTypes] = useState<any[]>([]);
  const [data, setData] = useState<any[]>([]);
  const [curType, setCurType] = useState('');
  const [open, setOpen] = useState(false);
  const [form] = Form.useForm();
  const [typeForm] = Form.useForm();
  const [typeOpen, setTypeOpen] = useState(false);

  const fetchTypes = async () => {
    try { const res: any = await client.get('/system/dict/type'); setTypes(res.data || []); } catch {}
  };
  const fetchData = async (dictType: string) => {
    try { const res: any = await client.get(`/system/dict/data/${dictType}`); setData(res.data || []); } catch {}
  };

  useEffect(() => { fetchTypes(); }, []);
  useEffect(() => { if (curType) fetchData(curType); }, [curType]);

  const onCreateType = async (values: any) => {
    await client.post('/system/dict/type', values);
    message.success('创建成功');
    setTypeOpen(false); typeForm.resetFields(); fetchTypes();
  };

  const onCreateData = async (values: any) => {
    await client.post('/system/dict/data', { ...values, dict_type: curType });
    message.success('创建成功');
    setOpen(false); form.resetFields(); fetchData(curType);
  };

  const dataColumns = [
    { title: '标签', dataIndex: 'dict_label' },
    { title: '值', dataIndex: 'dict_value' },
    { title: '排序', dataIndex: 'sort_order' },
    { title: '样式', dataIndex: 'css_class' },
  ];

  return (
    <div>
      <Tabs activeKey={curType} onChange={setCurType} tabBarExtraContent={
        <Button size="small" icon={<PlusOutlined />} onClick={() => setTypeOpen(true)}>新增字典</Button>
      } items={types.map((t: any) => ({
        key: t.dict_type, label: t.dict_name,
        children: (
          <div>
            <Space style={{ marginBottom: 16 }}>
              <Button type="primary" icon={<PlusOutlined />} onClick={() => setOpen(true)}>新增数据</Button>
            </Space>
            <Table rowKey="id" dataSource={data} columns={dataColumns} pagination={false} size="small" />
          </div>
        ),
      }))} />
      <Modal open={typeOpen} onCancel={() => setTypeOpen(false)} title="新增字典类型" onOk={() => typeForm.submit()}>
        <Form form={typeForm} layout="vertical" onFinish={onCreateType}>
          <Form.Item name="dict_name" label="名称" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="dict_type" label="编码" rules={[{ required: true }]}><Input /></Form.Item>
        </Form>
      </Modal>
      <Modal open={open} onCancel={() => setOpen(false)} title="新增字典数据" onOk={() => form.submit()}>
        <Form form={form} layout="vertical" onFinish={onCreateData}>
          <Form.Item name="dict_label" label="标签" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="dict_value" label="值" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="sort_order" label="排序"><InputNumber min={0} /></Form.Item>
        </Form>
      </Modal>
    </div>
  );
}

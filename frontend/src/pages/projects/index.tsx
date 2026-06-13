import { useEffect, useState } from 'react';
import { Table, Tag, Button, Modal, Form, Input, Select, message, Space } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import client from '../../api/client';

const STAGES: Record<number,string> = {1:'线索',2:'商机',3:'需求',4:'方案',5:'报价',6:'谈判',7:'合同',8:'交付',9:'验收',10:'回款',11:'运维',12:'结项'};

export default function ProjectKanban() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [form] = Form.useForm();

  const fetch = async () => {
    setLoading(true);
    try {
      const res: any = await client.get('/projects/?page=1&page_size=100');
      setData(res.data?.items || []);
    } finally { setLoading(false); }
  };

  useEffect(() => { fetch(); }, []);

  const onCreate = async (values: any) => {
    await client.post('/projects/', values);
    message.success('创建成功');
    setOpen(false);
    form.resetFields();
    fetch();
  };

  return (
    <div>
      <Space style={{ marginBottom: 16 }}>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setOpen(true)}>新增项目</Button>
      </Space>
      <Table rowKey="id" loading={loading} dataSource={data} columns={[
        { title: '名称', dataIndex: 'name' },
        { title: '阶段', dataIndex: 'stage', render: (v: number) => <Tag color={v>=7?'green':v>=4?'blue':'orange'}>{STAGES[v]||v}</Tag> },
        { title: '预算', dataIndex: 'budget', render: (v: any) => v ? `¥${Number(v).toLocaleString()}` : '-' },
        { title: '开始', dataIndex: 'start_date' },
        { title: '结束', dataIndex: 'end_date' },
      ]} pagination={false} />
      <Modal open={open} onCancel={() => setOpen(false)} title="新增项目" onOk={() => form.submit()}>
        <Form form={form} layout="vertical" onFinish={onCreate}>
          <Form.Item name="name" label="名称" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="stage" label="阶段" initialValue={1}>
            <Select options={Object.entries(STAGES).map(([k,v])=>({label:v,value:Number(k)}))} />
          </Form.Item>
          <Form.Item name="budget" label="预算"><Input type="number" /></Form.Item>
        </Form>
      </Modal>
    </div>
  );
}

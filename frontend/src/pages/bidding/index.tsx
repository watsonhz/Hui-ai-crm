import { useEffect, useState } from 'react';
import { Table, Tag, Button, Modal, Form, Input, Select, InputNumber, DatePicker, message, Space } from 'antd';
import { PlusOutlined } from '@ant-design/icons';
import client from '../../api/client';
import dayjs from 'dayjs';

const BID_STATUS: Record<number,string> = {1:'意向',2:'招标中',3:'投标中',4:'评标中',5:'中标',6:'失标',7:'废标',8:'暂停',9:'完成'};

export default function BiddingList() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [form] = Form.useForm();

  const fetch = async () => {
    setLoading(true);
    try {
      const res: any = await client.get('/bidding/?page=1&page_size=100');
      setData(res.data?.items || []);
    } finally { setLoading(false); }
  };

  useEffect(() => { fetch(); }, []);

  const onCreate = async (values: any) => {
    const payload = { ...values };
    if (values.bid_deadline) payload.bid_deadline = values.bid_deadline.toISOString();
    if (values.submit_deadline) payload.submit_deadline = values.submit_deadline.toISOString();
    await client.post('/bidding/', payload);
    message.success('创建成功');
    setOpen(false);
    form.resetFields();
    fetch();
  };

  return (
    <div>
      <Space style={{ marginBottom: 16 }}>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => setOpen(true)}>新增投标</Button>
      </Space>
      <Table rowKey="id" loading={loading} dataSource={data} columns={[
        { title: '标题', dataIndex: 'title' },
        { title: '客户', dataIndex: 'client_company' },
        { title: '金额', dataIndex: 'bid_amount', render: (v: any) => v ? `¥${Number(v).toLocaleString()}` : '-' },
        { title: '状态', dataIndex: 'bid_status', render: (v: number) => { const colors: Record<number,string>={1:'blue',2:'cyan',3:'geekblue',4:'purple',5:'green',6:'red',7:'magenta',8:'orange',9:'default'}; return <Tag color={colors[v]}>{BID_STATUS[v]||v}</Tag>; }},
        { title: '截止日期', dataIndex: 'bid_deadline', render: (v: string) => v ? dayjs(v).format('YYYY-MM-DD') : '-' },
      ]} pagination={false} />
      <Modal open={open} onCancel={() => setOpen(false)} title="新增投标" onOk={() => form.submit()}>
        <Form form={form} layout="vertical" onFinish={onCreate}>
          <Form.Item name="title" label="标题" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="client_company" label="客户公司"><Input /></Form.Item>
          <Form.Item name="bid_amount" label="金额"><InputNumber style={{ width: '100%' }} min={0} /></Form.Item>
          <Form.Item name="bid_status" label="状态" initialValue={1}>
            <Select options={Object.entries(BID_STATUS).map(([k,v])=>({label:v,value:Number(k)}))} />
          </Form.Item>
          <Form.Item name="bid_deadline" label="截止日期"><DatePicker style={{ width: '100%' }} /></Form.Item>
        </Form>
      </Modal>
    </div>
  );
}

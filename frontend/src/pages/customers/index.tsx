import { useEffect, useState } from 'react';
import { Table, Tag, Button, Modal, Form, Input, Select, message, Space, Popconfirm } from 'antd';
import { PlusOutlined, ReloadOutlined, SearchOutlined } from '@ant-design/icons';
import client from '../../api/client';

const LEVELS: Record<string, { color: string; label: string }> = {
  vip: { color: 'red', label: 'VIP' },
  key: { color: 'orange', label: '重点' },
  normal: { color: 'blue', label: '普通' },
};

const SOURCES = ['官网', '展会', '转介绍', '电话营销', '其他'];
const INDUSTRIES = ['政府', '金融', '医疗', '教育', '制造', '互联网', '其他'];

export default function CustomerList() {
  const [data, setData] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [detail, setDetail] = useState<any>(null);
  const [form] = Form.useForm();
  const [search, setSearch] = useState('');
  const [filterLevel, setFilterLevel] = useState<string | undefined>();
  const [pagination, setPagination] = useState({ page: 1, pageSize: 20, total: 0 });

  const fetch = async (page = 1, pageSize = 20) => {
    setLoading(true);
    try {
      const params: any = { page, page_size: pageSize };
      if (search) params.search = search;
      if (filterLevel) params.level = filterLevel;
      const res: any = await client.get('/customers/', { params });
      setData(res.data?.items || []);
      setPagination({ page, pageSize, total: res.data?.total || 0 });
    } finally { setLoading(false); }
  };

  useEffect(() => { fetch(); }, [search, filterLevel]);

  const onSave = async (values: any) => {
    if (form.getFieldValue('id')) {
      await client.put(`/customers/${form.getFieldValue('id')}`, values);
      message.success('更新成功');
    } else {
      await client.post('/customers/', values);
      message.success('创建成功');
    }
    setOpen(false); form.resetFields(); fetch();
  };

  const onDelete = async (id: number) => {
    await client.delete(`/customers/${id}`);
    message.success('已禁用'); fetch();
  };

  const columns = [
    { title: '编码', dataIndex: 'code', width: 100 },
    { title: '名称', dataIndex: 'name', ellipsis: true },
    { title: '行业', dataIndex: 'industry' },
    { title: '来源', dataIndex: 'source' },
    { title: '等级', dataIndex: 'level', render: (v: string) => {
      const lv = LEVELS[v] || { color: 'default', label: v };
      return <Tag color={lv.color}>{lv.label}</Tag>;
    }},
    { title: '联系人', dataIndex: 'contact_name' },
    { title: '电话', dataIndex: 'contact_phone' },
    { title: '操作', width: 200, render: (_: any, r: any) => (
      <Space>
        <Button size="small" onClick={() => setDetail(r)}>详情</Button>
        <Button size="small" onClick={() => { form.setFieldsValue(r); setOpen(true); }}>编辑</Button>
        <Popconfirm title="确定禁用?" onConfirm={() => onDelete(r.id)}>
          <Button size="small" danger>禁用</Button>
        </Popconfirm>
      </Space>
    )},
  ];

  return (
    <div>
      <Space style={{ marginBottom: 16, flexWrap: 'wrap' }}>
        <Button type="primary" icon={<PlusOutlined />} onClick={() => { form.resetFields(); setOpen(true); }}>新增客户</Button>
        <Input prefix={<SearchOutlined />} placeholder="搜索名称/编码" value={search}
          onChange={e => setSearch(e.target.value)} style={{ width: 200 }} allowClear />
        <Select placeholder="等级" value={filterLevel} onChange={setFilterLevel} allowClear style={{ width: 120 }}
          options={Object.entries(LEVELS).map(([k, v]) => ({ label: v.label, value: k }))} />
        <Button icon={<ReloadOutlined />} onClick={() => { setSearch(''); setFilterLevel(undefined); }}>重置</Button>
      </Space>

      <Table rowKey="id" loading={loading} dataSource={data} columns={columns} size="middle"
        pagination={{ ...pagination, showSizeChanger: true, showTotal: (t: number) => `共 ${t} 条` }}
        onChange={(p) => fetch(p.current || 1, p.pageSize || 20)}
        onRow={(r) => ({ onDoubleClick: () => setDetail(r), style: { cursor: 'pointer' } })} />

      <Modal open={open} onCancel={() => { setOpen(false); form.resetFields(); }}
        title={form.getFieldValue('id') ? '编辑客户' : '新增客户'} width={640} onOk={() => form.submit()}>
        <Form form={form} layout="vertical" onFinish={onSave}>
          <Form.Item name="name" label="名称" rules={[{ required: true }]}><Input /></Form.Item>
          <Form.Item name="code" label="编码"><Input /></Form.Item>
          <Space style={{ display: 'flex' }} wrap>
            <Form.Item name="industry" label="行业"><Select options={INDUSTRIES.map(v => ({ label: v, value: v }))} style={{ width: 180 }} /></Form.Item>
            <Form.Item name="source" label="来源"><Select options={SOURCES.map(v => ({ label: v, value: v }))} style={{ width: 180 }} /></Form.Item>
            <Form.Item name="level" label="等级" initialValue="normal">
              <Select options={Object.entries(LEVELS).map(([k, v]) => ({ label: v.label, value: k }))} style={{ width: 120 }} />
            </Form.Item>
          </Space>
          <Space style={{ display: 'flex' }} wrap>
            <Form.Item name="contact_name" label="联系人"><Input style={{ width: 180 }} /></Form.Item>
            <Form.Item name="contact_phone" label="电话"><Input style={{ width: 180 }} /></Form.Item>
            <Form.Item name="contact_email" label="邮箱"><Input style={{ width: 200 }} /></Form.Item>
          </Space>
          <Form.Item name="address" label="地址"><Input /></Form.Item>
          <Form.Item name="remark" label="备注"><Input.TextArea rows={3} /></Form.Item>
        </Form>
      </Modal>

      <Modal open={!!detail} onCancel={() => setDetail(null)} footer={null} title={detail?.name} width={640}>
        {detail && (
          <div>
            <p><strong>编码：</strong>{detail.code || '-'}</p>
            <p><strong>行业：</strong>{detail.industry || '-'}　<strong>来源：</strong>{detail.source || '-'}　<strong>等级：</strong><Tag color={LEVELS[detail.level]?.color}>{LEVELS[detail.level]?.label}</Tag></p>
            <p><strong>联系人：</strong>{detail.contact_name || '-'}　<strong>电话：</strong>{detail.contact_phone || '-'}　<strong>邮箱：</strong>{detail.contact_email || '-'}</p>
            <p><strong>地址：</strong>{detail.address || '-'}</p>
            <p><strong>备注：</strong>{detail.remark || '-'}</p>
            <p style={{ color: '#888', fontSize: 12 }}>创建：{new Date(detail.created_at).toLocaleString()}　更新：{new Date(detail.updated_at).toLocaleString()}</p>
          </div>
        )}
      </Modal>
    </div>
  );
}

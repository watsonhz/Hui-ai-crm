import { useState } from 'react';
import { Card, Form, Input, InputNumber, Button, Tag, Descriptions, message, Row, Col, Space, Select } from 'antd';
import { AlertOutlined, ThunderboltOutlined } from '@ant-design/icons';
import client from '../../api/client';

const DIMENSION_COLORS: Record<string, string> = { '时间': 'blue', '决策链': 'purple', '项目': 'orange' };

export default function AiDiagnosisPage() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);
  const [form] = Form.useForm();

  const run = async (values: any) => {
    setLoading(true);
    try {
      const payload = {
        customer_id: values.customer_id,
        project_id: values.project_id || null,
        contacts: values.contacts ? JSON.parse(values.contacts) : [],
        competitor_entries: values.competitor_entries ? JSON.parse(values.competitor_entries) : [],
        identified_roles: values.identified_roles ? values.identified_roles.split(',').map((s: string) => s.trim()) : [],
        required_roles: values.required_roles ? JSON.parse(values.required_roles) : {},
        support_level: values.support_level || 0,
        expected_support: values.expected_support ? JSON.parse(values.expected_support) : {},
      };
      const res: any = await client.post('/ai/diagnosis', payload);
      setResults(res.data || []);
      message.success(`检测完成：${(res.data || []).filter((r: any) => r.triggered).length} 个信号触发`);
    } catch { message.error('诊断失败'); }
    finally { setLoading(false); }
  };

  const triggered = results.filter(r => r.triggered);

  return (
    <div>
      <h2>AI 客户诊断 <Tag>12信号检测引擎</Tag></h2>
      <Row gutter={16}>
        <Col span={8}>
          <Card title="诊断参数" size="small">
            <Form form={form} layout="vertical" onFinish={run} initialValues={{ support_level: 0 }}>
              <Form.Item name="customer_id" label="客户ID" rules={[{ required: true }]}>
                <InputNumber style={{ width: '100%' }} min={1} />
              </Form.Item>
              <Form.Item name="project_id" label="项目ID"><InputNumber style={{ width: '100%' }} min={1} /></Form.Item>
              <Space>
                <Form.Item name="support_level" label="支持度"><InputNumber min={0} max={5} /></Form.Item>
                <Form.Item name="contacts" label="联系人JSON"><Input placeholder='[{"name":"张总","weight":8}]' /></Form.Item>
              </Space>
              <Form.Item name="identified_roles" label="已识别角色"><Input placeholder="经济决策者,技术决策者" /></Form.Item>
              <Form.Item name="competitor_entries" label="竞品动态JSON"><Input placeholder='[{"type":"价格战","detail":"..."}]' /></Form.Item>
              <Form.Item><Button type="primary" htmlType="submit" icon={<ThunderboltOutlined />} loading={loading} block>运行诊断</Button></Form.Item>
            </Form>
          </Card>
        </Col>
        <Col span={16}>
          {results.length === 0 ? (
            <Card>输入客户ID，点击"运行诊断"查看12信号检测结果</Card>
          ) : (
            <>
              <Card title={`检测结果：${triggered.length}/${results.length} 触发`} size="small" style={{ marginBottom: 8 }}>
                {triggered.map((r, i) => (
                  <Card key={i} size="small" type="inner" style={{ marginBottom: 4 }}>
                    <Descriptions column={1} size="small">
                      <Descriptions.Item label="信号"><Tag color="red">{r.signal_id}</Tag> {r.name} <Tag color={DIMENSION_COLORS[r.dimension]}>{r.dimension}</Tag> 严重度: {r.severity}</Descriptions.Item>
                      {r.diagnosis && <Descriptions.Item label="诊断">{r.diagnosis}</Descriptions.Item>}
                      {r.advice && <Descriptions.Item label="建议">{r.advice}</Descriptions.Item>}
                      {r.script && <Descriptions.Item label="话术">{r.script}</Descriptions.Item>}
                      {r.action && r.action.action && <Descriptions.Item label="行动"><Tag>{r.action.action}</Tag> 负责人: {r.action.owner} | 截止: {r.action.deadline}</Descriptions.Item>}
                    </Descriptions>
                  </Card>
                ))}
              </Card>
              {results.filter(r => !r.triggered).length > 0 && (
                <Card title={`未触发 (${results.filter(r => !r.triggered).length})`} size="small">
                  {results.filter(r => !r.triggered).map((r, i) => (
                    <Tag key={i} style={{ marginBottom: 4 }}>{r.signal_id} {r.name}</Tag>
                  ))}
                </Card>
              )}
            </>
          )}
        </Col>
      </Row>
    </div>
  );
}

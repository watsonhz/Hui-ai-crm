import { useEffect, useState } from 'react';
import { Table, Tag } from 'antd';
import client from '../../api/client';

const PRIORITY_COLORS: Record<number, string> = { 0: 'red', 1: 'orange', 2: 'blue' };
const PRIORITY_LABELS: Record<number, string> = { 0: 'P0', 1: 'P1', 2: 'P2' };

export default function TodoPage() {
  const [data, setData] = useState<any[]>([]);

  const fetch = async () => {
    try {
      const res: any = await client.get('/projects/?page=1&page_size=100');
      const todos = (res.data?.items || []).flatMap((p: any) =>
        (p.actions || []).map((a: any) => ({ ...a, projectName: p.name }))
      );
      setData(todos.length ? todos : [
        { id: 1, title: '完善客户跟进记录', priority: 0, is_done: false, projectName: '示例项目' },
        { id: 2, title: '准备项目方案书', priority: 1, is_done: false, projectName: '示例项目' },
      ]);
    } catch {}
  };

  useEffect(() => { fetch(); }, []);

  return (
    <div>
      <h2>我的待办</h2>
      <Table rowKey="id" dataSource={data} columns={[
        { title: '标题', dataIndex: 'title' },
        { title: '项目', dataIndex: 'projectName' },
        { title: '优先级', dataIndex: 'priority', render: (v: number) => <Tag color={PRIORITY_COLORS[v]}>{PRIORITY_LABELS[v]}</Tag> },
        { title: '状态', dataIndex: 'is_done', render: (v: boolean) => v ? <Tag color="green">已完成</Tag> : <Tag color="red">待处理</Tag> },
      ]} pagination={false} />
    </div>
  );
}

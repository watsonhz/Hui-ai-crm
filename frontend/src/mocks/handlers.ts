/** MSW handlers — mock all customer endpoints per the API spec.
 *
 *  Shape must match backend/app/schemas/response.py exactly:
 *    { code: 200, message: "success", data: ... }
 */

import { http, HttpResponse } from 'msw';
import type { Customer, CreateCustomerDto, UpdateCustomerDto, PaginatedResponse } from '@/types/customer';

// ---- Seed data (inline, must match api-spec shapes) ----
let seedId = 100;
const customers: Customer[] = Array.from({ length: 15 }, (_, i) => ({
  id: ++seedId,
  name: ['张伟', '李娜', '王强', '赵敏', '刘洋', '陈静', '孙磊', '周婷', '吴刚', '郑丽', '冯涛', '蒋欢', '韩雪', '沈飞', '杨光'][i],
  company: ['华为技术', '阿里巴巴', '比亚迪', '中国平安', '京东集团', '美的集团', '中兴通讯', '格力电器', '小米科技', '招商银行', '腾讯科技', '网易集团', '联想集团', '海康威视', '宁德时代'][i],
  industry: ['信息技术', '电子商务', '新能源', '金融保险', '电子商务', '家电制造', '通信设备', '家电制造', '消费电子', '金融银行', '互联网', '互联网', '信息技术', '安防监控', '新能源'][i],
  phone: `1380013${String(i).padStart(4, '0')}`,
  email: `customer${i + 1}@example.com`,
  source: ['展会', '官网', '推荐', '电话'][i % 4],
  level: (['A', 'B', 'C', 'D'] as const)[i % 4],
  status: (['潜在', '意向', '谈判', '成交', '流失'] as const)[i % 5],
  owner_id: null,
  created_at: new Date(Date.now() - (90 - i) * 86400000).toISOString(),
  updated_at: new Date(Date.now() - i * 3600000).toISOString(),
}));

function success<T>(data: T) {
  return HttpResponse.json({ code: 200, message: 'success', data });
}

function paginate(items: Customer[], page = 1, page_size = 20, params?: URLSearchParams): PaginatedResponse<Customer> {
  let filtered = [...items];

  const name = params?.get('name');
  const company = params?.get('company');
  const status = params?.get('status');
  const level = params?.get('level');

  if (name) filtered = filtered.filter((c) => c.name.includes(name));
  if (company) filtered = filtered.filter((c) => c.company.includes(company));
  if (status) filtered = filtered.filter((c) => c.status === status);
  if (level) filtered = filtered.filter((c) => c.level === level);

  const total = filtered.length;
  const start = (page - 1) * page_size;
  return { items: filtered.slice(start, start + page_size), total, page, page_size };
}

export const handlers = [
  // GET /api/v1/customers — paginated list
  http.get('/api/v1/customers', ({ request }) => {
    const url = new URL(request.url);
    const page = Number(url.searchParams.get('page')) || 1;
    const page_size = Number(url.searchParams.get('page_size')) || 20;
    return success(paginate(customers, page, page_size, url.searchParams));
  }),

  // GET /api/v1/customers/:id — detail
  http.get('/api/v1/customers/:id', ({ params }) => {
    const c = customers.find((x) => x.id === Number(params.id));
    if (!c) return HttpResponse.json({ code: 404, message: '客户不存在', data: null }, { status: 404 });
    return success(c);
  }),

  // POST /api/v1/customers — create
  http.post('/api/v1/customers', async ({ request }) => {
    const body = (await request.json()) as CreateCustomerDto;
    const c: Customer = {
      id: ++seedId,
      name: body.name,
      company: body.company || '',
      industry: body.industry || '',
      phone: body.phone || '',
      email: body.email || '',
      source: body.source || '',
      level: body.level || 'C',
      status: body.status || '潜在',
      owner_id: null,
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
    };
    customers.unshift(c);
    return success(c);
  }),

  // PUT /api/v1/customers/:id — update
  http.put('/api/v1/customers/:id', async ({ request, params }) => {
    const body = (await request.json()) as UpdateCustomerDto;
    const idx = customers.findIndex((x) => x.id === Number(params.id));
    if (idx === -1) return HttpResponse.json({ code: 404, message: '客户不存在', data: null }, { status: 404 });
    customers[idx] = { ...customers[idx], ...body, updated_at: new Date().toISOString() };
    return success(customers[idx]);
  }),

  // DELETE /api/v1/customers/:id — soft delete
  http.delete('/api/v1/customers/:id', ({ params }) => {
    const idx = customers.findIndex((x) => x.id === Number(params.id));
    if (idx === -1) return HttpResponse.json({ code: 404, message: '客户不存在', data: null }, { status: 404 });
    customers.splice(idx, 1);
    return success(null);
  }),
];

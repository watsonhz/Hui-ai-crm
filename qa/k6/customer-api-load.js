import http from 'k6/http';
import { check, sleep, group } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 50 },
    { duration: '60s', target: 50 },
    { duration: '30s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
  },
};

const BASE_URL = 'http://localhost:8000/api/v1';

export default function () {
  group('客户列表查询', () => {
    const listRes = http.get(`${BASE_URL}/customers/?page=1&page_size=20`);
    check(listRes, { 'GET /customers/ 200': (r) => r.status === 200 });
    sleep(0.5);
  });

  group('创建客户', () => {
    const payload = JSON.stringify({
      name: `测试客户${__VU}-${__ITER}`,
      phone: '13800138000',
      company: '测试公司',
      level: 'B',
    });
    const createRes = http.post(`${BASE_URL}/customers/`, payload, {
      headers: { 'Content-Type': 'application/json' },
    });
    check(createRes, { 'POST /customers/ 201': (r) => r.status === 201 });
    sleep(0.5);
  });

  group('客户详情', () => {
    http.get(`${BASE_URL}/customers/1`);
    sleep(0.2);
  });
}

import http from 'k6/http';
import { check, sleep, group } from 'k6';

export const options = {
  stages: [
    { duration: '20s', target: 10 },
    { duration: '40s', target: 50 },
    { duration: '30s', target: 50 },
    { duration: '10s', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.02'],
  },
  summaryTrendStats: ['min', 'avg', 'med', 'p(90)', 'p(95)', 'p(99)', 'max'],
};

const BASE = 'http://localhost:8000/api/v1';

export default function () {
  group('customer_crud', () => {
    const r1 = http.get(`${BASE}/customers/?page=1&page_size=20`);
    check(r1, { 'customers/200': (r) => r.status === 200 });
    sleep(0.3);

    const r2 = http.get(`${BASE}/customers/1`);
    check(r2, { 'customer/1/200': (r) => r.status === 200 || r.status === 404 });
    sleep(0.2);
  });

  group('bidding', () => {
    const r = http.get(`${BASE}/bidding/?page=1&page_size=20`);
    check(r, { 'bidding/200': (r) => r.status === 200 });
    sleep(0.3);

    const r2 = http.get(`${BASE}/bidding/calendar`);
    check(r2, { 'calendar/200': (r) => r.status === 200 });
    sleep(0.2);
  });

  group('projects', () => {
    const r = http.get(`${BASE}/projects/?page=1&page_size=20`);
    check(r, { 'projects/200': (r) => r.status === 200 });
    sleep(0.3);

    const r2 = http.get(`${BASE}/projects/kanban`);
    check(r2, { 'kanban/200': (r) => r.status === 200 });
    sleep(0.2);
  });

  group('organizations', () => {
    const r = http.get(`${BASE}/organizations/tree`);
    check(r, { 'org_tree/200': (r) => r.status === 200 });
    sleep(0.2);
  });

  group('health', () => {
    http.get(`${BASE}/health`);
    sleep(0.1);
  });
}

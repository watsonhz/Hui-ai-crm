import http from 'k6/http';
import { check, sleep, group } from 'k6';

export const options = {
  vus: 30,
  duration: '60s',
  thresholds: {
    http_req_duration: ['p(95)<500'],
    http_req_failed: ['rate<0.01'],
  },
};

const BASE_URL = 'http://localhost:8000/api/v1';

export default function () {
  group('投标列表', () => {
    const res = http.get(`${BASE_URL}/bidding/?page=1&page_size=20`);
    check(res, { 'GET /bidding/ 200': (r) => r.status === 200 });
    sleep(0.3);
  });

  group('投标日历', () => {
    http.get(`${BASE_URL}/bidding/calendar`);
    sleep(0.2);
  });

  group('项目看板', () => {
    http.get(`${BASE_URL}/projects/kanban`);
    sleep(0.3);
  });

  group('组织树', () => {
    http.get(`${BASE_URL}/organizations/tree`);
    sleep(0.2);
  });
}

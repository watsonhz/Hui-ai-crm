"""
Locust 性能测试 — AI-CRM Sprint2 性能基线 (TASK-008 Part C)

运行:
   locust -f tests/performance/locustfile.py --host=http://192.168.0.170:8000
   # 或 headless:
   locust -f tests/performance/locustfile.py --host=http://192.168.0.170:8000 \
     --headless -u 100 -r 10 -t 120s \
     --html=tests/reports/performance-baseline-sprint2.html

基线目标: P95 < 500ms, 并发 100 用户, 错误率 < 1%
"""
from locust import HttpUser, task, between, events
import time


class CRMBusinessUser(HttpUser):
    """模拟 CRM 业务用户（基础业务模块负载）。"""
    wait_time = between(1, 3)
    weight = 5

    def on_start(self):
        self.headers = {
            "Authorization": "Bearer perf-test-token",
            "Content-Type": "application/json",
        }

    @task(5)
    def list_bidding(self):
        self.client.get(
            "/api/v1/bidding",
            headers=self.headers,
            params={"page": 1, "page_size": 20},
            name="GET /bidding (list)",
        )

    @task(4)
    def list_projects(self):
        self.client.get(
            "/api/v1/projects",
            headers=self.headers,
            params={"page": 1, "page_size": 20},
            name="GET /projects (list)",
        )

    @task(3)
    def get_bidding_detail(self):
        self.client.get(
            "/api/v1/bidding/1",
            headers=self.headers,
            name="GET /bidding/{id}",
        )

    @task(3)
    def get_project_detail(self):
        self.client.get(
            "/api/v1/projects/1",
            headers=self.headers,
            name="GET /projects/{id}",
        )

    @task(2)
    def tree_organizations(self):
        self.client.get(
            "/api/v1/organizations/tree",
            headers=self.headers,
            name="GET /organizations/tree",
        )

    @task(2)
    def kanban_projects(self):
        self.client.get(
            "/api/v1/projects/board/kanban",
            headers=self.headers,
            name="GET /projects/kanban",
        )

    @task(1)
    def calendar_bidding(self):
        self.client.get(
            "/api/v1/bidding/calendar/upcoming",
            headers=self.headers,
            params={"days": 30},
            name="GET /bidding/calendar",
        )


class CRMAIUser(HttpUser):
    """模拟 AI 模块用户（AI 诊断/报告负载）。"""
    wait_time = between(2, 5)
    weight = 2

    def on_start(self):
        self.headers = {
            "Authorization": "Bearer perf-test-token",
            "Content-Type": "application/json",
        }

    @task(3)
    def health_check(self):
        self.client.get(
            "/health",
            name="GET /health",
        )

    @task(2)
    def ai_diagnosis_signals(self):
        self.client.get(
            "/api/v1/ai/diagnosis/signals",
            headers=self.headers,
            name="GET /ai/diagnosis/signals",
        )

    @task(1)
    def decision_chain_graph(self):
        self.client.get(
            "/api/v1/decision-chain",
            headers=self.headers,
            name="GET /decision-chain",
        )


class CRMWriteUser(HttpUser):
    """模拟写操作用户（创建/更新负载）。"""
    wait_time = between(3, 6)
    weight = 1

    def on_start(self):
        self.headers = {
            "Authorization": "Bearer perf-test-token",
            "Content-Type": "application/json",
        }

    @task(3)
    def create_bidding(self):
        self.client.post(
            "/api/v1/bidding",
            headers=self.headers,
            json={"title": "性能测试投标", "bid_status": 1},
            name="POST /bidding (create)",
        )

    @task(2)
    def create_organization(self):
        self.client.post(
            "/api/v1/organizations",
            headers=self.headers,
            json={"name": "性能测试部门", "org_type": "dept"},
            name="POST /organizations (create)",
        )

    @task(1)
    def create_project(self):
        self.client.post(
            "/api/v1/projects",
            headers=self.headers,
            json={"name": "性能测试项目", "stage": 1},
            name="POST /projects (create)",
        )


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print(f"\n{'='*60}")
    print(f"Sprint2 Performance Baseline")
    print(f"Target: P95 < 500ms | Users: 100 | Error < 1%")
    print(f"{'='*60}\n")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    stats = environment.stats
    total_requests = stats.total.num_requests
    total_failures = stats.total.num_failures
    error_rate = (total_failures / total_requests * 100) if total_requests > 0 else 0

    print(f"\n{'='*60}")
    print(f"Baseline Complete:")
    print(f"  Total Requests: {total_requests}")
    print(f"  Failures: {total_failures} ({error_rate:.2f}%)")
    print(f"  Avg Response: {stats.total.avg_response_time:.0f}ms")
    print(f"  P95 Response:  N/A (see HTML report)")
    print(f"  RPS: {stats.total.total_rps:.1f}")
    if error_rate < 1:
        print(f"  Result: PASS (error rate < 1%)")
    else:
        print(f"  Result: FAIL (error rate >= 1%)")
    print(f"{'='*60}\n")

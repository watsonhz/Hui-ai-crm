"""
Locust 性能压测 — Sprint3 AI + PGVector 基线 (TASK-012 Part C)

运行:
  locust -f tests/performance/locustfile-sprint3.py --host=http://192.168.0.170:8000 \
    --headless -u 50 -r 5 -t 180s \
    --html=tests/reports/performance-sprint3.html

Sprint3 目标:
  - AI 接口: P95 < 3s, 并发 50
  - CRUD 接口: P95 < 500ms
  - PGVector 搜索: P95 < 200ms
"""
from locust import HttpUser, task, between, events


class CRMUser(HttpUser):
    """基础 CRUD 用户（对照基线）。"""
    wait_time = between(1, 3)
    weight = 3

    def on_start(self):
        self.headers = {
            "Authorization": "Bearer perf-test-token",
            "Content-Type": "application/json",
        }

    @task(3)
    def list_bidding(self):
        self.client.get("/api/v1/bidding", headers=self.headers,
                        params={"page": 1, "page_size": 20},
                        name="CRUD: GET /bidding")

    @task(2)
    def list_projects(self):
        self.client.get("/api/v1/projects", headers=self.headers,
                        params={"page": 1, "page_size": 20},
                        name="CRUD: GET /projects")

    @task(1)
    def tree_organizations(self):
        self.client.get("/api/v1/organizations/tree", headers=self.headers,
                        name="CRUD: GET /orgs/tree")

    @task(1)
    def create_bidding(self):
        self.client.post("/api/v1/bidding", headers=self.headers,
                         json={"title": "perf-test", "bid_status": 1},
                         name="CRUD: POST /bidding")


class AIReportUser(HttpUser):
    """AI 报告生成用户（AI 接口压测重点）。"""
    wait_time = between(2, 5)
    weight = 2

    def on_start(self):
        self.headers = {
            "Authorization": "Bearer perf-test-token",
            "Content-Type": "application/json",
        }

    @task(3)
    def generate_daily_report(self):
        self.client.post("/api/v1/ai/reports/daily", headers=self.headers,
                         json={"date": "2026-06-13"},
                         name="AI: POST /reports/daily")

    @task(2)
    def generate_weekly_report(self):
        self.client.post("/api/v1/ai/reports/weekly", headers=self.headers,
                         json={"week": "2026-W24"},
                         name="AI: POST /reports/weekly")

    @task(1)
    def generate_monthly_report(self):
        self.client.post("/api/v1/ai/reports/monthly", headers=self.headers,
                         json={"month": "2026-06"},
                         name="AI: POST /reports/monthly")

    @task(2)
    def get_report_history(self):
        self.client.get("/api/v1/ai/reports/history", headers=self.headers,
                        params={"page": 1, "page_size": 10},
                        name="AI: GET /reports/history")


class KnowledgeSearchUser(HttpUser):
    """PGVector 知识库搜索用户。"""
    wait_time = between(1, 3)
    weight = 2

    def on_start(self):
        self.headers = {
            "Authorization": "Bearer perf-test-token",
            "Content-Type": "application/json",
        }

    @task(4)
    def semantic_search(self):
        search_queries = [
            "AI运维平台架构设计",
            "合同付款条款模板",
            "客户拜访最佳实践",
            "政企大客户管理方案",
            "PGVector向量检索性能优化",
        ]
        import random
        self.client.post("/api/v1/knowledge/search", headers=self.headers,
                         json={"query": random.choice(search_queries), "top_k": 10},
                         name="PGVector: POST /knowledge/search")

    @task(1)
    def list_documents(self):
        self.client.get("/api/v1/knowledge/documents", headers=self.headers,
                        params={"page": 1, "page_size": 10},
                        name="PGVector: GET /knowledge/documents")


class DiagnosisUser(HttpUser):
    """AI 12信号诊断用户。"""
    wait_time = between(3, 6)
    weight = 1

    def on_start(self):
        self.headers = {
            "Authorization": "Bearer perf-test-token",
            "Content-Type": "application/json",
        }

    @task(2)
    def run_diagnosis(self):
        self.client.post("/api/v1/ai/diagnosis/run-all", headers=self.headers,
                         json={"customer_id": 42},
                         name="AI: POST /diagnosis/run-all")


@events.test_start.add_listener
def on_start(environment, **kwargs):
    print("\n" + "=" * 60)
    print("Sprint3 Performance Baseline")
    print("Target: AI P95 < 3s | CRUD P95 < 500ms | PGVector P95 < 200ms")
    print("Users: 50 | Duration: 180s")
    print("=" * 60 + "\n")


@events.test_stop.add_listener
def on_stop(environment, **kwargs):
    stats = environment.stats
    total = stats.total.num_requests
    failures = stats.total.num_failures
    err_rate = (failures / total * 100) if total > 0 else 0

    print("\n" + "=" * 60)
    print(f"Sprint3 Complete: {total} req, {failures} fail ({err_rate:.1f}%)")
    print(f"  Avg: {stats.total.avg_response_time:.0f}ms")
    print(f"  RPS: {stats.total.total_rps:.1f}")
    print("=" * 60 + "\n")

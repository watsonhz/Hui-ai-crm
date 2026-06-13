"""
Locust 性能测试 — AI-CRM API 负载测试。

运行方式:
    cd C:/DevProjects/ai-crm
    locust -f tests/performance/locustfile.py --host=http://192.168.0.170:8000

然后访问 http://localhost:8089 启动测试。
"""

from locust import HttpUser, task, between


class CRMUser(HttpUser):
    """模拟 CRM 系统用户进行负载测试。"""

    wait_time = between(1, 3)  # 每次请求间隔 1-3 秒

    def on_start(self):
        """用户登录，获取 Token。"""
        # TODO: 待认证模块实现后补充登录逻辑
        self.headers = {
            "Authorization": "Bearer test-perf-token",
            "Content-Type": "application/json",
        }

    # === 基础业务模块 ===

    @task(3)
    def get_customers(self):
        """查询客户列表（高频操作）。"""
        self.client.get(
            "/api/v1/customers",
            headers=self.headers,
            params={"page": 1, "page_size": 20},
        )

    @task(2)
    def get_projects(self):
        """查询项目列表。"""
        self.client.get(
            "/api/v1/projects",
            headers=self.headers,
            params={"page": 1, "page_size": 20},
        )

    @task(1)
    def get_organizations(self):
        """查询组织树（低频操作）。"""
        self.client.get(
            "/api/v1/organizations/tree",
            headers=self.headers,
        )

    # === AI 模块 ===

    @task(1)
    def get_ai_reports(self):
        """获取 AI 报告。"""
        self.client.get(
            "/api/v1/ai/reports/daily",
            headers=self.headers,
        )

    # === 系统 ===

    @task(1)
    def health_check(self):
        """健康检查。"""
        self.client.get("/api/v1/health")

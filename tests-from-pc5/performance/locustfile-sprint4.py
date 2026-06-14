"""
Locust Sprint4 性能压测 — 登录并发 + 工单混合负载 (TASK-016 Part C)

目标: 登录 P95 < 500ms | 工单 P95 < 1s | 并发 100
"""
from locust import HttpUser, task, between, events
import random


class LoginUser(HttpUser):
    """并发登录压测。"""
    wait_time = between(1, 3)
    weight = 4

    def on_start(self):
        self.headers = {"Content-Type": "application/json"}

    @task(1)
    def password_login(self):
        users = [
            {"username": "admin", "password": "admin123"},
            {"username": "sales01", "password": "sales123"},
            {"username": "service01", "password": "svc123"},
            {"username": "marketing01", "password": "mkt123"},
            {"username": "viewer", "password": "view123"},
        ]
        u = random.choice(users)
        self.client.post("/api/v1/auth/login", json=u, name="Auth: POST /login")


class TicketUser(HttpUser):
    """工单 CRUD 混合负载。"""
    wait_time = between(2, 5)
    weight = 3

    def on_start(self):
        self.headers = {
            "Authorization": "Bearer perf-test-token",
            "Content-Type": "application/json",
        }

    @task(3)
    def create_ticket(self):
        priorities = ["P0", "P1", "P2", "P3"][:2]  # mostly P0/P1
        self.client.post("/api/v1/ai/service/tickets", headers=self.headers,
                         json={"title": f"perf-{random.randint(1,9999)}",
                               "priority": random.choice(priorities)},
                         name="Ticket: POST /tickets")

    @task(4)
    def list_tickets(self):
        self.client.get("/api/v1/ai/service/tickets", headers=self.headers,
                        params={"page": 1, "page_size": 20},
                        name="Ticket: GET /tickets")

    @task(1)
    def get_ticket_detail(self):
        self.client.get("/api/v1/ai/service/tickets/1", headers=self.headers,
                        name="Ticket: GET /tickets/{id}")


@events.test_start.add_listener
def on_start(environment, **kwargs):
    print("\n" + "=" * 60)
    print("Sprint4 Performance: Login + Tickets")
    print("Target: Login P95 < 500ms | Ticket P95 < 1s | 100 users")
    print("=" * 60 + "\n")


@events.test_stop.add_listener
def on_stop(environment, **kwargs):
    s = environment.stats.total
    err = (s.num_failures / s.num_requests * 100) if s.num_requests else 0
    print(f"\nSprint4 Done: {s.num_requests} req, {err:.1f}% err, "
          f"avg {s.avg_response_time:.0f}ms, rps {s.total_rps:.1f}\n")

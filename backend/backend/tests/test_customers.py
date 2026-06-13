"""Tests for the customer CRUD API."""

import pytest
from fastapi.testclient import TestClient


class TestCreateCustomer:
    """POST /api/v1/customers/"""

    def test_create_customer_success(self, client: TestClient):
        """Creating a customer with valid data returns 201 and the customer."""
        payload = {
            "name": "测试客户",
            "company": "测试有限公司",
            "phone": "13800138000",
            "email": "test@example.com",
            "level": "A",
            "source": "网络推广",
        }
        response = client.post("/api/v1/customers/", json=payload)
        assert response.status_code == 201
        body = response.json()
        assert body["code"] == 200
        assert body["message"] == "客户创建成功"
        assert body["data"]["id"] == 1
        assert body["data"]["name"] == "测试客户"
        assert body["data"]["level"] == "A"
        assert body["data"]["status"] == "active"
        assert body["data"]["created_at"] is not None

    def test_create_customer_minimal(self, client: TestClient):
        """Creating with only the required name field succeeds."""
        payload = {"name": "最低字段客户"}
        response = client.post("/api/v1/customers/", json=payload)
        assert response.status_code == 201
        body = response.json()
        assert body["data"]["name"] == "最低字段客户"
        assert body["data"]["level"] == "C"  # default
        assert body["data"]["status"] == "active"  # default

    def test_create_customer_validation_error_name_too_short(self, client: TestClient):
        """An empty name should fail with 422."""
        payload = {"name": ""}
        response = client.post("/api/v1/customers/", json=payload)
        assert response.status_code == 422

    def test_create_customer_validation_error_name_missing(self, client: TestClient):
        """Missing name field should fail with 422."""
        payload = {"company": "no name"}
        response = client.post("/api/v1/customers/", json=payload)
        assert response.status_code == 422

    def test_create_customer_invalid_phone(self, client: TestClient):
        """An invalid phone number should fail with 422."""
        payload = {"name": "test", "phone": "12345"}
        response = client.post("/api/v1/customers/", json=payload)
        assert response.status_code == 422

    def test_create_customer_invalid_email(self, client: TestClient):
        """An invalid email should fail with 422."""
        payload = {"name": "test", "email": "not-an-email"}
        response = client.post("/api/v1/customers/", json=payload)
        assert response.status_code == 422

    def test_create_customer_invalid_level(self, client: TestClient):
        """A level outside A/B/C/D should fail with 422."""
        payload = {"name": "test", "level": "X"}
        response = client.post("/api/v1/customers/", json=payload)
        assert response.status_code == 422


class TestListCustomers:
    """GET /api/v1/customers/"""

    @pytest.fixture(autouse=True)
    def seed_customers(self, client: TestClient):
        """Create several customers for list tests."""
        customers = [
            {"name": f"客户{i:02d}", "level": "A" if i % 3 == 0 else "B", "status": "active"}
            for i in range(1, 11)
        ]
        for c in customers:
            client.post("/api/v1/customers/", json=c)

    def test_get_customer_list_default(self, client: TestClient):
        """Default list returns paginated results."""
        response = client.get("/api/v1/customers/")
        assert response.status_code == 200
        body = response.json()
        assert body["code"] == 200
        assert body["data"]["total"] == 10
        assert body["data"]["page"] == 1
        assert body["data"]["page_size"] == 20
        assert len(body["data"]["items"]) == 10

    def test_get_customer_list_paginated(self, client: TestClient):
        """Pagination with page_size=3 works."""
        response = client.get("/api/v1/customers/?page=1&page_size=3")
        body = response.json()
        assert body["data"]["total"] == 10
        assert len(body["data"]["items"]) == 3
        assert body["data"]["page"] == 1
        assert body["data"]["page_size"] == 3

    def test_get_customer_list_page_two(self, client: TestClient):
        """Page 2 returns the correct slice."""
        response = client.get("/api/v1/customers/?page=2&page_size=3")
        body = response.json()
        assert len(body["data"]["items"]) == 3
        # items should be different from page 1
        response_p1 = client.get("/api/v1/customers/?page=1&page_size=3")
        p1_names = {c["name"] for c in response_p1.json()["data"]["items"]}
        p2_names = {c["name"] for c in body["data"]["items"]}
        assert p1_names.isdisjoint(p2_names)

    def test_get_customer_list_filter_by_name(self, client: TestClient):
        """Filter by name with partial match."""
        response = client.get("/api/v1/customers/?name=客户01")
        body = response.json()
        assert body["data"]["total"] == 1
        assert body["data"]["items"][0]["name"] == "客户01"

    def test_get_customer_list_filter_by_level(self, client: TestClient):
        """Filter by level returns only matching customers."""
        response = client.get("/api/v1/customers/?level=A")
        body = response.json()
        assert all(c["level"] == "A" for c in body["data"]["items"])

    def test_get_customer_list_sort(self, client: TestClient):
        """Sort by name ascending."""
        response = client.get("/api/v1/customers/?sort_order=name_asc")
        body = response.json()
        names = [c["name"] for c in body["data"]["items"]]
        assert names == sorted(names)

    def test_get_customer_list_empty(self, client: TestClient):
        """Filter with no matches returns empty list."""
        response = client.get("/api/v1/customers/?name=NONEXISTENT")
        body = response.json()
        assert body["data"]["total"] == 0
        assert body["data"]["items"] == []


class TestGetCustomerById:
    """GET /api/v1/customers/{id}"""

    @pytest.fixture(autouse=True)
    def seed_one(self, client: TestClient):
        """Create one test customer."""
        client.post(
            "/api/v1/customers/",
            json={"name": "唯一客户", "email": "unique@example.com"},
        )

    def test_get_customer_by_id(self, client: TestClient):
        """Fetch existing customer returns 200."""
        response = client.get("/api/v1/customers/1")
        assert response.status_code == 200
        body = response.json()
        assert body["data"]["id"] == 1
        assert body["data"]["name"] == "唯一客户"
        assert body["data"]["email"] == "unique@example.com"

    def test_get_customer_404(self, client: TestClient):
        """Fetching a non-existent customer returns 404."""
        response = client.get("/api/v1/customers/999")
        assert response.status_code == 200  # our error handler returns 200 with code 404
        body = response.json()
        assert body["code"] == 404
        assert body["data"] is None


class TestUpdateCustomer:
    """PUT /api/v1/customers/{id}"""

    @pytest.fixture(autouse=True)
    def seed_one(self, client: TestClient):
        """Create one test customer."""
        client.post(
            "/api/v1/customers/",
            json={"name": "原始客户", "level": "C"},
        )

    def test_update_customer(self, client: TestClient):
        """Update an existing customer."""
        payload = {"name": "已更新客户", "level": "A"}
        response = client.put("/api/v1/customers/1", json=payload)
        assert response.status_code == 200
        body = response.json()
        assert body["data"]["name"] == "已更新客户"
        assert body["data"]["level"] == "A"
        assert body["message"] == "客户更新成功"

    def test_update_customer_partial(self, client: TestClient):
        """Partial update leaves other fields unchanged."""
        response = client.put("/api/v1/customers/1", json={"level": "B"})
        body = response.json()
        assert body["data"]["level"] == "B"
        assert body["data"]["name"] == "原始客户"  # unchanged

    def test_update_customer_404(self, client: TestClient):
        """Update non-existent customer returns 404."""
        response = client.put("/api/v1/customers/999", json={"name": "x"})
        body = response.json()
        assert body["code"] == 404

    def test_update_customer_empty_body(self, client: TestClient):
        """PUT with empty body is accepted (no fields means no changes)."""
        response = client.put("/api/v1/customers/1", json={})
        assert response.status_code == 200
        body = response.json()
        assert body["data"]["name"] == "原始客户"


class TestSoftDeleteCustomer:
    """DELETE /api/v1/customers/{id}"""

    @pytest.fixture(autouse=True)
    def seed_one(self, client: TestClient):
        """Create one test customer."""
        client.post(
            "/api/v1/customers/",
            json={"name": "待删除客户"},
        )

    def test_soft_delete_customer(self, client: TestClient):
        """Soft-deleting a customer succeeds and the customer is no longer retrievable."""
        response = client.delete("/api/v1/customers/1")
        assert response.status_code == 200
        body = response.json()
        assert body["code"] == 200
        assert body["message"] == "客户删除成功"

        # Confirm it is no longer listed
        list_resp = client.get("/api/v1/customers/")
        assert list_resp.json()["data"]["total"] == 0

        # Confirm it returns 404 when fetched directly
        get_resp = client.get("/api/v1/customers/1")
        assert get_resp.json()["code"] == 404

    def test_soft_delete_twice_returns_404(self, client: TestClient):
        """Deleting a customer that is already deleted returns 404."""
        client.delete("/api/v1/customers/1")
        response = client.delete("/api/v1/customers/1")
        body = response.json()
        assert body["code"] == 404

    def test_delete_non_existent(self, client: TestClient):
        """Deleting a non-existent customer returns 404."""
        response = client.delete("/api/v1/customers/999")
        body = response.json()
        assert body["code"] == 404

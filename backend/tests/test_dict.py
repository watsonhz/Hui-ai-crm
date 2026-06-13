class TestDictAPI:
    def test_create_type(self, client):
        resp = client.post("/api/v1/system/dict/type", json={"dict_name": "客户来源", "dict_type": "customer_source"})
        assert resp.status_code == 200
        assert resp.json()["data"]["dict_name"] == "客户来源"

    def test_list_types(self, client):
        client.post("/api/v1/system/dict/type", json={"dict_name": "行业", "dict_type": "industry"})
        resp = client.get("/api/v1/system/dict/type")
        assert len(resp.json()["data"]) >= 1

    def test_create_data(self, client):
        client.post("/api/v1/system/dict/type", json={"dict_name": "性别", "dict_type": "gender"})
        resp = client.post("/api/v1/system/dict/data", json={"dict_type": "gender", "dict_label": "男", "dict_value": "male", "sort_order": 1})
        assert resp.status_code == 200

    def test_list_data(self, client):
        client.post("/api/v1/system/dict/type", json={"dict_name": "状态", "dict_type": "status"})
        client.post("/api/v1/system/dict/data", json={"dict_type": "status", "dict_label": "启用", "dict_value": "1", "sort_order": 1})
        resp = client.get("/api/v1/system/dict/data/status")
        assert len(resp.json()["data"]) >= 1

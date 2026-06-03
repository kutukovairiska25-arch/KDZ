import requests

BASE = "http://127.0.0.1:8000"


def test_flow():
    # 1. Импорт курьера
    r = requests.post(f"{BASE}/couriers", json={
        "data": [{"courier_id": 1, "courier_type": "bike", "regions": [1], "working_hours": ["09:00-18:00"]}]})
    assert r.status_code == 201

    # 2. Импорт заказа
    r = requests.post(f"{BASE}/orders",
                      json={"data": [{"order_id": 101, "weight": 5.0, "region": 1, "delivery_hours": ["10:00-12:00"]}]})
    assert r.status_code == 201

    # 3. Назначение
    r = requests.post(f"{BASE}/orders/assign", json={"courier_id": 1})
    assert r.status_code == 200
    assert "assign_time" in r.json()

    # 4. Завершение
    r = requests.post(f"{BASE}/orders/complete",
                      json={"courier_id": 1, "order_id": 101, "complete_time": "2024-01-01T11:30:00Z"})
    assert r.status_code == 200

    # 5. Получение курьера
    r = requests.get(f"{BASE}/couriers/1")
    assert r.status_code == 200
    data = r.json()
    assert "earnings" in data and "rating" in data

    print("✅ Все тесты requests прошли успешно!")


if __name__ == "__main__":
    test_flow()
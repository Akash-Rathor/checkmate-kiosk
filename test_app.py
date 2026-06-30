from fastapi.testclient import TestClient

from main import app, calculate_prep

from models.order import OrderItem

client = TestClient(app)


def test_calculate_prep():

    items = [
        OrderItem(item_id=1, qty=2),
        OrderItem(item_id=3, qty=1),
    ]

    estimated, schedule = calculate_prep(items)

    assert estimated == 180
    assert schedule == [(1, 180), (2, 75)]


def test_create_order():

    response = client.post(
        "/order",
        json={
            "items": [
                {"item_id": 1, "qty": 2},
                {"item_id": 3, "qty": 1},
            ]
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["subtotal_cents"] == 2297
    assert data["discount_cents"] == 230
    assert data["total_cents"] == 2067
    assert data["estimated_prep_seconds"] == 180
    assert data["prep_schedule"] == [[1, 180], [2, 75]]


def test_invalid_item():
    """item does not exists in db/menu"""
    response = client.post(
        "/order",
        json={
            "items": [
                {"item_id": 10, "qty": 1}
            ]
        },
    )

    assert response.status_code == 400


def test_incorrect_request_body():
    """request accepts items and not data."""
    response = client.post(
        "/order",
        json={
            "data": [
                {"item_id": 10, "qty": 1}
            ]
        },
    )

    assert response.status_code == 422

    resp = response.json()
    assert resp["detail"][0]["msg"]=="Field required"
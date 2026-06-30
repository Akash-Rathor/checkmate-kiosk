from fastapi import FastAPI, HTTPException
from models.order import OrderRequest, OrderResponse
from db.menu import MENU

app = FastAPI()

def calculate_prep(items):
    stations = [(1, 0), (2, 0)]

    for item in items:
        prep = MENU[item.item_id]["prep_seconds"] * item.qty

        station = min(stations, key=lambda s: s[1])
        print("station",station)
        stations.remove(station)

        stations.append((station[0], station[1] + prep))


    stations.sort(key=lambda s: s[1], reverse=True)

    return max(time_occupied for station_id, time_occupied in stations), stations


@app.post("/order", response_model=OrderResponse)
def create_order(order: OrderRequest):

    if not order.items:
        raise HTTPException(status_code=400, detail="items cannot be empty")

    subtotal = 0
    discount = 0

    for item in order.items:
        print(order.items)

        if item.qty <= 0:
            raise HTTPException(status_code=400, detail="qty must be a positive integer")

        if item.item_id not in MENU:
            raise HTTPException(status_code=400, detail=f"Invalid item_id {item.item_id}")

        subtotal += MENU[item.item_id]["price_cents"] * item.qty

    if subtotal >= 2000:
        discount = round(subtotal * 0.10)

    total = subtotal - discount

    estimated, schedule = calculate_prep(order.items)

    return {
        "subtotal_cents": subtotal,
        "discount_cents": discount,
        "total_cents": total,
        "estimated_prep_seconds": estimated,
        "prep_schedule": schedule,
    }
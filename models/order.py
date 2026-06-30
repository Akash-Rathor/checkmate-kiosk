from pydantic import BaseModel
from typing import List, Tuple

# request models
class OrderItem(BaseModel):
    item_id: int
    qty: int


class OrderRequest(BaseModel):
    items: List[OrderItem]


# response models
class OrderResponse(BaseModel):
    subtotal_cents: int
    discount_cents: int
    total_cents: int
    estimated_prep_seconds: int
    prep_schedule: list[tuple[int, int]]
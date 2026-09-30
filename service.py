from typing import TypedDict


class Order(TypedDict):
    order_id: int
    status: str
    product: str
    payment_status: str

ORDERS: dict[int, Order] = {
    123: {
        "order_id": 123,
        "status": "delivered",
        "product": "Headphones",
        "payment_status": "paid",
    },
    456: {
        "order_id": 456,
        "status": "processing",
        "product": "Keyboard",
        "payment_status": "paid",
    },
}


async def find_order(order_id: int) -> Order | None:
    return ORDERS.get(order_id)
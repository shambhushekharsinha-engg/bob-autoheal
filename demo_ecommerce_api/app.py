"""
Demo E-Commerce API — BUGGY VERSION
====================================
This module intentionally contains 4 bugs that the AutoHeal Agent will discover
and fix. It serves as the "before" state of the application.

Bugs:
  BUG-001 (L35): KeyError — no check if item exists before accessing inventory
  BUG-002 (L37): Logic error — negative quantities are not rejected
  BUG-003 (L40): Logic error — ordering more than stock raises 500 instead of 400
  BUG-004 (L40): Wrong HTTP status code — 500 used instead of 400 for business logic error
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(
    title="Demo E-Commerce API",
    description="A sample API used to demonstrate the IBM Bob AutoHeal workflow.",
    version="1.0.0-BUGGY",
)

# In-memory inventory database
inventory: Dict[str, int] = {
    "laptop": 10,
    "mouse": 50,
    "keyboard": 20,
}


class Order(BaseModel):
    item: str
    quantity: int


@app.get("/", summary="Health check")
def read_root():
    return {"status": "ok", "message": "Welcome to the Demo E-Commerce API"}


@app.get("/inventory", summary="List all inventory items")
def get_inventory():
    return inventory


@app.post("/order", summary="Place an order")
def place_order(order: Order):
    # BUG-001: No check for item existence — raises unhandled KeyError → HTTP 500
    # BUG-002: Negative quantities accepted (e.g., quantity=-5 increases stock)
    stock = inventory[order.item]

    # BUG-003 / BUG-004: Out-of-stock raises HTTP 500 instead of HTTP 400
    if order.quantity > stock:
        raise HTTPException(status_code=500, detail="Not enough stock")

    inventory[order.item] -= order.quantity
    return {
        "message": "Order placed successfully",
        "item": order.item,
        "quantity_ordered": order.quantity,
        "remaining_stock": inventory[order.item],
    }

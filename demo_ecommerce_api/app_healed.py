"""
Demo E-Commerce API — HEALED VERSION
======================================
This module is what the AutoHeal Agent produces after diagnosing and fixing all 4 bugs.
It serves as the "after" state, demonstrating the agent's impact.

Fixes applied by Bob AutoHeal Agent:
  FIX-001 (BUG-001): Added item-existence check → raises HTTP 404 for unknown items
  FIX-002 (BUG-002): Added Pydantic Field(gt=0) constraint → raises HTTP 422 for bad input
  FIX-003 (BUG-003): Out-of-stock condition now raises HTTP 400 (Bad Request)
  FIX-004 (BUG-004): Corrected HTTP status code from 500 to 400 for business logic errors
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict

app = FastAPI(
    title="Demo E-Commerce API",
    description="A sample API used to demonstrate the IBM Bob AutoHeal workflow.",
    version="1.0.0-HEALED",
)

# In-memory inventory database
inventory: Dict[str, int] = {
    "laptop": 10,
    "mouse": 50,
    "keyboard": 20,
}


class Order(BaseModel):
    item: str
    # FIX-002: quantity must be > 0; Pydantic will raise 422 automatically
    quantity: int = Field(..., gt=0, description="Number of items to order (must be >= 1)")


@app.get("/", summary="Health check")
def read_root():
    return {"status": "ok", "message": "Welcome to the Demo E-Commerce API"}


@app.get("/inventory", summary="List all inventory items")
def get_inventory():
    return inventory


@app.post("/order", summary="Place an order")
def place_order(order: Order):
    # FIX-001: Check if item exists before accessing inventory
    if order.item not in inventory:
        raise HTTPException(status_code=404, detail=f"Item '{order.item}' not found in inventory")

    stock = inventory[order.item]

    # FIX-003 / FIX-004: Out-of-stock is a client error (400), not a server error (500)
    if order.quantity > stock:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough stock. Requested {order.quantity}, available {stock}",
        )

    inventory[order.item] -= order.quantity
    return {
        "message": "Order placed successfully",
        "item": order.item,
        "quantity_ordered": order.quantity,
        "remaining_stock": inventory[order.item],
    }

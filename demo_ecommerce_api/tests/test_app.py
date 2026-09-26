"""
Test Suite for Demo E-Commerce API
====================================
These tests are written FIRST (test-driven) and expose the 4 intentional bugs in app.py.
Running this suite against the buggy app produces 3 FAILED tests.
After the IBM Bob AutoHeal Agent heals app.py, all 5 tests should PASS.

Test Coverage Target: >= 90%
"""

import pytest
from fastapi.testclient import TestClient
from app import app, inventory

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_inventory():
    """Reset inventory state before each test to ensure isolation."""
    inventory.clear()
    inventory.update({
        "laptop": 10,
        "mouse": 50,
        "keyboard": 20,
    })
    yield


# ──────────────────────────────────────────────────────────────────────────────
# PASSING TESTS (these should already work)
# ──────────────────────────────────────────────────────────────────────────────

class TestHealthCheck:
    """Tests for the root health-check endpoint."""

    def test_read_root_returns_200(self):
        """Root endpoint should return HTTP 200."""
        response = client.get("/")
        assert response.status_code == 200

    def test_read_root_returns_expected_keys(self):
        """Root endpoint should return status and message keys."""
        response = client.get("/")
        data = response.json()
        assert "status" in data
        assert "message" in data


class TestInventory:
    """Tests for the inventory listing endpoint."""

    def test_get_inventory_returns_200(self):
        """Inventory endpoint should return HTTP 200."""
        response = client.get("/inventory")
        assert response.status_code == 200

    def test_get_inventory_contains_correct_items(self):
        """Inventory should contain all 3 default items."""
        response = client.get("/inventory")
        data = response.json()
        assert "laptop" in data
        assert "mouse" in data
        assert "keyboard" in data

    def test_place_order_success(self):
        """A valid order for an in-stock item should succeed."""
        response = client.post("/order", json={"item": "laptop", "quantity": 1})
        assert response.status_code == 200
        data = response.json()
        assert data["remaining_stock"] == 9
        assert data["item"] == "laptop"
        assert data["quantity_ordered"] == 1


# ──────────────────────────────────────────────────────────────────────────────
# FAILING TESTS (these expose bugs — should fail before healing, pass after)
# ──────────────────────────────────────────────────────────────────────────────

class TestOrderBugs:
    """
    Tests that EXPOSE bugs in the original app.py.
    These 3 tests FAIL on the buggy version, and PASS on the healed version.
    """

    def test_order_unknown_item_returns_404(self):
        """
        BUG-001: Ordering a non-existent item raises a raw KeyError (HTTP 500).
        EXPECTED: HTTP 404 Not Found.
        """
        response = client.post("/order", json={"item": "monitor", "quantity": 1})
        assert response.status_code == 404, (
            f"Expected 404 for unknown item, got {response.status_code}. "
            "BUG-001: KeyError is not handled."
        )

    def test_order_negative_quantity_rejected(self):
        """
        BUG-002: Negative quantities are silently accepted, which INCREASES stock.
        EXPECTED: HTTP 422 Unprocessable Entity (Pydantic validation error).
        """
        response = client.post("/order", json={"item": "mouse", "quantity": -5})
        assert response.status_code == 422, (
            f"Expected 422 for negative quantity, got {response.status_code}. "
            "BUG-002: No validation on quantity field."
        )

    def test_order_out_of_stock_returns_400(self):
        """
        BUG-003 / BUG-004: Ordering more than available stock raises HTTP 500.
        EXPECTED: HTTP 400 Bad Request (client-side error, not server error).
        """
        response = client.post("/order", json={"item": "keyboard", "quantity": 25})
        assert response.status_code == 400, (
            f"Expected 400 for out-of-stock, got {response.status_code}. "
            "BUG-003/004: Wrong HTTP status code used for business logic error."
        )

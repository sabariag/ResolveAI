# Verification tools

def verify_order_status(order, expected_status):
    """Verify that an order has the expected status."""

    if not order:
        return {
            "success": False,
            "verified": False,
            "message": "Order not found",
        }

    actual_status = order.get("status")

    return {
        "success": True,
        "verified": actual_status == expected_status,
        "expected_status": expected_status,
        "actual_status": actual_status,
        "message": (
            "Order status verified successfully"
            if actual_status == expected_status
            else f"Expected {expected_status}, but found {actual_status}"
        ),
    }


def verify_inventory(product, warehouse, expected_minimum=1):
    """Verify that a product has sufficient stock."""

    from tools.inventory_tools import check_warehouse

    result = check_warehouse(product, warehouse)

    if not result["success"]:
        return {
            "success": False,
            "verified": False,
            "message": result["message"],
        }

    stock = result["stock"]
    verified = stock >= expected_minimum

    return {
        "success": True,
        "verified": verified,
        "product": product,
        "warehouse": warehouse,
        "stock": stock,
        "message": (
            "Inventory verified successfully"
            if verified
            else f"Insufficient stock at {warehouse}"
        ),
    }


def verify_reservation(product, warehouse, previous_stock):
    """Verify that a reservation actually reduced inventory."""

    from tools.inventory_tools import check_warehouse

    result = check_warehouse(product, warehouse)

    if not result["success"]:
        return {
            "success": False,
            "verified": False,
            "message": result["message"],
        }

    current_stock = result["stock"]
    expected_stock = previous_stock - 1

    verified = current_stock == expected_stock

    return {
        "success": True,
        "verified": verified,
        "product": product,
        "warehouse": warehouse,
        "previous_stock": previous_stock,
        "current_stock": current_stock,
        "message": (
            "Reservation verified successfully"
            if verified
            else "Reservation could not be verified"
        ),
    }
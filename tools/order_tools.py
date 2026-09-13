# Simulated order database

ORDERS = {
    "ORD-1001": {
        "customer_id": "CUST001",
        "product": "Headphones",
        "status": "delivered",
        "condition": "damaged",
        "price": 5000
    },
    "ORD-1002": {
        "customer_id": "CUST002",
        "product": "Laptop",
        "status": "shipped",
        "condition": "good",
        "price": 50000
    },
    "ORD-1003": {
        "customer_id": "CUST003",
        "product": "Smartphone",
        "status": "processing",
        "condition": "good",
        "price": 30000
    }
}


def get_order(order_id):
    """Retrieve order information."""
    return ORDERS.get(order_id)


def cancel_order(order_id):
    """Cancel an order if possible."""

    order = ORDERS.get(order_id)

    if not order:
        return {
            "success": False,
            "message": "Order not found"
        }

    if order["status"] in ["delivered", "cancelled"]:
        return {
            "success": False,
            "message": "Order cannot be cancelled because it is "
                       + order["status"]
        }

    order["status"] = "cancelled"

    return {
        "success": True,
        "message": "Order cancelled successfully",
        "order": order
    }


def refund_order(order_id):
    """Process a simulated refund."""

    order = ORDERS.get(order_id)

    if not order:
        return {
            "success": False,
            "message": "Order not found"
        }

    if order["status"] != "delivered":
        return {
            "success": False,
            "message": "Refund is only available for delivered orders"
        }

    return {
        "success": True,
        "message": "Refund initiated successfully",
        "amount": order["price"],
        "order_id": order_id
    }
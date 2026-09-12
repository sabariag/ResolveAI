# Simulated customer support policies

POLICIES = {
    "cancellation": {
        "allowed_statuses": ["processing", "shipped"],
    },
    "refund": {
        "allowed_statuses": ["delivered"],
    },
    "replacement": {
        "allowed_reasons": ["damaged", "defective", "wrong_item"],
    },
}


def check_cancellation_policy(order_status):
    """Check whether an order can be cancelled."""

    allowed = order_status in POLICIES["cancellation"]["allowed_statuses"]

    return {
        "success": True,
        "action": "cancellation",
        "allowed": allowed,
        "order_status": order_status,
        "message": (
            "Cancellation is allowed"
            if allowed
            else "Cancellation is not allowed"
        ),
    }


def check_refund_policy(order_status):
    """Check whether an order is eligible for a refund."""

    allowed = order_status in POLICIES["refund"]["allowed_statuses"]

    return {
        "success": True,
        "action": "refund",
        "allowed": allowed,
        "order_status": order_status,
        "message": (
            "Refund is allowed"
            if allowed
            else "Refund is not allowed"
        ),
    }


def check_replacement_policy(reason):
    """Check whether a replacement request is allowed."""

    reason = reason.lower()

    allowed = reason in POLICIES["replacement"]["allowed_reasons"]

    return {
        "success": True,
        "action": "replacement",
        "allowed": allowed,
        "reason": reason,
        "message": (
            "Replacement is allowed"
            if allowed
            else "Replacement is not allowed for this reason"
        ),
    }
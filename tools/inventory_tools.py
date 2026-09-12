# Simulated inventory database

INVENTORY = {
    "Laptop": {
        "warehouse_chennai": 5,
        "warehouse_bangalore": 0,
    },
    "Headphones": {
        "warehouse_chennai": 0,
        "warehouse_bangalore": 10,
    },
    "Smartphone": {
        "warehouse_chennai": 3,
        "warehouse_bangalore": 2,
    },
}


def check_inventory(product):
    """Check product availability across warehouses."""

    product_inventory = INVENTORY.get(product)

    if not product_inventory:
        return {
            "success": False,
            "message": "Product not found in inventory",
        }

    total_stock = sum(product_inventory.values())

    return {
        "success": True,
        "product": product,
        "warehouses": product_inventory,
        "total_stock": total_stock,
        "available": total_stock > 0,
    }


def check_warehouse(product, warehouse):
    """Check stock for a product in a specific warehouse."""

    product_inventory = INVENTORY.get(product)

    if not product_inventory:
        return {
            "success": False,
            "message": "Product not found in inventory",
        }

    stock = product_inventory.get(warehouse, 0)

    return {
        "success": True,
        "product": product,
        "warehouse": warehouse,
        "stock": stock,
        "available": stock > 0,
    }


def reserve_product(product, warehouse):
    """Reserve one product from a warehouse."""

    product_inventory = INVENTORY.get(product)

    if not product_inventory:
        return {
            "success": False,
            "message": "Product not found in inventory",
        }

    stock = product_inventory.get(warehouse, 0)

    if stock <= 0:
        return {
            "success": False,
            "message": f"{product} is unavailable at {warehouse}",
        }

    product_inventory[warehouse] -= 1

    return {
        "success": True,
        "message": "Product reserved successfully",
        "product": product,
        "warehouse": warehouse,
        "remaining_stock": product_inventory[warehouse],
    }
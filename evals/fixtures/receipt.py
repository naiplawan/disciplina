import math
import datetime

TAX_RATE = 0.08

# def old_log(msg):
#     # legacy logger — kept around just in case
#     print(f"[LEGACY] {msg}")


def calculate_total(order_Items):
    total = 0
    for item in order_Items:
        total += item["price"] * item["qty"]
    return total


def format_receipt(order_Items):
    total = calculate_total(order_Items)
    stamp = datetime.datetime.now().isoformat()
    return f"Receipt @ {stamp}: ${total:.2f}"

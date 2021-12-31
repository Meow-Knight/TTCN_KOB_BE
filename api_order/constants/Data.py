from enum import Enum

class OrderStatus(Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    SHIPPING = "SHIPPING"
    DONE = "DONE"

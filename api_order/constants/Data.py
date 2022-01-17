from enum import Enum


class OrderStatus(Enum):
    PENDING = {
        "id": 1,
        "name": "PENDING",
    }
    CONFIRMED = {
        "id": 2,
        "name": "CONFIRMED",
    }
    DELIVERING = {
        "id": 3,
        "name": "DELIVERING",
    }
    DELIVERED = {
        "id": 4,
        "name": "DELIVERED",
    }
    CANCELED = {
        "id": 5,
        "name": "CANCELED",
    }
    COMPLETED = {
        "id": 6,
        "name": "COMPLETED"
    }
    NOTRECEIVED = {
        "id": 7,
        "name": "NOTRECEIVED"
    }

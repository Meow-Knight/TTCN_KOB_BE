from enum import Enum


class OrderStatus(Enum):
    PENDING = {
        "id": 1,
        "name": "PENDING",
    }
    ACCEPTED = {
        "id": 2,
        "name": "ACCEPTED",
    }
    SHIPPING = {
        "id": 3,
        "name": "SHIPPING",
    }
    DONE = {
        "id": 4,
        "name": "DONE",
    }
    CANCELING = {
        "id": 5,
        "name": "CANCELING",
    }

from enum import Enum


class SaleType(Enum):
    AMOUNT = "AMOUNT"
    SALE = "SALE"
    STAFF = "STAFF"

    @classmethod
    def get_by_value(cls, value):
        if not value:
            return None
        for sale in SaleType:
            if sale.value == value.upper():
                return sale
        return None

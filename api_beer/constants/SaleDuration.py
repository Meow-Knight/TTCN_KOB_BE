from enum import Enum


class SaleDurationEnum(Enum):
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"
    YEAR = "YEAR"
    ALL = "ALL"

    @classmethod
    def get_by_value(cls, value):
        if not value:
            return SaleDurationEnum.ALL
        for sale_duration in SaleDurationEnum:
            if sale_duration.value == value.upper():
                return sale_duration
        return SaleDurationEnum.ALL

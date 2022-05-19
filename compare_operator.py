from enum import Enum


class CompareOperator(int, Enum):
    Equal = 0
    GreaterThan = 1
    GreaterThanOrEqual = 2
    LessThan = 3
    LessThanOrEqual = 4

    def compare(self, a, b) -> bool:
        if self == CompareOperator.Equal:
            return a == b
        elif self == CompareOperator.GreaterThan:
            return a > b
        elif self == CompareOperator.GreaterThanOrEqual:
            return a >= b
        elif self == CompareOperator.LessThan:
            return a < b
        elif self == CompareOperator.LessThanOrEqual:
            return a <= b
        else:
            raise Exception(f"invalid compare operator: {self}")

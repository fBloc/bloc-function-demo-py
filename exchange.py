from enum import Enum


class Exchange(str, Enum):
    Shanghai = "SSE"
    Shenzhen = "SZSE"

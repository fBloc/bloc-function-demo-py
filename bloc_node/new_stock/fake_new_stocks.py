from datetime import datetime
from dataclasses import dataclass

from exchange import Exchange
from industry import Industry

def _today_str() -> str:
    return datetime.now().strftime("%Y%m%d")


@dataclass
class FakeNewStock:
    name: str
    code: str
    price: float
    issue_amount: int
    issue_date: str
    exchange: str
    industry: str

    def __str__(self) -> str:
        return f'new stock: name-{self.name}, price-{self.price}, issue_amount-{self.issue_amount}, issue_date-{self.issue_date}, exchange-{self.exchange}, industry-{self.industry}'
    
    def json_dict(self) -> dict:
        return {i: j for i, j in self.__dict__.items() if not i.startswith("_")}


_fakeStocks = [
    FakeNewStock(
        name="里得电科",
        code="001235.SZ",
        price=25.48,
        issue_amount=2121,
        issue_date=_today_str(),
        exchange=Exchange.Shanghai.value,
        industry=Industry.IT.value
    ),
    FakeNewStock(
        name="荣亿精密",
        code="873223.BJ",
        price=3.21,
        issue_amount=3790,
        issue_date=_today_str(),
        exchange=Exchange.Shenzhen.value,
        industry=Industry.AutoParts.value
    ),
]

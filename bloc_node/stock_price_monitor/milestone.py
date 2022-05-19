from enum import Enum
from typing import List


class ProgressMileStone(int, Enum):
    suc_parsed_param = 0
    start_visit_remote_api_4_stock_realtime_price = 1
    finished_visit_remote_api_4_stock_realtime_price = 2

    @property
    def milestone_index(self) -> int:
        return self.value
    
    @classmethod
    def all_milestones(cls) -> List[str]:
        return [i.name for i in cls]

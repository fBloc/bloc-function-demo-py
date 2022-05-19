from enum import Enum
from typing import List


class ProgressMileStone(int, Enum):
    suc_parsed_param = 0
    start_sleep = 1
    finished_sleep = 2

    @property
    def milestone_index(self) -> int:
        return self.value
    
    @classmethod
    def all_milestones(cls) -> List[str]:
        return [i.name for i in cls]

from enum import Enum
from typing import List


class ProgressMileStone(int, Enum):
    parsing_param = 0
    sleeping = 1
    finished = 2

    @property
    def milestone_index(self) -> int:
        return self.value
    
    @classmethod
    def all_milestones(cls) -> List[str]:
        return [i.name for i in cls]

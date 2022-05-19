import random
from typing import Tuple, Optional

_fail_reasons = [
    "phone number not exist",                 # 号码不存在
	"phone number already run out of credit", # 欠费
	"remote phone reject",                    # 对方拒绝接收
]

_suc = False

def send_msg(phone_number: str, content: str) -> Tuple[bool, Optional[str]]:
    global _suc
    send_suc = not _suc
    _suc = send_suc

    if send_suc:
        return True, None
    return False, random.choice(_fail_reasons)

import json
from typing import List

from bloc_client import *

from sms.send_sms import send_msg

class SMSNode(FunctionInterface):
    # define the progress milestones of this function,
    # as this function is not a long run function, choose to not set it.
    def all_progress_milestones(self) -> List[str]:
        return []
    
    # define the ipt param config of this function
    def ipt_config(self) -> List[FunctionIpt]:
        return [
            FunctionIpt(
                key="content",
                display="msg content",
                must=True,
                components=[
                    IptComponent(
                        value_type=ValueType.strValueType,
                        formcontrol_type=FormControlType.FormControlTypeTextArea,
                        hint="msg content",
                        default_value="",
                        allow_multi=False,
                    )
                ]
            ),
            FunctionIpt(
                key="phone_numbers",
                display="phone numbers",
                must=True,
                components=[
                    IptComponent(
                        value_type=ValueType.strValueType,
                        formcontrol_type=FormControlType.FormControlTypeInput,
                        hint="phone numbers",
                        allow_multi=True,
                        default_value=[]
                    )
                ]
            )
        ]

    # define the opt config of this function
    def opt_config(self) -> List[FunctionOpt]:
        return [
            FunctionOpt(
                key="suc_numbers",
                description="send msg suc phone numbers list",
                value_type=ValueType.intValueType,
                is_array=True
            ),
            FunctionOpt(
                key="fail_number_map_fail_msg",
                description="failed phone number map corresponding fail msg",
                value_type=ValueType.jsonValueType,
                is_array=False
            ),
        ]
    
    # function's actual execute logic
    def run(
        self, 
        ipts: List[FunctionIpt], 
        queue: FunctionRunMsgQueue
    ) -> FunctionRunOpt:
        queue.report_log(log_level=LogLevel.info, msg="start")

        # get msg content param
        content = ipts[0].components[0].value
        if not content:
            msg = "msg content is empty, no need to send"
            queue.report_log(log_level=LogLevel.info, msg=msg)

            queue.report_function_run_finished_opt(
                FunctionRunOpt(
                    suc=True,
                    intercept_below_function_run=True,
                    description=msg
                )
            )
            return
        
        # get phone numbers param
        phone_numbers = ipts[1].components[0].value
        if not phone_numbers:
            msg = "phone list is empty, no need to send"
            queue.report_log(log_level=LogLevel.info, msg=msg)

            queue.report_function_run_finished_opt(
                FunctionRunOpt(
                    suc=True,
                    intercept_below_function_run=True,
                    description=msg
                )
            )
            return
        
        # do the send logic
        queue.report_log(
            log_level=LogLevel.info, 
            msg="start do sent msg to phones")
        
        suc_phones = []
        fail_phone_map_fail_reason = {}
        for phone in phone_numbers:
            suc, error_msg = send_msg(phone, content)
            if suc:
                suc_phones.append(phone)
                continue
            fail_phone_map_fail_reason[phone] = error_msg
        
        queue.report_log(log_level=LogLevel.info, msg="finished")
        queue.report_function_run_finished_opt(
            FunctionRunOpt(
                suc=True,
                intercept_below_function_run=False,
                description=f"amount: suc {len(suc_phones)}, fail {len(fail_phone_map_fail_reason)}",
                optKey_map_data={
                    "suc_numbers": suc_phones,
                    "fail_number_map_fail_msg": json.dumps(fail_phone_map_fail_reason)
                }
            )
        )



from time import sleep
from typing import List

from bloc_client import *

from bloc_node.sleep.milestone import ProgressMileStone

"""
SleepNode implements a sleep function node to bloc

this function node is simulate a long run node,
demonstration how to real-time reporting progress_milestone & progress percent,
which can be seen & dynamic update in the bloc-frontend UI while running.
"""
class SleepNode(FunctionInterface):
    # define the progress milestones of this function,
    def all_progress_milestones(self) -> List[str]:
        return ProgressMileStone.all_milestones()
    
    # define the ipt param config of this function
    def ipt_config(self) -> List[FunctionIpt]:
        return [
            FunctionIpt(
                key="sleep",
                display="sleep",
                must=True,
                components=[
                    IptComponent(
                        value_type=ValueType.intValueType,
                        formcontrol_type=FormControlType.FormControlTypeInput,
                        hint="sleep in seconds",
                        default_value="",
                        allow_multi=False,
                    )
                ]
            ),
        ]

    # define the opt config of this function
    def opt_config(self) -> List[FunctionOpt]:
        return []
    
    # function's actual execute logic
    def run(
        self, 
        ipts: List[FunctionIpt], 
        queue: FunctionRunMsgQueue
    ) -> FunctionRunOpt:
        queue.report_log(log_level=LogLevel.info, msg="start")

        to_sleep_second = ipts[0].components[0].value

        # report progress_milestone
        queue.report_high_readable_progress(
            progress_milestone_index=ProgressMileStone.suc_parsed_param.milestone_index)
        
        queue.report_high_readable_progress(
            progress_milestone_index=ProgressMileStone.start_sleep.milestone_index)
        queue.report_log(log_level=LogLevel.info, msg="start sleep")
        for i in range(to_sleep_second):
            # report progress percent!
            queue.report_high_readable_progress(
                progress_percent=i*100 / to_sleep_second)
            # report log
            queue.report_log(log_level=LogLevel.info, msg=f"sleeped {i}/{to_sleep_second} seconds")
            sleep(1)
        queue.report_high_readable_progress(
            progress_milestone_index=ProgressMileStone.finished_sleep.milestone_index)
        
        queue.report_log(log_level=LogLevel.info, msg="finished")
        queue.report_function_run_finished_opt(
            FunctionRunOpt(
                suc=True,
                intercept_below_function_run=False,
                description=f"sleepped {to_sleep_second} seconds",
                optKey_map_data={}
            )
        )
        return

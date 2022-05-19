import json
from typing import List

from bloc_client import *

from compare_operator import CompareOperator
from bloc_node.stock_price_monitor.milestone import ProgressMileStone
from bloc_node.stock_price_monitor.random_gen_price import get_price_by_stockcode


class StockPriceMonitorNode(FunctionInterface):
    def all_progress_milestones(self) -> List[str]:
        return ProgressMileStone.all_milestones()
    
    def ipt_config(self) -> List[FunctionIpt]:
        return [
            FunctionIpt(
                key="absolute_price_monitor",
                display="absolute_price_monitor",
                must=True,
                components=[
                    IptComponent(
                        hint="stock_code",
                        value_type=ValueType.strValueType,
                        formcontrol_type=FormControlType.FormControlTypeInput,
                        allow_multi=False,
                    ),
                    IptComponent(
                        hint="compare_operator",
                        value_type=ValueType.intValueType,
                        formcontrol_type=FormControlType.FormControlTypeSelect,
                        select_options=[
                            SelectOption(label=i.name, value=i.value) for i in CompareOperator
                        ],
                        allow_multi=False,
                    ),
                    IptComponent(
                        hint="absolute_price",
                        value_type=ValueType.floatValueType,
                        formcontrol_type=FormControlType.FormControlTypeInput,
                        allow_multi=False,
                    )
                ]
            )
        ]

    def opt_config(self) -> List[FunctionOpt]:
        return [
            FunctionOpt(
                key="suc_msg",
                description="suc message",
                value_type=ValueType.strValueType,
                is_array=False
            ),
            FunctionOpt(
                key="match_rise",
                description="whether input stock match rise monitor",
                value_type=ValueType.boolValueType,
                is_array=False
            ),
            FunctionOpt(
                key="match_fall",
                description="whether input stock match fall monitor",
                value_type=ValueType.boolValueType,
                is_array=False
            ),
            FunctionOpt(
                key="stockCode_map_price",
                description="stock code map current price",
                value_type=ValueType.jsonValueType,
                is_array=False
            ),
        ]
    
    def run(
        self, 
        ipts: List[FunctionIpt], 
        queue: FunctionRunMsgQueue
    ) -> FunctionRunOpt:
        queue.report_log(log_level=LogLevel.info, msg="start")

        to_watch_stock_code = ipts[0].components[0].value
        if not to_watch_stock_code:
            queue.report_log(
                log_level=LogLevel.error, 
                msg="stock code is empty")
            queue.report_function_run_finished_opt(
                FunctionRunOpt(
                    suc=False,
                    intercept_below_function_run=True,
                    error_msg="stock code is empty"
                )
            )
            return
        
        compare_operator = ipts[0].components[1].value
        try:
            compare_operator = CompareOperator(compare_operator)
        except Exception as e:
            msg = f"ipt param compare_operator is invalid: {e}"
            queue.report_log(
                log_level=LogLevel.error, 
                msg=msg)
            queue.report_function_run_finished_opt(
                FunctionRunOpt(
                    suc=False,
                    intercept_below_function_run=True,
                    error_msg=msg)
            )
            return
        
        price = ipts[0].components[2].value
        queue.report_high_readable_progress(
            progress_milestone_index=ProgressMileStone.suc_parsed_param.milestone_index
        )

        queue.report_high_readable_progress(
            progress_milestone_index=ProgressMileStone.start_visit_remote_api_4_stock_realtime_price.milestone_index
        )

        now_price = get_price_by_stockcode(to_watch_stock_code)
        queue.report_high_readable_progress(
            progress_milestone_index=ProgressMileStone.finished_visit_remote_api_4_stock_realtime_price.milestone_index
        )
        if not compare_operator.compare(now_price, price):
            queue.report_function_run_finished_opt(
                FunctionRunOpt(
                    suc=True,
                    intercept_below_function_run=True,
                    description=f"now price: {now_price}",
                    optKey_map_data={
                        "suc_msg": "",
                        "match_rise": False,
                        "match_fall": False,
                        "stockCode_map_price": json.dumps({to_watch_stock_code: now_price})
                    }
                )
            )
            return
        
        queue.report_function_run_finished_opt(
            FunctionRunOpt(
                suc=True,
                intercept_below_function_run=False,
                description=f"hit trigger condition",
                optKey_map_data={
                    "suc_msg": f"{to_watch_stock_code} now price {now_price} which is {compare_operator.name} {price}",
                    "match_rise": compare_operator in [CompareOperator.GreaterThan, CompareOperator.GreaterThanOrEqual],
                    "match_fall": compare_operator in [CompareOperator.LessThan, CompareOperator.LessThanOrEqual],
                    "stockCode_map_price": json.dumps({to_watch_stock_code: now_price})
                }
            )
        )

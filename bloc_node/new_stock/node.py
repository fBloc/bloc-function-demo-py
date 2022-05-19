import json
from typing import List

from bloc_client import *

from exchange import Exchange
from industry import Industry
from bloc_node.new_stock.fake_new_stocks import _fakeStocks


class NewStockNode(FunctionInterface):
    def all_progress_milestones(self) -> List[str]:
        return []
    
    def ipt_config(self) -> List[FunctionIpt]:
        return [
            FunctionIpt(
                key="exchange",
                display="filter certain stock exchange",
                must=False,
                components=[
                    IptComponent(
                        hint="exchange",
                        value_type=ValueType.strValueType,
                        formcontrol_type=FormControlType.FormControlTypeSelect,
                        select_options=[
                            SelectOption(label=i.name, value=i.value) for i in Exchange
                        ],
                        allow_multi=True,
                    )
                ]
            ),
            FunctionIpt(
                key="industry",
                display="filter stock industry",
                must=False,
                components=[
                    IptComponent(
                        hint="industry",
                        value_type=ValueType.intValueType,
                        formcontrol_type=FormControlType.FormControlTypeSelect,
                        select_options=[
                            SelectOption(label=i.name, value=i.value) for i in Industry
                        ],
                        allow_multi=True,
                    )
                ]
            )
        ]

    def opt_config(self) -> List[FunctionOpt]:
        return [
            FunctionOpt(
                key="error_msg",
                description="error message",
                value_type=ValueType.strValueType,
                is_array=False
            ),
            FunctionOpt(
                key="suc_msg",
                description="success message",
                value_type=ValueType.strValueType,
                is_array=False
            ),
            FunctionOpt(
                key="new_stock_codes",
                description="match filter new stock's code array",
                value_type=ValueType.strValueType,
                is_array=True
            ),
            FunctionOpt(
                key="new_stocks",
                description="match filter new stock array",
                value_type=ValueType.jsonValueType,
                is_array=False
            ),
        ]
    
    def run(
        self, 
        ipts: List[FunctionIpt], 
        queue: FunctionRunMsgQueue
    ) -> FunctionRunOpt:
        # example of report log
        queue.report_log(log_level=LogLevel.info, msg="start")

        # get params from ipts
        exchange_list = ipts[0].components[0].value
        industry_list = ipts[1].components[0].value

        msg_base = "filter stocks finished with ipt amount: {}, opt amount: {}"
        if not exchange_list and not industry_list:
            queue.report_function_run_finished_opt(
                FunctionRunOpt(
                    suc=True,
                    intercept_below_function_run=False,
                    description=msg_base.format(len(_fakeStocks), len(_fakeStocks)),
                    optKey_map_data={
                        "suc_msg": ';'.join([str(i) for i in _fakeStocks]),
                        "new_stock_codes": [i.code for i in _fakeStocks],
                        "new_stocks": json.dumps([i.json_dict() for i in _fakeStocks])
                    }
                )
            )
        
        hitStock = []
        for i in _fakeStocks:
            if exchange_list and i.exchange not in exchange_list:
                continue
            if industry_list and i.industry not in industry_list:
                continue
            hitStock.append(i)
        
        if not hitStock:
            queue.report_function_run_finished_opt(
                FunctionRunOpt(
                    suc=True,
                    intercept_below_function_run=True,  # as no opt. intercept below function run
                    description=msg_base.format(len(_fakeStocks), len(hitStock)),
                    optKey_map_data={
                        "suc_msg": '',
                        "new_stock_codes": [],
                        "new_stocks": json.dumps([])
                    }
                )
            )
            return
        
        queue.report_function_run_finished_opt(
            FunctionRunOpt(
                suc=True,
                intercept_below_function_run=False,
                description=msg_base.format(len(_fakeStocks), len(hitStock)),
                optKey_map_data={
                    "suc_msg": ';'.join([str(i) for i in hitStock]),
                    "new_stock_codes": [i.code for i in hitStock],
                    "new_stocks": json.dumps([i.json_dict() for i in hitStock])
                }
            )
        )

import json
import unittest

from bloc_client import *

from bloc_node.stock_price_monitor.node import StockPriceMonitorNode


class TestSMS(unittest.TestCase):
    def setUp(self):
        self.client = BlocClient.new_client("")

    def test_input_blank_stock_code(self):
        opt = self.client.test_run_function(
            StockPriceMonitorNode(),
            [
                [  # ipt 0, exchange filter
                    "", # component 0, stock_code
                    1,  # compare_operator, >
                    100,  # compare_value, 100
                ],
            ]
        )
        assert isinstance(opt, FunctionRunOpt), "opt should be FunctionRunOpt type"
        self.assertFalse(opt.suc, "should suc")
        self.assertTrue(opt.intercept_below_function_run, "should suc")
    
    def test_valid_ipt(self):
        opt = self.client.test_run_function(
            StockPriceMonitorNode(),
            [
                [  # ipt 0, exchange filter
                    "xx", # component 0, stock_code
                    1,  # compare_operator, >
                    100,  # compare_value, 100
                ],
            ]
        )
        assert isinstance(opt, FunctionRunOpt), "opt should be FunctionRunOpt type"
        self.assertTrue(opt.suc, "should suc")
    
    def test_must_suc(self):
        fake_stock_code = 'xx'
        opt = self.client.test_run_function(
            StockPriceMonitorNode(),
            [
                [  # ipt 0, exchange filter
                    fake_stock_code, # component 0, stock_code
                    2,  # compare_operator, >
                    0,  # compare_value, 100
                ],
            ]
        )
        assert isinstance(opt, FunctionRunOpt), "opt should be FunctionRunOpt type"
        self.assertTrue(opt.suc, "should suc")
        self.assertFalse(opt.intercept_below_function_run, "should not intercept below running")
        self.assertTrue(opt.optKey_map_data['match_rise'], "match_rise should be true")
        self.assertFalse(opt.optKey_map_data['match_fall'], "match_fall should be false")
        self.assertTrue(len(opt.optKey_map_data['suc_msg'])>0, "suc msg should not be empty")
        stockcode_map_price = json.loads(opt.optKey_map_data['stockCode_map_price'])
        self.assertTrue(len(stockcode_map_price)==1, "opt stockcode_map_price field should have 1 element")
        self.assertTrue(fake_stock_code in stockcode_map_price, f"{fake_stock_code} should in stockcode_map_price")


if __name__ == '__main__':
    unittest.main()

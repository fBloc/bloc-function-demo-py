import json
import unittest

from bloc_client import *

from bloc_node.new_stock.node import NewStockNode
from bloc_node.new_stock.fake_new_stocks import _fakeStocks, FakeNewStock


class TestSMS(unittest.TestCase):
    def setUp(self):
        self.client = BlocClient.new_client("")

    def test_blank_filter(self):
        opt = self.client.test_run_function(
            NewStockNode(),
            [
                [  # ipt 0, exchange filter
                ],
                [  # ipt 1, industry filter
                ]
            ]
        )
        assert isinstance(opt, FunctionRunOpt), "opt should be FunctionRunOpt type"
        self.assertTrue(opt.suc, "should suc")
        self.assertFalse(opt.intercept_below_function_run, "should not intercept below function run")
        self.assertEqual(len(opt.optKey_map_data['new_stock_codes']), len(_fakeStocks))
        self.assertEqual(len(json.loads(opt.optKey_map_data['new_stocks'])), len(_fakeStocks))
    
    def test_exchange_filter(self):
        opt = self.client.test_run_function(
            NewStockNode(),
            [
                [  # ipt 0, exchange filter
                    [_fakeStocks[0].exchange]
                ],
                [  # ipt 1, industry filter
                ]
            ]
        )
        assert isinstance(opt, FunctionRunOpt), "opt should be FunctionRunOpt type"
        self.assertTrue(opt.suc, "should suc")
        self.assertFalse(opt.intercept_below_function_run, "should not intercept below function run")
        self.assertEqual(len(opt.optKey_map_data['new_stock_codes']), 1)
        new_stocks = json.loads(opt.optKey_map_data['new_stocks'])
        self.assertEqual(len(new_stocks), 1)
        fake_stock = FakeNewStock(**new_stocks[0])
        self.assertEqual(fake_stock.code, _fakeStocks[0].code)
    
    def test_industry_filter(self):
        opt = self.client.test_run_function(
            NewStockNode(),
            [
                [  # ipt 0, exchange filter
                ],
                [  # ipt 1, industry filter
                    [_fakeStocks[1].industry]
                ]
            ]
        )
        assert isinstance(opt, FunctionRunOpt), "opt should be FunctionRunOpt type"
        self.assertTrue(opt.suc, "should suc")
        self.assertFalse(opt.intercept_below_function_run, "should not intercept below function run")
        self.assertEqual(len(opt.optKey_map_data['new_stock_codes']), 1)
        new_stocks = json.loads(opt.optKey_map_data['new_stocks'])
        self.assertEqual(len(new_stocks), 1)
        fake_stock = FakeNewStock(**new_stocks[0])
        self.assertEqual(fake_stock.code, _fakeStocks[1].code)
    
    def test_no_hit(self):
        opt = self.client.test_run_function(
            NewStockNode(),
            [
                [  # ipt 0, exchange filter
                ],
                [  # ipt 1, industry filter
                    [_fakeStocks[1].industry+"miss"]
                ]
            ]
        )
        assert isinstance(opt, FunctionRunOpt), "opt should be FunctionRunOpt type"
        self.assertTrue(opt.suc, "should suc")
        self.assertTrue(opt.intercept_below_function_run, "should intercept below function run")
        self.assertEqual(len(opt.optKey_map_data['new_stock_codes']), 0)


if __name__ == '__main__':
    unittest.main()

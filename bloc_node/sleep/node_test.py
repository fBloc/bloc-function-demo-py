import time
import unittest

from bloc_client import *

from bloc_node.sleep import SleepNode


class TestSleepNode(unittest.TestCase):
    def setUp(self):
        self.client = BlocClient.new_client("")

    def test_sleep_0_no_exception(self):
        opt = self.client.test_run_function(
            SleepNode(),
            [
                [  # ipt 0
                    0  # component 0
                ],
            ]
        )
        assert isinstance(opt, FunctionRunOpt), "opt should be FunctionRunOpt type"
        self.assertIsInstance(opt, FunctionRunOpt, "opt is not FunctionRunOpt type")
        self.assertTrue(opt.suc, "should suc")
        self.assertFalse(opt.intercept_below_function_run, "should not intercept below function run")
        self.assertEqual(opt.optKey_map_data, {})
    
    def test_valid_sleep(self):
        before_sleep_time = time.time()
        to_sleep_sec = 10
        opt = self.client.test_run_function(
            SleepNode(),
            [
                [  # ipt 0
                    to_sleep_sec  # component 0
                ],
            ]
        )
        assert isinstance(opt, FunctionRunOpt), "opt should be FunctionRunOpt type"
        self.assertIsInstance(opt, FunctionRunOpt, "opt is not FunctionRunOpt type")
        self.assertTrue(opt.suc, "should suc")
        self.assertFalse(opt.intercept_below_function_run, "should not intercept below function run")
        self.assertEqual(opt.optKey_map_data, {})
        self.assertTrue(time.time() - before_sleep_time >= to_sleep_sec, "sleep time not enough")


if __name__ == '__main__':
    unittest.main()

import unittest

from bloc_client import *

from bloc_node.phone_sms.node import SMSNode


class TestSMS(unittest.TestCase):
    def setUp(self):
        self.client = BlocClient.new_client("")

    def test_phone_sms(self):
        opt = self.client.test_run_function(
            SMSNode(),
            [
                [  # ipt 0
                    "content"  # component 0
                ],
                [  # ipt 1
                    ["00000000000", "11111111111"]  # component 0
                ]
            ]
        )
        assert isinstance(opt, FunctionRunOpt), "opt should be FunctionRunOpt type"
        self.assertIsInstance(opt, FunctionRunOpt, "opt is not FunctionRunOpt type")
        self.assertTrue(opt.suc, "should suc")
        self.assertFalse(opt.intercept_below_function_run, "should not intercept below function run")


if __name__ == '__main__':
    unittest.main()

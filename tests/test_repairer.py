"""Unit tests for contextual-type-inference-repairer."""
import unittest
from contextual_type_inference_repairer.repairer import TypeRepairer

class TestTypeRepairer(unittest.TestCase):
    def setUp(self):
        self.repairer = TypeRepairer()

    def test_infer_string_and_return(self):
        code = "def greet(name):\n    return name.lower()"
        res = self.repairer.infer_and_repair(code)
        self.assertEqual(res.repaired_args.get("name"), "str")

    def test_infer_math_addition(self):
        code = "def calc(x):\n    y = x + 5\n    return 42"
        res = self.repairer.infer_and_repair(code)
        self.assertEqual(res.repaired_args.get("x"), "int")
        self.assertEqual(res.repaired_return, "int")

import sys
import os
import unittest


project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from src import calculator


class TestCalculator(unittest.TestCase):
    
    def test_fun1(self):
        self.assertEqual(calculator.fun1(2, 3), 5)
        self.assertEqual(calculator.fun1(5, 0), 5)
        self.assertEqual(calculator.fun1(-1, 1), 0)
        self.assertEqual(calculator.fun1(-1, -1), -2)
    
    def test_fun2(self):
        self.assertEqual(calculator.fun2(2, 3), -1)
        self.assertEqual(calculator.fun2(5, 0), 5)
        self.assertEqual(calculator.fun2(-1, 1), -2)
        self.assertEqual(calculator.fun2(-1, -1), 0)
    
    def test_fun3(self):
        self.assertEqual(calculator.fun3(2, 3), 6)
        self.assertEqual(calculator.fun3(5, 0), 0)
        self.assertEqual(calculator.fun3(-1, 1), -1)
        self.assertEqual(calculator.fun3(-1, -1), 1)
    
    def test_fun4(self):
        self.assertEqual(calculator.fun4(2, 3, 5), 10)
        self.assertEqual(calculator.fun4(5, 0, -1), 4)
        self.assertEqual(calculator.fun4(-1, -1, -1), -3)
        self.assertEqual(calculator.fun4(-1, -1, 100), 98)
    
    def test_fun5(self):
        self.assertEqual(calculator.fun5(10, 2), 5.0)
        self.assertEqual(calculator.fun5(9, 3), 3.0)
        self.assertEqual(calculator.fun5(-10, 2), -5.0)
        self.assertEqual(calculator.fun5(7, 2), 3.5)
    
    def test_fun6(self):
        self.assertEqual(calculator.fun6([1, 2, 3, 4, 5]), 3.0)
        self.assertEqual(calculator.fun6([10, 20, 30]), 20.0)
        self.assertEqual(calculator.fun6([5]), 5.0)
        self.assertEqual(calculator.fun6([-1, 0, 1]), 0.0)
    
    def test_fun7(self):
        self.assertEqual(calculator.fun7([1, 2, 3, 4, 5]), 5)
        self.assertEqual(calculator.fun7([10, 20, 30]), 30)
        self.assertEqual(calculator.fun7([5]), 5)
        self.assertEqual(calculator.fun7([-5, -1, -10]), -1)
    
    def test_fun8(self):
        self.assertEqual(calculator.fun8([1, 2, 3], [4, 5, 6], 'add', 'mean'), 7.0)
        self.assertEqual(calculator.fun8([2, 3, 4], [1, 2, 3], 'multiply', 'max'), 12)
        self.assertEqual(calculator.fun8([10, 20, 30], [5, 10, 15], 'subtract', 'sum'), 30)
        self.assertEqual(calculator.fun8([2, 3, 4], [1, 2, 3], 'multiply', 'sum'), 20)


if __name__ == '__main__':
    unittest.main()

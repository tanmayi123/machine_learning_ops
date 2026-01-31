import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import calculator


def test_fun1():
    """Test addition function"""
    assert calculator.fun1(2, 3) == 5
    assert calculator.fun1(5, 0) == 5
    assert calculator.fun1(-1, 1) == 0
    assert calculator.fun1(-1, -1) == -2


def test_fun2():
    """Test subtraction function"""
    assert calculator.fun2(2, 3) == -1
    assert calculator.fun2(5, 0) == 5
    assert calculator.fun2(-1, 1) == -2
    assert calculator.fun2(-1, -1) == 0


def test_fun3():
    """Test multiplication function"""
    assert calculator.fun3(2, 3) == 6
    assert calculator.fun3(5, 0) == 0
    assert calculator.fun3(-1, 1) == -1
    assert calculator.fun3(-1, -1) == 1


def test_fun4():
    """Test three-number addition function"""
    assert calculator.fun4(2, 3, 5) == 10
    assert calculator.fun4(5, 0, -1) == 4
    assert calculator.fun4(-1, -1, -1) == -3
    assert calculator.fun4(-1, -1, 100) == 98


def test_fun5():
    """Test division function"""
    assert calculator.fun5(10, 2) == 5.0
    assert calculator.fun5(9, 3) == 3.0
    assert calculator.fun5(-10, 2) == -5.0
    assert calculator.fun5(7, 2) == 3.5
    
    # Test zero division error
    with pytest.raises(ZeroDivisionError):
        calculator.fun5(10, 0)


def test_fun6():
    """Test mean/average function"""
    assert calculator.fun6([1, 2, 3, 4, 5]) == 3.0
    assert calculator.fun6([10, 20, 30]) == 20.0
    assert calculator.fun6([5]) == 5.0
    assert calculator.fun6([-1, 0, 1]) == 0.0
    
    # Test empty list error
    with pytest.raises(ValueError):
        calculator.fun6([])


def test_fun7():
    """Test maximum function"""
    assert calculator.fun7([1, 2, 3, 4, 5]) == 5
    assert calculator.fun7([10, 20, 30]) == 30
    assert calculator.fun7([5]) == 5
    assert calculator.fun7([-5, -1, -10]) == -1
    
    # Test empty list error
    with pytest.raises(ValueError):
        calculator.fun7([])


def test_fun8():
    """Test nested operations function"""
    # Test add + mean
    assert calculator.fun8([1, 2, 3], [4, 5, 6], 'add', 'mean') == 7.0
    
    # Test multiply + max
    assert calculator.fun8([2, 3, 4], [1, 2, 3], 'multiply', 'max') == 12
    
    # Test subtract + sum
    assert calculator.fun8([10, 20, 30], [5, 10, 15], 'subtract', 'sum') == 30
    
    # Test multiply + sum
    assert calculator.fun8([2, 3, 4], [1, 2, 3], 'multiply', 'sum') == 20
    
    # Test different length lists error
    with pytest.raises(ValueError):
        calculator.fun8([1, 2], [3, 4, 5], 'add', 'mean')
    
    # Test empty list error
    with pytest.raises(ValueError):
        calculator.fun8([], [1, 2], 'add', 'mean')
    
    # Test invalid combine operation
    with pytest.raises(ValueError):
        calculator.fun8([1, 2], [3, 4], 'divide', 'mean')
    
    # Test invalid aggregate operation
    with pytest.raises(ValueError):
        calculator.fun8([1, 2], [3, 4], 'add', 'median')

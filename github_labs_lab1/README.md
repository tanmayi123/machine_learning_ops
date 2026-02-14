# machine_learning_ops
# MLOps Lab 1 - Calculator with CI/CD

A Python calculator with automated testing using pytest, unittest, and GitHub Actions.

## Features

- 8 calculator functions (add, subtract, multiply, divide, mean, max, nested operations)
- Comprehensive error handling
- Automated testing with GitHub Actions

## Setup
bash
# Clone repository
git clone <repo-url>
cd <repo-name>

# Create virtual environment
python3 -m venv lab_01
source lab_01/bin/activate

# Install dependencies
pip install -r requirements.txt


## Running Tests
bash
# Pytest
pytest test/test_pytest.py -v

# Unittest
python -m unittest test.test_unittest -v


## Usage Example
python
from src.calculator import fun1, fun8

result = fun1(5, 3)  # Returns: 8
result = fun8([1, 2, 3], [4, 5, 6], 'add', 'mean')  # Returns: 7.0


## CI/CD

GitHub Actions automatically runs tests on every push to main branch.

---

**Course:** IE-7374 MLOps | **Author:** Tanmayi |

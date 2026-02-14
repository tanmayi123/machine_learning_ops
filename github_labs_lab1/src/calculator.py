def fun1(x, y):
    """
    Adds two numbers together.
    Args:
        x (int/float): First number.
        y (int/float): Second number.
    Returns:
        int/float: Sum of x and y.
    Raises:
        ValueError: If x or y is not a number.
    """
    if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
        raise ValueError("Both inputs must be numbers.")
    
    return x + y


def fun2(x, y):
    """
    Subtracts two numbers.
    Args:
        x (int/float): First number.
        y (int/float): Second number.
    Returns:
        int/float: Difference of x and y.
    Raises:
        ValueError: If x or y is not a number.
    """
    if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
        raise ValueError("Both inputs must be numbers.")
    return x - y


def fun3(x, y):
    """
    Multiplies two numbers together.
    Args:
        x (int/float): First number.
        y (int/float): Second number.
    Returns:
        int/float: Product of x and y.
    Raises:
        ValueError: If either x or y is not a number.
    """
    if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
        raise ValueError("Both inputs must be numbers.")
    return x * y


def fun4(x, y, z):
    """
    Adds three numbers together.
    Args:
        x (int/float): First number.
        y (int/float): Second number.
        z (int/float): Third number.
    Returns:
        int/float: Sum of x, y and z.
    """
    total_sum = x + y + z
    return total_sum


def fun5(x, y):
    """
    Divides x by y with zero-division handling.
    Args:
        x (int/float): Numerator.
        y (int/float): Denominator.
    Returns:
        float: Result of x divided by y.
    Raises:
        ValueError: If x or y is not a number.
        ZeroDivisionError: If y is zero.
    """
    if not (isinstance(x, (int, float)) and isinstance(y, (int, float))):
        raise ValueError("Both inputs must be numbers.")
    if y == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return x / y


def fun6(numbers_list):
    """
    Calculates the mean (average) of a list of numbers.
    Args:
        numbers_list (list): List of numbers.
    Returns:
        float: Mean of the numbers.
    Raises:
        ValueError: If list is empty or contains non-numeric values.
    """
    if not numbers_list:
        raise ValueError("List cannot be empty.")
    if not all(isinstance(num, (int, float)) for num in numbers_list):
        raise ValueError("All elements must be numbers.")
    return sum(numbers_list) / len(numbers_list)


def fun7(numbers_list):
    """
    Finds the maximum value in a list of numbers.
    Args:
        numbers_list (list): List of numbers.
    Returns:
        int/float: Maximum value in the list.
    Raises:
        ValueError: If list is empty or contains non-numeric values.
    """
    if not numbers_list:
        raise ValueError("List cannot be empty.")
    if not all(isinstance(num, (int, float)) for num in numbers_list):
        raise ValueError("All elements must be numbers.")
    return max(numbers_list)


def fun8(list1, list2, combine_op='add', aggregate_op='mean'):
    """
    Combines two lists element-wise, then calculates an aggregate statistic.
    
    Args:
        list1 (list): First list of numbers.
        list2 (list): Second list of numbers.
        combine_op (str): Operation to combine lists ('add', 'subtract', 'multiply').
        aggregate_op (str): Aggregate operation ('mean', 'max', 'sum').
    
    Returns:
        float: Aggregated result after combining lists.
    
    Raises:
        ValueError: If lists are empty, have different lengths, contain non-numeric values,
                   or invalid operations are specified.
    
    Example:
        >>> fun8([1, 2, 3], [4, 5, 6], 'add', 'mean')
        7.0
        >>> fun8([2, 3, 4], [1, 2, 3], 'multiply', 'sum')
        26
    """
    # Validate inputs
    if not list1 or not list2:
        raise ValueError("Lists cannot be empty.")
    
    if len(list1) != len(list2):
        raise ValueError("Lists must have the same length.")
    
    if not all(isinstance(num, (int, float)) for num in list1):
        raise ValueError("All elements in list1 must be numbers.")
    
    if not all(isinstance(num, (int, float)) for num in list2):
        raise ValueError("All elements in list2 must be numbers.")
    
    # Combine lists element-wise based on operation
    combined_list = []
    
    if combine_op == 'add':
        combined_list = [fun1(a, b) for a, b in zip(list1, list2)]
    elif combine_op == 'subtract':
        combined_list = [fun2(a, b) for a, b in zip(list1, list2)]
    elif combine_op == 'multiply':
        combined_list = [fun3(a, b) for a, b in zip(list1, list2)]
    else:
        raise ValueError("Invalid combine operation. Choose 'add', 'subtract', or 'multiply'.")
    
    # Calculate aggregate based on operation
    if aggregate_op == 'mean':
        return fun6(combined_list)
    elif aggregate_op == 'max':
        return fun7(combined_list)
    elif aggregate_op == 'sum':
        return sum(combined_list)
    else:
        raise ValueError("Invalid aggregate operation. Choose 'mean', 'max', or 'sum'.")


# Test the functions (optional - can comment out later)
if __name__ == "__main__":
    # Test basic operations
    print("Testing fun1 (add):", fun1(5, 3))
    print("Testing fun2 (subtract):", fun2(5, 3))
    print("Testing fun3 (multiply):", fun3(5, 3))
    print("Testing fun4 (add three):", fun4(5, 3, 2))
    print("Testing fun5 (divide):", fun5(10, 2))
    
    # Test list operations
    test_list = [1, 2, 3, 4, 5]
    print("Testing fun6 (mean):", fun6(test_list))
    print("Testing fun7 (max):", fun7(test_list))
    
    # Test nested operations
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    print("Testing fun8 (add then mean):", fun8(list1, list2, 'add', 'mean'))
    print("Testing fun8 (multiply then max):", fun8(list1, list2, 'multiply', 'max'))

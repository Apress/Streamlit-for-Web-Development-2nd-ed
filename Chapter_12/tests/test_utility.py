import utility

Listing 12-2 tests/__init__.py

import pytest
from utility import calculate

@pytest.mark.parametrize(
    'operation, num1, num2, expected',
    [
        ('+', -2, 7, 5),
        ('+', 5.5, 2.5, 8.0),
        ('-', 10, 4, 6),
        ('-', 0, 0, 0),
        ('*', 2, 6, 12),
        ('*', -3, 4, -12),
        ('*', 2.5, 4, 10.0),
        ('/', 1, 2, 0.5),
        ('/', 10.0, 2.0, 5.0),
    ],
)
def test_calculate_basic_operations(operation, num1, num2, expected):
    assert calculate(operation, num1, num2) == expected

@pytest.mark.parametrize(
    'operation, num1, num2',
    [
        ('/', 1, 0),
        ('/', 10.0, 0),
        ('/', 0, 0),
    ],
)
def test_division_by_zero(operation, num1, num2):
    assert calculate(operation, num1, num2) is None

# Test invalid operations
@pytest.mark.parametrize(
    'operation, num1, num2',
    [
        ('%', 5, 3),
        ('abc', 5, 3),
    ],
)
def test_invalid_operations(operation, num1, num2):
    assert calculate(operation, num1, num2) is None

""" Calculator Class Tests """
from decimal import Decimal
import os
import pytest
from calculator import Calculator

@pytest.fixture
def mock_history_file():
    """Fixture to create a mock history file"""
    # Create a mock history file before each test
    # Create a mock history file
    mock_history_data = "operation,operands,result\nadd,'[Decimal('5'), Decimal('3')]',8\n"
    filename = os.path.join('data', 'test_history.csv')
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(mock_history_data)
    # Clean up after test
    if os.path.exists('test_history.csv'):
        os.remove('test_history.csv')

@pytest.fixture
def calculator():
    """Fixture for creating a Calculator instance with a temporary history file."""
    test_file = 'test_history.csv'
    yield Calculator(history_file=test_file)
    # Clean up after test
    if os.path.isfile(test_file):
        os.remove(test_file)

def test_init_with_empty_file():
    """Test initialization with an empty history file."""
    # Create an empty mock history file
    with open('test_history.csv', 'w', encoding='utf-8'):
        pass

    calc = Calculator(history_file='test_history.csv')
    assert calc.history.empty

def test_add_to_history(calculator):
    """Test adding an operation to history."""
    calc = calculator
    calc.add_to_history("add", [1, 2], 3.0)

    assert calc.history.shape[0] == 1
    assert calc.history.iloc[0]['operation'] == "add"
    assert calc.history.iloc[0]['operands'] == "[1, 2]"
    assert calc.history.iloc[0]['result'] == 3.0

def test_save_history_new_file(calculator):
    """Test saving history to a new file."""
    calc = calculator
    calc.add_to_history("add", [1, 2], 3.0)

    # Test if the history is saved in the file
    with open('test_history.csv', 'r', encoding='utf-8') as f:
        content = f.readlines()

    assert len(content) == 2  # Header + 1 entry

def test_load_history_success(calculator):
    """Test loading history from a valid file."""
    # Create a mock history file with content
    with open(os.path.join('data', 'test_history.csv'), 'w', encoding='utf-8') as f:
        f.write("operation,operands,result\n")
        f.write("subtract,'[Decimal('5'), Decimal('2')]',3\n")

    calc = calculator
    loaded_history = calc.load_history('test_history.csv')
    assert not loaded_history.empty
    assert loaded_history.shape[0] == 1

def test_load_history_file_not_exist(calculator):
    """Test loading history from a non-existent file."""
    result = calculator.load_history('non_existent.csv')
    assert result.empty  # Should return an empty DataFrame

def test_clear_history(calculator):
    """Test clearing the history."""
    calc = calculator
    calc.add_to_history("add", [1, 2], 3.0)
    assert not calc.history.empty

    calc.clear_history()
    assert calc.history.empty

def test_save_as_new_file(calculator):
    """Test saving the current history to a new file."""
    calc = calculator
    calc.add_to_history("add", [Decimal('5'), Decimal('3')], Decimal(3))
    calc.save_as_new_file('new_history.csv')

    assert os.path.isfile('data/new_history.csv')  # Check if the new file was created

    # Clean up after test
    if os.path.isfile('data/new_history.csv'):
        os.remove('data/new_history.csv')

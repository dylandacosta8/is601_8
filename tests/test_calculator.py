""" Calculator Tests """
import os
from decimal import Decimal
from unittest.mock import MagicMock
import pytest
from calculator import Calculator
from calculator.factory import CommandFactory

# Fixtures for calculator
@pytest.fixture
def calculator():
    """Fixture to create a Calculator instance with a valid test history file."""
    history_file = os.path.join('data', 'test_history.csv')
    os.makedirs('data', exist_ok=True)

    # Create an empty test history file
    with open(history_file, 'w', encoding='utf-8'):
        pass

    calc = Calculator(history_file=history_file)

    # Mock the methods of the calculator instance
    calc.add_to_history = MagicMock()
    calc.save_as_new_file = MagicMock()
    calc.clear_history = MagicMock()
    calc.delete_last_calculation = MagicMock()
    calc.show_history = MagicMock()
    calc.load_history = MagicMock()

    yield calc

    # Cleanup the test history file
    if os.path.exists(history_file):
        os.remove(history_file)

# Test cases
def test_add(calculator, fake_data):
    """Test the add function using the AddCommand with fake data."""
    add_command = CommandFactory.create_command("add", calculator)

    for record in fake_data:
        if record['operation'] == 'add':
            result = add_command.execute(Decimal(record['operand1']), Decimal(record['operand2']))
            expected_result = Decimal(record['operand1']) + Decimal(record['operand2'])
            assert result == expected_result, f"Expected {expected_result} but got {result}"

def test_subtract(calculator, fake_data):
    """Test the subtract function using the SubtractCommand with fake data."""
    subtract_command = CommandFactory.create_command("subtract", calculator)

    for record in fake_data:
        if record['operation'] == 'subtract':
            result = subtract_command.execute(Decimal(record['operand1']), Decimal(record['operand2']))
            expected_result = Decimal(record['operand1']) - Decimal(record['operand2'])
            assert result == expected_result, f"Expected {expected_result} but got {result}"

def test_multiply(calculator, fake_data):
    """Test multiplication using the MultiplyCommand with fake data."""
    multiply_command = CommandFactory.create_command("multiply", calculator)

    for record in fake_data:
        if record['operation'] == 'multiply':
            result = multiply_command.execute(Decimal(record['operand1']), Decimal(record['operand2']))
            expected_result = Decimal(record['operand1']) * Decimal(record['operand2'])
            assert result == expected_result, f"Expected {expected_result} but got {result}"

def test_divide(calculator, fake_data):
    """Test division using the DivideCommand with fake data."""
    divide_command = CommandFactory.create_command("divide", calculator)

    for record in fake_data:
        if record['operation'] == 'divide' and Decimal(record['operand2']) != 0:
            result = divide_command.execute(Decimal(record['operand1']), Decimal(record['operand2']))
            expected_result = Decimal(record['operand1']) / Decimal(record['operand2'])
            assert abs(result - expected_result) < Decimal('0.0001'), f"Expected {expected_result} but got {result}"

@pytest.fixture
def history_command(calculator):
    """Fixture to create a HistoryCommand instance."""
    return CommandFactory.create_command("history", calculator)

# Test cases for HistoryCommand
def test_history_command_help(history_command, capsys):
    """Test the help command."""
    history_command.execute("help")
    captured = capsys.readouterr()
    assert "Usage: history <subcommand> [<filename>]" in captured.out

def test_history_load_file_exists(history_command):
    """Test loading history from an existing file."""
    mock_history_data = "operation,operands,result\nadd,[Decimal('5'), Decimal('3')],8\n"
    filename = os.path.join('data', 'test_load.csv')

    # Create a mock history file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(mock_history_data)

    history_command.execute("load", filename)

    # Verify that load_history was called with the correct filename
    history_command.calculator.load_history.assert_called_once_with(filename)

    # Clean up
    os.remove(filename)

def test_history_load_file_not_exists(history_command, capsys):
    """Test loading history from a non-existing file."""
    history_command.execute("load", "non_existing_file.csv")
    path = str(os.path.join('data','non_existing_file.csv'))
    expected_message = f"History file {path} does not exist."
    print(expected_message)
    captured = capsys.readouterr()
    assert expected_message in captured.out

def test_history_save(history_command):
    """Test saving history to a file."""
    filename = os.path.join('data', 'test_save.csv')
    history_command.execute("save", filename)
    history_command.calculator.save_as_new_file.assert_called_once_with(filename)

    # Clean up
    if os.path.exists(filename):
        os.remove(filename)

def test_history_clear(history_command):
    """Test clearing the history."""
    history_command.execute("clear")
    history_command.calculator.clear_history.assert_called_once()

def test_history_delete(history_command):
    """Test deleting the last calculation."""
    history_command.execute("delete")
    history_command.calculator.delete_last_calculation.assert_called_once()

def test_history_show(history_command):
    """Test showing the current history."""
    history_command.execute("show")
    history_command.calculator.show_history.assert_called_once()

def test_history_show_with_filename(history_command):
    """Test showing history from a specified file."""
    mock_history_data = "operation,operands,result\nadd,[Decimal('5'), Decimal('3')],8\n"
    filename = os.path.join('data', 'test_show.csv')

    # Create a mock history file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(mock_history_data)

    history_command.execute("show", filename)
    history_command.calculator.load_history.assert_called_once_with(filename)
    history_command.calculator.show_history.assert_called_once()

    # Clean up
    os.remove(filename)

def test_history_execute_invalid_subcommand(history_command, capsys):
    """Test handling of an invalid subcommand."""
    history_command.execute("invalid")
    captured = capsys.readouterr()
    assert "Invalid subcommand. Use load, save, clear, delete, or show." in captured.out

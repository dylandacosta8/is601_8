from calculator import Calculator
from decimal import Decimal, InvalidOperation
import logging

logger = logging.getLogger('calculator_app')

class AddCommand:
    def __init__(self, calculator: Calculator):
        self.calculator = calculator

    def execute(self, operand1: Decimal, operand2: Decimal) -> Decimal:
        """Execute the addition operation and record it in history."""
        # LBYL: Check if operands are valid before performing addition
        if not isinstance(operand1, Decimal) or not isinstance(operand2, Decimal):
            logger.error("Operands must be of type Decimal.")
            raise TypeError("Operands must be of type Decimal.") #COV-NA
        
        try:
            # EAFP: Perform the addition and handle any arithmetic-related errors (e.g., Overflow)
            result = operand1 + operand2
            self.calculator.add_to_history("add", [operand1, operand2], result)
            logger.info(f"Executed Add: {operand1} + {operand2} = {result}")
            return result
        except (InvalidOperation, OverflowError) as e: #COV-NA
            # Handle specific cases where Decimal arithmetic may fail
            logger.error(f"Failed to add {operand1} and {operand2}: {e}")
            raise ArithmeticError(f"Error during addition: {e}") #COV-NA

    def show_help(self) -> None:
        """Provide help for the Add command."""
        print("\nUsage: add <value1> <value2>")
        print("Description: Adds two numbers.")

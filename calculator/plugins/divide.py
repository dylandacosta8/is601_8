from calculator import Calculator
from decimal import Decimal, InvalidOperation
import logging

logger = logging.getLogger('calculator_app')

class DivideCommand:
    def __init__(self, calculator: Calculator):
        self.calculator = calculator

    def execute(self, operand1: Decimal, operand2: Decimal) -> Decimal:
        """Execute the division operation and record it in history."""
        # LBYL: Check if operands are valid Decimal types and check for division by zero.
        if not isinstance(operand1, Decimal) or not isinstance(operand2, Decimal):
            logger.error("Operands must be of type Decimal.") 
            raise TypeError("Operands must be of type Decimal.") #COV-NA
        
        if operand2 == 0:
            logger.error("Division by zero attempted.") 
            raise ZeroDivisionError("Cannot divide by zero.") #COV-NA
        
        try:
            # EAFP: Perform the division and catch any Decimal-related exceptions.
            result = operand1 / operand2
            self.calculator.add_to_history("divide", [operand1, operand2], result)
            logger.info(f"Executed Divide: {operand1} / {operand2} = {result}")
            return result
        except (InvalidOperation, ZeroDivisionError, OverflowError) as e: #COV-NA
            # Handle specific errors that could occur during division.
            logger.error(f"Error during division of {operand1} by {operand2}: {e}")
            raise ArithmeticError(f"Error during division: {e}") #COV-NA

    def show_help(self) -> None:
        """Provide help for the Divide command."""
        print("\nUsage: divide <value1> <value2>")
        print("Description: Divides the first number by the second. Raises an error if the second number is zero.")

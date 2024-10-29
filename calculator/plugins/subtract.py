from calculator import Calculator
from decimal import Decimal
import logging

logger = logging.getLogger('calculator_app')

class SubtractCommand:
    def __init__(self, calculator: Calculator):
        self.calculator = calculator

    def execute(self, operand1: Decimal, operand2: Decimal) -> Decimal:
        """Execute the subtraction operation and record it in history."""
        # LBYL: Check if both operands are valid Decimal numbers before proceeding
        if isinstance(operand1, Decimal) and isinstance(operand2, Decimal):
            try:
                # EAFP: Perform the subtraction and handle any unexpected issues
                result = operand1 - operand2
                self.calculator.add_to_history("subtract", [operand1, operand2], result)
                logger.info(f"Executed Subtract: {operand1} - {operand2} = {result}")
                return result
            except Exception as e: #COV-NA
                logger.error(f"Error during subtraction: {e}")
                raise e  # Reraise the exception after logging #COV-NA
        else:
            logger.warning(f"Invalid operands for subtraction: {operand1}, {operand2}")
            raise ValueError("Operands must be Decimal numbers") #COV-NA

    def show_help(self) -> None:
        """Provide help for the Subtract command."""
        print("\nUsage: subtract <value1> <value2>")
        print("Description: Subtracts the second number from the first.")

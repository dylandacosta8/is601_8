from calculator import Calculator
from decimal import Decimal
import logging

logger = logging.getLogger('calculator_app')

class MultiplyCommand:
    def __init__(self, calculator: Calculator):
        self.calculator = calculator

    def execute(self, operand1: Decimal, operand2: Decimal) -> Decimal:
        """Execute the multiplication operation and record it in history."""
        # LBYL: Check if both operands are valid Decimal numbers before proceeding
        if isinstance(operand1, Decimal) and isinstance(operand2, Decimal):
            try:
                # EAFP: Perform the multiplication and catch any unexpected exceptions
                result = operand1 * operand2
                self.calculator.add_to_history("multiply", [operand1, operand2], result)
                logger.info(f"Executed Multiply: {operand1} * {operand2} = {result}")
                return result
            except Exception as e: #COV-NA
                logger.error(f"Error during multiplication: {e}")
                raise e  # Reraise the exception after logging #COV-NA
        else:
            logger.warning(f"Invalid operands for multiplication: {operand1}, {operand2}")
            raise ValueError("Operands must be Decimal numbers") #COV-NA

    def show_help(self) -> None:
        """Provide help for the Multiply command."""
        print("\nUsage: multiply <value1> <value2>")
        print("Description: Multiplies two numbers.")

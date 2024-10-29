import pkgutil
import importlib
from calculator import Calculator

class CommandFactory:
    command_classes = {}

    @classmethod
    def load_command_classes(cls):
        """Load all command classes from the plugins package."""
        for loader, module_name, is_pkg in pkgutil.iter_modules(['calculator/plugins']):
            # EAFP: Assume the module imports correctly, catch ImportError if it fails
            try:
                module = importlib.import_module(f"calculator.plugins.{module_name}")
                for name in dir(module):
                    cls_obj = getattr(module, name)
                    # LBYL: Check if it's a class and has the required methods before adding
                    if isinstance(cls_obj, type) and hasattr(cls_obj, 'execute') and hasattr(cls_obj, 'show_help'):
                        cls.command_classes[module_name] = cls_obj
            except ImportError as e: #COV-NA
                print(f"Failed to import {module_name}: {e}")

    @classmethod
    def create_command(cls, command_name: str, calculator: Calculator):
        """Create an instance of the specified command."""
        # LBYL: Check if the command exists before creating it
        if command_name in cls.command_classes:
            return cls.command_classes[command_name](calculator)  # Instantiate command with calculator
        else:
            # EAFP: Raise an error if the command doesn't exist, handle elsewhere
            raise ValueError(f"Unknown command: {command_name}") #COV-NA

CommandFactory.load_command_classes()

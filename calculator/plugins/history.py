import os
from calculator.command import Command
import logging

logger = logging.getLogger('calculator_app')

class HistoryCommand(Command):
    def __init__(self, calculator):
        self.calculator = calculator #TODO

    def execute(self, subcommand: str, filename: str = None) -> None:
        """Execute a history command based on the subcommand."""

        if filename:

            if "data" in filename:
                pass
            else:
                filename = os.path.join('data', filename)

        if subcommand == "help":
            self.show_help()
            return

        if subcommand == "load":
            # LBYL: Check if filename is provided and if the file exists.
            if filename is None:
                filename = input("Enter the filename to load history: ")

            if os.path.exists(filename):
                try:
                    self.calculator.load_history(filename)
                    logger.info(f"Successfully loaded history from {filename}")
                except Exception as e: #COV-NA
                    logger.error(f"Error loading history from {filename}: {e}")
                    print(f"Failed to load history: {e}")
            else:
                logger.warning(f"File not found: {filename}")
                print(f"History file '{filename}' does not exist.")
        
        elif subcommand == "save":
            # LBYL: Check if filename is provided.
            if filename is None:
                filename = input("Enter the filename to save history: ")

            # EAFP: Attempt to save history and handle any potential errors.
            try:
                self.calculator.save_as_new_file(filename)
                logger.info(f"Successfully saved history to {filename}")
            except Exception as e: #COV-NA
                logger.error(f"Error saving history to {filename}: {e}")
                print(f"Failed to save history: {e}")
        
        elif subcommand == "clear":
            try:
                # EAFP: Clear history and handle any errors that occur.
                self.calculator.clear_history()
                logger.info("History cleared successfully.")
            except Exception as e: #COV-NA
                logger.error(f"Error clearing history: {e}")
                print(f"Failed to clear history: {e}")
        
        elif subcommand == "delete":
            try:
                # EAFP: Delete the last entry in history.
                self.calculator.delete_last_calculation()
                logger.info("Last calculation deleted successfully.")
            except Exception as e: #COV-NA
                logger.error(f"Error deleting last calculation: {e}")
                print(f"Failed to delete last calculation: {e}")
        
        elif subcommand == "show":
            if filename is not None:
                # LBYL: Check if the file exists before showing history.
                if os.path.exists(filename):
                    try:
                        self.calculator.load_history(filename)
                        logger.info(f"History loaded from {filename} for display.")
                        self.calculator.show_history()
                    except Exception as e: #COV-NA
                        logger.error(f"Error loading and showing history from {filename}: {e}")
                        print(f"Failed to show history from {filename}: {e}")
                else:
                    logger.warning(f"File not found: {filename}")
                    print(f"History file '{filename}' does not exist.")
            else:
                try:
                    # EAFP: Display the current history and handle any errors.
                    self.calculator.show_history()
                    logger.info("Displayed current history.")
                except Exception as e: #COV-NA
                    logger.error(f"Error showing history: {e}")
                    print(f"Failed to show history: {e}")
        
        else:
            print("Invalid subcommand. Use load, save, clear, delete, or show.")
            logger.warning(f"Invalid subcommand: {subcommand}")

    def show_help(self) -> None:
        """Provide help information for history commands."""
        print(
            "\nHistory command help: \n"
            "Usage: history <subcommand> [<filename>]\n"
            " - load <filename>: Load history from a specified file and set it as the active file.\n"
            " - save <filename>: Save a copy of the current history to a new file.\n"
            " - clear: Clear the current history in the active file.\n"
            " - delete: Delete the last entry from the active history.\n"
            " - show [filename]: Show the current history or load history from the specified file first."
        )

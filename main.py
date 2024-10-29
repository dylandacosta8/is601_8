import os
import logging
import concurrent.futures
from calculator.factory import CommandFactory
from calculator import Calculator
from decimal import Decimal
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get the environment variable (now ENV instead of ENVIRONMENT)
environment = os.getenv('ENV', 'prod').lower()

# Set the logging format with a timestamp
log_format = "%(asctime)s - %(levelname)s - %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

os.makedirs('logs', exist_ok=True)
log_file = os.path.join('logs', 'calc.log')

# Configure logging based on environment, writing to a file
if environment == 'dev':
    logging.basicConfig(level=logging.DEBUG, format=log_format, datefmt=date_format, filename=log_file, filemode='a')
elif environment == 'uat':
    logging.basicConfig(level=logging.INFO, format=log_format, datefmt=date_format, filename=log_file, filemode='a')
else:  # 'prod'
    logging.basicConfig(level=logging.WARNING, format=log_format, datefmt=date_format, filename=log_file, filemode='a')

# REPL function
def repl():
    # Prompt the user to load a history file or use the default 'history.csv'
    user_history_file = input("Enter the history file to load (press Enter for 'history.csv'): ").strip()

    # LBYL: Check if the user has entered something
    if not user_history_file:
        user_history_file = os.path.join('data', 'history.csv')
    else:
        user_history_file = os.path.join('data', user_history_file)

    # Initialize the Calculator with the specified or default history file
    calculator = Calculator(history_file=user_history_file)

    # Display menu function
    def display_menu():
        logging.debug("Displaying available plugins")
        print("\nAvailable commands:")
        for command in CommandFactory.command_classes.keys():
            print(f" - {command}")
        print("\nRun <command> help to see additional usage details.")

    # Display the menu when the application starts
    display_menu()

    while True:
        # Print the currently active history file
        print(f"\n[Active history file: {calculator.active_history_file}]")

        user_input = input("Enter command or 'help' to see options or 'exit' to quit: ").strip().lower()

        if user_input == "exit":
            logging.info("User exited the application.")
            print("\nExiting the calculator. Goodbye!")
            break
        elif user_input == "help":
            display_menu()
            continue

        try:
            parts = user_input.split()
            operation = parts[0]

            # Handle help commands
            if len(parts) > 1 and parts[1] == "help":
                # LBYL: Check if the command exists before calling help
                command_instance = CommandFactory.create_command(operation, calculator)
                if command_instance:
                    command_instance.show_help()
                else:
                    print("\nInvalid command for help. Type 'help' to see available plugins.")
                continue

            # Handle history subcommands
            if operation == "history" and len(parts) > 1:
                history_command = parts[1]
                command_instance = CommandFactory.create_command("history", calculator)
                if command_instance:
                    if history_command == "load" and len(parts) == 3:
                        filename = parts[2]
                        # EAFP: Assume loading will succeed and catch exceptions later
                        command_instance.execute("load", filename)
                    elif history_command == "save" and len(parts) == 3:
                        filename = parts[2]
                        command_instance.execute("save", filename)
                    elif history_command == "clear":
                        command_instance.execute("clear")
                    elif history_command == "delete":
                        command_instance.execute("delete")
                    elif history_command == "show":
                        command_instance.execute("show")
                    else:
                        print("\nInvalid subcommand. Use load, save, clear, delete, or show.")
                else:
                    print("\nHistory command not found.")
                continue

            # Convert values to Decimal for arithmetic operations
            # LBYL: Check if the input values are valid before conversion
            if len(parts) > 1:
                try:
                    values = [Decimal(value) for value in parts[1:]]
                except ValueError:
                    logging.error("Invalid decimal value provided.")
                    print("\nPlease enter valid numbers.")
                    continue
            else:
                values = []

            # Check if the operation is valid
            # LBYL: Check if the command exists before execution
            command_instance = CommandFactory.create_command(operation, calculator)
            if command_instance is None:
                logging.warning(f"Invalid operation attempted: {operation}")
                print("\nInvalid operation. Type 'help' to see available plugins.")
                continue

            # EAFP: Assume the execution will succeed and catch exceptions later
            with concurrent.futures.ProcessPoolExecutor() as executor:
                future = executor.submit(command_instance.execute, *values)
                result = future.result()  # This will block until the result is available

            logging.debug(f"Operation '{operation}' executed with result: {result}")
            print(f"\nResult: {result}")

        except ValueError:
            logging.error("Invalid input provided.")
            print("\nInvalid input. Please enter valid numbers and an operation.")
        except ZeroDivisionError:
            logging.error("Division by zero attempted.")
            print("\nError: Division by zero.")
        except Exception as e:
            logging.exception(f"An error occurred during command execution: {e}")
            print(f"\nAn error occurred: {e}")
            print("Run <command> help to see usage details.")

# Starting the REPL
if __name__ == "__main__":
    repl()

import pandas as pd
from decimal import Decimal
import logging
import os

logger = logging.getLogger('calculator_app')

class Calculator:
    def __init__(self, history_file: str = None):
        self.history_file = history_file
        self.active_history_file = self.history_file  # Track the currently active file
        
        # LBYL: Check if the file exists and is not empty
        if os.path.isfile(self.history_file) and os.path.getsize(self.history_file) > 0:
            self.history = self.load_history(self.history_file)  # Load history from the file COV-NA
            logger.info(f"History loaded from {self.history_file}")
        else:
            # EAFP: Assume the history file might not exist or be empty, handle with empty history
            self.history = pd.DataFrame(columns=["operation", "operands", "result"])
            logger.info(f"Starting with empty history, no valid file found at {self.history_file}")
        
        self.new_entries = []  # Keep track of new entries added during the session

    def add_to_history(self, operation: str, operands: list, result: Decimal) -> None:
        """Add a calculation to the history and save it to the active history file."""
        new_entry = {
            "operation": operation,
            "operands": str(operands),
            "result": result
        }
        self.history = pd.concat([self.history, pd.DataFrame([new_entry])], ignore_index=True)
        self.new_entries.append(new_entry)
        logger.info(f"Added to history: {operation} with operands {operands} = {result}")
        self.save_history()

    def save_history(self) -> None:
        """Save only new entries to the active history file."""
        if self.new_entries:  # LBYL: Check if there are new entries to save
            new_entries_df = pd.DataFrame(self.new_entries)
            
            # EAFP: Assume file creation will work, handle errors if it fails
            try:
                if not os.path.isfile(self.active_history_file):
                    new_entries_df.to_csv(self.active_history_file, mode='w', index=False)
                    logger.info(f"History saved to new file: {self.active_history_file}")
                else:
                    # Append only the new entries to the active history file
                    new_entries_df.to_csv(self.active_history_file, mode='a', index=False, header=False)
                    logger.info(f"New entries appended to {self.active_history_file}")
                self.new_entries.clear()  # Clear the new entries after saving
            except Exception as e: #COV-NA
                logger.error(f"Error saving history: {e}")

    def load_history(self, new_filename: str = None) -> pd.DataFrame:
        """Load history from a new file or the active file."""
        if new_filename:

            if "data" in new_filename: #COV-NA
                full_path = new_filename
            else:
                full_path = os.path.join('data', new_filename)
            
            # LBYL: Check if the file exists before attempting to load
            if os.path.isfile(full_path):
                try:
                    self.active_history_file = full_path
                    loaded_history = pd.read_csv(full_path)
                    self.history = loaded_history
                    logger.info(f"Switched to history file: {self.active_history_file}")
                    return loaded_history
                except Exception as e: #COV-NA
                    logger.error(f"Error loading history from {full_path}: {e}")
                    return pd.DataFrame(columns=["operation", "operands", "result"])
            else:
                logger.error(f"History file '{full_path}' does not exist.")
                return pd.DataFrame(columns=["operation", "operands", "result"])
        
        # EAFP: Assume loading from the active file works, handle errors if it fails
        try: #COV-NA
            if os.path.isfile(self.active_history_file):
                loaded_history = pd.read_csv(self.active_history_file)
                self.history = loaded_history
                logger.info(f"History loaded from {self.active_history_file}")
                return loaded_history
            else:
                logger.warning(f"No history file found: {self.active_history_file}. Starting with empty history.")
                return pd.DataFrame(columns=["operation", "operands", "result"])
        except Exception as e: #COV-NA
            logger.error(f"Failed to load history: {e}")
            return pd.DataFrame(columns=["operation", "operands", "result"])

    def clear_history(self) -> None:
        """Clear the calculation history by deleting the active file."""
        # LBYL: Check if the file exists before deleting
        if os.path.isfile(self.active_history_file):
            try:
                os.remove(self.active_history_file)  # EAFP: Attempt to remove the file
                logger.info(f"Cleared history by deleting file: {self.active_history_file}")
                self.history = pd.DataFrame(columns=["operation", "operands", "result"])  # Reset history DataFrame
            except Exception as e: #COV-NA
                logger.error(f"Failed to clear history file: {e}")
        else:
            logger.warning(f"Attempted to clear non-existent history file: {self.active_history_file}")

    def delete_last_calculation(self) -> None:
        """Delete the last calculation from the active history file."""
        if os.path.isfile(self.active_history_file) and os.path.getsize(self.active_history_file) > 0: #COV-NA  # LBYL: Check if the file exists and is not empty
            try:
                # Read the current history from the active file
                with open(self.active_history_file, 'r') as file:
                    lines = file.readlines()
                
                # Check if there are lines to delete
                if lines:
                    # Remove the last line
                    lines = lines[:-1]  # Retain all but the last line
                    
                    # Write the updated lines back to the file
                    with open(self.active_history_file, 'w') as file:
                        file.writelines(lines)
                    
                    logger.info(f"Deleted the last calculation from {self.active_history_file}.")
                else:
                    logger.warning("Attempted to delete from an empty history file.")
            except Exception as e:
                logger.error(f"Error while deleting the last calculation: {e}")
        else:
            logger.warning(f"Active history file '{self.active_history_file}' does not exist or is empty.")

    def show_history(self) -> None:
        """Print the current history in a user-friendly format."""
        self.history = self.load_history(self.active_history_file)
        
        if self.history.empty:  # LBYL: Check if history is empty
            print("No history recorded.")
            return

        try:
            # Split operands into operand1 and operand2 columns for display
            display_history = self.history.copy()
            display_history[['operand1', 'operand2']] = pd.DataFrame(
                display_history['operands'].apply(lambda op: eval(op) if isinstance(op, str) else op).tolist(),
                index=display_history.index
            )
        except Exception as e:  # EAFP: Handle any error in processing history
            logger.error(f"Failed to process operands for display: {e}")
            print("Error processing history data.")
            return

        # Display formatted history
        print("\nCurrent History:")
        print(f"{'Index':<5} {'Operation':<15} {'Operand1':<10} {'Operand2':<10} {'Result':<10}")
        print("=" * 60)
        for index, row in display_history.iterrows():
            print(f"{index + 1:<5} {row['operation']:<15} {row['operand1']:<10} {row['operand2']:<10} {row['result']:<10}")
        print("")

    def save_as_new_file(self, new_filename: str) -> None:
        """Save a copy of the current history to a new file."""

        self.history = self.load_history(self.active_history_file)

        
        if self.history.empty: #COV-NA
            print("No history to save.")
            return 
        else:
            if new_filename:
                # Ensure the directory exists; if not, create it
                os.makedirs('data', exist_ok=True)
                if "data" in new_filename:
                    full_path = new_filename
                else:
                    full_path = os.path.join('data', new_filename)
        
            # Ensure only the necessary columns are saved
            history_to_save = self.history[['operation', 'operands', 'result']]
            history_to_save.to_csv(full_path, mode='w', index=False)
            logger.info(f"History saved as a copy to {full_path}")

    def get_history(self):
        """Retrieve the calculation history as a list of dictionaries."""
        return self.history.to_dict(orient='records') if isinstance(self.history, pd.DataFrame) else self.history

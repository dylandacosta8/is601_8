import importlib
import pkgutil
import os
import logging

logger = logging.getLogger('calculator_app')

class PluginManager:
    def __init__(self, calculator):
        self.plugins = {}
        self.calculator = calculator

    def load_plugins(self):
        plugins_dir = "calculator.plugins"
        for module_name in self.list_command_modules(plugins_dir):
            try:
                # LBYL: Check if the module exists and if it contains the expected command class
                logger.debug(f"Attempting to import module: {module_name}")
                
                # EAFP: Try importing the module and retrieving the command class directly
                module = importlib.import_module(f"{plugins_dir}.{module_name}")
                command_class_name = f"{module_name.capitalize()}Command"
                
                if hasattr(module, command_class_name):  # LBYL: Check if class exists before accessing
                    command_class = getattr(module, command_class_name)
                    command_instance = command_class(self.calculator)
                    self.plugins[module_name] = command_instance
                    logger.info(f"Successfully loaded plugin: {module_name}")
                else:
                    logger.error(f"Command class '{command_class_name}' not found in {module_name}")
            except ImportError as e: #COV-NA
                # EAFP: Catch import errors to handle invalid or missing modules
                logger.error(f"Failed to import module '{module_name}': {e}")
            except Exception as e: #COV-NA
                # Catch any other errors in case something unexpected happens
                logger.error(f"Failed to load command '{module_name}': {e}")

    def list_command_modules(self, package):
        try:
            # EAFP: Use exception handling to manage file system errors, such as package not found
            command_modules = [name for _, name, _ in pkgutil.iter_modules([package.replace('.', os.sep)])]
            logger.debug(f"Found command modules: {command_modules}")
            return command_modules
        except FileNotFoundError as e:
            # Handle specific case where package directory is not found
            logger.error(f"Package directory not found for '{package}': {e}")
            return []
        except Exception as e:
            # Catch any other errors
            logger.exception(f"Error listing command modules in package '{package}': {e}")
            return []

    def get_command(self, command_name):
        # LBYL: Check if the command exists in the plugins before trying to access it
        if command_name in self.plugins: #COV-NA
            command = self.plugins[command_name] #COV-NA
            logger.debug(f"Retrieved command: {command_name}")
            return command
        else: #COV-NA
            # EAFP: Log the missing command and return None as a fallback
            logger.warning(f"Command not found: {command_name}")
            return None 

    def list_plugins(self):
        # LBYL: Verify if there are plugins loaded before attempting to list them
        if self.plugins: #COV-NA
            plugin_keys = list(self.plugins.keys())
            logger.debug(f"Listing loaded plugins: {plugin_keys}")
            return plugin_keys
        else: #COV-NA
            # If no plugins are loaded, log and return an empty list
            logger.info("No plugins loaded.")
            return []

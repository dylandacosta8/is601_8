""" Plugin Manager Tests """
from unittest.mock import patch, MagicMock
import pytest
from calculator.plugins import PluginManager

@pytest.fixture
def plugin_manager():
    """Create a PluginManager instance for testing."""
    mock_calculator = MagicMock()  # Mock the calculator instance
    return PluginManager(mock_calculator)

def test_load_plugins_success(plugin_manager):
    """Test successful loading of plugins."""
    with patch("importlib.import_module") as mock_import:
        # Create a mock for the command class
        mock_command_class = MagicMock()
        mock_import.return_value = MagicMock(**{ 'AddCommand': mock_command_class })

        with patch.object(plugin_manager, 'list_command_modules', return_value=['add']):
            plugin_manager.load_plugins()

        # Assert that the plugin has been loaded correctly
        assert 'add' in plugin_manager.plugins
        assert isinstance(plugin_manager.plugins['add'], MagicMock)  # Just check if it's a mock

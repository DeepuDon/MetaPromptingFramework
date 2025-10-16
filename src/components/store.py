import os
import yaml
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def store_template(data: dict, name: str, template_dir: str = "templates") -> bool:
    """
    Stores a dictionary as a YAML template file.

    Args:
        data (dict): The dictionary to store.
        name (str): The name of the template (without extension).
        template_dir (str): The directory where the template will be stored. Defaults to "templates".

    Returns:
        bool: True if storage is successful, False otherwise.
    """
    try:
        template_path = Path(template_dir)
        template_path.mkdir(parents=True, exist_ok=True)
        file_path = template_path / f"{name}.yaml"
        
        with open(file_path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
        
        logging.info(f"Template '{name}' stored successfully at '{file_path}'")
        return True
    except IOError as e:
        logging.error(f"Failed to write to file for template '{name}': {e}")
        return False
    except yaml.YAMLError as e:
        logging.error(f"YAML error while storing template '{name}': {e}")
        return False
    except Exception as e:
        logging.error(f"An unexpected error occurred during storage of template '{name}': {e}")
        return False

def load_template(name: str, template_dir: str = "templates") -> dict | None:
    """
    Loads a YAML template file into a dictionary.

    Args:
        name (str): The name of the template (without extension).
        template_dir (str): The directory where the template is stored. Defaults to "templates".

    Returns:
        dict | None: The loaded dictionary, or None if loading fails.
    """
    file_path = Path(template_dir) / f"{name}.yaml"
    
    if not file_path.exists():
        logging.warning(f"Template file not found for '{name}' at '{file_path}'")
        return None
        
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
        
        logging.info(f"Template '{name}' loaded successfully from '{file_path}'")
        return data
    except IOError as e:
        logging.error(f"Failed to read file for template '{name}': {e}")
        return None
    except yaml.YAMLError as e:
        logging.error(f"YAML error while loading template '{name}': {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred during loading of template '{name}': {e}")
        return None

if __name__ == "__main__":
    import shutil
    from unittest.mock import patch

    print("--- Running Prompt Template Manager Tests ---")
    
    TEST_DIR = "temp_test_templates"
    NEW_DIR = "new_temp_dir"
    DEFAULT_DIR = "templates"

    # Cleanup before tests
    for d in [TEST_DIR, NEW_DIR, DEFAULT_DIR]:
        if Path(d).exists():
            shutil.rmtree(d, ignore_errors=True)
    
    os.makedirs(TEST_DIR)

    # Test 1: Successful store and load
    print("\n[Test 1: Store and Load a valid template]")
    template_name_1 = "test_template_1"
    template_data_1 = {"role": "system", "content": "You are a helpful assistant."}
    assert store_template(template_data_1, template_name_1, template_dir=TEST_DIR) is True
    loaded_data_1 = load_template(template_name_1, template_dir=TEST_DIR)
    assert loaded_data_1 == template_data_1
    print("Test 1 Passed")

    # Test 2: Load a non-existent template
    print("\n[Test 2: Load a non-existent template]")
    template_name_2 = "non_existent_template"
    assert load_template(template_name_2, template_dir=TEST_DIR) is None
    print("Test 2 Passed")

    # Test 3: Store in a new directory
    print("\n[Test 3: Store in a new directory]")
    template_name_3 = "test_template_3"
    template_data_3 = {"prompt": "Generate a summary."}
    assert store_template(template_data_3, template_name_3, template_dir=NEW_DIR) is True
    assert (Path(NEW_DIR) / f"{template_name_3}.yaml").exists()
    print("Test 3 Passed")

    # Test 4: Load from a file with invalid YAML
    print("\n[Test 4: Load a file with invalid YAML]")
    template_name_4 = "invalid_yaml_template"
    invalid_yaml_path = Path(TEST_DIR) / f"{template_name_4}.yaml"
    with open(invalid_yaml_path, 'w') as f:
        f.write("role: system\ncontent: - this is not valid yaml")
    assert load_template(template_name_4, template_dir=TEST_DIR) is None
    print("Test 4 Passed")

    # Test 5: Storing circular reference data
    print("\n[Test 5: Store data with circular reference]")
    template_name_5 = "circular_ref_template"
    template_data_5 = {}
    template_data_5["a"] = template_data_5  # Create circular reference
    # PyYAML handles circular references, so this should succeed.
    assert store_template(template_data_5, template_name_5, template_dir=TEST_DIR) is True
    print("Test 5 Passed")

    # Test 6: Mock an IOError on file write
    print("\n[Test 6: Mock IOError on store]")
    template_name_6 = "ioerror_test"
    template_data_6 = {"test": "data"}
    with patch('builtins.open') as mock_open:
        mock_open.side_effect = IOError("Mocked I/O Error")
        assert store_template(template_data_6, template_name_6, template_dir=TEST_DIR) is False
    print("Test 6 Passed")

    # Test 7: Use default directory
    print("\n[Test 7: Use default directory]")
    template_name_7 = "default_dir_test"
    template_data_7 = {"default": "test"}
    assert store_template(template_data_7, template_name_7) is True
    assert (Path(DEFAULT_DIR) / f"{template_name_7}.yaml").exists()
    loaded_data_7 = load_template(template_name_7)
    assert loaded_data_7 == template_data_7
    print("Test 7 Passed")

    # Cleanup after tests
    for d in [TEST_DIR, NEW_DIR, DEFAULT_DIR]:
        if Path(d).exists():
            shutil.rmtree(d, ignore_errors=True)
    
    print("\n--- All tests passed ---")
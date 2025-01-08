import os
import importlib.util
import sys

def get_exports(base_directory):
    """
    Search for def.py files in all subdirectories of a base directory,
    and extract the `export` list from each module.

    :param base_directory: The directory to start searching from.
    :return: A dictionary with the file path as the key and `export` list as the value.
    """
    results = []

    for root, dirs, files in os.walk(base_directory):
        for file in files:
            if file == "def.py":
                file_path = os.path.join(root, file)
                module_name = os.path.splitext(file)[0]

                # Dynamically load the module
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                
                # Adjust the module's package for relative imports
                package_name = os.path.basename(root)  # Assuming the folder name is the package
                module.__package__ = package_name

                # Add the parent directory to sys.path
                sys.path.insert(0, os.path.dirname(root))

                # Load the module
                try:
                    spec.loader.exec_module(module)
                except Exception as e:
                    print(f"Error loading module {file_path}: {e}")
                    continue

                # Check if the module has an `export` attribute
                if hasattr(module, "export"):
                    results.extend(module.export)

                # Clean up sys.path modification
                sys.path.pop(0)

    return results

def get_categorized_exports(base_directory):
    """
    Get the exports from a base directory and sort them by type and plugin

    :param base_directory: The directory to start searching from.
    :return: A sorted list of exports.
    """
    exports = get_exports(base_directory)

    if _has_duplicate_names(exports):
        raise ValueError("Duplicate export names found.")

    # Sort the exports plugin then type
    # Structure: {plugin_name: {type: [export]}}
    sorted_exports = {}
    for export in exports:
        plugin_name = export.get_plugin_name()
        function_type = type(export).__name__

        if function_type not in sorted_exports:
            sorted_exports[function_type] = {}

        if plugin_name not in sorted_exports[function_type]:
            sorted_exports[function_type][plugin_name] = []

        sorted_exports[function_type][plugin_name].append(export)

    return sorted_exports

def _has_duplicate_names(exports):
    """
    Check for duplicate names in the exports.

    :param exports: The list of exports.
    :return: A list of duplicate names.
    """
    all_functions = [f"{type(export).__name__}.{str(export)}" for export in exports]

    return len(all_functions) != len(set(all_functions))
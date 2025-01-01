import subprocess
import threading
import time
import ast

class dconf:
    def __init__(self, base_path):
        """
        Initialize the dconf wrapper.

        :param base_path: The directory path in dconf to manage (e.g., '/org/gnome/desktop/')
        """
        if not base_path.endswith('/'):
            base_path += '/'
        self.base_path = base_path

    def _run_command(self, command):
        """
        Run a dconf command and return the result.

        :param command: List of command arguments to run with subprocess.
        :return: The stdout output of the command as a string.
        """
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running command {' '.join(command)}: {e.stderr}")
            return None

    def _parse_value(self, value):
        """Recursively parse the value into its appropriate Python type."""
        # Handle booleans
        if value in ['true', 'false']:
            return value == 'true'
        # Handle numbers
        elif value.replace('.', '', 1).isdigit() and value.count('.') < 2:
            return float(value) if '.' in value else int(value)
        # Handle arrays (lists)
        elif value.startswith('[') and value.endswith(']'):
            try:
                # Use ast.literal_eval to parse the list and then recurse
                parsed_list = ast.literal_eval(value)
                return [self._parse_value(str(item)) for item in parsed_list]
            except Exception as e:
                print(f"Error parsing list: {e}")
                return value
        # Handle strings
        elif value.startswith("'") and value.endswith("'"):
            return value[1:-1]
        # Fallback for unhandled cases
        return value

    def read(self, key):
        """Read a value from dconf and return it as the correct Python type."""
        full_key = self.base_path + key
        raw_value = self._run_command(['dconf', 'read', full_key])
        
        if raw_value is None:
            return None

        try:
            return self._parse_value(raw_value)
        except Exception as e:
            print(f"Error parsing value for {full_key}: {e}")
            return raw_value

    def list(self, key):
        """
        List all keys under a given key.

        :param key: The key to list (relative to the base_path).
        :return: A list of keys under the given key.
        """
        full_key = self.base_path + key
        output = self._run_command(['dconf', 'list', full_key])
        if output is None:
            return []

        return output.splitlines()

    def list_values(self, key):
        """
        List all key-value pairs under a given key.

        :param key: The key to list (relative to the base_path).
        :return: A dictionary of key-value pairs under the given key.
        """
        full_key = self.base_path + key
        output = self._run_command(['dconf', 'list', full_key])
        if output is None:
            return []
        return [value for value in output.splitlines() if '/' not in value]

    def list_subfolders(self, key):
        """
        List all subfolders under a given key.

        :param key: The key to list (relative to the base_path).
        :return: A list of subfolders under the given key.
        """
        full_key = self.base_path + key
        output = self._run_command(['dconf', 'list', full_key])
        if output is None:
            return []
        return [value for value in output.splitlines() if '/' in value]

        result = {}
        lines = output.splitlines()
        for line in lines:
            key, value = line.split('=', 1)
            result[key.strip()] = value.strip()

        return result

    def write(self, key, value):
        """
        Write a value to dconf.

        :param key: The key to write (relative to the base_path).
        :param value: The value to write. Should be formatted as a dconf-compatible string.
        """
        full_key = self.base_path + key
        self._run_command(['dconf', 'write', full_key, value])

    def reset(self, key):
        """
        Reset a dconf key to its default value.

        :param key: The key to reset (relative to the base_path).
        """
        full_key = self.base_path + key
        self._run_command(['dconf', 'reset', full_key])

    def dump(self):
        """
        Dump all keys and values under the base_path.

        :return: A dictionary of key-value pairs.
        """
        output = self._run_command(['dconf', 'dump', self.base_path])
        if output is None:
            return {}

        result = {}
        lines = output.splitlines()
        current_key = None

        for line in lines:
            if line.startswith('['):
                current_key = line.strip('[]')
            elif current_key:
                key, value = line.split('=', 1)
                result[f"{current_key}/{key.strip()}"] = value.strip()

        return result

    def watch(self, callback):
        """
        Watch for changes in the directory using dconf watch and call the callback.

        :param callback: A function to call with the dconf path that changed.
        """
        def watch_thread():
            try:
                command = ['dconf', 'watch', self.base_path]
                process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

                for line in process.stdout:
                    if line.startswith(self.base_path):
                        changed_path = line.strip()
                        callback(changed_path)
            except Exception as e:
                print(f"Error watching dconf: {e}")

        thread = threading.Thread(target=watch_thread, daemon=True)
        thread.start()
import subprocess
import threading
import time
import ast

def read(key):
    """
    Read a value from dconf using an absolute key.

    :param key: The absolute key to read.
    :return: The value of the key.
    """
    raw_value = subprocess.run(['dconf', 'read', key], capture_output=True, text=True)
    return raw_value.stdout.strip()
    
def write(key, value):
    """
    Write a value to dconf using an absolute key.

    :param key: The absolute key to write.
    :param value: The value to write.
    """
    subprocess.run(['dconf', 'write', key, value])
    
def reset(key):
    """
    Reset a dconf key to its default value using an absolute key.

    :param key: The absolute key to reset.
    """
    subprocess.run(['dconf', 'reset', key])

def dump(path):
    """
    Dump all keys and values under an absolute path.

    :param path: The absolute path to dump.
    :return: A dictionary of key-value pairs.
    """
    output = subprocess.run(['dconf', 'dump', path], capture_output=True, text=True)
    result = {}
    lines = output.stdout.splitlines()
    current_key = None

    for line in lines:
        if line.startswith('['):
            current_key = line.strip('[]')
        elif current_key:
            key, value = line.split('=', 1)
            result[f"{current_key}/{key.strip()}"] = value.strip()

    return result

def watch(path, callback):
    """
    Watch for changes in the directory using dconf watch and call the callback.

    :param path: The absolute path to watch.
    :param callback: A function to call with the dconf path that changed.
    """
    def watch_thread():
        try:
            command = ['dconf', 'watch', path]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

            for line in process.stdout:
                if line.startswith(path):
                    changed_path = line.strip()
                    callback(changed_path)
        except Exception as e:
            print(f"Error watching dconf: {e}")
    thread = threading.Thread(target=watch_thread, daemon=True)
    thread.start()
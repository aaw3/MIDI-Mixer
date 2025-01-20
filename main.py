import mido
from config import Config
from messages import Messages
import threading
import time
from lighting import Lighting
from loader import get_categorized_exports
from gui import MixerBoard

def list_midi_ports():
    """List all available MIDI input ports."""
    print("Available MIDI input ports:")
    for index, port_name in enumerate(mido.get_input_names()):
        print(f"{index}: {port_name}")

def select_midi_port():
    list_midi_ports()

    config = Config()
    port_name = None
    while True:
        # Prompt user to select a port
        try:
            port_number = int(input("Enter the number of the MIDI input port you want to use: "))
        except ValueError:
            print("Invalid input. Try again.")
            continue
        midi_ports = mido.get_input_names()
        if port_number < 0 or port_number >= len(midi_ports):
            print("Invalid port number. Try again.")
            continue

        port_name = midi_ports[port_number]
        config.save_input(port_name)
        break

        return port_name

    try: 
        midi_input = mido.open_input(port_name)
        midi_input.close()
        return port_name
    except:
        print("Trying to use old port failed, please select a new port.")
        port_name = None
        select_midi_port()

new_port_selected = False

port_name = None
def handle_console_input():
    """Handle console input to change the MIDI input port."""
    while True:
        result = input()
        # Enter key was pressed
        if result == "":
            global new_port_selected, port_name
            port_name = select_midi_port()
            print("New MIDI input port selected: ", port_name)
            new_port_selected = True


def send_note_off(outport, note, delay, use_note_on=False):
    """Send the appropriate message to turn off the note."""
    time.sleep(delay)
    if use_note_on:
        note_off_msg = mido.Message('note_on', note=note, velocity=0)
    else:
        note_off_msg = mido.Message('note_off', note=note, velocity=0)

    outport.send(note_off_msg)
    print(f"Sent asynchronously: {note_off_msg}")



def main():
    global new_port_selected, port_name
    running = True
    # List all available MIDI input ports if none were selected
    # Note: The right shifted mode makes some buttons act as faders and knobs for unrelated rows, therefore develop has been paused
    # Clients can manage the shifting through the arrow buttons on a software level

    port_name = select_midi_port()

    print(f"Listening to MIDI input from: {port_name}")

    print("Press enter to reselect the MIDI input port.")



    exports = get_categorized_exports("modules")
    gui = MixerBoard(exports)
    guiThread = threading.Thread(target=gui.start)
    guiThread.start()

    # Start a thread to handle console input
    threading.Thread(target=handle_console_input).start()

    while running:
        try:
            with mido.open_input(port_name) as inport, mido.open_output(port_name) as outport:
                stop_event = threading.Event()

                snake_thread = threading.Thread(target=Lighting.Display.Snake, args=(outport, stop_event), daemon=True)
                snake_thread.start()

                print("Press Ctrl+C to stop.")

                while True:
                    if not guiThread.is_alive():
                        stop_event.set()  # Stop the Snake thread
                        if snake_thread.is_alive():
                            snake_thread.join()
                        running = False
                        break

                    message = inport.poll()  # Non-blocking MIDI message retrieval

                    if new_port_selected:
                        new_port_selected = False
                        stop_event.set()  # Stop the Snake thread
                        snake_thread.join()  # Wait for the thread to finish
                        time.sleep(1)
                        break

                    if message:
                        Messages.handle_midi_message(message)

        except KeyboardInterrupt:
            print("Ctrl+C pressed. Exiting.")
            stop_event.set()  # Stop the Snake thread
            if snake_thread.is_alive():
                snake_thread.join()  # Ensure the thread terminates
            running = False
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            stop_event.set()  # Ensure the Snake thread is stopped on other exceptions
            if snake_thread.is_alive():
                snake_thread.join()
            running = False
            break


if __name__ == "__main__":
    main()

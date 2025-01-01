import mido
from config import Config
from messages import Messages
import threading
import time
from lighting import Lighting
from easyeffects import EasyEffects

def list_midi_ports():
    """List all available MIDI input ports."""
    print("Available MIDI input ports:")
    for index, port_name in enumerate(mido.get_input_names()):
        print(f"{index}: {port_name}")


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
    # List all available MIDI input ports if none were selected
    # Note: The right shifted mode makes some buttons act as faders and knobs for unrelated rows, therefore develop has been paused
    # Clients can manage the shifting through the arrow buttons on a software level
    config = Config()
    port_name = config.get_saved_input()
    
    if not port_name:
        list_midi_ports()
    

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

    print(f"Listening to MIDI input from: {port_name}")

    easyeffects = EasyEffects()

    try:
        with mido.open_input(port_name) as inport, mido.open_output(port_name) as outport:
            print("Press Ctrl+C to stop.")

            threading.Thread(target=Lighting.Display.Snake, args=(outport,)).start()

            for message in inport:
                #print(message)
                # Use async to delay the send message by 0.5 seconds on another thread
                #outport.send(message)
                #if message.type == "note_on" or message.type == "note_off":
                #    threading.Thread(target=send_note_off, args=(outport, message.note, 0.5, True)).start()
                Messages.handle_midi_message(message)

                easyeffects.run_test()



    except KeyboardInterrupt:
        print("Exiting.")

if __name__ == "__main__":
    main()

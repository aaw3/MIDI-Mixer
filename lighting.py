import threading
import time
import mido

class Lighting:
    class Display:
        def set_button_lighting_off(outport, note, delay, use_note_on=False):
            """Turn off the light of a button."""
            time.sleep(delay)
            if use_note_on:
                outport.send(mido.Message('note_on', note=note, velocity=0))
            else:
                outport.send(mido.Message('note_off', note=note, velocity=0))

        def set_button_light_on(output, note, delay=0):
            """Turn on the light of a button."""
            if delay > 0:
                time.sleep(delay)
            
            output.send(mido.Message('note_on', note=note, velocity=127))
            
        @staticmethod
        def Snake(outport, reverse=False):
            delay = 0.1
            size = 5
            size_delay = delay * size
            """Display a snake pattern on the Launchpad."""
            note_array = [24, 0, 8, 16, 17, 9, 1, 25, 26, 2, 10, 18, 19, 11, 3, 27, 28, 4, 12, 20, 21, 13, 5, 29, 30, 6, 14, 22, 23, 15, 7, 31, 99, 98, 97, 96, 47, 46, 92, 91, 95, 93, 94]
            while True:
                for note in note_array:
                    Lighting.Display.set_button_light_on(outport, note)
                    threading.Thread(target=Lighting.Display.set_button_lighting_off, args=(outport, note, size_delay, True)).start()
                    time.sleep(delay)
                if reverse:
                    for note in reversed(note_array):
                        Lighting.Display.set_button_light_on(outport, note)
                        threading.Thread(target=Lighting.Display.set_button_lighting_off, args=(outport, note, size_delay, True)).start()
                        time.sleep(delay)
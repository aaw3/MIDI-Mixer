from mappings import Mapping
from gui import MixerBoard
import time
import threading

class Messages:
    
    
    
    @staticmethod
    def handle_midi_message(message):
        #print(message)
        if message.type == Mapping.MessageType.CONTROL_CHANGE.value:
            if message.control in Mapping.FADER:
                Messages.handle_fader_message(message)
            elif message.control in Mapping.KNOB and (Messages._knob_check_accepted_values(Mapping.KNOB[message.control], message) or Messages._knob_check_scale_range(Mapping.KNOB[message.control], message)):
                Messages.handle_knob_message(message)
            else:
                if message.control in Mapping.BUTTON:
                    if message.value in Mapping.BUTTON[message.control].extra["accepted_values"]:
                        Messages.handle_button_message(message)

        elif message.type == Mapping.MessageType.NOTE_ON.value or message.type == Mapping.MessageType.NOTE_OFF.value:
                if message.note in Mapping.BUTTON:
                    Messages.handle_button_message(message)
                else:
                    print(f"Unmapped Note On: {message.note}, Velocity: {message.velocity}")

#        elif message.type == Mapping.MessageType.NOTE_OFF.value:
#            print(f"Note Off: {message.note}")

        elif message.type == Mapping.MessageType.PITCHWHEEL.value:
            # Only Faders
            Messages.handle_fader_message(message)

        else:
            print(f"Unhandled Message: {message}")

    def _knob_check_accepted_values(knob, message):
        return "accepted_values" in knob.extra and message.value in knob.extra["accepted_values"] and message.value in knob.extra["accepted_values"]
        

    def _knob_check_scale_range(knob, message):
        if "scale_range" in knob.extra:
            min_value, max_value = knob.extra["scale_range"]
            return min_value <= message.value <= max_value
        return False

    def handle_knob_message(message):
        knob = Mapping.KNOB[message.control]
        knob_value = message.value
        if knob.scale_type == "binary":
            if knob_value == Mapping.KnobMessage.UP.value:
                knob_value = 1
            elif knob_value == Mapping.KnobMessage.DOWN.value:
                knob_value = -1
        elif knob.scale_type == "linear":
            knob_value = knob_value / 127
        #print(f"Knob: {Mapping.KNOB[message.control].name}, Value: {knob_value}")
        # Knob
        extra_args = MixerBoard.extra_args[knob.name] if knob.name in MixerBoard.extra_args else None
        function = MixerBoard.get_function_by_component_name(knob.name)

        if not function:
            return

        knob_number = int(knob.name.split("_")[-1])

        list_extra_args = list(extra_args) if extra_args else []
        list_extra_args.insert(0, knob_number)

        extra_args = tuple(list_extra_args)

        try:
            function.call(knob_value, *extra_args)
        except Exception as e:
            print(f"Knob: Error calling function {function} with args {extra_args}: {e}")
    
    def handle_fader_message(message):
        if message.type == Mapping.MessageType.PITCHWHEEL.value:
            fader = Mapping.FADER[message.channel]
        elif message.type == Mapping.MessageType.CONTROL_CHANGE.value:
            fader = Mapping.FADER[message.control]
            
        
        if fader.scale_type == "signed":
            fader_value = message.pitch
            min_value, max_value = fader.extra["scale_range"]
            if fader_value > 0:
                fader_value = fader_value / max_value
            elif fader_value < 0:
                fader_value = fader_value / -min_value
        elif fader.scale_type == "unsigned":
            min_value, max_value = fader.extra["scale_range"]
            fader_value = message.value / max_value
        #print(f"Fader: {fader.name}, Value: {fader_value}")
        
        extra_args = MixerBoard.get_extra_args(fader.name)
        function = MixerBoard.get_function_by_component_name(fader.name)

        # Fader
        if not function:
            return

        if function.get_signed() == False:
            fader_value = (fader_value + 1) / 2

        print("fader_name", fader.name, "fader_number", fader.name.split("_")[-1])
        fader_number = int(fader.name.split("_")[-1])

        list_extra_args = list(extra_args) if extra_args else []
        list_extra_args.insert(0, fader_number)

        extra_args = tuple(list_extra_args)

        try:
            Messages.throttled_process(fader.name, fader_value, function.get_message_rate(), function.call, extra_args)
        except Exception as e:
            print(f"Fader: Error calling function {function} with args {extra_args}: {e}")

    def handle_button_message(message):
        #print("handling button message")
        if message.type == Mapping.MessageType.NOTE_ON.value or message.type == Mapping.MessageType.NOTE_OFF.value:
            velocity = message.velocity
            button = Mapping.BUTTON[message.note]
            # Get GUI name of button
            button_name = Mapping.GUI_BUTTON_TO_COMPONENT[button]
            extra_args = MixerBoard.extra_args[button_name] if button_name in MixerBoard.extra_args else None
            function = MixerBoard.get_function_by_component_name(button_name)


        #list_extra_args = list(extra_args)
        #list_extra_args.insert(0, fader_number)
#
        #extra_args = tuple(list_extra_args)


            if not function:
                return

            list_extra_args = list(extra_args) if extra_args else []
            list_extra_args.insert(0, button_name)

            extra_args = tuple(list_extra_args)


            if velocity == 127:
                # Button DOWN
                try:
                    function.call_down(velocity, *extra_args)
                except Exception as e:
                    print(f"Button Down: Error calling function {function} with args {extra_args}: {e}")
            elif velocity == 0:
                # Button UP
                try:
                    function.call_up(velocity, *extra_args)
                except Exception as e:
                    print(f"Button Up: Error calling function {function} with args {extra_args}: {e}")
                
                


    throttle_tracker = {}
    def throttled_process(name, position, calls_per_second, callback, args=None):
        """
        Throttle the processing of a named entity to a maximum number of calls per second.

        :param name: A unique identifier for the entity (e.g., slider name).
        :param position: The value to process for the entity.
        :param calls_per_second: Maximum allowed calls per second for this entity.
        :param callback: Function to call for processing the position.
        """
        current_time = time.time()
        min_interval = 1 / calls_per_second

        # Initialize tracker for the entity if not already present
        if name not in Messages.throttle_tracker:
            Messages.throttle_tracker[name] = {"last_time": 0, "latest_position": None, "timer_active": False}

        tracker = Messages.throttle_tracker[name]
        elapsed_time = current_time - tracker["last_time"]

        if elapsed_time >= min_interval:
            # Process the current position immediately
            if not args:
                callback(position)
            else:
                callback(position, *args)
            tracker["last_time"] = current_time
            tracker["latest_position"] = None
            tracker["timer_active"] = False
        else:
            # Save the latest position for deferred processing
            tracker["latest_position"] = position
            if not tracker["timer_active"]:
                time_to_next_call = min_interval - elapsed_time
                tracker["timer_active"] = True

                # Schedule the next processing
                def process_deferred():
                    if tracker["latest_position"] is not None:
                        if not args:
                            callback(tracker["latest_position"])
                        else:
                            callback(tracker["latest_position"], *args)
                        tracker["last_time"] = time.time()
                        tracker["latest_position"] = None
                    tracker["timer_active"] = False

                # Use threading or simulate delayed execution
                threading.Timer(time_to_next_call, process_deferred).start()
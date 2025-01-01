from mappings import Mapping

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
        print(f"Knob: {Mapping.KNOB[message.control].name}, Value: {knob_value}")
    
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
        print(f"Fader: {fader.name}, Value: {fader_value}")

    def handle_button_message(message):
        #print("handling button message")
        if message.type == Mapping.MessageType.NOTE_ON.value or message.type == Mapping.MessageType.NOTE_OFF.value:
            velocity = message.velocity
            button = Mapping.BUTTON[message.note]
            if velocity == 127:
                print(f"BTN_UP: {button.extra["shift"] if "shift" in button.extra else ""} {button.extra["fader_effect"] if "fader_effect" in button.extra else ""} {button.name}")
            elif velocity == 0:
                print(f"BTN_DOWN: {button.name}")
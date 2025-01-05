import mido
from enum import Enum


class Mapping:

    # Make enum for message types
    class MessageType(Enum):
        NOTE_ON = "note_on"
        NOTE_OFF = "note_off"
        CONTROL_CHANGE = "control_change"
        PITCHWHEEL = "pitchwheel"
    
    class KnobMessage(Enum):
        UP = 1
        DOWN = 65

    class ComponentType(Enum):
        FADER = "fader"
        KNOB = "knob"
        BUTTON = "button"
    
    class Component:
        def __init__(self, name, component_type, scale_type, extra=None):
            self.name = name
            self.component_type = component_type
            self.scale_type = scale_type
            self.extra = extra
    
    # Define mappings

    # pitchwheel
    FADER = {
        0: Component(name="FADER_0", component_type=ComponentType.FADER, scale_type="signed", extra={"scale_range": (-8192, 8064)}),
        1: Component(name="FADER_1", component_type=ComponentType.FADER, scale_type="signed", extra={"scale_range": (-8192, 8064)}),
        2: Component(name="FADER_2", component_type=ComponentType.FADER, scale_type="signed", extra={"scale_range": (-8192, 8064)}),
        3: Component(name="FADER_3", component_type=ComponentType.FADER, scale_type="signed", extra={"scale_range": (-8192, 8064)}),
        4: Component(name="FADER_4", component_type=ComponentType.FADER, scale_type="signed", extra={"scale_range": (-8192, 8064)}),
        5: Component(name="FADER_5", component_type=ComponentType.FADER, scale_type="signed", extra={"scale_range": (-8192, 8064)}),
        6: Component(name="FADER_6", component_type=ComponentType.FADER, scale_type="signed", extra={"scale_range": (-8192, 8064)}),
        7: Component(name="FADER_7", component_type=ComponentType.FADER, scale_type="signed", extra={"scale_range": (-8192, 8064)}),
        ### Shifted Faders ###
        40: Component(name="FADER_8",  component_type=ComponentType.FADER, scale_type="unsigned", extra={"scale_range": (0, 127)}),
        41: Component(name="FADER_9",  component_type=ComponentType.FADER, scale_type="unsigned", extra={"scale_range": (0, 127)}),
        42: Component(name="FADER_10", component_type=ComponentType.FADER, scale_type="unsigned", extra={"scale_range": (0, 127)}),
        43: Component(name="FADER_11", component_type=ComponentType.FADER, scale_type="unsigned", extra={"scale_range": (0, 127)}),
        44: Component(name="FADER_12", component_type=ComponentType.FADER, scale_type="unsigned", extra={"scale_range": (0, 127)}),
        45: Component(name="FADER_13", component_type=ComponentType.FADER, scale_type="unsigned", extra={"scale_range": (0, 127)}),
        46: Component(name="FADER_14", component_type=ComponentType.FADER, scale_type="unsigned", extra={"scale_range": (0, 127)}),
        47: Component(name="FADER_15", component_type=ComponentType.FADER, scale_type="unsigned", extra={"scale_range": (0, 127)}),

    }


    # control_change
    KNOB = {
        16: Component(name="KNOB_0", component_type=ComponentType.KNOB, scale_type="binary", extra={"accepted_values": (KnobMessage.UP.value, KnobMessage.DOWN.value)}),
        17: Component(name="KNOB_1", component_type=ComponentType.KNOB, scale_type="binary", extra={"accepted_values": (KnobMessage.UP.value, KnobMessage.DOWN.value)}),
        18: Component(name="KNOB_2", component_type=ComponentType.KNOB, scale_type="binary", extra={"accepted_values": (KnobMessage.UP.value, KnobMessage.DOWN.value)}),
        19: Component(name="KNOB_3", component_type=ComponentType.KNOB, scale_type="binary", extra={"accepted_values": (KnobMessage.UP.value, KnobMessage.DOWN.value)}),
        20: Component(name="KNOB_4", component_type=ComponentType.KNOB, scale_type="binary", extra={"accepted_values": (KnobMessage.UP.value, KnobMessage.DOWN.value)}),
        21: Component(name="KNOB_5", component_type=ComponentType.KNOB, scale_type="binary", extra={"accepted_values": (KnobMessage.UP.value, KnobMessage.DOWN.value)}),
        22: Component(name="KNOB_6", component_type=ComponentType.KNOB, scale_type="binary", extra={"accepted_values": (KnobMessage.UP.value, KnobMessage.DOWN.value)}),
        23: Component(name="KNOB_7", component_type=ComponentType.KNOB, scale_type="binary", extra={"accepted_values": (KnobMessage.UP.value, KnobMessage.DOWN.value)}),
        ### Shifted Knobs ###
        30: Component(name="KNOB_8",  component_type=ComponentType.KNOB, scale_type="linear", extra={"scale_range": (0, 127)}),
        31: Component(name="KNOB_9",  component_type=ComponentType.KNOB, scale_type="linear", extra={"scale_range": (0, 127)}),
        32: Component(name="KNOB_10", component_type=ComponentType.KNOB, scale_type="linear", extra={"scale_range": (0, 127)}),
        33: Component(name="KNOB_11", component_type=ComponentType.KNOB, scale_type="linear", extra={"scale_range": (0, 127)}),
        34: Component(name="KNOB_12", component_type=ComponentType.KNOB, scale_type="linear", extra={"scale_range": (0, 127)}),
        35: Component(name="KNOB_13", component_type=ComponentType.KNOB, scale_type="linear", extra={"scale_range": (0, 127)}),
        36: Component(name="KNOB_14", component_type=ComponentType.KNOB, scale_type="linear", extra={"scale_range": (0, 127)}),
        37: Component(name="KNOB_15", component_type=ComponentType.KNOB, scale_type="linear", extra={"scale_range": (0, 127)}),
    }

    KNOB_MESSAGE = {
        65: KnobMessage.DOWN,
        64: KnobMessage.UP,
    }

    # note_on/note_off + velocity
    BUTTON = {
            16: Component(name="MUTE_0", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "MUTE"}),
            17: Component(name="MUTE_1", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "MUTE"}),
            18: Component(name="MUTE_2", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "MUTE"}),
            19: Component(name="MUTE_3", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "MUTE"}),
            20: Component(name="MUTE_4", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "MUTE"}),
            21: Component(name="MUTE_5", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "MUTE"}),
            22: Component(name="MUTE_6", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "MUTE"}),
            23: Component(name="MUTE_7", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "MUTE"}),

            8:  Component(name="SOLO_0", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "SOLO"}),
            9:  Component(name="SOLO_1", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "SOLO"}),
            10: Component(name="SOLO_2", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "SOLO"}),
            11: Component(name="SOLO_3", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "SOLO"}),
            12: Component(name="SOLO_4", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "SOLO"}),
            13: Component(name="SOLO_5", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "SOLO"}),
            14: Component(name="SOLO_6", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "SOLO"}),
            15: Component(name="SOLO_7", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "SOLO"}),

            0: Component(name="REC_ARM_0", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "REC"}),
            1: Component(name="REC_ARM_1", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "REC"}),
            2: Component(name="REC_ARM_2", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "REC"}),
            3: Component(name="REC_ARM_3", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "REC"}),
            4: Component(name="REC_ARM_4", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "REC"}),
            5: Component(name="REC_ARM_5", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "REC"}),
            6: Component(name="REC_ARM_6", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "REC"}),
            7: Component(name="REC_ARM_7", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "REC"}),

            24: Component(name="SELECT_0", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "kSEL"}),
            25: Component(name="SELECT_1", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "SEL"}),
            26: Component(name="SELECT_2", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "SEL"}),
            27: Component(name="SELECT_3", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "SEL"}),
            28: Component(name="SELECT_4", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "SEL"}),
            29: Component(name="SELECT_5", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "SEL"}),
            30: Component(name="SELECT_6", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "SEL"}),
            31: Component(name="SELECT_7", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "fader_effect": "SEL"}),


            94: Component(name="PLAY", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "LEFT"}),
            93: Component(name="STOP", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "LEFT"}),
            95: Component(name="REC", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "LEFT"}),
            91: Component(name="REWIND", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "LEFT"}),
            92: Component(name="FAST_FORWARD", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "LEFT"}),
            46: Component(name="CHANNEL_LEFT", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "LEFT"}),
            47: Component(name="CHANNEL_RIGHT", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "LEFT"}),
            96: Component(name="UP", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "LEFT"}),
            97: Component(name="DOWN", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "LEFT"}),
            98: Component(name="LEFT", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "LEFT"}),
            99: Component(name="RIGHT", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "LEFT"}),
        
            52: Component(name="PLAY", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "RIGHT"}),
            53: Component(name="STOP", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "RIGHT"}),
            54: Component(name="REC", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "RIGHT"}),
            55: Component(name="REWIND", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "RIGHT"}),
            56: Component(name="FAST_FORWARD", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "RIGHT"}),
            57: Component(name="CHANNEL_LEFT", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "RIGHT"}),
            58: Component(name="CHANNEL_RIGHT", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "RIGHT"}),
            59: Component(name="UP", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "RIGHT"}),
            60: Component(name="DOWN", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "RIGHT"}),
            61: Component(name="LEFT", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "RIGHT"}),
            62: Component(name="RIGHT", component_type=ComponentType.BUTTON, scale_type="binary", extra={"accepted_values": (0, 127), "shift": "RIGHT"}),
    }

    GUI_BUTTON_TO_COMPONENT = {
        # Mute
        BUTTON[16]: "BUTTON_0_0",
        BUTTON[17]: "BUTTON_1_0",
        BUTTON[18]: "BUTTON_2_0",
        BUTTON[19]: "BUTTON_3_0",
        BUTTON[20]: "BUTTON_4_0",
        BUTTON[21]: "BUTTON_5_0",
        BUTTON[22]: "BUTTON_6_0",
        BUTTON[23]: "BUTTON_7_0",

        # Solo
        BUTTON[8]: "BUTTON_0_1",
        BUTTON[9]: "BUTTON_1_1",
        BUTTON[10]: "BUTTON_2_1",
        BUTTON[11]: "BUTTON_3_1",
        BUTTON[12]: "BUTTON_4_1",
        BUTTON[13]: "BUTTON_5_1",
        BUTTON[14]: "BUTTON_6_1",
        BUTTON[15]: "BUTTON_7_1",

        # Rec Arm
        BUTTON[0]: "BUTTON_0_2",
        BUTTON[1]: "BUTTON_1_2",
        BUTTON[2]: "BUTTON_2_2",
        BUTTON[3]: "BUTTON_3_2",
        BUTTON[4]: "BUTTON_4_2",
        BUTTON[5]: "BUTTON_5_2",
        BUTTON[6]: "BUTTON_6_2",
        BUTTON[7]: "BUTTON_7_2",

        # Select
        BUTTON[24]: "BUTTON_0_3",
        BUTTON[25]: "BUTTON_1_3",
        BUTTON[26]: "BUTTON_2_3",
        BUTTON[27]: "BUTTON_3_3",
        BUTTON[28]: "BUTTON_4_3",
        BUTTON[29]: "BUTTON_5_3",
        BUTTON[30]: "BUTTON_6_3",
        BUTTON[31]: "BUTTON_7_3",

        # Control
        BUTTON[94]: "CONTROL_0",
        BUTTON[93]: "CONTROL_1",
        BUTTON[95]: "CONTROL_2",
        BUTTON[91]: "CONTROL_3",
        BUTTON[92]: "CONTROL_4",
        BUTTON[46]: "CONTROL_5",
        BUTTON[47]: "CONTROL_6",
        BUTTON[96]: "CONTROL_7",
        BUTTON[97]: "CONTROL_8",
        BUTTON[98]: "CONTROL_9",
        BUTTON[99]: "CONTROL_10",

    }
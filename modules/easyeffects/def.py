# List of function definitions for the EasyEffects plugin

from modules.base import KnobFunction, FaderFunction, ButtonFunction, DynamicArgs
from modules.easyeffects.equalizer import decrement_fader_shift, increment_fader_shift, update_eq_gain
from modules.easyeffects.criteria import non_negative

export = []

# Fader EQ
faderEQ = FaderFunction("Fader EQ", "EasyEffects", True, 10, update_eq_gain, [DynamicArgs("EQ Number", int, 0, "Equalizer Effect Number")])
export.append(faderEQ)

# Decrement Fader Shift
decrementFaderShift = ButtonFunction("Decrement Fader Shift", "EasyEffects", decrement_fader_shift)
export.append(decrementFaderShift)

# Increment Fader Shift
incrementFaderShift = ButtonFunction("Increment Fader Shift", "EasyEffects", increment_fader_shift)
export.append(incrementFaderShift)
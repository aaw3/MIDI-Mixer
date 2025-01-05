from modules.easyeffects.dconf.dconf_utils import write

# Shift faders right to multiply by 8 to access the next 8 faders in the EQ
fader_shift = 0

def decrement_fader_shift():
    global fader_shift
    fader_shift -= 8
    if fader_shift < 0:
        fader_shift = 0

    print("Fader shift is now: ", fader_shift)

def increment_fader_shift():
    global fader_shift
    fader_shift += 8
    print("Fader shift is now: ", fader_shift)

def update_eq_gain(gain: float, fader_number: int, equalizer_number: int):
    band_number = fader_number
    gain = gain * 36
    print("Parameters: ", gain, equalizer_number, band_number)
    print("Fader shift: ", fader_shift)
    print("String: ", f"/com/github/wwmm/easyeffects/streamoutputs/equalizer/{equalizer_number}/leftchannel/band{str(band_number + fader_shift)}-gain", str(gain))
    print("Calling with values: ", gain, equalizer_number, band_number)
    write(f"/com/github/wwmm/easyeffects/streamoutputs/equalizer/{equalizer_number}/leftchannel/band{str(band_number + fader_shift)}-gain", str(gain))
    write(f"/com/github/wwmm/easyeffects/streamoutputs/equalizer/{equalizer_number}/rightchannel/band{str(band_number + fader_shift)}-gain", str(gain))
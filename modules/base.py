class DynamicArgs:
    """
    DynamicArgs class is used to store the dynamic argument details.

    :param name: The name of the dynamic argument
    :param type: The type of the dynamic argument
    :param default: The default value of the dynamic argument
    :param description: The description of the dynamic argument
    :param criteria_callback: Function that returns True if the value returned from the checkbox is valid, otherwise False
    """

    def __init__(self, name: str, type: str, default, description: str, criteria_callback=None, options=None):
        self.name = name
        self.type = type
        self.default = default
        self.description = description
        self.criteria_callback = criteria_callback
        self.options = options

    def __str__(self):
        return f"Dynamic Argument: {self.name}, {self.type}, {self.default}, {self.description}"

    def get_name(self):
        return self.name

    def get_type(self):
        return self.type

    def get_default(self):
        return self.default

    def get_description(self):
        return self.description

    def get_criteria_callback(self):
        return self.criteria_callback

    def get_options(self):
        return self.options


class ControlFunction:
    """
    Base class for common control functions.

    :param name: The name of the control function
    :param plugin_name: The name of the plugin associated with the control function
    :param callback_extra_args: Extra argument definitions for callbacks
    """

    def __init__(self, name: str, plugin_name: str, callback_extra_args: list[DynamicArgs] = None):
        self.name = name
        self.plugin_name = plugin_name
        self.callback_extra_args = callback_extra_args

    def __str__(self):
        return f"{self.plugin_name}: {self.name}"

    def get_type_name(self):
        return type(self).__name__

    def get_name(self):
        return self.name

    def get_plugin_name(self):
        return self.plugin_name

    def get_callback_extra_args(self):
        return self.callback_extra_args


class KnobFunction(ControlFunction):
    """
    KnobFunction class for knob-specific details.

    :param callback: The callback function for the knob
    """

    def __init__(self, name: str, plugin_name: str, callback, callback_extra_args: list[DynamicArgs] = None):
        super().__init__(name, plugin_name, callback_extra_args)
        self.callback = callback

    def call(self, *args):
        self.callback(*args)


class FaderFunction(ControlFunction):
    """
    FaderFunction class for fader-specific details.

    :param signed: Whether the fader is signed
    :param callback: The callback function for the fader
    :param samples: The number of samples to use for the fader, 16000 will cause lag
    """

    def __init__(self, name: str, plugin_name: str, signed: bool, message_rate: int, callback, callback_extra_args: list[DynamicArgs] = None):
        super().__init__(name, plugin_name, callback_extra_args)
        self.signed = signed
        self.callback = callback
        self.message_rate = message_rate

    def get_signed(self):
        return self.signed

    def get_message_rate(self):
        return self.message_rate

    def call(self, *args):
        self.last_value = args[0]
        self.callback(*args)


class ButtonFunction(ControlFunction):
    """
    ButtonFunction class for button-specific details.

    :param callback_down: The callback function for button press
    :param callback_up: The callback function for button release
    """

    def __init__(self, name: str, plugin_name: str, callback_down, callback_up=None, callback_extra_args: list[DynamicArgs] = None):
        super().__init__(name, plugin_name, callback_extra_args=callback_extra_args)
        self.callback_down = callback_down
        self.callback_up = callback_up

    def call_down(self, *args):
        if self.callback_down:
            self.callback_down(*args)

    def call_up(self, *args):
        if self.callback_up:
            self.callback_up(*args)

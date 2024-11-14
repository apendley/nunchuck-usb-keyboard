from adafruit_hid.keycode import Keycode

# Key codes can be found at:
# https://docs.circuitpython.org/projects/hid/en/stable/api.html#adafruit_hid.keycode.Keycode

nunchuck_config = {
    # Key mapping for each cardinal direction.
    # Set to None (or omit the key/value pair entirely) to leave a direction unmapped.
    "up":    Keycode.UP_ARROW,
    "right": Keycode.RIGHT_ARROW,
    "down":  Keycode.DOWN_ARROW,
    "left":  Keycode.LEFT_ARROW,

    # Key mapping for each button.
    # Set to None (or omit the key/value pair entirely) to leave a button unmapped.
    "c":     Keycode.C,
    "z":     Keycode.Z,

    # Dead zones for each axis.
    # Default if omitted or set to None is 65.
    "x_dead_zone": 65,
    "y_dead_zone": 65,

    # Delay between each nunchuck read, for simple debouncing.
    # Default if omitted or set to None is 1.0 / 60.0, or ~60fps.
    "debounce_time": 1.0 / 60.0,

    # Print out debug information to serial output.
    # Default if omitted or None is False.
    "debug": False
}

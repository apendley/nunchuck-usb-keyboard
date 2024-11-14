import supervisor
import time
import board
import adafruit_nunchuk
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

########################
# I2C:
# Many Adafruit boards with a Stemma QT port (such as
# the QT Py RP2040 and the Trinkey QT2040) use board.STEMMA_I2C().
# Other boards may use board.I2C(), or a custom I2C configuration.
########################
i2c = board.STEMMA_I2C()

########################
# Nunchuck
########################
nunchuck = None

print("\nLooking for nunchuck...")
while nunchuck is None:
    try:
        nunchuck = adafruit_nunchuk.Nunchuk(i2c)
        print("Nunchuck found!")
    except:
        # Try again a second
        time.sleep(1.0)

########################
# Keyboard
########################
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

########################
# Nunchuck config
########################
from nunchuck_config import nunchuck_config

def get_config_value(key, default=None):
    if key in nunchuck_config.keys():
        return nunchuck_config[key]
    else:
        return default

key_up = get_config_value("up")
key_left = get_config_value("left")
key_down = get_config_value("down")
key_right = get_config_value("right")
key_z = get_config_value("z")
key_c = get_config_value("c")

x_dead_zone = get_config_value("x_dead_zone", default=65)
y_dead_zone = get_config_value("y_dead_zone", default=65)
debounce_time = get_config_value("debounce_time", default=1.0 / 60.0)
is_debugging = get_config_value("debug", default=False)

########################
# Helpers
########################
def null_print(*argv):
    pass

if is_debugging:
    debug_print = print
else:
    debug_print = null_print

def get_axis_state(axis_value, axis_dead_zone):
    if abs(axis_value) > axis_dead_zone:
        if axis_value > 0:
            return 1
        else:
            return -1
    else:
        return 0 

def update_axis_keys(axis_name, axis_value, axis_state, axis_state_prev, positive_key, negative_key):
    if axis_state != axis_state_prev:
        if axis_state_prev > 0:
            debug_print("release positive", axis_name, "axis key, axis value:", axis_value)
            if positive_key is not None:
                keyboard.release(positive_key)
        elif axis_state_prev < 0:
            debug_print("release negative", axis_name, "axis key, axis value:", axis_value)
            if negative_key is not None:
                keyboard.release(negative_key)

        if axis_state > 0:
            debug_print("press positive", axis_name, "axis key, axis value:", axis_value)
            if positive_key is not None:
                keyboard.press(positive_key)
        elif axis_state < 0:
            debug_print("press negative", axis_name, "axis key, axis value:", axis_value)
            if negative_key is not None:
                keyboard.press(negative_key)

def update_button_key(button_name, button_state, button_state_prev, button_key):
    if button_state != button_state_prev:
        debug_print("button", button_name, "changed, current:", button_state, ", prev:", button_state_prev)

        if button_key is not None:
            if button_state:
                keyboard.press(button_key)
            else:
                keyboard.release(button_key)

########################
# Program state
########################
# Axis states: if the state is zero, the axis is not pressed either direction.
# Otherwise, state is 1 or -1 to indicate that either direction on that axis is "pressed".
x_axis_state = 0
y_axis_state = 0

# button states, True if pressed, False if not.
c_button_state = False
z_button_state = False

########################
# Main loop
########################
debug_print("\nNunchuck config:", nunchuck_config)

while True:
    try:
        nunchuck_values = nunchuck.values
    except:
        # Reload the program until the nunchuck is detected
        print("Error reading nunchuck, reloading...")
        supervisor.reload()

    # Save previous state
    x_axis_state_prev = x_axis_state
    y_axis_state_prev = y_axis_state
    c_button_state_prev = c_button_state
    z_button_state_prev = z_button_state

    # Get new state from nunchuck
    x_axis = nunchuck_values.joystick.x - 127
    x_axis_state = get_axis_state(x_axis, x_dead_zone)
    y_axis = nunchuck_values.joystick.y - 127
    y_axis_state = get_axis_state(y_axis, y_dead_zone)    
    c_button_state = nunchuck_values.buttons.C
    z_button_state = nunchuck_values.buttons.Z

    # Press simulated direction keys based on axis states
    update_axis_keys("x", x_axis, x_axis_state, x_axis_state_prev, key_right, key_left)
    update_axis_keys("y", y_axis, y_axis_state, y_axis_state_prev, key_up, key_down)

    # Press keys that are mapped to the nunchuck buttons
    update_button_key("C", c_button_state, c_button_state_prev, key_c)
    update_button_key("Z", z_button_state, z_button_state_prev, key_z)

    # Use time.sleep as a simple debounce mechanism
    time.sleep(debounce_time)

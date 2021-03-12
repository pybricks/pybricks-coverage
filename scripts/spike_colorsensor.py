#
# source spike_colorsensor.py
#

"""
A test for the Spike Color Sensor

Test designed to
    run on the TechnicHub
    use port-B (just to take a port) Port-A seemed too obvious

First phase:
    functions for each of the documented functions and parameters
"""


from pybricks import version
from pybricks.hubs import TechnicHub
from pybricks.parameters import Color, Port
from pybricks.pupdevices import ColorSensor
from pybricks.tools import wait

# instantiate the devices
hub = TechnicHub()
sensor = ColorSensor(Port.B)

# show version and battery level as reference
print(version)
print("hub_battery_voltage:", hub.battery.voltage(), "mV")

hub.light.on(Color.BLUE)
sensor.lights.off()

# tool(s)


def strFixed(instr):
    __outstr = "%-36s" % instr
    return __outstr


# detect color

"""
Parameters: surface (bool)
 – Choose true  to scan the color of objects and surfaces.
 - Choose false to scan the color of screens and other external light sources.
"""


def t01_color_surface_default():
    __result = sensor.color()
    return strFixed("t01_color_surface_default") + str(__result)


def t02_color_surface_True():
    __result = sensor.color(surface=True)
    return strFixed("t02_color_surface_True") + str(__result)


def t03_color_surface_False():
    __result = sensor.color(surface=False)
    return strFixed("t03_color_surface_False") + str(__result)


def t04_color_surface_WRONG():
    __result = sensor.color(surface="WRONG")
    return strFixed("t04_color_surface_\"WRONG\"") + str(__result)


"""
reflection()
Measures the reflection of a surface.

Returns:
 Reflection, ranging from 0.0 (no reflection) to 100.0 (high reflection).

Return type:    percentage: %
"""


def t10_reflection():
    __result = sensor.reflection()
    return strFixed("t10_reflection") + str(__result)


# No parameter documented; should report something like this:
# TypeError: function takes 0 positional arguments but 1 were given
def t11_reflection_NoParmDocumented():
    try:
        __result = sensor.reflection(None, None)  # ("NoParmDocumented")
    except Exception as e:
        __result = e
    return strFixed("t11_reflection_NoParmDocumented") + str(__result)
# The number of parameters in the error message may be incorrect
# https://docs.micropython.org/en/latest/genrst/core_language.html
#       #error-messages-for-methods-may-display-unexpected-argument-counts


"""
ambient()
Measures the ambient light intensity.

Returns:    Ambient light intensity, ranging from 0 (dark) to 100 (bright).
Return type:    percentage: %
"""


def t12_ambient():
    __result = sensor.ambient()
    return strFixed("t12_ambient") + str(__result)


# No parameter documented; should report something like this:
# TypeError: function takes 0 positional arguments but 1 were given
def t13_ambient_NoParmDocumented():
    try:
        __result = sensor.ambient(None, None)  # ("NoParmDocumented")
    except Exception as e:
        __result = e
    return strFixed("t13_ambient_NoParmDocumented") + str(__result)
# The number of parameters in the error message may be incorrect
# https://docs.micropython.org/en/latest/genrst/core_language.html
#    #error-messages-for-methods-may-display-unexpected-argument-counts


# Advanced color sensing

"""
hsv(surface=True)
Scans the color of a surface or an external light source.

This method is similar to color(),
but it gives the full range of hue, saturation and brightness values,
instead of rounding it to the nearest detectable color.

Parameters: surface (bool)
 – Choose true to scan the color of objects and surfaces.
 - Choose false to scan the color of screens and other external light sources.
Returns:    Measured color.
The color is described by
a hue (0–359), a saturation (0–100), and a brightness value (0–100).

Return type:    Color
"""


def t20_hsv_surface_default():
    __result = sensor.hsv()
    return strFixed("t20_hsv_surface_default") + str(__result)


def t21_hsv_surface_True():
    __result = sensor.hsv(surface=True)
    return strFixed("t21_hsv_surface_True") + str(__result)


def t22_hsv_surface_False():
    __result = sensor.hsv(surface=False)
    return strFixed("t22_hsv_surface_False") + str(__result)


"""
detectable_colors(colors)
Configures which colors the color() method should detect.

Specify only colors that you wish to detect in your application.
This way, the full-color measurements are
rounded to the nearest desired color, and other colors are ignored.
This improves reliability.

If you give no arguments,
the currently chosen colors will be returned as a tuple.

Parameters: colors (list)
 – List of Color objects: the colors that you want to detect.
You can pick standard colors such as Color.MAGENTA,
or provide your own colors like
   Color(h=348, s=96, v=40, name='MY_MAGENTA_BRICK')
for even better results.
You measure your own colors with the hsv() method.
"""

# correct Color values

green = Color(h=132, s=94, v=26, name='GREEN_BRICK')
magenta = Color(h=348, s=96, v=40, name='MAGENTA_BRICK')
brown = Color(h=17, s=78, v=15, name='BROWN_BRICK')
red = Color(h=359, s=97, v=39, name='RED_BRICK')
my_colors = (green, magenta, brown, red, None)
sensor.detectable_colors(my_colors)


# Limits: Hue (0–359) Saturation (0–100) brightness Value (0–100)
# at the moment there is **no** validation of the values given here
w1_max = Color(h=359, s=100, v=100)
w2_max = Color(h=1000, s=1000, v=1100)
w3Err = Color(h=36, s=-1, v=25)
error_colors = (w1_max, w2_max, w3Err, None)
sensor.detectable_colors(error_colors)


def t30_color_detectable():
    __result = sensor.color()
    print("\t\tw1_max", w1_max)
    print("\t\tw2_max", w2_max)
    print("\t\tw3Err ", w3Err)
    return strFixed("t30_color_detectable") + str(__result)


# Built-in lights
"""
lights.on(brightness)
Turns on the lights at the specified brightness.

Parameters: brightness (tuple of brightness: %)
 – Brightness of each light, in the order shown above.
If you give one brightness value instead of a tuple,
all lights get the same brightness.

lights.off()

"""


def t40_lights_on():
    # Turn on all 3 lights at 100% brightness.
    __result = "\"all 3 sensor lights on\""
    sensor.lights.on(100)
    wait(100)  # wait a bit to be able to see
    return strFixed("t40_lights_on") + str(__result)


def t41_lights_on_at_zero_percent():
    # Turn off all 3 lights using 0% brightness.
    __result = "\"all 3 sensor lights on at ZERO %\""
    sensor.lights.on(0)
    wait(100)  # wait a bit to be able to see
    return strFixed("t41_lights_on_at_zero_percent") + str(__result)


def t42_lights_off():
    # Turn off all 3 lights.
    __result = "\"all 3 sensor lights off\""
    sensor.lights.off()
    wait(100)  # wait a bit to be able to see
    return strFixed("t42_lights_off") + str(__result)


def t43_lights_on_one_at_a_time():
    # Turn on one light at a time, at half the brightness.
    # Do this for all 3 lights and repeat that 5 times.
    __result = "\"rotate sensor lights\""
    for i in range(5):
        sensor.lights.on(50, 0, 0)
        wait(100)  # wait a bit to be able to see
        sensor.lights.on(0, 50, 0)
        wait(100)  # wait a bit to be able to see
        sensor.lights.on(0, 0, 50)
        wait(100)  # wait a bit to be able to see
    return strFixed("t43_lights_on_one_at_a_time") + str(__result)


def t44_lights_on_wrong_values():
    # value can be from zero to 100 for brightness.
    __result = "\"lights on at more than 100% and negative\""
    sensor.lights.on(256, 0, 0)
    wait(100)  # wait a bit to be able to see
    sensor.lights.on(0, 256, 0)
    wait(100)  # wait a bit to be able to see
    sensor.lights.on(0, -80, 256)
    wait(100)  # wait a bit to be able to see
    return strFixed("t44_lights_on_wrong_values") + str(__result)


def t45_lights_off_too_many_parm():
    # lights.off expects NO parameter.
    __result = "\"lights off: refuse any parameter\""
    try:
        sensor.lights.off(256, -10, 990)  # ("NoParmDocumented")
    except Exception as e:
        # print("t13 exception", e)
        __result = e
    return strFixed("t45_lights_off_too_many_parm") + str(__result)
# The number of parameters in the error message may be incorrect


# Run the tests
print(t01_color_surface_default())
print(t02_color_surface_True())
print(t03_color_surface_False())
print(t04_color_surface_WRONG())

print(t10_reflection())
print(t11_reflection_NoParmDocumented())

print(t12_ambient())
print(t13_ambient_NoParmDocumented())

# do 3 to show the results here are not stable
print(t20_hsv_surface_default())
print(t20_hsv_surface_default())
print(t20_hsv_surface_default())

print(t21_hsv_surface_True())

print(t22_hsv_surface_False())

print(t30_color_detectable())

print(t40_lights_on())
print(t41_lights_on_at_zero_percent())
print(t42_lights_off())
print(t43_lights_on_one_at_a_time())
print(t44_lights_on_wrong_values())
print(t45_lights_off_too_many_parm())

sensor.lights.off()  # save the battery a bit between tests
wait(1000)

# ########################################

print("end of test")

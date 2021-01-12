from pybricks.hubs import InventorHub
from pybricks.tools import wait, StopWatch
from pybricks.parameters import Icon, Side
from pybricks.geometry import Matrix
from pybricks import version

print(version)

from urandom import randint

hub = InventorHub()

# Display random pixels, in and out of bounds
ITERATIONS = 5000
watch = StopWatch()
for i in range(ITERATIONS):
    hub.display.pixel(row=randint(-30, 30), column=randint(-30, 30), brightness=randint(-20, 150))
watch.pause()
print("Showing", ITERATIONS, "random pixels took", watch.time(), "ms, or ", watch.time()/ITERATIONS*1000, "us per pixel.")

# Turn display off
hub.display.off()

# Display some images in different orientations
for side in (Side.TOP, Side.LEFT, Side.BOTTOM, Side.RIGHT, Side.FRONT):
    hub.display.orientation(side)
    hub.display.image(Icon.UP)
    wait(500)

# Display image composites
hub.display.image(Icon.ARROW_LEFT_DOWN + Icon.ARROW_RIGHT_UP)
wait(1000)

# Display images at different brightness
for i in range(-5, 105):
    hub.display.image(Icon.HEART / 100 * i)
    wait(30)

# Custom image as list
PYRAMID_LIST = Matrix([
    [100, 100, 100, 100, 100],
    [100, 50,  50,  50,  100],
    [100, 50,  0,   50,  100],
    [100, 50,  50,  50,  100],
    [100, 100, 100, 100, 100],
])

# Display the square and invert it.
hub.display.image(PYRAMID_LIST)
wait(1000)

# Custom image as Matrix
hub.display.image(Icon.SQUARE - Matrix(PYRAMID_LIST)/2)
wait(1000)

# Create a list of intensities from 0 to 100 and back.
brightness = list(range(0, 100, 4)) + list(range(100, 0, -4))

# Create an animation of the heart icon with changing brightness.
hub.display.animate([Icon.HEART * i/100 for i in brightness], interval=30)
wait(4000)

# Display all characters.
for i in range(32, 127):
    hub.display.char(char=chr(i))
    wait(200)

# Display text, one letter at a time.
hub.display.text('Hello, world!')
hub.display.text('Hello, world!', on=50, off=10)

# Display numbers as int and float
for i in range(-150, 150):
    hub.display.number(i)
    hub.display.number(i + 0.1)
    wait(100)


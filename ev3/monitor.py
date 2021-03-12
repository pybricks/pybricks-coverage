#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop, Button
from pybricks.tools import wait
from pybricks.messaging import BluetoothMailboxServer, TextMailbox


SPEED = 100


class SpikeMonitor:

    def __init__(self):
        # Initialize devices.
        self.ev3 = EV3Brick()
        self.usb_motor = Motor(Port.D)
        self.left_motor = Motor(Port.B)
        self.right_motor = Motor(Port.A)

        # Relax target tolerances so the motion is considered complete even
        # if off by a few more degrees than usual. This way, it won't block.
        # But set speed tolerance strict, so we move at least until fully
        # stopped, which is when we are pressing the button.
        self.left_motor.control.target_tolerances(speed=0, position=30)
        self.right_motor.control.target_tolerances(speed=0, position=30)

        # Run all motors to end points.
        self.targets = {
            'usb_in': self.usb_motor.run_until_stalled(-SPEED, duty_limit=50) + 10,
            'usb_out': self.usb_motor.run_until_stalled(SPEED, duty_limit=50) - 10,
            'center_pressed': self.left_motor.run_until_stalled(-SPEED, duty_limit=50) + 10,
            'left_pressed': self.left_motor.run_until_stalled(SPEED, duty_limit=50),
            'right_pressed': self.right_motor.run_until_stalled(SPEED, duty_limit=50) + 10,
            'bluetooth_pressed': self.right_motor.run_until_stalled(-SPEED, duty_limit=50) - 10,
        }

        # Set other targets between end points.
        self.targets['left_released'] = (self.targets['left_pressed'] + self.targets['center_pressed']) / 2
        self.targets['center_released'] = self.targets['left_released']

        self.targets['right_released'] = (self.targets['right_pressed'] + self.targets['bluetooth_pressed']) / 2
        self.targets['bluetooth_released'] = self.targets['right_released']

        # Get in initial state.
        self.press_center(False)
        self.press_bluetooth(False)
        self.insert_usb(False)

        # Turn the hub off.
        self.shutdown()
        self.ev3.speaker.beep()

    def insert_usb(self, insert):
        key = 'usb_in' if insert else 'usb_out'
        self.usb_motor.run_target(SPEED, self.targets[key])

    def press_left(self, press):
        if press:
            self.left_motor.run_target(SPEED, self.targets['left_pressed'])
            self.left_motor.dc(80)
        else:
            while abs(self.left_motor.speed()) > 100:
                wait(10)
            self.left_motor.run_target(SPEED, self.targets['left_released'], Stop.COAST)

    def press_center(self, press):
        if press:
            self.left_motor.run_target(SPEED, self.targets['center_pressed'])
        else:
            self.left_motor.run_target(SPEED, self.targets['center_released'], Stop.COAST)

    def press_right(self, press):
        if press:
            self.right_motor.run_target(SPEED, self.targets['right_pressed'])
        else:
            self.right_motor.run_target(SPEED, self.targets['right_released'], Stop.COAST)
        
    def press_bluetooth(self, press):
        if press:
            self.right_motor.run_target(SPEED, self.targets['bluetooth_pressed'])
            self.right_motor.dc(-100)
        else:
            while abs(self.right_motor.speed()) > 100:
                wait(10)
            self.right_motor.run_target(SPEED, self.targets['bluetooth_released'], Stop.COAST)

    def click_center(self, duration=100):
        self.press_center(False)
        self.press_center(True)
        wait(duration)
        self.press_center(False)

    def click_bluetooth(self, duration=200):
        self.press_bluetooth(False)
        self.press_bluetooth(True)
        wait(duration)
        self.press_bluetooth(False)

    def click_left(self, duration=100):
        self.press_left(False)
        self.press_left(True)
        wait(duration)
        self.press_left(False)

    def click_right(self, duration=100):
        self.press_right(False)
        self.press_right(True)
        wait(duration)
        self.press_right(False)

    def activate_dfu(self):
        self.press_bluetooth(True)
        wait(600)
        self.insert_usb(True)
        wait(8000)
        self.press_bluetooth(False)

    def shutdown(self):
        self.click_center(duration=4000)

    def test_buttons(self):
        while True:
            while True:
                pressed = self.ev3.buttons.pressed()
                if any(pressed):
                    break

            if Button.CENTER in pressed:
                self.click_center()
            elif Button.UP in pressed:
                self.click_bluetooth()
            elif Button.LEFT in pressed:
                self.click_left()
            elif Button.RIGHT in pressed:
                self.click_right()
            elif Button.DOWN in pressed:
                break

            while any(self.ev3.buttons.pressed()):
                wait(10)


if __name__ == "__main__":
    spike = SpikeMonitor()
    spike.test_buttons()


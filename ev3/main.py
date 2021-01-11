#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait
from pybricks.messaging import BluetoothMailboxServer, TextMailbox

SPEED = 100

class SpikeManager:

    def __init__(self):
        # Initialize all devices
        self.ev3 = EV3Brick()
        self.usb_motor = Motor(Port.D)
        self.bt_motor = Motor(Port.C)
        self.left_button_motor = Motor(Port.B)
        self.right_button_motor = Motor(Port.A)

        # Reset all motor to mechanical stop
        self.usb_motor.run_until_stalled(-SPEED, duty_limit=50)
        self.bt_motor.run_until_stalled(-SPEED, duty_limit=20)
        self.left_button_motor.run_until_stalled(-SPEED, duty_limit=100)
        self.right_button_motor.run_until_stalled(SPEED, duty_limit=30)
        wait(500)

        # Reset the angles
        self.usb_motor.reset_angle(10)
        self.bt_motor.reset_angle(-20)
        self.left_button_motor.reset_angle(-25)
        self.right_button_motor.reset_angle(20)

        # Go to neutral position
        self.reset()

    def reset(self):
        self.usb_motor.run_target(SPEED, 0)
        self.bt_motor.run_target(SPEED, 0)
        self.left_button_motor.run_target(SPEED, 0)
        self.right_button_motor.run_target(SPEED, 0)

    def insert_usb(self):
        self.usb_motor.run_target(SPEED, 70, then=Stop.COAST)

    def remove_usb(self):
        self.usb_motor.run_target(SPEED, 0, then=Stop.COAST)

    def activate_dfu(self):
        self.bt_motor.dc(-40)
        wait(600)
        self.insert_usb()
        wait(8000)
        self.bt_motor.run_target(SPEED, 0)

    def shutdown(self):
        self.left_button_motor.run_target(SPEED, 20)
        wait(4000)
        self.left_button_motor.run_target(SPEED, 0)

# Initialize mechanisms
spike_manager = SpikeManager()

# Wait for incoming bluetooth connection
server = BluetoothMailboxServer()
mbox = TextMailbox('command', server)
print('waiting for connection...')
server.wait_for_connection()
print('connected!')

while True:
    # Wait for new instruction
    mbox.wait()
    command = mbox.read()
    print(command)

    # Execute command
    if command == 'activate_dfu':
        spike_manager.activate_dfu()
    elif command == 'remove_usb':
        spike_manager.remove_usb()
    elif command == 'shutdown':
        spike_manager.shutdown()
    elif command == 'stop':
        break

    # Say we are done with this command
    mbox.send(command)

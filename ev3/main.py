#!/usr/bin/env pybricks-micropython

from pybricks.messaging import BluetoothMailboxServer, TextMailbox
from pybricks.tools import wait

from monitor import SpikeMonitor

# Create monitor object and initialize mechanisms
spike = SpikeMonitor()

# Start server
server = BluetoothMailboxServer()

# Keep accepting connections and commands from PC script.
while True:

    # Wait for incoming bluetooth connection

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
        if command == 'power_on':
            spike.click_center()
        if command == 'activate_dfu':
            spike.activate_dfu()
        elif command == 'remove_usb':
            spike.insert_usb(False)
        elif command == 'shutdown':
            spike.shutdown()

        # Say we are done with this command
        mbox.send(command)

        if command == 'stop':
            break

#!/usr/bin/env pybricks-micropython

from pybricks.messaging import BluetoothMailboxServer, TextMailbox

from monitor import SpikeMonitor

# Create monitor object and initialize mechanisms
spike = SpikeMonitor()

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
        spike.activate_dfu()
    elif command == 'remove_usb':
        spike.insert_usb(False)
    elif command == 'shutdown':
        spike.shutdown()
    elif command == 'stop':
        break

    # Say we are done with this command
    mbox.send(command)

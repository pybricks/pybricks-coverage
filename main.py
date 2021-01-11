#!/usr/bin/env python3
from mailbox.messaging import BluetoothMailboxClient, TextMailbox

# This is the address of the server EV3 we are connecting to.
SERVER = '24:71:89:4A:02:E2'

client = BluetoothMailboxClient()
mbox = TextMailbox('command', client)

print('establishing connection...')
client.connect(SERVER)
print('connected!')

for command in ('activate_dfu', 'remove_usb', 'shutdown', 'stop'):
    # Send command
    mbox.send(command)

    # Wait until they are done
    mbox.wait()

mbox.send('stop')

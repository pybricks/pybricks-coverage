#!/usr/bin/env python3

import asyncio
from mailbox.messaging import BluetoothMailboxClient, TextMailbox

# Main
async def main():
    for command in ('activate_dfu', 'remove_usb', 'shutdown'):
        # Send command
        mbox.send(command)

        # Wait until they are done
        data = None
        while data != command:
            data = mbox.read()
            await asyncio.sleep(0.1)

    # Tell EV3 to stop
    mbox.send('stop')

# Connect to the EV3
client = BluetoothMailboxClient()
mbox = TextMailbox('command', client)
client.connect('24:71:89:4A:02:E2')

# Start main run loop
asyncio.run(main())

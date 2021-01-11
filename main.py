#!/usr/bin/env python3

import asyncio
from mailbox.messaging import BluetoothMailboxClient, TextMailbox

async def execute_command(mailbox, command, wait=True):
    """Sends command to EV3 and awaits execution"""
    # send the command
    mailbox.send(command)

    # Return if we don't need to wait for completion
    if not wait:
        return

    # Wait until they echo back
    data = None
    while data != command:
        data = mailbox.read()
        await asyncio.sleep(0.1)

# Main
async def main(mailbox):
    """Main program"""

    # Trigger DFU mode
    await execute_command(mailbox, 'activate_dfu')
    await execute_command(mailbox, 'remove_usb')
    await execute_command(mailbox, 'shutdown')

    # Tell EV3 to stop
    await execute_command(mailbox, 'stop', wait=False)

    # Tell EV3 to stop
    mbox.send('stop')

# Connect to the EV3
client = BluetoothMailboxClient()
mbox = TextMailbox('command', client)
client.connect('24:71:89:4A:02:E2')

# Start main run loop
asyncio.run(main(mbox))

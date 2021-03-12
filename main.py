#!/usr/bin/env python3

from asyncio import sleep, run
from mailbox.messaging import BluetoothMailboxClient, TextMailbox

from pybricksdev.dfu import flash_dfu
from pybricksdev.flash import create_firmware
from pybricksdev.connections import BLEPUPConnection
from pybricksdev.ble import find_device

from os import listdir, path, walk

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
        await sleep(0.1)

# Main
async def main(mailbox, dfu=False):
    """Main program"""

    if dfu:
        # Trigger DFU mode
        await execute_command(mailbox, 'activate_dfu')

        # Run DFU (blocking)
        firmware, metadata = await create_firmware('../pybricks-micropython/bricks/primehub/build/firmware.zip')
        flash_dfu(firmware, metadata)
        await execute_command(mailbox, 'remove_usb')
    else:
        # Otherwise, just turn on the hub with the button
        await execute_command(mailbox, 'power_on')


    # Connect to the hub that just booted up
    hub = BLEPUPConnection()
    address = await find_device("Pybricks Hub")
    await hub.connect(address)

    # TODO: Some of these scripts require interaction. Need to program
    # the buttons that way, or print that from hub in test scripts.
    
    scripts = []
    for (dirpath, dirnames, filenames) in walk('./scripts'):
        scripts += [path.join(dirpath, name) for name in filenames if '.py' == name[-3:]]

    for file_name in scripts:
        print("Now running:", file_name)
        await hub.run(file_name)
    await hub.disconnect()

    await execute_command(mailbox, 'shutdown')

    # Tell EV3 to stop
    await execute_command(mailbox, 'stop')

# Connect to the EV3
client = BluetoothMailboxClient()
mbox = TextMailbox('command', client)
client.connect('24:71:89:4A:02:E2')

# Start main run loop
run(main(mbox))

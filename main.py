#!/usr/bin/env python3
from mailbox.messaging import BluetoothMailboxClient, TextMailbox

# This is the address of the server EV3 we are connecting to.
SERVER = '24:71:89:4A:02:E2'

client = BluetoothMailboxClient()
mbox = TextMailbox('greeting', client)

print('establishing connection...')
client.connect(SERVER)
print('connected!')

# In this program, the client sends the first message and then waits for the
# server to reply.
mbox.send('hello!')
mbox.wait()
print(mbox.read())

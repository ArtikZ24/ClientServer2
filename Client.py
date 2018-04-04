#!/usr/bin/env python

import socket
import time
import string
import random

TCP_IP = '127.0.0.1'
TCP_PORT = 62
BUFFER_SIZE = 1024
MESSAGE = "ADD Hello, World!"


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while True:
    message = raw_input("Command: ")
    if "AUTO" in message:
        message_number = message.split(" ")[1]
        message_delay = message.split(" ")[2]
        for i in range(0, int(message_number)):
            message = id_generator()
            s.send("ADD " + message)
            time.sleep(message_delay)
    else:
        s.send(message)
        data = s.recv(BUFFER_SIZE)
        print "received data:", data

s.close()

print "received data:", data
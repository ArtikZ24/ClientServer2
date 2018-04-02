#!/usr/bin/env python

import socket
from threading import Thread
from SocketServer import ThreadingMixIn
import hashlib
import json

DataDict = {}


class ClientThread(Thread):

    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        print "[+] New thread started for " + ip + ":" + str(port)

    def run(self):
        while True:
            data = conn.recv(2048)
            if not data: break
            print "received data:", data

            if "GET" in data:
                if data in DataDict:
                    conn.send(DataDict[data])
                else:
                    conn.send("data not found")

            if "ADD" in data:
                data = data[4:]
                print "adding data {}".format(data[4:])
                hash_object = hashlib.sha512(data)
                hex_dig = hash_object.hexdigest()
                print(hex_dig)
                DataDict[data] = hex_dig
                conn.send(hex_dig)  # echo

            if "PRINT ALL" in data:
                print DataDict
                data_string = json.dumps(DataDict)
                conn.send(data_string)


TCP_IP = '0.0.0.0'
TCP_PORT = 60
BUFFER_SIZE = 20  # Normally 1024, but we want fast response

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(4)
    print "Waiting for incoming connections..."
    (conn, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
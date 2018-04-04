#!/usr/bin/env python

import socket
from threading import Thread
from SocketServer import ThreadingMixIn


class ClientThread(Thread):

    def __init__(self, ip, port):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.data = None
        print "[+] New thread started for " + ip + ":" + str(port)

    def sendToService(self, message):
        SERVICE_IP = '127.0.0.1'
        SERVICE_PORT = 60
        BUFFER_SIZE = 2048

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((SERVICE_IP, SERVICE_PORT))
        s.send(message)
        data = s.recv(BUFFER_SIZE)
        s.close()
        print "server received data:", data
        return data

    def run(self):
        while True:
            data = conn.recv(2048)
            if not data: break
            print "received data:", data
            # conn.send(data)  # echo
            # conn.send(data)  # echo
            if "GET" in data:
                data = self.sendToService(data)
                conn.send("Getting Data")
                conn.send(data + " KEY")

            if "ADD" in data:
                data = self.sendToService(data)
                conn.send(data + " HASH")

            if "PRINT ALL" in data:
                data = self.sendToService(data)
                conn.send(data)


TCP_IP = '0.0.0.0'
TCP_PORT = 62
BUFFER_SIZE = 2048

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
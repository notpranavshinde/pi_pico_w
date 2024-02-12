from machine import Pin
import network
import socket
import time
from secret import ssid, password
# to be added: another file with network configs

# Connect to network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)

print(wlan.ifconfig())

# Set up server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))

    # Generate string
    response = "Hello, Pico W!"

    # Send string
    conn.send(response)
    conn.close()

    # Receive string
    ai = socket.getaddrinfo("192.168.0.23", 80)#replace this ip with the ip of the other pico.
    addr = ai[-1]
    s = socket.socket()
    s.connect(addr)
    s.send(b"GET Data")
    received_string = str(s.recv(512))
    print(received_string)
    s.close()
    time.sleep(0.2)

from machine import Pin, ADC
import network
import socket
import time
import secret

def connect_to_wifi(ssid, password, max_wait=20):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
    
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print('ip = ' + status[0])
    return wlan

def create_socket():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('listening on', addr)
    return s

def handle_client(s):
    while True:
        try:
            cl, addr = s.accept()
            print("Connection from:", addr)
            request = cl.recv(1024).decode()
            print("Received:", request)
            
            response = "something to send"
            cl.send(response.encode())
            print("Sent:", response)
            
            cl.close()
        except OSError as e:
            cl.close()
            print('connection closed')

def main():
    ssid = secret.ssid
    password = secret.password
    connect_to_wifi(ssid, password)
    s = create_socket()
    handle_client(s)

if __name__ == "__main__":
    main()

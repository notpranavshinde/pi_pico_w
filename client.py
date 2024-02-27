import network
import socket
import time
import secrets

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

def send_request(server_ip, port=80):
    addr_info = socket.getaddrinfo(server_ip, port)
    addr = addr_info[0][-1]
    
    s = socket.socket()  # Create a new socket
    try:
        s.connect(addr)
        stuff_to_send = input("what to send?")
        
        s.send(stuff_to_send.encode())
        response = s.recv(512)
        print("Received:", response.decode())
    finally:
        s.close()  # Ensure the socket is closed even if an error occurs


def main():
    ssid = secrets.ssid
    password = secrets.password
    server_ip = "192.168.84.27"  # Example server IP, change as needed
    
    connect_to_wifi(ssid, password)
    while True:
        send_request(server_ip)
        time.sleep(0.2)  # Wait a bit before sending the next request

if __name__ == "__main__":
    main()


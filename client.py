def send_request(server_ip, port=80):
    addr_info = socket.getaddrinfo(server_ip, port)
    addr = addr_info[0][-1]
    
    s = socket.socket()  # Create a new socket
    try:
        s.connect(addr)
        print("Sending 'Hello from Client'")
        s.send(b"Hello from Client")
        response = s.recv(512)
        print("Received:", response.decode())
    finally:
        s.close()  # Ensure the socket is closed even if an error occurs

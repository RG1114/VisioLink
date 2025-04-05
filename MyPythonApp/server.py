import socket

def get_host_ip():
    """Determine the laptop's local IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Use a public IP address (Google DNS) to force the OS to assign the correct network interface.
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

HOST = get_host_ip()  # Automatically get the local IP address.
PORT = 65432        # Port number

print(f"Server is hosting on IP: {HOST} and port: {PORT}")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Server is listening...")
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            # You can update this to get dynamic input or send commands based on some logic.
            command = input("Enter command (move forward/move backwards/idle): ")
            if command:
                conn.sendall(command.encode('utf-8'))

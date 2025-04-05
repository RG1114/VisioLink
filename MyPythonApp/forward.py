# server.py
import socket
import threading
from flask import Flask, request, jsonify

app = Flask(__name__)
mobile_conn = None  # This will hold the socket connection to the mobile

def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

def socket_listener():
    global mobile_conn
    HOST = get_host_ip()
    PORT = 65432
    print(f"Socket Server is hosting on IP: {HOST} and port: {PORT}",flush=True)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting for mobile app to connect...",flush=True)
        mobile_conn, addr = s.accept()
        print("Connected by", addr,flush=True)

        # Optional: Keep listening for command inputs if needed
        while True:
            try:
                # You could send "heartbeat" or receive something too here
                pass
            except:
                break

@app.route('/receive-detection', methods=['POST'])
def receive_detection():
    global mobile_conn
    data = request.get_json()
    data=data["result"]
    print(f" Received Detection Data: {data}",flush=True)
    
    if mobile_conn:
        try:
            # Send JSON as string
            mobile_conn.sendall((str(data) + "\n").encode('utf-8'))
        except Exception as e:
            print(f" Error sending to mobile: {e}",flush=True)
            return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    threading.Thread(target=socket_listener, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)

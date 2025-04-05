import socket
import threading
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
mobile_conn = None
latest_gesture = None  # Stores the last detected gesture

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

# forward.py (changes in socket_listener function)
def socket_listener():
    global mobile_conn
    HOST = get_host_ip()
    PORT = 65432
    print(f"Socket Server is hosting on IP: {HOST} and port: {PORT}")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow port reuse
        s.bind((HOST, PORT))
        s.listen()
        print("📲 Waiting for mobile app to connect...")
        while True:  # Outer loop to accept new connections
            mobile_conn, addr = s.accept()
            print("✅ Connected by", addr)
            try:
                with mobile_conn:
                    while True:
                        # Keep connection alive by listening for data
                        data = mobile_conn.recv(1024)
                        if not data:
                            break  # Client closed connection
            except Exception as e:
                print(f"❌ Connection error: {e}")
            finally:
                mobile_conn = None  # Reset connection on exit
                print("⚠️ Mobile client disconnected")

@app.route('/my-ip', methods=['GET'])
def get_my_ip():
    return jsonify({'ip': get_host_ip()})

@app.route('/connection-status')
def connection_status():
    print("mobile_conn:", mobile_conn) #temporary 
    return jsonify({'connected': mobile_conn is not None})


# forward.py (changes in /receive-detection route)
@app.route('/receive-detection', methods=['POST'])
def receive_detection():
    global latest_gesture, mobile_conn
    data = request.get_json()
    latest_gesture = data["result"]
    print(f"📦 Received Detection: {latest_gesture}")
    if mobile_conn:
        try:
            mobile_conn.sendall((str(latest_gesture) + "\n").encode('utf-8'))
        except Exception as e:
            print(f"❌ Error sending to mobile: {e}")
            mobile_conn = None  # Reset connection on failure
    return jsonify({'status': 'success'}), 200

@app.route('/get-latest-gesture')
def get_latest_gesture():
    return jsonify({'gesture': latest_gesture})

if __name__ == '__main__':
    threading.Thread(target=socket_listener, daemon=True).start()
    app.run(host="0.0.0.0", port=5001)

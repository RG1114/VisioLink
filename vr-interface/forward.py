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

def socket_listener():
    global mobile_conn
    HOST = get_host_ip()
    PORT = 65432
    print(f"Socket Server is hosting on IP: {HOST} and port: {PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("📲 Waiting for mobile app to connect...")
        mobile_conn, addr = s.accept()
        print("✅ Connected by", addr)
        
        while True:
            try:
                # Keep connection alive
                pass
            except Exception as e:
                print(f"❌ Connection error: {e}")
                mobile_conn = None
                break

@app.route('/my-ip', methods=['GET'])
def get_my_ip():
    """Return the IP that the socket server is listening on."""
    return jsonify({'ip': get_host_ip()})

@app.route('/connection-status')
def connection_status():
    return jsonify({'connected': mobile_conn is not None})

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
            return jsonify({'status': 'error'}), 500

    return jsonify({'status': 'success'}), 200

@app.route('/get-latest-gesture')
def get_latest_gesture():
    return jsonify({'gesture': latest_gesture})

if __name__ == '__main__':
    threading.Thread(target=socket_listener, daemon=True).start()
    app.run(host="0.0.0.0", port=5001)

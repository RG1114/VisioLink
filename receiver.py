from flask import Flask, request

app = Flask(__name__)

@app.route('/receive-detection', methods=['POST'])
def receive_detection():
    data = request.get_json()
    print("📦 Received detection data:", data)
    return {'status': 'received'}, 200

if __name__ == "__main__":
    app.run(port=5000)
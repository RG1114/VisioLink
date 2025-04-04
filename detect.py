from ultralytics import YOLO
import cv2
import time
import requests  # For HTTP request

stop_flag = False  # global flag for stopping detection

def run_detection():
    global stop_flag
    model = YOLO("final.pt")
    cap = cv2.VideoCapture(0)

    start_time = time.time()

    while True:
        if stop_flag:
            print("Stopping detection manually.")
            break

        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(source=frame, conf=0.5, verbose=True)

        # # Show result on screen
        # annotated_frame = results[0].plot()
        # cv2.imshow("Detection", annotated_frame)

        # Example: Send result over HTTP (optional, can be sent once or periodically)
        detected_classes = results[0].names
        # data_to_send = {
        #     "result": [detected_classes[i] for i in results[0].boxes.cls.tolist()]
        # }
        detected_class_names = [results[0].names[i] for i in results[0].boxes.cls.tolist()]
        if "Fire" in detected_class_names:
            data_to_send = {
                "result": "move forward"
            }
        else:
            data_to_send = {
                "result": "idle"  # or whatever fallback you want
            }
        try:
            requests.post("http://localhost:5000/receive-detection", json=data_to_send)
        except:
            pass  # Ignore errors for now

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Stop after 5 seconds (demo timeout)
        if time.time() - start_time > 40:
            stop_detection()

    cap.release()
    cv2.destroyAllWindows()

def stop_detection():
    global stop_flag
    stop_flag = True

if __name__ == "__main__":
    run_detection()
    print("Object detection completed!")


# detect.py
# import requests

# SERVER_URL = "http://localhost:5000/receive-detection"  # Update if server is on another IP

# def main():
#     print("🔁 Type a message to send to server. Type 'exit' to quit.")
#     while True:
#         msg = input("👉 Enter message: ")
#         if msg.lower() == 'exit':
#             print("👋 Exiting.")
#             break

#         data = {"result": msg}
#         try:
#             response = requests.post(SERVER_URL, json=data)
#             if response.status_code == 200:
#                 print("✅ Sent successfully.")
#             else:
#                 print(f"❌ Server error: {response.status_code} - {response.text}")
#         except Exception as e:
#             print(f"❌ Failed to send: {e}")

# if __name__ == "__main__":
#     main()


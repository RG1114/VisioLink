from ultralytics import YOLO
import cv2

def run_detection():
    model_path = "./final.pt"  # Place the .pt file in same directory or update path
    model = YOLO(model_path)
    model.predict(source="0", show=True, conf=0.5)  # 0 = webcam

if __name__ == "__main__":
    run_detection()
    print("Object detection completed!")

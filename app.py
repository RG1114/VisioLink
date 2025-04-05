import pygame
import socket
import threading
import queue
from flask import Flask, request, jsonify
import sys
import io
from app_ml import start_detection, stop_detection



# ========== Flask Setup ==========
app = Flask(__name__)
mobile_conn = None
data_queue = queue.Queue()
log_queue = queue.Queue()


def get_host_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip


def socket_listener():
    global mobile_conn
    HOST = get_host_ip()
    PORT = 65432
    custom_print(f"[Socket] Hosting on {HOST}:{PORT}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        custom_print("[Socket] Waiting for mobile connection...")
        mobile_conn, addr = s.accept()
        custom_print(f"[Socket] Connected by {addr}")

        while True:
            try:
                pass  # Optional: handle incoming socket data
            except:
                break


@app.route('/receive-detection', methods=['POST'])
def receive_detection():
    global mobile_conn
    data = request.get_json()["result"]
    custom_print(f"[Flask] Received Detection Data: {data}")
    data_queue.put(data)

    if mobile_conn:
        try:
            mobile_conn.sendall((str(data) + "\n").encode('utf-8'))
        except Exception as e:
            custom_print(f"[Error] Sending to mobile: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'success'}), 200


def start_flask():
    app.run(host="0.0.0.0", port=5000)


def start_socket():
    socket_listener()

# ========== Redirect print to GUI ==========
class StreamToQueue(io.StringIO):
    def write(self, msg):
        if msg.strip():
            log_queue.put(msg.strip())

def custom_print(*args, **kwargs):
    message = ' '.join(str(a) for a in args)
    print(message)
    log_queue.put(message)

sys.stdout = StreamToQueue()

# ========== Pygame Setup ==========

def draw_button(surface, rect, text, color, hover_color, mouse_pos, font):
    current_color = hover_color if rect.collidepoint(mouse_pos) else color
    pygame.draw.rect(surface, current_color, rect)
    label = font.render(text, True, (255, 255, 255))
    label_rect = label.get_rect(center=rect.center)
    surface.blit(label, label_rect)

def main():
    threading.Thread(target=start_flask, daemon=True).start()
    threading.Thread(target=start_socket, daemon=True).start()

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Detection Viewer")
    font = pygame.font.Font(None, 30)

    clock = pygame.time.Clock()
    result_text = "Waiting for detection..."

    button1 = pygame.Rect(150, 500, 150, 50)
    button2 = pygame.Rect(500, 500, 150, 50)

    logs = []

    running = True
    while running:
        screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button1.collidepoint(event.pos):
                    custom_print("[Button 1] clicked")
                    start_detection()
                # if button2.collidepoint(event.pos):
                #     custom_print("[Button 2] clicked")
                #     stop_detection()

        # Get new detection if available
        if not data_queue.empty():
            result_text = data_queue.get()

        # Get new log lines
        while not log_queue.empty():
            logs.append(log_queue.get())
            if len(logs) > 8:
                logs = logs[-8:]

        # Show detection result
        detection_surface = font.render(f"Detection: {result_text}", True, (255, 255, 255))
        screen.blit(detection_surface, (50, 50))

        # Show logs
        for i, line in enumerate(reversed(logs)):
            log_surface = font.render(line, True, (200, 200, 200))
            screen.blit(log_surface, (50, 120 + i * 25))

        # Draw buttons
        draw_button(screen, button1, "Start Game", (70, 130, 180), (100, 170, 220), mouse_pos, font)
        # draw_button(screen, button2, "Action 2", (180, 70, 130), (220, 100, 170), mouse_pos, font)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()

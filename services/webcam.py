import base64
import os
from threading import Lock, Thread
import time
import cv2
from cv2 import VideoCapture, imencode


class WebcamStream:
    def __init__(self):
        self.stream = VideoCapture(index=0)
        _, self.frame = self.stream.read()
        self.running = False
        self.lock = Lock()

    def start(self):
        if self.running:
            return self

        self.running = True

        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self):
        while self.running:
            _, frame = self.stream.read()

            self.lock.acquire()
            self.frame = frame
            self.lock.release()

    def read(self, encode=False):
        self.lock.acquire()
        frame = self.frame.copy()
        self.lock.release()

        if encode:
            _, buffer = imencode(".jpeg", frame)
            return base64.b64encode(buffer)

        return frame

    def stop(self):
        self.running = False
        if self.thread.is_alive():
            self.thread.join()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.stream.release()


def capture_image():
    # Open the default camera (index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        raise IOError("Cannot open camera")

    print("Camera opened successfully")
    time.sleep(1)
    # Take a snapshot
    ret, frame = cap.read()
    if not ret:
        print("Error reading frame")
    else:
        # Save the snapshot to a file
        img_path = "data/vision"
        os.makedirs(img_path, exist_ok=True)
        image_path = os.path.join(img_path, "image.jpg")
        cv2.imwrite(image_path, frame)
        print(f"Snapshot saved to {image_path.lower()}")

    # Release the camera
    cap.release()
    print("Camera released")
    return image_path

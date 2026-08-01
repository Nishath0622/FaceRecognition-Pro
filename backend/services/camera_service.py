"""
Camera Stream Service
Handles live webcam feed with optional face detection/recognition overlay.
"""

import cv2
import threading
import time
import logging
from config import CAMERA_WIDTH, CAMERA_HEIGHT

logger = logging.getLogger(__name__)


class CameraService:
    def __init__(self):
        self._cap = None
        self._lock = threading.Lock()
        self._mode = "none"   # none | detect | recognize
        self._running = False

    def set_mode(self, mode: str):
        allowed = {"none", "detect", "recognize"}
        if mode not in allowed:
            raise ValueError(f"Invalid mode '{mode}'. Choose from {allowed}")
        self._mode = mode
        logger.info("Camera mode set to: %s", mode)
        if mode == "none":
            self.release()

    def get_mode(self) -> str:
        return self._mode

    def _open(self):
        if self._cap is None or not self._cap.isOpened():
            self._cap = cv2.VideoCapture(0)
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
            time.sleep(0.5)  # warm-up

    def release(self):
        with self._lock:
            if self._cap and self._cap.isOpened():
                self._cap.release()
                self._cap = None
        logger.info("Camera released")

    def generate_frames(self, face_service):
        """
        Generator that yields MJPEG frames.
        face_service is passed to avoid circular import.
        """
        from config import CASCADE_PATH
        detector = cv2.CascadeClassifier(CASCADE_PATH)

        self._open()
        while True:
            with self._lock:
                if self._cap is None or not self._cap.isOpened():
                    break
                ok, frame = self._cap.read()

            if not ok:
                time.sleep(0.05)
                continue

            frame = cv2.flip(frame, 1)  # mirror

            if self._mode in ("detect", "recognize"):
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)
                faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(60, 60))

                for (x, y, w, h) in faces:
                    if self._mode == "recognize" and face_service.is_trained:
                        results = face_service.recognize_from_frame(frame)
                        for r in results:
                            rx, ry, rw, rh = r["bbox"]
                            color = (0, 220, 100) if r["matched"] else (0, 80, 220)
                            cv2.rectangle(frame, (rx, ry), (rx + rw, ry + rh), color, 2)
                            label = f"{r['name']} {r['confidence']}%"
                            cv2.putText(frame, label, (rx, ry - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    else:
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 200, 255), 2)
                        cv2.putText(frame, "Face", (x, y - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 200, 255), 2)

            _, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n"
                   + buf.tobytes() + b"\r\n")


camera_service = CameraService()

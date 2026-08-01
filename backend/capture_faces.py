"""
capture_faces.py — Standalone webcam capture script (run from backend/)
Usage:
    python capture_faces.py

This captures 40 face samples from your webcam and saves them to
dataset/<PersonName>/ so you can upload and train without the UI.
"""

import cv2
import os

CASCADE = "Cascades/haarcascade_frontalface_default.xml"
DATASET = "dataset"
SAMPLES = 40

detector = cv2.CascadeClassifier(CASCADE)
cam = cv2.VideoCapture(0)
cam.set(3, 640); cam.set(4, 480)

name = input("Enter person name: ").strip()
if not name:
    print("Name cannot be empty"); exit(1)

save_dir = os.path.join(DATASET, name)
os.makedirs(save_dir, exist_ok=True)

count = 0
print(f"[INFO] Look at the camera. Capturing {SAMPLES} samples…  (Press ESC to quit early)")

while True:
    ok, frame = cam.read()
    if not ok:
        break
    frame = cv2.flip(frame, 1)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = detector.detectMultiScale(gray, 1.3, 5, minSize=(80, 80))

    for (x, y, w, h) in faces:
        count += 1
        path = os.path.join(save_dir, f"{name}_{count}.jpg")
        cv2.imwrite(path, gray[y:y+h, x:x+w])
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 220, 100), 2)
        cv2.putText(frame, f"Sample {count}/{SAMPLES}", (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 220, 100), 2)

    cv2.putText(frame, f"Captured: {count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.imshow("Capture Faces — Press ESC to stop", frame)

    if cv2.waitKey(1) & 0xFF == 27 or count >= SAMPLES:
        break

cam.release()
cv2.destroyAllWindows()
print(f"\n[DONE] Saved {count} images to {save_dir}/")
print("Now run: python -c \"from services.training_service import training_service; print(training_service.train())\"")
print("Or click 'Train Model' in the web UI.")

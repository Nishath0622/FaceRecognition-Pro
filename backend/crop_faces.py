import cv2
import os

dataset_root = "dataset"
output_root = "dataset_clean"

os.makedirs(output_root, exist_ok=True)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

total_faces = 0

for person in os.listdir(dataset_root):
    person_path = os.path.join(dataset_root, person)

    if not os.path.isdir(person_path):
        continue

    print(f"Processing: {person}")

    output_person_path = os.path.join(output_root, person)
    os.makedirs(output_person_path, exist_ok=True)

    count = 0

    for file in os.listdir(person_path):
        img_path = os.path.join(person_path, file)

        img = cv2.imread(img_path)
        if img is None:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            face = gray[y:y+h, x:x+w]
            face = cv2.resize(face, (200, 200))

            save_path = os.path.join(output_person_path, f"{person}_{count}.jpg")
            cv2.imwrite(save_path, face)

            count += 1
            total_faces += 1

    print(f"Saved {count} faces for {person}")

print("\nDONE!")
print("Total faces:", total_faces)
import os
import shutil
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from config import DATASET_DIR

dataset_bp = Blueprint("dataset", __name__)

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def _allowed(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ✅ UPLOAD IMAGES
@dataset_bp.route("/upload", methods=["POST"])
def upload_images():
    name = request.form.get("name", "").strip()

    if not name:
        return jsonify({"error": "Person name is required"}), 400

    files = request.files.getlist("images")

    if not files:
        return jsonify({"error": "No images provided"}), 400

    safe_name = secure_filename(name)
    person_dir = os.path.join(DATASET_DIR, safe_name)
    os.makedirs(person_dir, exist_ok=True)

    existing_images = [
        f for f in os.listdir(person_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]

    saved = 0

    for f in files:
        if f and _allowed(f.filename):
            ext = f.filename.rsplit(".", 1)[1].lower()
            file_index = len(existing_images) + saved + 1

            save_path = os.path.join(
                person_dir, f"{safe_name}_{file_index}.{ext}"
            )

            f.save(save_path)
            saved += 1

    total_images = len([
        f for f in os.listdir(person_dir)
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])

    return jsonify({
        "success": True,
        "person": name,
        "images_saved": saved,
        "total_for_person": total_images
    })


# ✅ DATASET STATS (FIXED — NO training_service)
@dataset_bp.route("/stats", methods=["GET"])
def stats():
    persons = 0
    total_images = 0

    if os.path.exists(DATASET_DIR):
        for entry in os.scandir(DATASET_DIR):
            if entry.is_dir():
                persons += 1
                images = [
                    f for f in os.listdir(entry.path)
                    if f.lower().endswith((".jpg", ".jpeg", ".png"))
                ]
                total_images += len(images)

    return jsonify({
        "persons": persons,
        "total_images": total_images
    })


# ✅ LIST PERSONS WITH IMAGE COUNT
@dataset_bp.route("/persons", methods=["GET"])
def list_persons():
    persons = []

    if os.path.exists(DATASET_DIR):
        for entry in os.scandir(DATASET_DIR):
            if entry.is_dir():
                image_files = [
                    f for f in os.listdir(entry.path)
                    if f.lower().endswith((".jpg", ".jpeg", ".png"))
                ]

                persons.append({
                    "name": entry.name,
                    "image_count": len(image_files)
                })

    return jsonify({"persons": persons})


# ✅ DELETE PERSON
@dataset_bp.route("/delete/<person_name>", methods=["DELETE"])
def delete_person(person_name):
    safe_name = secure_filename(person_name)
    person_dir = os.path.join(DATASET_DIR, safe_name)

    if not os.path.exists(person_dir):
        return jsonify({"error": "Person not found"}), 404

    shutil.rmtree(person_dir)

    return jsonify({
        "success": True,
        "deleted": safe_name
    })

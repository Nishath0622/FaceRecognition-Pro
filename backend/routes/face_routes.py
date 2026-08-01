"""
Face Routes
/api/face/detect
/api/face/recognize
/api/face/model-info
/api/face/train
"""

import cv2
import numpy as np
from flask import Blueprint, request, jsonify
from services.face_service import face_service

face_bp = Blueprint("face", __name__)


# ---------------- DETECT FACES ----------------
@face_bp.route("/detect", methods=["POST"])
def detect():
    try:
        # ✅ Check image exists
        if "image" not in request.files:
            return jsonify({
                "face_count": 0,
                "faces": [],
                "error": "No image provided"
            }), 400

        img_bytes = request.files["image"].read()
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({
                "face_count": 0,
                "faces": [],
                "error": "Invalid image"
            }), 400

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 🔥 Detect faces
        faces = face_service.cascade.detectMultiScale(
            gray, 
            scaleFactor=1.1, 
            minNeighbors=3, 
            minSize=(20, 20)
        )
        
        # 🔥 Format face data
        face_data = []
        for (x, y, w, h) in faces:
            face_data.append({
                "x": int(x),
                "y": int(y),
                "width": int(w),
                "height": int(h)
            })

        return jsonify({
            "face_count": len(faces),
            "faces": face_data
        })

    except Exception as e:
        return jsonify({
            "face_count": 0,
            "faces": [],
            "error": str(e)
        }), 500


# ---------------- RECOGNIZE ----------------
@face_bp.route("/recognize", methods=["POST"])
def recognize():
    try:
        # ✅ Check image exists
        if "image" not in request.files:
            return jsonify({
                "face_count": 0,
                "results": [],
                "error": "No image provided"
            }), 400

        img_bytes = request.files["image"].read()
        result = face_service.recognize_faces(img_bytes)

        # ✅ Only return 422 if REAL error exists
        if result.get("error"):
            return jsonify(result), 422

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "face_count": 0,
            "results": [],
            "error": str(e)
        }), 500


# ---------------- MODEL INFO ----------------
@face_bp.route("/model-info", methods=["GET"])
def model_info():
    try:
        return jsonify(face_service.get_model_info())
    except Exception as e:
        return jsonify({
            "trained": False,
            "persons": [],
            "person_count": 0,
            "error": str(e)
        }), 500


# ---------------- TRAIN MODEL ----------------
@face_bp.route("/train", methods=["POST"])
def train():
    try:
        result = face_service.train()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500
"""
Stream Routes
/api/stream/video_feed      GET   - MJPEG stream
/api/stream/mode/<mode>     POST  - set camera mode
/api/stream/status          GET   - current mode
"""

from flask import Blueprint, Response, jsonify
from services.camera_service import camera_service
from services.face_service import face_service

stream_bp = Blueprint("stream", __name__)


@stream_bp.route("/video_feed")
def video_feed():
    """Live MJPEG camera stream with optional overlay."""
    return Response(
        camera_service.generate_frames(face_service),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@stream_bp.route("/mode/<string:mode>", methods=["POST"])
def set_mode(mode):
    """Set detection mode: none | detect | recognize"""
    try:
        camera_service.set_mode(mode)
        return jsonify({"status": "ok", "mode": mode})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@stream_bp.route("/status", methods=["GET"])
def status():
    """Return current camera mode."""
    return jsonify({"mode": camera_service.get_mode()})

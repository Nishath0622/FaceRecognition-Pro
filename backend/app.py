from flask import Flask
from flask_cors import CORS
from routes.face_routes import face_bp
from routes.dataset_routes import dataset_bp
from routes.stream_routes import stream_bp
import os


def create_app():
    app = Flask(__name__)

    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Ensure required folders exist
    for folder in ["dataset", "uploads"]:
        os.makedirs(folder, exist_ok=True)

    # Register Blueprints
    app.register_blueprint(face_bp, url_prefix="/api/face")
    app.register_blueprint(dataset_bp, url_prefix="/api/dataset")
    app.register_blueprint(stream_bp, url_prefix="/api/stream")

    # Root route
    @app.route("/")
    def home():
        return "Face Recognition Pro Backend Running 🚀"

    # Health check route
    @app.route("/api/health")
    def health():
        return {
            "status": "ok",
            "message": "Face Recognition Pro API is running"
        }

    return app


# 🔥 MAIN ENTRY POINT (VERY IMPORTANT)
if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
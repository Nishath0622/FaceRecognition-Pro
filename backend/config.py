"""
Configuration settings for Face Recognition Pro
"""
import os

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
CASCADE_PATH = os.path.join(BASE_DIR, "Cascades", "haarcascade_frontalface_default.xml")

# Recognition threshold (lower = stricter)
CONFIDENCE_THRESHOLD = 70

# Dataset capture settings
SAMPLES_PER_PERSON = 40
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Image preprocessing
IMG_SIZE = (200, 200)

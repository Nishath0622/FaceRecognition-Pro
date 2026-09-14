# Face Recognition Pro 🔍

A full-stack face recognition application that supports face detection, face recognition, dataset management, model training, and real-time webcam recognition.

## 🚀 Tech Stack

### Backend
- Python
- Flask
- OpenCV
- Haar Cascade
- DeepFace
- NumPy
- Pillow

### Frontend
- React
- Vite
- Tailwind CSS
- Axios
- React Router
- React Dropzone
- React Hot Toast
- Lucide React

---

## 📁 Project Structure

```text
face_recognition_pro/
│
├── backend/
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   ├── capture_faces.py
│   ├── routes/
│   │   ├── face_routes.py
│   │   ├── dataset_routes.py
│   │   └── stream_routes.py
│   ├── services/
│   │   ├── face_service.py
│   │   ├── training_service.py
│   │   └── camera_service.py
│   ├── Cascades/
│   │   └── haarcascade_frontalface_default.xml
│   ├── dataset/
│   └── trainer/
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── package-lock.json
    ├── vite.config.js
    ├── tailwind.config.js
    ├── postcss.config.js
    └── src/
        ├── main.jsx
        ├── App.jsx
        ├── index.css
        ├── api/
        │   └── client.js
        ├── components/
        │   └── Navbar.jsx
        └── pages/
            ├── Dashboard.jsx
            ├── RecognizePage.jsx
            ├── DatasetPage.jsx
            └── LivePage.jsx
🧠 How It Works
User
 │
 ▼
React Frontend
 │
 │ HTTP Requests
 ▼
Flask REST API
 │
 ├── Dataset Management
 ├── Face Detection
 ├── Face Recognition
 └── Live Camera
 │
 ▼
OpenCV / DeepFace
 │
 ▼
Result
 │
 ▼
React UI
✨ Features

1. Dataset Management

Users can add a person's name and upload multiple face images.

dataset/
├── Nisha/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── image3.jpg
└── Person2/
    ├── image1.jpg
    └── image2.jpg

Users can also view the known persons, image counts, delete a person, and train the model.

2. Face Detection

The system detects faces and returns their locations using OpenCV and Haar Cascade.

Detection answers:

"Where is the face?"

3. Face Recognition

The system identifies whether a detected face belongs to a known person using DeepFace.

Recognition answers:

"Whose face is this?"

4. Live Recognition

The webcam can operate in:

Off — stream stopped
Detect — detects faces and displays bounding boxes
Recognize — detects and recognizes known persons

The processed video is delivered to the frontend as an MJPEG stream.

🔄 Recognition Flow
Upload Image
     ↓
React
     ↓
Axios
     ↓
Flask API
     ↓
Face Detection
     ↓
DeepFace Recognition
     ↓
Compare with Known Persons
     ↓
Person / Unknown
     ↓
Result returned to React

🔌 API Endpoints
Method	Endpoint	Purpose
POST	/api/face/detect	Detect faces
POST	/api/face/recognize	Recognize faces
POST	/api/face/train	Train/prepare recognition system
GET	/api/face/model-info	Get model information
POST	/api/dataset/upload	Upload person images
GET	/api/dataset/persons	Get known persons
GET	/api/dataset/stats	Get dataset statistics
DELETE	/api/dataset/delete/<name>	Delete person's data
GET	/api/stream/video_feed	Live video stream
POST	/api/stream/mode/<mode>	Change stream mode


🖥️ Frontend

The React application contains four main pages:

Dashboard — model status, dataset statistics and quick actions
Recognize — upload an image and detect/recognize faces
Dataset — add persons, upload images and train
Live Feed — real-time webcam detection/recognition
Frontend Architecture
index.html
    ↓
main.jsx
    ↓
App.jsx
    ↓
React Router
    ↓
Pages + Navbar
    ↓
api/client.js
    ↓
Flask Backend

Axios is centralized in client.js so all API communication is handled consistently.

🐍 Backend

The Flask backend is divided into routes and services.

Routes
   ↓
Services
   ↓
OpenCV / DeepFace
   ↓
Dataset / Recognition
Routes
face_routes.py — face detection, recognition and training
dataset_routes.py — dataset operations
stream_routes.py — live streaming operations
Services
face_service.py — face processing and recognition
training_service.py — training/recognition preparation
camera_service.py — webcam and live frame processing


🔍 Haar Cascade vs DeepFace

Haar Cascade is mainly used for face detection.

Image → Haar Cascade → Face Location

DeepFace is used for face recognition.

Face → DeepFace → Facial Representation → Matching

Therefore, detection and recognition are separate stages of the system.

⚙️ Installation
Backend
cd face_recognition_pro/backend

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt

python app.py

Backend runs on:

http://localhost:5000
Frontend

Open another terminal:

cd face_recognition_pro/frontend

npm install

npm run dev

Frontend runs on:

http://localhost:3000
📸 Basic Usage
Start the Flask backend.
Start the React frontend.
Open http://localhost:3000.
Go to Dataset.
Add a person's name and upload face images.
Click Train Model.
Go to Recognize and upload an image.
Select Recognize to identify a person.
Go to Live Feed for real-time webcam recognition.
🔗 Frontend–Backend Connection

Vite proxies /api requests from React to Flask.

React
localhost:3000
     │
     │ /api/...
     ▼
Vite Proxy
     │
     ▼
Flask
localhost:5000




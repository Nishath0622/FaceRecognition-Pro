# Face Recognition Pro 🔍

A professional, production-ready face recognition system built with:
- **Backend**: Python + Flask + DeepFace
- **Frontend**: React + Tailwind CSS + Vite

---

## 📁 Project Structure

```
face_recognition_pro/
│
├── backend/
│   ├── app.py                   ← Flask entry point
│   ├── config.py                ← All settings (paths, thresholds)
│   ├── requirements.txt
│   ├── capture_faces.py         ← Standalone webcam capture script
│   │
│   ├── routes/
│   │   ├── face_routes.py       ← /api/face/*
│   │   ├── dataset_routes.py    ← /api/dataset/*
│   │   └── stream_routes.py     ← /api/stream/*
│   │
│   ├── services/
│   │   ├── face_service.py      ← DeepFace recognition logic
│   │   ├── training_service.py  ← Model training logic
│   │   └── camera_service.py    ← Webcam MJPEG streaming
│   │
│   ├── Cascades/
│   │   └── haarcascade_frontalface_default.xml
│   │
│   ├── dataset/                 ← Face images (auto-created)
│   │   └── PersonName/
│   │       └── *.jpg
│   │
│   └── trainer/                 ← Trained model (auto-created)
│       ├── trainer.yml
│       └── names.json
│
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    ├── tailwind.config.js
    └── src/
        ├── App.jsx
        ├── main.jsx
        ├── index.css
        ├── api/
        │   └── client.js
        ├── components/
        │   └── Navbar.jsx
        └── pages/
            ├── Dashboard.jsx
            ├── RecognizePage.jsx
            ├── LivePage.jsx
            └── DatasetPage.jsx
```

---

## 🚀 How to Run

### Prerequisites
- Python 3.9 or higher
- Node.js 18 or higher
- A webcam (for live feed)

---

### Step 1 — Backend Setup

```bash
# Open a terminal and go to the backend folder
cd face_recognition_pro/backend

# Create a virtual environment (recommended)
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask server
python app.py
```

Backend will run at → **http://localhost:5000**

---

### Step 2 — Frontend Setup

```bash
# Open a NEW terminal and go to the frontend folder
cd face_recognition_pro/frontend

# Install Node dependencies
npm install

# Start the development server
npm run dev
```

Frontend will run at → **http://localhost:3000**

Open your browser and go to **http://localhost:3000**

---

### Step 3 — Add Faces to Dataset

**Option A — Via Web UI (Recommended):**
1. Go to **Dataset** page in the browser
2. Enter a person's name
3. Drop in 20–50 photos of that person
4. Click **Upload Images**
5. Click **Train Model** (top right)

**Option B — Via Webcam Script:**
```bash
# From backend/ folder with venv active
python capture_faces.py
# Enter the person's name when prompted
# The script captures 40 face images from your webcam
# Then click "Train Model" in the UI or run training via API
```

**Option C — Copy existing dataset (legacy format):**
```
backend/dataset/User.1.1.jpg
backend/dataset/User.1.2.jpg   ← ID 1 = Person 1
backend/dataset/User.2.1.jpg   ← ID 2 = Person 2
```
Then click **Train Model**.

---

### Step 4 — Recognize Faces

1. Go to **Recognize** page
2. Upload any photo
3. Click **Recognize**
4. See results with confidence scores

### Step 5 — Live Camera Feed

1. Go to **Live Feed** page
2. Click **Detect** or **Recognize**
3. Your webcam stream appears with face overlays

---

## 🔌 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/face/detect` | Detect faces in uploaded image |
| POST | `/api/face/recognize` | Recognize faces in uploaded image |
| POST | `/api/face/train` | Load DeepFace embeddings from dataset |
| GET | `/api/face/model-info` | Model status & known persons |
| POST | `/api/dataset/upload` | Upload images for a person |
| GET | `/api/dataset/persons` | List all persons in dataset |
| GET | `/api/dataset/stats` | Dataset statistics |
| DELETE | `/api/dataset/delete/<name>` | Delete a person's data |
| GET | `/api/stream/video_feed` | MJPEG live stream |
| POST | `/api/stream/mode/<mode>` | Set stream mode (none/detect/recognize) |

---

## ⚠️ Special Cases

### Twins / Look-alikes
- DeepFace may struggle with identical twins
- **Suggestion**: When confidence is between 60–85%, trigger a secondary verification (e.g. ask for ID, OTP, or voice input)

### Facial Changes (glasses, beard, injury)
- Upload multiple variants per person (with/without glasses, different lighting, different expressions)
- More samples = more robust model

### Unknown persons
- Any face with confidence below threshold is labelled "Unknown"
- Confidence threshold is set in `config.py` → `CONFIDENCE_THRESHOLD = 70`

---

## ⚙️ Configuration (backend/config.py)

| Setting | Default | Description |
|---------|---------|-------------|
| `CONFIDENCE_THRESHOLD` | 70 | Lower = stricter matching |
| `SAMPLES_PER_PERSON` | 40 | Target samples when using capture script |
| `IMG_SIZE` | (200, 200) | Face ROI size for preprocessing |

---

## 🏭 Deployment

### Backend (Production)
```bash
pip install gunicorn
gunicorn -w 2 -b 0.0.0.0:5000 "app:create_app()"
```

### Frontend (Production Build)
```bash
npm run build
# Serve the dist/ folder with any static server
# e.g. nginx, or: npx serve dist
```

### Docker (optional)
You can containerise each service. A basic `Dockerfile` per service is recommended.

---

## 📦 Dependencies

**Backend:**
- `flask` — Web framework
- `flask-cors` — Cross-origin support
- `opencv-contrib-python` — Face detection + Haar cascade
- `deepface` — Deep learning face recognition
- `numpy` — Array operations
- `Pillow` — Image loading

**Frontend:**
- `react` + `react-router-dom` — SPA routing
- `tailwindcss` — Utility CSS
- `axios` — HTTP client
- `react-dropzone` — Drag & drop uploads
- `react-hot-toast` — Notifications
- `lucide-react` — Icons

from deepface import DeepFace
import numpy as np
import os
import cv2
import pickle


class FaceRecognitionService:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        backend_dir = os.path.abspath(os.path.join(BASE_DIR, ".."))
        self.dataset_path = os.path.join(backend_dir, "dataset")

        # ✅ cache file inside backend folder
        self.cache_path = os.path.join(backend_dir, "embeddings.pkl")
        self.lbph_path = os.path.join(backend_dir, "lbph_model.yml")
        self.names_path = os.path.join(backend_dir, "names.pkl")
        
        # 🔥 Haar Cascade for face detection
        cascade_path = os.path.join(backend_dir, "Cascades", "haarcascade_frontalface_default.xml")
        self.cascade = cv2.CascadeClassifier(cascade_path)

        print("📁 Dataset path:", self.dataset_path)

        # 🔥 LBPH recognizer
        self.lbph = cv2.face.LBPHFaceRecognizer_create()
        self.names = []

        # Load LBPH if exists
        if os.path.exists(self.lbph_path):
            try:
                self.lbph.read(self.lbph_path)
            except Exception as e:
                print(f"⚠️  Could not load LBPH model: {e}")
        
        if os.path.exists(self.names_path):
            try:
                with open(self.names_path, "rb") as f:
                    self.names = pickle.load(f)
            except Exception as e:
                print(f"⚠️  Could not load names: {e}")

        # 🔥 preload embeddings
        self.db = self._load_database()

    def train(self):
        """Train LBPH model with lenient face detection"""
        print("\n" + "="*60)
        print("🚀 Starting LBPH training...\n")
        
        images = []
        labels = []
        self.names = []
        name_to_id = {}
        id_counter = 0
        total_files = 0
        skipped = 0
        added = 0
        
        print(f"📁 Dataset path: {self.dataset_path}")
        print(f"✓ Path exists: {os.path.exists(self.dataset_path)}\n")
        
        if not os.path.exists(self.dataset_path):
            print("❌ Dataset folder not found")
            return {
                "persons_trained": 0,
                "total_samples": 0,
                "error": "Dataset folder not found"
            }
        
        # 🔄 Scan all persons
        all_items = os.listdir(self.dataset_path)
        print(f"📂 Found {len(all_items)} items in dataset folder\n")
        
        for person in all_items:
            person_path = os.path.join(self.dataset_path, person)
            if not os.path.isdir(person_path):
                print(f"  ⊘ Skipping non-folder: {person}")
                continue
                
            if person not in name_to_id:
                name_to_id[person] = id_counter
                self.names.append(person)
                id_counter += 1
            
            person_label = name_to_id[person]
            person_files = os.listdir(person_path)
            image_files = [f for f in person_files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
            print(f"📸 [{person_label}] {person}: {len(image_files)} images")
            
            # 🔍 Process each image
            for file in image_files:
                total_files += 1
                img_path = os.path.join(person_path, file)
                
                try:
                    img = cv2.imread(img_path)
                    if img is None:
                        print(f"    ⚠️  Cannot read: {file}")
                        skipped += 1
                        continue
                    
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    
                    # 🔥 Try to detect faces with lenient parameters
                    faces = self.cascade.detectMultiScale(
                        gray, 
                        scaleFactor=1.1,      # More lenient (scan at finer scales)
                        minNeighbors=3,       # Lower threshold
                        minSize=(20, 20)      # Smaller minimum face size
                    )
                    
                    if len(faces) > 0:
                        # Use the largest face detected
                        (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])
                        face_roi = gray[y:y+h, x:x+w]
                        images.append(face_roi)
                        labels.append(person_label)
                        added += 1
                    else:
                        # ⚠️ If no face detected, try using the entire image
                        # This is a fallback for challenging lighting/angles
                        if gray.size > 400:  # Make sure image is reasonably sized
                            images.append(gray)
                            labels.append(person_label)
                            added += 1
                        else:
                            skipped += 1
                    
                except Exception as e:
                    print(f"    ❌ Error: {file} - {str(e)}")
                    skipped += 1
                    continue
        
        print(f"\n{'='*60}")
        print(f"📊 TRAINING SUMMARY:")
        print(f"   Total files found: {total_files}")
        print(f"   Successfully added: {added}")
        print(f"   Skipped/Failed: {skipped}")
        print(f"   Unique persons: {len(self.names)}")
        print(f"{'='*60}\n")
        
        # 🔥 Train LBPH
        if len(images) > 0:
            print("🔥 Training LBPH model...")
            try:
                self.lbph.train(images, np.array(labels))
                self.lbph.write(self.lbph_path)
                print(f"✅ Model saved to: {self.lbph_path}")
                
                with open(self.names_path, "wb") as f:
                    pickle.dump(self.names, f)
                print(f"✅ Names saved to: {self.names_path}\n")
                
                return {
                    "persons": len(self.names),
                    "samples": len(images)
                }
            except Exception as e:
                print(f"❌ Training error: {str(e)}\n")
                return {
                    "persons_trained": 0,
                    "total_samples": 0,
                    "error": f"Training failed: {str(e)}"
                }
        else:
            print("❌ No valid images found to train\n")
            return {
                "persons_trained": 0,
                "total_samples": 0,
                "error": "No valid images found"
            }

    # ---------------- LOAD DATASET ----------------
    def _load_database(self, force_reload=False):
        database = []

        # ⚡ LOAD CACHE IF EXISTS (unless force reload)
        if not force_reload and os.path.exists(self.cache_path):
            print("⚡ Loading cached embeddings...")
            with open(self.cache_path, "rb") as f:
                return pickle.load(f)

        if not os.path.exists(self.dataset_path):
            print("❌ Dataset folder not found")
            return database

        # 🔄 LOAD FROM DATASET
        for person in os.listdir(self.dataset_path):
            person_path = os.path.join(self.dataset_path, person)

            if not os.path.isdir(person_path):
                continue

            print(f"🔄 Loading: {person}")

            for file in os.listdir(person_path):
                img_path = os.path.join(person_path, file)

                if not file.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue

                try:
                    embedding = DeepFace.represent(
                        img_path=img_path,
                        model_name="Facenet",
                        detector_backend="opencv",
                        enforce_detection=False
                    )[0]["embedding"]

                    database.append({
                        "name": person,
                        "embedding": embedding
                    })

                except Exception:
                    print("Skipping:", img_path)

        print(f"\n✅ Loaded {len(database)} embeddings\n")

        # 💾 SAVE CACHE
        with open(self.cache_path, "wb") as f:
            pickle.dump(database, f)

        return database

    # ---------------- RECOGNITION ----------------
    def recognize_faces(self, image_bytes: bytes):
        """Recognize faces using DeepFace for accurate results"""
        try:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None:
                return {
                    "face_count": 0,
                    "results": [],
                    "error": "Invalid image"
                }

            if len(self.db) == 0:
                return {
                    "face_count": 0,
                    "results": [],
                    "error": "No dataset loaded"
                }

            # 🔥 USE DEEPFACE FOR ACCURATE RECOGNITION
            print("🔍 Using DeepFace for accurate face recognition...")
            
            query_embedding = DeepFace.represent(
                img_path=img,
                model_name="Facenet",
                detector_backend="opencv",
                enforce_detection=False
            )[0]["embedding"]

            # 🔥 MATCHING
            min_dist = float("inf")
            best_match = "Unknown"

            for data in self.db:
                dist = np.linalg.norm(
                    np.array(query_embedding) - np.array(data["embedding"])
                )

                if dist < min_dist:
                    min_dist = dist
                    best_match = data["name"]

            print(f"Match: {best_match} | Distance: {min_dist}")

            # 🔥 THRESHOLD
            if min_dist < 18:
                print(f"✅ Recognized: {best_match}")
                return {
                    "face_count": 1,
                    "results": [{
                        "name": best_match,
                        "matched": True,
                        "confidence": int(max(0, 100 - min_dist * 5))
                    }],
                    "error": None
                }

            print("❌ No match found")
            return {
                "face_count": 1,
                "results": [{
                    "name": "Unknown",
                    "matched": False,
                    "confidence": 0
                }],
                "error": None
            }

        except Exception as e:
            print(f"🔥 Recognition error: {str(e)}")
            return {
                "face_count": 0,
                "results": [],
                "error": str(e)
            }

    @property
    def is_trained(self):
        return bool(self.names and os.path.exists(self.lbph_path)) or len(self.db) > 0

    def recognize_from_frame(self, frame: np.ndarray):
        """Recognize faces in a video frame using DeepFace for live streaming."""
        results = []

        if frame is None or len(self.db) == 0:
            return results

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

        for (x, y, w, h) in faces:
            name = "Unknown"
            matched = False
            confidence = 0

            try:
                # 🔥 USE DEEPFACE FOR ACCURATE RECOGNITION
                face_roi = frame[y:y+h, x:x+w]  # Use color frame for DeepFace
                
                embedding = DeepFace.represent(
                    img_path=face_roi,
                    model_name="Facenet",
                    detector_backend="opencv",
                    enforce_detection=False
                )[0]["embedding"]

                # 🔥 MATCHING
                min_dist = float("inf")
                best_match = "Unknown"
                for data in self.db:
                    dist = np.linalg.norm(np.array(embedding) - np.array(data["embedding"]))
                    if dist < min_dist:
                        min_dist = dist
                        best_match = data["name"]

                if min_dist < 18:
                    name = best_match
                    matched = True
                    confidence = int(max(0, 100 - min_dist * 5))
                else:
                    name = "Unknown"
                    matched = False
            except Exception as e:
                print(f"Live recognition error: {e}")
                name = "Unknown"
                matched = False

            results.append({
                "bbox": (x, y, w, h),
                "name": name,
                "matched": matched,
                "confidence": confidence,
            })

        return results

    # ---------------- MODEL INFO ----------------
    def get_model_info(self):
        persons = []
        if os.path.exists(self.dataset_path):
            for person in os.listdir(self.dataset_path):
                person_path = os.path.join(self.dataset_path, person)
                if os.path.isdir(person_path):
                    persons.append(person)

        return {
            "trained": True if len(self.db) > 0 else False,
            "persons": persons,
            "person_count": len(persons)
        }


# 🔥 SINGLETON INSTANCE
face_service = FaceRecognitionService()
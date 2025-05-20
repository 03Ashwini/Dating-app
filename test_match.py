import os
import dlib
from matching.face_matcher import face_rec_model, shape_predictor

# --- Setup paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Full paths to your test images
img1_path = os.path.join(BASE_DIR, "test_faces", "person1.jpg")
img2_path = os.path.join(BASE_DIR, "test_faces", "person2.jpg")

# Optional debug: Print the full paths (for troubleshooting)
print("Image 1 Path:", img1_path)
print("Image 2 Path:", img2_path)

# --- Load images ---
try:
    img1 = dlib.load_rgb_image(img1_path)
    img2 = dlib.load_rgb_image(img2_path)
except RuntimeError as e:
    print(f"❌ Failed to load image: {e}")
    exit()

# --- Detect faces ---
detector = dlib.get_frontal_face_detector()
faces1 = detector(img1)
faces2 = detector(img2)

if len(faces1) == 0 or len(faces2) == 0:
    print("❌ Could not detect face(s). Make sure the images contain clear faces.")
    exit()

# --- Get face encodings ---
shape1 = shape_predictor(img1, faces1[0])
shape2 = shape_predictor(img2, faces2[0])
face_desc1 = face_rec_model.compute_face_descriptor(img1, shape1)
face_desc2 = face_rec_model.compute_face_descriptor(img2, shape2)

# --- Calculate Euclidean distance ---
distance = sum((a - b) ** 2 for a, b in zip(face_desc1, face_desc2)) ** 0.5

# --- Output Results ---
print(f"🔍 Face Distance: {distance:.4f}")
if distance < 0.6:
    print("✅ Faces Match")
else:
    print("❌ Faces Do Not Match")

import dlib
import os
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load model paths
predictor_path = os.path.join(BASE_DIR, 'shape_predictor_68_face_landmarks.dat')
face_rec_model_path = os.path.join(BASE_DIR, 'dlib_face_recognition_resnet_model_v1.dat')

# Load models
shape_predictor = dlib.shape_predictor(predictor_path)
face_rec_model = dlib.face_recognition_model_v1(face_rec_model_path)
face_detector = dlib.get_frontal_face_detector()

def get_face_encoding(image_path):
    """Returns 128-d face encoding for the given image"""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image not found: {image_path}")

    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = face_detector(rgb_img, 1)

    if len(faces) == 0:
        raise ValueError("No face detected in image")

    shape = shape_predictor(rgb_img, faces[0])
    face_descriptor = face_rec_model.compute_face_descriptor(rgb_img, shape)

    return np.array(face_descriptor)

def is_match(img1_path, img2_path, threshold=0.6):
    """Compares two face encodings and returns True if match"""
    enc1 = get_face_encoding(img1_path)
    enc2 = get_face_encoding(img2_path)
    distance = np.linalg.norm(enc1 - enc2)

    return distance < threshold

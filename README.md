# Dating App Project

## 🔍 Face Recognition Models

This project uses two large pre-trained face recognition model files which are **not included** in this repository due to their large size:

- shape_predictor_68_face_landmarks.dat
- dlib_face_recognition_resnet_model_v1.dat

### How to get these model files:

1. Download the files from [Dlib's official model download page](http://dlib.net/files/):
   - [shape_predictor_68_face_landmarks.dat.bz2](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2)
   - [dlib_face_recognition_resnet_model_v1.dat.bz2](http://dlib.net/files/dlib_face_recognition_resnet_model_v1.dat.bz2)

2. Extract the `.bz2` files to get the `.dat` files.

3. Place the extracted `.dat` files inside the `matching/` folder of the project.

---

**Note:** Without these model files, face recognition features in this project will not work correctly.

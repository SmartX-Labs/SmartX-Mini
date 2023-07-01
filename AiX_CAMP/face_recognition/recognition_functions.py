import cv2
import imutils
from imutils import face_utils
import numpy as np
import dlib
import glob
import face_recognition

import pickle
import os


# 기존에 저장된 얼굴 인코딩 값들을 불러옵니다
def load_saved_encodings(save_path):
    saved_encodings = {}
    if os.path.exists(save_path):
        with open(save_path, 'rb') as f:
            saved_encodings = pickle.load(f)
    print(f"Loaded {len(saved_encodings)} known face encodings")
    return saved_encodings  


# 저장되어 있는 얼굴들을 가져와 인코딩합니다
def get_known_encodings(known_path="../dataset/single_face", save_path=None):
    face_encodings = {}

    if not save_path: 
        save_path = f"{known_path}/saved_encodings.pkl"
    saved_encodings = load_saved_encodings(save_path)

    for f in glob.glob(f"{known_path}/*.jpg"):
        known_face = face_recognition.load_image_file(f)
        name = (f.split("/")[-1]).split(".")[0]
        
        if name in saved_encodings:
            face_encoding = saved_encodings[name]
            face_encodings[name] = face_encoding
        else:
            if len(face_recognition.face_encodings(known_face)) != 1 :
                continue
            face_encoding = face_recognition.face_encodings(known_face)[0]
            saved_encodings[name] = face_encoding
            face_encodings[name] = face_encoding

    # 알려진 얼굴들의 인코딩 값을 저장합니다
    with open(save_path, 'wb') as f:
        pickle.dump(face_encodings, f)
    print("Saved known face encodings to ", save_path)

    return list(face_encodings.keys()), list(face_encodings.values())


# 영상 내 얼굴들의 위치를 파악합니다
def detect_faces(img):
    face_locations = face_recognition.face_locations(img)
    return face_locations


# 등록된 얼굴인지 식별합니다
def identify_faces(distances, known_names, threshold=0.44):
    identifications = []
    for dist in distances:
        min_dist = min(dist)

        identity = "Unknown"
        if min_dist < threshold:
            i = np.argmin(dist)
            identity = known_names[i]
        identifications.append(identity)
    return identifications


# 사진 내의 모든 얼굴들을 인코딩하고 등록된 얼굴인지 식별합니다
def recognize_faces(img, face_locations, known_encodings, known_names, threshold=0.6):
    # 사진 내 탐지된 모든 얼굴을 인코딩합니다
    target_encodings = face_recognition.face_encodings(img, face_locations)
    
    # 저장되어 있는, 알려진 얼굴의 인코딩 값들과 사진에서 탐지된 인코딩 값들의 거리를 계산합니다
    distances = []
    for target_encoding in target_encodings:
        dist = face_recognition.face_distance(known_encodings, target_encoding)
        distances.append(dist)
    
    # 판단 기준 threshold보다 더 가까운지 먼지 여부에 따라 얼굴을 식별합니다
    results = identify_faces(distances, known_names, threshold)
    return results


def draw_recognition_results(img, face_locations, detected_names):
    for (t, r, b, l), name in zip(face_locations, detected_names):
        cv2.rectangle(img, (l, t), (r, b), (0, 0, 255), 2)
        cv2.rectangle(img, (l, b - 20), (r, b), (0, 0, 255), cv2.FILLED)
        cv2.putText(img, name, (l + 6, b - 8), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1) 
    cv2.imshow("Result", img)
    

if __name__ == "__main__":   
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--target_path", default="../dataset/multiple_face/bts2.jpg")
    parser.add_argument("--known_path", default="../dataset/single_face")
    parser.add_argument("--save_path", default="../dataset/single_face/saved_encodings.pkl")
    parser.add_argument("--threshold", type=float, default=0.44)
    parser.add_argument("--resize", type=float, default=600)
    args = parser.parse_args()

    img = cv2.imread(args.target_path)
    img = imutils.resize(img, width=args.resize)
 
    known_names, known_encodings = get_known_encodings(args.known_path, args.save_path)
    face_locations = detect_faces(img)
    recognized_names = recognize_faces(img, face_locations, known_encodings, known_names, args.threshold)
    draw_recognition_results(img, face_locations, recognized_names)

    cv2.waitKey(0)

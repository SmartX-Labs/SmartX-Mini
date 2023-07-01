from imutils import face_utils
import numpy as np
import imutils
import dlib
import cv2


# 이미지 내에서 얼굴의 위치를 파악합니다
def detect_faces(gray, detector):
    rects = detector(gray, 1)
    return rects


# 탐지된 얼굴 하나를 네모 박스로 표시합니다
def draw_rect(image, idx, rect):
    (x, y, w, h) = face_utils.rect_to_bb(rect)
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.putText(image, f"Face #{idx+1}", (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


# 탐지된 얼굴들을 모두 네모 박스로 표시합니다
def draw_rects(image, rects):
    for idx, rect in enumerate(rects):
        (x, y, w, h) = face_utils.rect_to_bb(rect)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, f"Face #{idx+1}", (x-10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


# 파악된 얼굴 위치에서 68개의 특징점을 추출합니다
def predict_landmark(gray, rect, predictor):
    landmarks = predictor(gray, rect)
    landmarks = face_utils.shape_to_np(landmarks)
    
    return landmarks


# 한 사람의 얼굴에서 탐지된 68개의 특징점들을 그립니다
def draw_landmarks(image, landmarks):
    for (x, y) in landmarks:
        cv2.circle(image, (x, y), 1, (0, 0, 255), -1)


# 한 사람의 얼굴에서 탐지된 68개의 특징점들로, 얼굴 눈, 코, 입 등 주요 부분들에 도형을 그립니다
def draw_face_shapes(image, landmarks):
    output = face_utils.visualize_facial_landmarks(image, landmarks)
    return output


# 한 사람의 얼굴에서 눈, 코, 입 등 8개 주요 부분들의 위치를 추출합니다
def get_facepart_rects(image, landmarks):
    face_rects = {}
    for (name, (i, j)) in face_utils.FACIAL_LANDMARKS_IDXS.items():
        (x, y, w, h) = cv2.boundingRect(np.array([landmarks[i:j]]))
        face_rects[name] = (x, y, w, h)

    return face_rects


# 한 사람의 얼굴에서 눈, 코, 입 등 8개 주요 부분들을 잘라 보여줍니다
def crop_show_facepart_rects(image, idx, face_rects):
    for name, (x, y, w, h) in face_rects.items():
        roi = image[y:y+h, x:x+w]
        roi = imutils.resize(roi, width=250, inter=cv2.INTER_CUBIC)
        cv2.putText(roi, name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 2)
        cv2.imshow(f"{idx}: {name.upper()}", roi)


# 얼굴들의 위치와 각 얼굴별 68개의 특징점을 보여줍니다
def show_raw_landmarks(image, detector, predictor):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detect_faces(image, detector)

    for idx, rect in enumerate(rects):
        draw_rect(image, idx, rect)
        landmarks = predict_landmark(gray, rect, predictor)
        draw_landmarks(image, landmarks)

    cv2.imshow("Raw detection", image)


# 두 개의 이미지를 보여줍니다
# 얼굴들의 위치, 68개 특징점을 보여줍니다 (Landmarks)
# 또한, 주요 부위에 도형을 그리고, show_parts가 참이라면 눈, 코 입 등 주요 부위 별로 잘라서 보여줍니다 (Faceparts)
def show_landmark_shape(image, detector, predictor, show_parts=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = detect_faces(gray, detector)

    clone = image.copy()
    clone2 = image.copy()

    for (idx, rect) in enumerate(rects):
        draw_rect(clone2, idx, rect)
        landmarks = predict_landmark(gray, rect, predictor)
        clone = draw_face_shapes(clone, landmarks)
        draw_landmarks(clone2, landmarks)

        if show_parts:
            face_rects = get_facepart_rects(image, landmarks)
            crop_show_facepart_rects(image, idx, face_rects)

    cv2.imshow("Landmarks", clone2)
    cv2.imshow("Faceparts", clone)
import argparse
import cv2
import imutils

from recognition_functions import get_known_encodings, detect_faces, recognize_faces, draw_recognition_results

if __name__ == "__main__":   
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_path", default="../dataset/multiple_face/bts2.jpg")
    parser.add_argument("--known_path", default="../dataset/single_face")
    parser.add_argument("--save_path", default="../dataset/single_face/saved_encodings.pkl")
    parser.add_argument("--threshold", type=float, default=0.6)
    args = parser.parse_args()

    img = cv2.imread(args.img_path)
    img = imutils.resize(img, width=800)

    known_names, known_encodings = get_known_encodings(args.known_path)
    face_locations = detect_faces(img)
    recognized_names = recognize_faces(img, face_locations, known_encodings, known_names, args.threshold)
    draw_recognition_results(img, face_locations, recognized_names)

    cv2.waitKey(0)
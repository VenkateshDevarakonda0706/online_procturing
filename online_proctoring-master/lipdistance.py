import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

def calculate_lip_distance(landmarks):
    # Indices for the top and bottom of the lips
    top_lip_idx = 13  # Upper lip
    bottom_lip_idx = 14  # Lower lip
    
    top_lip = landmarks[top_lip_idx]
    bottom_lip = landmarks[bottom_lip_idx]

    # Calculate the Euclidean distance between the two points
    lip_distance = ((top_lip.x - bottom_lip.x) ** 2 + (top_lip.y - bottom_lip.y) ** 2) ** 0.5
    return lip_distance

cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(image_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            lip_distance = calculate_lip_distance(face_landmarks.landmark)
            print(f"Lip Distance: {lip_distance}")
            mp_drawing.draw_landmarks(image, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION)
    
    cv2.imshow('MediaPipe FaceMesh', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()

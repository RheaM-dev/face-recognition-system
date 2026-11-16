import cv2
import os
import numpy as np

DATASET_DIR = "dataset"
MODEL_FILE = "trainer.yml"

face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def capture_faces(user_id, num_samples=30):
    """Save grayscale face photos for one user. Returns how many were saved."""
    os.makedirs(DATASET_DIR, exist_ok=True)
    cam = cv2.VideoCapture(0)
    count = 0

    while count < num_samples:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            face_img = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
            cv2.imwrite(f"{DATASET_DIR}/user.{user_id}.{count}.jpg", face_img)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Registering face (press q to cancel)", frame)
        if cv2.waitKey(100) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()
    return count


def train_model():
    """Train the recogniser on every photo in the dataset folder.
    Returns True if a model was saved, False if there was nothing to train on."""
    if not os.path.exists(DATASET_DIR):
        return False

    images = []
    labels = []

    for file in os.listdir(DATASET_DIR):
        if file.endswith(".jpg"):
            path = os.path.join(DATASET_DIR, file)
            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
            user_id = int(file.split(".")[1])    # "user.3.12.jpg" -> 3
            images.append(img)
            labels.append(user_id)

    if len(images) == 0:
        return False

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(images, np.array(labels))
    recognizer.save(MODEL_FILE)
    return True


def recognize_faces(db, threshold=70):
    """Live recognition. Marks attendance for every recognised user."""
    if not os.path.exists(MODEL_FILE):
        print("No trained model found. Register a user first.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(MODEL_FILE)
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_img = cv2.resize(gray[y:y + h, x:x + w], (200, 200))
            user_id, distance = recognizer.predict(face_img)

            label = "Unknown"
            color = (0, 0, 255)                      # red

            if distance < threshold:                 # lower = better match
                user = db.get_user(user_id)
                if user is not None:
                    newly_marked = db.mark_attendance(user_id)
                    status = "Marked" if newly_marked else "Already marked"
                    label = f"{user.name} ({status})"
                    color = (0, 255, 0)              # green

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, f"{label} [{round(distance)}]", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow("Attendance (press q to stop)", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()


def delete_user_images(user_id):
    """Delete every saved photo of one user. Returns how many were removed."""
    if not os.path.exists(DATASET_DIR):
        return 0

    removed = 0
    prefix = f"user.{user_id}."            # the final dot matters

    for file in os.listdir(DATASET_DIR):
        if file.startswith(prefix):
            os.remove(os.path.join(DATASET_DIR, file))
            removed += 1

    return removed

capture_faces(2)
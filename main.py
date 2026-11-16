import os
from database import FaceDatabase
from user import Userinfo
import face_functions


def show_menu():
    print("\n===== FACE RECOGNITION ATTENDANCE SYSTEM =====")
    print("1. Register new user")
    print("2. Start attendance")
    print("3. View attendance records")
    print("4. View all users")
    print("5. Delete a user")
    print("6. Exit")


def register_user(db):
    name = input("Enter name: ").strip()
    roll_no = input("Enter roll number: ").strip()

    if not name or not roll_no:
        print("Name and roll number cannot be empty.")
        return

    user_id = db.add_user(Userinfo(name, roll_no))
    if user_id is None:
        print("This roll number is already registered.")
        return

    print("Look at the camera and move your head slightly...")
    count = face_functions.capture_faces(user_id)

    if count < 10:
        db.delete_user(user_id)
        face_functions.delete_user_images(user_id)
        print("Not enough face photos were captured. Registration cancelled.")
        return

    face_functions.train_model()
    print(f"{name} registered successfully!")


def start_attendance(db):
    print("Starting camera... press q in the camera window to stop.")
    face_functions.recognize_faces(db)


def view_attendance(db):
    records = db.get_attendance()
    if not records:
        print("No attendance records yet.")
        return

    print(f"\n{'Name':<20}{'Roll No':<15}{'Date':<12}{'Time'}")
    print("-" * 60)
    for name, roll_no, date, time in records:
        print(f"{name:<20}{roll_no:<15}{date:<12}{time}")


def view_users(db):
    users = db.get_all_users()
    if not users:
        print("No users registered.")
        return

    for user in users:
        print(user)


def delete_user(db):
    users = db.get_all_users()
    if not users:
        print("No users to delete.")
        return

    view_users(db)
    try:
        user_id = int(input("Enter the ID to delete: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    if db.get_user(user_id) is None:
        print("User not found.")
        return

    db.delete_user(user_id)
    face_functions.delete_user_images(user_id)

    if not face_functions.train_model():             # no photos left at all
        if os.path.exists(face_functions.MODEL_FILE):
            os.remove(face_functions.MODEL_FILE)

    print("User deleted.")


def main():
    db = FaceDatabase()

    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            register_user(db)
        elif choice == "2":
            start_attendance(db)
        elif choice == "3":
            view_attendance(db)
        elif choice == "4":
            view_users(db)
        elif choice == "5":
            delete_user(db)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
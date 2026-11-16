# Face Recognition Attendance System

A menu-driven Python project that registers people with their face, recognises them through the webcam, and marks their attendance in a database.

**Name:RHEA MADHIKAR
**Roll number:2025BCS0215

---

## What this project does

I built this to see how attendance could be taken automatically, without anyone writing names on paper. The program can:

1. **Register a new user:** takes a name and roll number, saves them in the database, and captures 30 photos of the person's face from the webcam.
2. **Recognise faces live:** opens the webcam, finds each face, and works out who it is.
3. **Mark attendance:** records the date and time when a registered person is recognised. A person is marked only **once per day**, even if they stay in front of the camera.
4. **Show records:** prints the attendance report with names, roll numbers, dates and times.
5. **Show all users** and **delete a user:** removing someone also deletes their photos and retrains the model, so the system forgets them.

If someone it doesn't know appears, the box turns red and says **Unknown**, and nothing is saved.

---

## Technologies used

| Tool | What I used it for |
|---|---|
| Python | the whole project |
| OpenCV (`opencv-contrib-python`) | webcam access, image handling, face detection (Haar cascade), face recognition (LBPH) |
| NumPy | images are NumPy arrays. I used array slicing to crop faces and an array for the training labels. |
| SQLite (`sqlite3`) | the database that stores users and attendance |
| `datetime`, `os` | date and time for attendance, and creating, listing and deleting files and folders |

---

## Python concepts covered

- **Functions:** default arguments, return values, and splitting the job into small functions
- **OOP:** the `Userinfo` class (constructor, attributes, `__str__`) and the `FaceDatabase` class that holds all database code
- **NumPy:** array slicing to crop faces, and a label array for training
- **Database:** creating tables, primary and foreign keys, a `UNIQUE` constraint, insert, select and delete, a **JOIN** for the attendance report, and parameterised queries (`?`) to avoid SQL injection
- **Exception handling:** `try / except / finally` for duplicate roll numbers and invalid input
- **File handling:** saving, reading and deleting image files
- **Modules:** one project split across several files that import from each other
- **Loops and conditions:** a menu loop, the camera loop, and input validation

---

## How it works

1. **Registration:** the user's details go into the `users` table, and the database gives them an id.
2. **Capture:** the webcam finds the face in each frame using a Haar cascade. The face is cropped, converted to grayscale, resized to 200 x 200, and saved as `dataset/user.<id>.<number>.jpg`. The id in the file name is the label.
3. **Training:** all the photos are read, and an LBPH face recogniser learns from them. The model is saved to `trainer.yml`.
4. **Recognition:** for each face in the live video, the model returns the closest user id and a **distance score**. The lower the score, the better the match. If the score is under the threshold (70), the id is looked up in the database, and attendance is marked. Otherwise the face is shown as Unknown.

Face **detection** (where is a face?) and face **recognition** (whose face is it?) are two separate steps. I used detection first, and then recognition on the cropped face.

---

## Project structure

```
FaceAttendanceSystem/
├── main.py            # the menu and the program flow
├── user.py            # Userinfo class (one person's details)
├── database.py        # FaceDatabase class (all SQLite code)
├── face_functions.py  # camera, training and recognition functions
├── requirements.txt   # libraries needed
└── README.md
```

These are created automatically when the program runs:

- `face_database.db`: the SQLite database
- `dataset/`: the saved face photos
- `trainer.yml`: the trained model

### Database tables

**users**

| Column | Type | Notes |
|---|---|---|
| id | INTEGER | primary key, assigned automatically |
| name | TEXT | required |
| roll_no | TEXT | required and unique |

**attendance**

| Column | Type | Notes |
|---|---|---|
| id | INTEGER | primary key |
| user_id | INTEGER | foreign key to `users(id)` |
| date | TEXT | for example 2026-10-20 |
| time | TEXT | for example 12:21:40 |

---

## How to run it

You need Python 3.10 or newer and a webcam.

1. Open the project folder in a terminal.
2. Create and activate a virtual environment:
```
   python -m venv venv
   venv\Scripts\activate
```
3. Install the libraries:
```
   pip install -r requirements.txt
```
4. Start the program:
```
   python main.py
```

### Using the menu

```
1. Register new user
2. Start attendance
3. View attendance records
4. View all users
5. Delete a user
6. Exit
```

- **Register:** type the name and roll number, then look at the camera and move your head slightly until the window closes.
- **Attendance:** the camera opens, and recognised people appear in green with their name. Press **q** in the camera window to stop.

---

## Things I learned and problems I ran into

- OpenCV 5.0 could not load the face cascade file, so I pinned version **4.10.0.84** in `requirements.txt`.
- `dlib` and the `face_recognition` library are hard to install on Windows, so I used OpenCV's built-in recogniser, which installs with one command.
- Test code left at the bottom of a file runs every time that file is imported, so I kept test code in separate scratch files.
- The distance threshold matters. A value that is too high lets strangers through, and one that is too low rejects real users, so I tuned it by watching the distance numbers on screen.

---

## Limitations

- It works best on **front-facing faces in good light**. Haar cascades struggle with side views and dim rooms.
- LBPH is a classic method and not deep learning, so it is less accurate than modern systems. It is not meant for security use.
- Register **one person at a time**. If two faces are in the frame during registration, both are saved under the same id.
- Photos taken in one lighting condition recognise less well in a very different one.

## Ideas for the future

- Export the attendance report to a CSV file
- A simple graphical interface
- A deep-learning detector for better accuracy
- Registration by uploading photos as well as using the webcam

---

*Face photos are personal data. This project stores them only on the local computer, and they should be deleted when no longer needed.*
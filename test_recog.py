from database import FaceDatabase
from user import Userinfo
from face_functions import recognize_faces

db = FaceDatabase()
db.add_user(Userinfo("Test Person", "CS101"))   # gets id 1 on a fresh database, None if already there
recognize_faces(db)
from database import FaceDatabase
from user import Userinfo

face_db = FaceDatabase()
print("Database Created Successfully")

# ---------------------------------add users------------------------------------------
print("Add user:", face_db.add_user(Userinfo("p_1", "CS101")))
print("Same roll no. again CASE:", face_db.add_user(Userinfo("p_2", "CS101")))
print("Add second user:", face_db.add_user(Userinfo("p_3", "CS102")))

# ------------------------------------get one user------------------------------------
print("Get user 1:", face_db.get_user(1))
print("Get user 99:", face_db.get_user(99))

# ------------------------------------get all users------------------------------------
print("All users:")
for u in face_db.get_all_users():
    print(u)

# ------------------------------------attendance------------------------------------
print("Mark attendance, first time:", face_db.mark_attendance(1))
print("Mark attendance, second time:", face_db.mark_attendance(1))
print("Attendance report:")
for row in face_db.get_attendance():
    print(row)

# delete
face_db.delete_user(2)
print("After deleting user 2:")
for u in face_db.get_all_users():
    print(u)
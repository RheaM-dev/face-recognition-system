class Userinfo:
    def __init__(self, name, roll_no,id= None):
        self.name = name
        self.roll_no = roll_no
        self.id = id

    def __str__(self):
        return f"USER NAME:- {self.name}, ROLL NO:- {self.roll_no}, ID:- {self.id}"


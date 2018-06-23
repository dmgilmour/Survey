import random
from shared_model import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    registered = db.Column(db.Boolean, default = False)
    reg_code = db.Column(db.String(16))

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def set_reg_code(reg_code):
        self.reg_code = reg_code


from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from app.models.abstract import BaseModel
from app.models.enums import Status
from app.models.enums.user import UserRole


@login_manager.user_loader
def load_user(uid):
    return User.query.filter_by(id=int(uid)).filter_by(status=Status.active).first()


class User(BaseModel, UserMixin):
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(15), nullable=False)
    last_name = db.Column(db.String(15), nullable=False)
    full_name = db.column_property(first_name + ' ' + last_name)
    phone_number = db.Column(db.String(15), nullable=True)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.active, server_default=Status.active.name)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.staff, server_default=UserRole.staff.name)
    note = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return "User({0})".format(self.username)

    def generate_password_hash(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_user_status(self):
        return "Aktif" if self.status == Status.active else "Pasif"

    def get_user_role(self):
        return "Personel" if self.role == UserRole.staff else "Admin"

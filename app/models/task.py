from sqlalchemy import func

from app import db
from app.models.abstract import BaseModel
from app.models.enums import Status
from app.models.enums.task import StationDirection, LeafletDirection


class Task(BaseModel):
    title = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    note = db.Column(db.Text, nullable=True)
    status = db.Column(db.Enum(Status), nullable=False, default=Status.active, server_default=Status.active.name)

    def __repr__(self):
        return "Task({0})".format(self.title)

    def get_task_status(self):
        return "Aktif" if self.status == Status.active else "Pasif"


class Assignment(BaseModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User")
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    task = db.relationship("Task", backref="assignments")

    def __repr__(self):
        return "Assignment({0} -> {1})".format(self.task.title, self.user.username)


class Line(BaseModel):
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    task = db.relationship("Task", backref="lines")
    title = db.Column(db.String(250), nullable=False)  # Hattın İsmi
    code = db.Column(db.String(10), nullable=True)  # Hattın Kodu
    number_of_daily_expeditions = db.Column(db.Integer, nullable=True)  # Günlük Sefer Sayısı
    number_of_daily_vehicles = db.Column(db.Integer, nullable=True)  # Günlük Araç Sayısı
    number_of_total_vehicles = db.Column(db.Integer, nullable=True)  # Toplam Araç Sayısı
    average_distance = db.Column(db.Integer, nullable=True)  # Ortalama Mesafe (KM)
    average_time_of_expeditions = db.Column(db.Integer, nullable=True)  # Ortalama Sefer Süresi (DK)
    frequency_of_expeditions = db.Column(db.Integer, nullable=True)  # Sefer Aralığı (DK)

    def __repr__(self):
        return "Line({0} -> {1})".format(self.task.title, self.title)

    def get_total_passenger(self, direction=None):
        filter_array = [Entry.leaflet.has(Leaflet.line_id == self.id)]

        if direction:
            filter_array.append(
                Entry.leaflet.has(Leaflet.direction == getattr(LeafletDirection, direction))
            )

        total_passenger = Entry.query.with_entities(
            func.sum(Entry.entry).label('total_entry'),
        ).filter(
            *filter_array
        ).first()

        return total_passenger

    def get_total_leaflet(self, direction=None):
        filter_array = [Leaflet.line_id == self.id]

        if direction:
            filter_array.append(
                Leaflet.direction == getattr(LeafletDirection, direction)
            )

        total_leaflet = Leaflet.query.with_entities(
            func.count(Leaflet.id).label('total_leaflet'),
        ).filter(
            *filter_array
        ).first()

        return total_leaflet


class Station(BaseModel):
    line_id = db.Column(db.Integer, db.ForeignKey('line.id'), nullable=False)
    line = db.relationship("Line", backref="stations")
    title = db.Column(db.String(250), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    direction = db.Column(db.Enum(StationDirection), nullable=False)
    latitude = db.Column(db.String(255), nullable=True)  # Enlem
    longitude = db.Column(db.String(255), nullable=True)  # Boylam

    def __repr__(self):
        return "Station({0} -> {1})".format(self.line.title, self.title)

    def get_station_direction(self):
        return "Gidiş" if self.direction == StationDirection.forward else "Dönüş"

    def get_passangers(self, direction=None):
        filter_array = [Entry.station_id == self.id]

        if direction:
            filter_array.append(
                Entry.leaflet.has(Leaflet.direction == getattr(LeafletDirection, direction))
            )

        total_passenger = Entry.query.with_entities(
            func.sum(Entry.entry).label('total_entry'),
        ).filter(
            *filter_array
        ).first()

        return total_passenger


class Leaflet(BaseModel):
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    task = db.relationship("Task", backref="leaflets")
    line_id = db.Column(db.Integer, db.ForeignKey('line.id'), nullable=False)
    line = db.relationship("Line", backref="leaflets")
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User")
    plate = db.Column(db.String(15), nullable=False)
    departure_time = db.Column(db.Time(), nullable=False)
    finish_time = db.Column(db.Time(), nullable=True)
    number = db.Column(db.Integer, nullable=False)
    direction = db.Column(db.Enum(LeafletDirection), nullable=False)
    is_completed = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return "Leaflet({0} -> {1})".format(self.line.title, self.departure_time)

    def get_leaflet_direction(self):
        return "Gidiş" if self.direction == StationDirection.forward else "Dönüş"

    def get_total_entry(self):
        total = Entry.query.with_entities(
            func.sum(Entry.entry).label('total_entry'),
            func.sum(Entry.exit).label('total_exit'),
        ).filter_by(leaflet_id=self.id).first()

        return total


class Entry(BaseModel):
    leaflet_id = db.Column(db.Integer, db.ForeignKey('leaflet.id'), nullable=False)
    leaflet = db.relationship("Leaflet", backref="entries")
    station_id = db.Column(db.Integer, db.ForeignKey('station.id'), nullable=True)
    station = db.relationship("Station", backref="entries")
    station_name = db.Column(db.String(255), nullable=True)
    entry = db.Column(db.Integer, nullable=True)
    exit = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return "Entry({0} -> {1}/{2})".format(self.station_name, self.entry, self.exit)

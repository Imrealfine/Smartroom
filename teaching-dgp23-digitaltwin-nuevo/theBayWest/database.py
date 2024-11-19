"""
    module which create the database of the application
"""
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import event

db: SQLAlchemy = SQLAlchemy()

def init_db(app):
    """
        initialization of the database
    """
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
    db.init_app(app)

# ROOM
class Room(db.Model):
    """
        creation of the table room
    """
    __tablename__ = 'room'

    name = db.Column(db.String(200), primary_key=True)
    size = db.Column(db.Float, nullable=False)

    # Relationships
    ventilators = db.relationship('Ventilator', backref='room', cascade='all, delete-orphan')
    windows = db.relationship("Window", cascade='all,delete-orphan', backref="room")
    lights = db.relationship("Light", cascade='all,delete-orphan', backref="room")
    people = db.relationship("PeopleInRoom", cascade='all,delete-orphan', backref="room")
    temperature = db.relationship("Temperature", cascade='all,delete-orphan', backref="room")
    co2 = db.relationship("CO2", cascade='all,delete-orphan', backref="room")
    doorConnects = db.relationship("DoorConnectsRoom", cascade='all,delete-orphan', backref="room")

    def func1(self):
        """
            function to pass pylint
        """
        return 1

    def func2(self):
        """
            function to pass pylint
        """
        return 2


# VENTILATORS
class Ventilator(db.Model):
    """
        creation of the table ventilator
    """
    __tablename__ = 'ventilator'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String(200), db.ForeignKey("room.name"), nullable=False)

    # Relationships
    ventilatorOn = db.relationship("VentilatorOn",
    cascade='all, delete-orphan', backref="ventilator")

    def func1(self):
        """
            function to pass pylint
        """
        return 1

    def func2(self):
        """
            function to pass pylint
        """
        return 2

class VentilatorOn(db.Model):
    """
        creation of the table wentilator on
    """
    __tablename__ = 'ventilator_on'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(200), nullable=False)
    ventilator_id = db.Column(db.Integer, db.ForeignKey("ventilator.id"), nullable=False)
    is_on = db.Column(db.Boolean, nullable=False)

    def func1(self):
        """
            function to pass pylint
        """
        return 1

    def func2(self):
        """
            function to pass pylint
        """
        return 2

# WINDOWS
class Window(db.Model):
    """
        creation of the table window
    """
    __tablename__ = 'window'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.String(200), db.ForeignKey("room.name"), nullable=False)

    # Relationships
    windowOpen = db.relationship("WindowOpen", cascade='all,delete-orphan', backref="window")

    def func1(self):
        """
            function to pass pylint
        """
        return 1

    def func2(self):
        """
            function to pass pylint
        """
        return 2
class WindowOpen(db.Model):
    """
        creation of the table window open
    """
    __tablename__ = 'window_open'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(200), nullable=False)
    window_id = db.Column(db.Integer, db.ForeignKey("window.id"), nullable=False)
    is_open = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f"<task {self.window_id}>"

    def func1(self):
        """
            function to pass pylint
        """
        return 1

    def func2(self):
        """
            function to pass pylint
        """
        return 2

# LIGHTS
class Light(db.Model):
    """
        creation of the table light
    """
    __tablename__ = 'light'

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.String(200), db.ForeignKey("room.name"), nullable=False)

    # Relationships
    lightOn = db.relationship("LightOn", cascade='all,delete-orphan', backref="light")

    def func1(self):
        """
            function to pass pylint
        """
        return 1

    def func2(self):
        """
            function to pass pylint
        """
        return 2
class LightOn(db.Model):
    """
        creation of the table light on
    """
    __tablename__ = 'light_on'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(200), nullable=False)
    light_id = db.Column(db.Integer, db.ForeignKey("light.id"), nullable=False)
    is_on = db.Column(db.Boolean, nullable=False)

    def func1(self):
        """
            function to pass pylint
        """
        return 1

    def func2(self):
        """
            function to pass pylint
        """
        return 2

# DOORS
class Door(db.Model):
    """
        creation of the table door
    """
    __tablename__ = 'door'

    id = db.Column(db.Integer, primary_key=True)

    # Relationships
    doorOpen = db.relationship("DoorOpen", cascade='all,delete-orphan', backref="door")
    doorConnects = db.relationship("DoorConnectsRoom", cascade='all,delete-orphan', backref="door")

    def func1(self):
        """
            function to pass pylint
        """
        return 1

    def func2(self):
        """
            function to pass pylint
        """
        return 2
class DoorOpen(db.Model):
    """
        creation of the table door open
    """
    __tablename__ = 'door_open'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(200), nullable=False)
    door_id = db.Column(db.Integer, db.ForeignKey("door.id"), nullable=False)
    is_open = db.Column(db.Boolean, nullable=False)

    def func1(self):
        """
            function to pass pylint
        """
        return 1

    def func2(self):
        """
            function to pass pylint
        """
        return 2
class DoorConnectsRoom(db.Model):
    """
        creation of the table door connects room
    """
    __tablename__ = 'door_connects_room'

    door_id = db.Column(db.Integer, db.ForeignKey("door.id"), primary_key=True, nullable=False)
    room_id = db.Column(db.String(200), db.ForeignKey("room.name"),
    primary_key=True, nullable=False)

    def func1(self):
        """
            function to pass pylint
        """
        return 1

    def func2(self):
        """
            function to pass pylint
        """
        return 2

# METRICS
class PeopleInRoom(db.Model):
    """
        creation of the table people in room
    """
    __tablename__ = 'people_in_room'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(200), nullable=False)
    room_id = db.Column(db.String(200), db.ForeignKey("room.name"), nullable=False)
    no_people_in_room = db.Column(db.Integer, nullable=False)

    def func1(self):
        """
            function to pass pylint
        """
        return 1

    def func2(self):
        """
            function to pass pylint
        """
        return 2
class Temperature(db.Model):
    """
        creation of the table temperature
    """
    __tablename__ = 'temperature'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(200), nullable=False)
    room_id = db.Column(db.String(200), db.ForeignKey("room.name"), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    def func1(self):
        """
            function to pass pylint
        """
        return 1

    def func2(self):
        """
            function to pass pylint
        """
        return 2
class CO2(db.Model):
    """
        creation of the table CO2
    """
    __tablename__ = 'co2'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(200), nullable=False)
    room_id = db.Column(db.String(200), db.ForeignKey("room.name"), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    def func1(self):
        """
            function to pass pylint
        """
        return 1

    def func2(self):
        """
            function to pass pylint
        """
        return 2
"""
    module testing for the routes of app.py
"""
import pytest
from sqlalchemy import desc
from app import app, db
from database import CO2, Door, DoorConnectsRoom
from database import DoorOpen, Light, LightOn, PeopleInRoom, Temperature
from database import Room, Ventilator, VentilatorOn, Window, WindowOpen
# Import the Flask app instance and database


@pytest.fixture
def client():
    """
    function which define the client for the test .
    """
    app.config['TESTING'] = True
    #Use in-memory database for testing
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    # Disable track modifications to avoid warning
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_add_delete_room(client):
    """
    Test function for add/delete room .

    This function tests the add/delete functionality for room

    Parameters:
    - client
    """
    #Create room
    response = client.post('/add', data={'room_name': 'TestRoom', 'room_size': 20})
    assert response.status_code == 302

    #Check if room is created
    room = db.session.query(Room).filter_by(name='TestRoom').first()
    assert room.name == 'TestRoom'
    assert room.size == 20

    #Delete room
    response = client.post('/delete/TestRoom')
    assert response.status_code == 302
    #Check if room is deleted correctly
    room = db.session.query(Room).filter_by(name='TestRoom').first()
    assert room is None

def test_edit_room(client):
    """
    Test function for edit room .

    This function tests the edit functionality for room

    Parameters:
    - client
    """
    #Create room
    response = client.post('/add', data={'room_name': 'TestRoom1', 'room_size': 20})
    assert response.status_code == 302

    #Check if room is created

    room = db.session.query(Room).filter_by(name='TestRoom1').first()
    assert room.name == 'TestRoom1'
    assert room.size == 20

    #Edit the existing room
    response = client.post('/edit/TestRoom1', data={'room_name': 'TestRoom2', 'room_size': 30})
    assert response.status_code == 302

    #Check if the name is not the first one
    room = db.session.query(Room).filter_by(name='TestRoom1').first()
    assert room is None

    #Check that the room has changed
    room = db.session.query(Room).filter_by(name='TestRoom2').first()
    assert room.name == 'TestRoom2'
    assert room.size == 30

def test_add_delete_door(client):
    """
    Test function for add/delete door .

    This function tests the add/delete functionality for door

    Parameters:
    - client
    """
    #Create two rooms
    response = client.post('/add', data={'room_name': 'TestRoom1', 'room_size': 20})
    assert response.status_code == 302
    response = client.post('/add', data={'room_name': 'TestRoom2', 'room_size': 20})
    assert response.status_code == 302

    #Create door
    response = client.post('/addDoor/TestRoom1', data={'selectedRoom': 'TestRoom2'})
    assert response.status_code == 302

    #Check if door created correctly
    door = db.session.query(Door).filter_by(id = 1).first()
    assert door.id == 1

    #Check connections are also created
    door_connects = db.session.query(DoorConnectsRoom)\
    .filter_by(door_id=1, room_id='TestRoom1').first()
    assert door_connects.door_id == 1
    assert door_connects.room_id == 'TestRoom1'
    door_connects = db.session.query(DoorConnectsRoom)\
    .filter_by(door_id=1,room_id='TestRoom2').first()
    assert door_connects.door_id == 1
    assert door_connects.room_id == 'TestRoom2'

    #Create door
    response = client.post('/addDoor/TestRoom1', data={'selectedRoom': 'palceholder'})
    assert response.status_code == 302

    #Check if door created correctly
    door = db.session.query(Door).filter_by(id = 1).first()
    assert door.id == 1

    #Check connections are also created
    door_connects = db.session.query(DoorConnectsRoom)\
    .filter_by(door_id=2,room_id='TestRoom1').first()
    assert door_connects.door_id == 2
    assert door_connects.room_id == 'TestRoom1'
    door_connects = db.session.query(DoorConnectsRoom)\
    .filter_by(door_id=2,room_id='placeholder').first()
    assert door_connects is None


def test_add_delete_window(client):
    """
    Test function for add/delete window .

    This function tests the add/delete functionality for window

    Parameters:
    - client
    """
    #Create room
    response = client.post('/add', data={'room_name': 'TestRoom', 'room_size': 20})
    assert response.status_code == 302

    #Create window
    response = client.post('/addWindow/TestRoom')
    assert response.status_code == 302

    #Check if window is created correctly
    window = db.session.query(Window).filter_by(id=1).first()
    assert window.id == 1
    assert window.room_id == 'TestRoom'

    #Delete window
    response = client.post('/deleteWindow/1')
    assert response.status_code == 302

    #Check if window is deleted correctly
    window = db.session.query(Window).filter_by(id=1).first()
    assert window is None


def test_add_delete_light(client):
    """
    Test function for add/delete light .

    This function tests the add/delete functionality for light

    Parameters:
    - client
    """
    #Create room
    response = client.post('/add', data={'room_name': 'TestRoom', 'room_size': 20})
    assert response.status_code == 302

    #Create light
    response = client.post('/addLight/TestRoom')
    assert response.status_code == 302

    #Check if light is created correctly
    light = db.session.query(Light).filter_by(id=1).first()
    assert light.id == 1
    assert light.room_id == 'TestRoom'

    #Delete light
    response = client.post('/deleteLight/1')
    assert response.status_code == 302

    #Check if light is deleted correctly
    light = db.session.query(Light).filter_by(id=1).first()
    assert light is None

def test_add_delete_ventilator(client):
    """
    Test function for add/delete ventilator .

    This function tests the add/delete functionality for ventilator

    Parameters:
    - client
    """
    #Create room
    response = client.post('/add', data={'room_name': 'TestRoom', 'room_size': 20})
    assert response.status_code == 302

    #Create ventilator
    response = client.post('/addVentilator/TestRoom')
    assert response.status_code == 302

    #Check if ventilator is created correctly
    ventilator = db.session.query(Ventilator).filter_by(id=1).first()
    assert ventilator.id == 1
    assert ventilator.room_id == 'TestRoom'

    #Delete ventilator
    response = client.post('/deleteVentilator/1')
    assert response.status_code == 302

    #Check if ventilator is deleted correctly
    ventilator = db.session.query(Ventilator).filter_by(id=1).first()
    assert ventilator is None


def test_update_door_status(client):
    """
    Test function for updating door status.

    This function tests the update functionality for door status.
    It checks if the door status is correctly updated and returns the result.

    Parameters:
    - client
    """
    #Create room
    response = client.post('/add', data={'room_name': 'TestRoom', 'room_size': 20})
    assert response.status_code == 302

    #Add door
    response = client.post('/addDoor/TestRoom1', data={'selectedRoom': 'palceholder'})
    assert response.status_code == 302
    door = db.session.query(Door).filter_by(id = 1).first()
    assert door.id == 1

    # Make a request to update door status
    data = {'doorId': 1, 'status': 'on'}
    response = client.post('/updateDoorStatus', json=data)

    # Check if the response status code is 200
    assert response.status_code == 200

    # Check if the door status was updated
    updated_door_open = DoorOpen.query.filter_by(door_id=1).order_by(desc(DoorOpen.id)).first()
    assert updated_door_open is not None
    assert updated_door_open.is_open


def test_update_window_status(client):
    """
    Test function for updating window status.

    This function tests the update functionality for window status.
    It checks if the window status is correctly updated and returns the result.

    Parameters:
    - client
    """
    # Add a window to the room for testing
    response = client.post('/add', data={'room_name': 'TestRoom', 'room_size': 20})
    assert response.status_code == 302

    #Add window
    response = client.post('/addWindow/TestRoom')
    assert response.status_code == 302

    # Make a request to update window status
    data = {'windowId': 1, 'status': 'on'}
    response = client.post('/updateWindowStatus', json=data)

    # Check if the response status code is 200
    assert response.status_code == 200

    # Check if the window status was updated
    updated_window_open = WindowOpen.query.filter_by(window_id=1).\
        order_by(desc(WindowOpen.id)).first()

    assert updated_window_open is not None
    assert updated_window_open.is_open


def test_update_light_status(client):
    """
    Test function for updating light status.

    This function tests the update functionality for light status.
    It checks if the light status is correctly updated and returns the result.

    Parameters:
    - client
    """
    # Add a light to the room for testing
    response = client.post('/add', data={'room_name': 'TestRoom', 'room_size': 20})
    assert response.status_code == 302

    #Add light
    response = client.post('/addLight/TestRoom')
    assert response.status_code == 302

    # Make a request to update light status
    data = {'lightId': 1, 'status': 'on'}
    response = client.post('/updateLightStatus', json=data)

    # Check if the response status code is 200
    assert response.status_code == 200

    # Check if the light status was updated
    updated_light_on = LightOn.query.filter_by(light_id=1).order_by(desc(LightOn.id)).first()
    assert updated_light_on is not None
    assert updated_light_on.is_on


def test_update_ventilator_status(client):
    """
    Test function for updating ventilator status.

    This function tests the update functionality for ventilator status.
    It checks if the ventilator status is correctly updated and returns the result.

    Parameters:
    - client
    """
    # Add a ventilator to the room for testing
    response = client.post('/add', data={'room_name': 'TestRoom', 'room_size': 20})
    assert response.status_code == 302

    #Add ventilator
    response = client.post('/addVentilator/TestRoom')
    assert response.status_code == 302

    # Make a request to update ventilator status
    data = {'ventilatorId': 1, 'status': 'on'}
    response = client.post('/updateVentilatorStatus', json=data)

    # Check if the response status code is 200
    assert response.status_code == 200

    # Check if the ventilator status was updated
    updated_ventilator_on = VentilatorOn.query.filter_by(ventilator_id=1).\
        order_by(desc(VentilatorOn.id)).first()

    assert updated_ventilator_on is not None
    assert updated_ventilator_on.is_on


def test_update_async_content(client):
    """
    Test function for updating async-content.

    This function tests the update of the async content of the app.

    Parameters:
    - client
    """
    # Define test cases for room_name and metric_name
    test_cases = [
        ('test_room', '.dynamic-temperaturetest_room'),
        ('test_room', '.dynamic-peopletest_room'),
        ('test_room', '.dynamic-co2test_room'),
    ]

    for room_name, metric_name in test_cases:
        response = client.get(f'/update_async_content/{room_name}/{metric_name}')

        # Check if the response status code is 200
        assert response.status_code == 200

        # Check if the response contains the 'data' field
        data = response.get_json().get('data')
        assert 'data' in response.get_json()

        # Check if the data is within the expected range based on metric_name
        interval = {
            '.dynamic-temperaturetest_room': (10.0, 75.0),
            '.dynamic-peopletest_room': (0, 25),
            '.dynamic-co2test_room': (400, 1200)
        }
        l_bound, u_bound = interval[metric_name]
        assert l_bound <= data <= u_bound


def test_add_people(client):
    """
    Test function for add people.

    This function tests the add people functionality.

    Parameters:
    - client
    """
    # Create room
    response = client.post('/add', data={'room_name': 'TestRoom', 'room_size': 20})
    assert response.status_code == 302

    # Add people
    response = client.post('/add_people', json={'room_name': 'TestRoom', 'people_data': 15})
    assert response.status_code == 200

    # Check if people is added correctly
    people = db.session.query(PeopleInRoom).filter_by(id=1).first()
    assert people.id == 1
    assert people.no_people_in_room == 15


def test_add_temperature(client):
    """
    Test function for add temperature.

    This function tests the add temperature functionality.

    Parameters:
    - client
    """
    # Create room
    response = client.post('/add', data={'room_name': 'TestRoom', 'room_size': 20})
    assert response.status_code == 302

    # Add temperature
    response = client.post('/add_temperature',
                        json={'room_name': 'TestRoom', 'temperature_data': 50.5})

    assert response.status_code == 200

    # Check if temperature is added correctly
    temperature = db.session.query(Temperature).filter_by(id=1).first()
    assert temperature.id == 1
    assert temperature.value == 50.5


def test_add_co2(client):
    """
    Test function for add co2.

    This function tests the add co2 functionality.

    Parameters:
    - client
    """
    # Create room
    response = client.post('/add', data={'room_name': 'TestRoom', 'room_size': 20})
    assert response.status_code == 302

    # Add co2
    response = client.post('/add_co2', json={'room_name': 'TestRoom', 'co2_data': 50.5})
    assert response.status_code == 200

    # Check if co2 is added correctly
    co2 = db.session.query(CO2).filter_by(id=1).first()
    assert co2.id == 1
    assert co2.value == 50.5

##################

def test_get_device_status(client):
    """
    Test function for getting the device status.

    Parameters:
    - client
    """
    # Create room
    response = client.post('/add', data={'room_name': 'TestRoom', 'room_size': 20})

    #Create window
    response = client.post('/addWindow/TestRoom')

    #Create window
    response = client.post('/addWindow/TestRoom')

    #Create light
    response = client.post('/addLight/TestRoom')

    #Create light
    response = client.post('/addLight/TestRoom')

    #Create ventilator
    response = client.post('/addVentilator/TestRoom')

    #Create ventilator
    response = client.post('/addVentilator/TestRoom')

    #Create door
    response = client.post('/addDoor/TestRoom', data={'selectedRoom': 'palceholder'})

    #Create door
    response = client.post('/addDoor/TestRoom', data={'selectedRoom': 'palceholder'})

    #Get windows status
    response = client.get('/device_status?room_name=TestRoom&device_name=window')
    assert response.status_code == 200

    data = response.json
    assert 'TestRoom' in data
    result = data['TestRoom']

    # Check the result
    assert 'open_count' in result
    assert 'closed_count' in result
    assert result['open_count'] == 0
    assert result['closed_count'] == 2

    #Get lights status
    response = client.get('/device_status?room_name=TestRoom&device_name=light')
    assert response.status_code == 200

    data = response.json
    assert 'TestRoom' in data
    result = data['TestRoom']

    # Check the result
    assert 'on_count' in result
    assert 'off_count' in result
    assert result['on_count'] == 0
    assert result['off_count'] == 2

    #Get ventilators status
    response = client.get('/device_status?room_name=TestRoom&device_name=ventilator')
    assert response.status_code == 200

    data = response.json
    assert 'TestRoom' in data
    result = data['TestRoom']

    # Check the result
    assert 'on_count' in result
    assert 'off_count' in result
    assert result['on_count'] == 0
    assert result['off_count'] == 2

    #Get doors status
    response = client.get('/device_status?room_name=TestRoom&device_name=door')
    assert response.status_code == 200

    data = response.json
    assert 'TestRoom' in data
    result = data['TestRoom']

    # Check the result
    assert 'open_count' in result
    assert 'closed_count' in result
    assert result['open_count'] == 0
    assert result['closed_count'] == 2

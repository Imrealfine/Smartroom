"""
    module principal of the application with the main and the
    route
"""
from datetime import datetime
import random

from sqlite3 import IntegrityError

import csv
import pandas as pd

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
from sqlalchemy import distinct

from flask import Flask
from flask import render_template, redirect, send_file
from flask import request, jsonify

from database import CO2, Door, DoorConnectsRoom, DoorOpen
from database import Light, LightOn, PeopleInRoom, Temperature
from database import Room,Ventilator, VentilatorOn, Window, WindowOpen
from database import init_db, db


app = Flask(__name__)
init_db(app)

#session = db.session
@app.route('/', methods=["POST", "GET"])
def index():
    """
        route to have all the rooms present in the database
    """
    if request.method == "POST":
        #pass
        search_text = request.form["search_text"]
        rooms = Room.query.filter(Room.name.like('%' + search_text + '%'))\
        .order_by(Room.name).all() # orden alfabético
    else:
        rooms = Room.query.order_by(Room.name).all() # orden alfabético
    return render_template("index.html", rooms=rooms)
#To have a json of the room's name
@app.route('/get_rooms', methods=['GET'])
def get_rooms():
    """
        Returns all the rooms of the database
    """
    try:
        rooms = Room.query.all()
        room_names = [room.name for room in rooms]
        return jsonify({'rooms': room_names})
    except SQLAlchemyError as sqla_exception:
        return jsonify({'error': str(sqla_exception)})

# Adaptar esta función al Popup (la parte donde se cumple el if)
@app.route("/add", methods=["POST"])
def add():
    """
        route to add room
    """
    # Poner en la db
    room_name = request.form["room_name"]
    if not room_name:
        return "You must specify a name for the room"
    room_size = request.form["room_size"]

    new_room = Room(name=room_name, size=room_size)

    try:
        db.session.add(
            new_room)
        db.session.commit()
        return redirect('/')
    except SQLAlchemyError as sqla_exception:
        print(f"SQLAlchemy error occurred: {sqla_exception}")
        return jsonify({'error': 'A database error occurred'}), 500

@app.route('/edit/<string:room_name>', methods=["GET", "POST"])
def edit_room(room_name: str):
    """
        route to edit
    """
    room = request.form['room_name']
    room_size = request.form['room_size']

    room_to_edit = Room.query.filter_by(name=room_name).first()

    for ventilator in room_to_edit.ventilators:
        ventilator.room_id = room

    for window in room_to_edit.windows:
        window.room_id = room

    for light in room_to_edit.lights:
        light.room_id = room

    for people in room_to_edit.people:
        people.room_id = room

    for temperature in room_to_edit.temperature:
        temperature.room_id = room

    for co2 in room_to_edit.co2:
        co2.room_id = room

    connections = DoorConnectsRoom.query.filter_by(room_id=room_name)
    for item in connections:
        item.room_id = room

    if room_to_edit:
        room_to_edit.name = room
        room_to_edit.size = room_size
        db.session.commit()
        return redirect('/')
    #else:
    return "Room not found"

@app.route('/delete/<string:room_name>', methods=["POST"])
def delete_room(room_name: str):
    """
        route to delete room
    """
    room_to_delete = db.session.query(Room).filter_by(name=room_name).first()
    try:
        db.session.delete(room_to_delete)
        db.session.commit()

        return redirect('/')
    except SQLAlchemyError as sqla_exception:
        print(f"SQLAlchemy error occurred: {sqla_exception}")
        return jsonify({'error': 'A database error occurred'}), 500

@app.route("/deleteDoor/<int:door_id>", methods=["POST"])
def delete_door(door_id: int):
    """
        route to delete door
    """
    door_to_delete = db.session.query(Door).filter_by(id = door_id).first()
    try:
        db.session.delete(door_to_delete)
        db.session.commit()

        return redirect('/')
    except SQLAlchemyError as sqla_exception:
        print(f"SQLAlchemy error occurred: {sqla_exception}")
        return jsonify({'error': 'A database error occurred'}), 500

@app.route('/addDoor/<string:room_name>', methods=['POST'])
def add_door(room_name: str):
    """
        func to add a door
    """
    if request.method == 'POST':
        selected_room = request.form['selectedRoom']
        new_door = Door()
        db.session.add(new_door)
        db.session.commit()

        connection1 = DoorConnectsRoom(door_id=new_door.id, room_id=room_name)
        db.session.add(connection1)
        db.session.commit()

        if selected_room != "placeholder":
            connection2 = DoorConnectsRoom(door_id=new_door.id, room_id=selected_room)
            db.session.add(connection2)
            db.session.commit()

        # Get the timestamp for the new door entry
        timestamp = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")

        door_closed = DoorOpen(timestamp=timestamp, door_id=new_door.id, is_open=False)
        db.session.add(door_closed)
        db.session.commit()

        # Fetch all doors in the same room
        doors_in_room = DoorConnectsRoom.query.filter_by(room_id=room_name).all()

        # Create entries for all other doors with the latest timestamp
        for other_door_connection in doors_in_room:
            if other_door_connection.door_id != new_door.id:
                latest_door_open = DoorOpen.query.filter_by(door_id=other_door_connection.door_id).\
                    order_by(desc(DoorOpen.timestamp)).first()
                is_open_value = latest_door_open.is_open if latest_door_open else False
                other_door_open = DoorOpen(
                    timestamp=timestamp,
                    door_id=other_door_connection.door_id,
                    is_open=is_open_value
                )
                db.session.add(other_door_open)

        db.session.commit()

    return redirect('/')

@app.route("/addWindow/<string:room_name>", methods=["POST"])
def add_window(room_name: str):
    """
        func to add window
    """
    try:
        # Add a new window to the room
        new_window = Window(room_id=room_name)
        db.session.add(new_window)
        db.session.commit()

        # Get the timestamp for the new window entry
        timestamp = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")

        # Create an entry in WindowOpen for the new window
        window_closed = WindowOpen(timestamp=timestamp, window_id=new_window.id, is_open=False)
        db.session.add(window_closed)
        db.session.commit()

        # Fetch all windows in the same room
        windows_in_room = Window.query.filter_by(room_id=room_name).all()

        # Create entries for all other windows with the latest timestamp
        for other_window in windows_in_room:
            if other_window.id != new_window.id:

                latest_window_open = None
                if other_window.windowOpen:
                    latest_window_open = other_window.windowOpen[-1]

                is_open_value = latest_window_open.is_open if latest_window_open else False

                other_window_closed = WindowOpen(
                    timestamp=timestamp,
                    window_id=other_window.id,
                    is_open=is_open_value
                )

                db.session.add(other_window_closed)

        db.session.commit()

        return redirect('/')
    except IntegrityError as integrity_error:
        db.session.rollback()
        print(f"Integrity error occurred: {integrity_error}")
        return jsonify({'error': 'An integrity error occurred'}), 500
    except SQLAlchemyError as sqla_exception:
        print(f"SQLAlchemy error occurred: {sqla_exception}")
        return jsonify({'error': 'A database error occurred'}), 500

@app.route("/deleteWindow/<int:window_id>", methods=["POST"])
def delete_window(window_id: int):
    """
        route to delete window
    """
    window_to_delete = db.session.query(Window).filter_by(id=window_id).first()
    try:
        db.session.delete(window_to_delete)
        db.session.commit()

        return redirect('/')
    except SQLAlchemyError as sqla_exception:
        print(f"SQLAlchemy error occurred: {sqla_exception}")
        return jsonify({'error': 'A database error occurred'}), 500

@app.route("/addLight/<string:room_name>", methods=["POST"])
def add_light(room_name: str):
    """
        function to add a light
    """
    try:
        # Add a new light to the room
        new_light = Light(room_id=room_name)
        db.session.add(new_light)
        db.session.commit()

        # Get the timestamp for the new light entry
        timestamp = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")

        # Create an entry in LightOn for the new light
        light_off = LightOn(timestamp=timestamp, light_id=new_light.id, is_on=False)
        db.session.add(light_off)
        db.session.commit()

        # Fetch all lights in the same room
        lights_in_room = Light.query.filter_by(room_id=room_name).all()

        # Create entries for all other lights with the latest timestamp
        for other_light in lights_in_room:
            if other_light.id != new_light.id:
                latest_light_on = other_light.lightOn[-1] if other_light.lightOn else None
                is_on_value = latest_light_on.is_on if latest_light_on else False

                other_light_on = LightOn(
                    timestamp=timestamp,
                    light_id=other_light.id,
                    is_on=is_on_value
                )

                db.session.add(other_light_on)

        db.session.commit()

        return redirect('/')
    except IntegrityError as integrity_error:
        db.session.rollback()
        print(f"Integrity error occurred: {integrity_error}")
        return jsonify({'error': 'An integrity error occurred'}), 500
    except SQLAlchemyError as sqla_exception:
        print(f"SQLAlchemy error occurred: {sqla_exception}")
        return jsonify({'error': 'A database error occurred'}), 500


@app.route("/deleteLight/<int:light_id>", methods=["POST"])
def delete_light(light_id: int):
    """
        route to delete light
    """
    light_to_delete = db.session.query(Light).filter_by(id=light_id).first()
    try:
        db.session.delete(light_to_delete)
        db.session.commit()

        return redirect('/')
    except SQLAlchemyError as sqla_exception:
        print(f"SQLAlchemy error occurred: {sqla_exception}")
        return jsonify({'error': 'A database error occurred'}), 500

@app.route("/addVentilator/<string:room_name>", methods=["POST"])
def add_ventilator(room_name: str):
    """
        function to add a ventilator
    """
    try:
        # Add a new ventilator to the room
        new_ventilator = Ventilator(room_id=room_name)
        db.session.add(new_ventilator)
        db.session.commit()

        # Get the timestamp for the new ventilator entry
        timestamp = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")

        # Create an entry in VentilatorOn for the new ventilator
        ventilator_off = VentilatorOn(timestamp=timestamp,
                                    ventilator_id=new_ventilator.id, is_on=False)
        db.session.add(ventilator_off)
        db.session.commit()

        # Fetch all ventilators in the same room
        ventilators_in_room = Ventilator.query.filter_by(room_id=room_name).all()

        # Create entries for all other ventilators with the latest timestamp
        for other_ventilator in ventilators_in_room:
            if other_ventilator.id != new_ventilator.id:

                latest_ventilator_on = None
                if other_ventilator.ventilatorOn:
                    latest_ventilator_on = other_ventilator.ventilatorOn[-1]

                is_on_value = latest_ventilator_on.is_on if latest_ventilator_on else False
                other_ventilator_on = VentilatorOn(timestamp=timestamp,
                                                ventilator_id=other_ventilator.id,
                                                is_on=is_on_value)
                db.session.add(other_ventilator_on)

        db.session.commit()

        return redirect('/')
    except IntegrityError as integrity_error:
        db.session.rollback()
        print(f"Integrity error occurred: {integrity_error}")
        return jsonify({'error': 'An integrity error occurred'}), 500
    except SQLAlchemyError as sqla_exception:
        print(f"SQLAlchemy error occurred: {sqla_exception}")
        return jsonify({'error': 'A database error occurred'}), 500

@app.route("/deleteVentilator/<int:ventilator_id>", methods=["POST"])
def delete_ventilator(ventilator_id: int):
    """
        route to delete ventilator
    """
    ventilator_to_delete = db.session.query(Ventilator).filter_by(id=ventilator_id).first()
    try:
        db.session.delete(ventilator_to_delete)
        db.session.commit()

        return redirect('/')
    except SQLAlchemyError as sqla_exception:
        print(f"SQLAlchemy error occurred: {sqla_exception}")
        return jsonify({'error': 'A database error occurred'}), 500

@app.route('/updateDoorStatus', methods=['POST'])
def update_door_status():
    """
        function to update the door status
    """
    try:
        data = request.json
        door_id = data.get('doorId')
        status = data.get('status')
        room_id = data.get('room_id')
        tmp = status == "on"
        timestamp = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")

        # Update the status of the selected door
        door_open = DoorOpen(door_id=door_id, is_open=tmp, timestamp=timestamp)
        db.session.add(door_open)
        db.session.commit()

        response = {'message': f'Door {door_id} is now {status}'}

        # Fetch all doors in the same room
        doors_in_room = DoorConnectsRoom.query.filter_by(room_id=room_id).all()

        # Create entries for all other doors with the latest timestamp
        for other_door_connection in doors_in_room:
            if other_door_connection.door_id != door_id:
                latest_door_open = DoorOpen.query.filter_by(door_id=other_door_connection.door_id).\
                    order_by(desc(DoorOpen.timestamp)).first()

                is_open_value = latest_door_open.is_open if latest_door_open else False

                other_door_open = DoorOpen(
                    timestamp=timestamp,
                    door_id=other_door_connection.door_id,
                    is_open=is_open_value
                )

                db.session.add(other_door_open)

        db.session.commit()

        return jsonify(response)
    except SQLAlchemyError as sqla_exception:
        print(f"SQLAlchemy error occurred: {sqla_exception}")
        return jsonify({'error': 'A database error occurred'}), 500


@app.route('/updateLightStatus', methods=['POST'])
def update_light_status():
    """
    Route to update the light status
    """
    try:
        data = request.json
        light_id = data.get('lightId')
        status = data.get('status')
        tmp = status == "on"
        timestamp = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")

        # Update the status of the selected light
        light_on = LightOn(light_id=light_id, is_on=tmp, timestamp=timestamp)
        db.session.add(light_on)
        db.session.commit()

        # Fetch all lights in the same room
        lights_in_room = Light.query.\
            filter_by(room_id=light_on.light.room_id).all()

        # Create entries for all other lights with the same timestamp
        for other_light in lights_in_room:
            if other_light.id != light_id:

                other_light_on = LightOn(
                    light_id=other_light.id,
                    is_on=other_light.lightOn[-1].is_on,
                    timestamp=timestamp
                )

                db.session.add(other_light_on)

        db.session.commit()

        response = {'message': f'Light {light_id} is now {status}'}
        return jsonify(response)
    except IntegrityError as integrity_error:
        db.session.rollback()
        print(f"Integrity error occurred: {integrity_error}")
        return jsonify({'error': 'An integrity error occurred'}), 500
    except SQLAlchemyError as sqla_exception:
        print(f"SQLAlchemy error occurred: {sqla_exception}")
        return jsonify({'error': 'A database error occurred'}), 500

@app.route('/updateVentilatorStatus', methods=['POST'])
def update_ventilator_status():
    """
    Route to update the ventilator status
    """
    try:
        data = request.json
        ventilator_id = data.get('ventilatorId')
        status = data.get('status')
        tmp = status == "on"
        timestamp = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")

        # Update the status of the selected ventilator
        ventilator_on = VentilatorOn(ventilator_id=ventilator_id, is_on=tmp, timestamp=timestamp)
        db.session.add(ventilator_on)
        db.session.commit()

        # Fetch all ventilators in the same room
        ventilators_in_room = Ventilator.query.filter_by(
            room_id=ventilator_on.ventilator.room_id
        ).all()

        # Create entries for all other ventilators with the same timestamp
        for other_ventilator in ventilators_in_room:
            if other_ventilator.id != ventilator_id:

                other_ventilator_on = VentilatorOn(
                    ventilator_id=other_ventilator.id,
                    is_on=other_ventilator.ventilatorOn[-1].is_on,
                    timestamp=timestamp
                )

                db.session.add(other_ventilator_on)

        db.session.commit()

        response = {'message': f'Ventilator {ventilator_id} is now {status}'}
        return jsonify(response)
    except IntegrityError as integrity_error:
        db.session.rollback()
        print(f"Integrity error occurred: {integrity_error}")
        return jsonify({'error': 'An integrity error occurred'}), 500
    except SQLAlchemyError as sqla_exception:
        print(f"SQLAlchemy error occurred: {sqla_exception}")
        return jsonify({'error': 'A database error occurred'}), 500

@app.route('/updateWindowStatus', methods=['POST'])
def update_window_status():
    """
    Route to update the window status
    """
    try:
        data = request.json
        window_id = data.get('windowId')
        status = data.get('status')
        tmp = status == "on"
        timestamp = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")

        # Update the status of the selected window
        window_open = WindowOpen(window_id=window_id, is_open=tmp, timestamp=timestamp)
        db.session.add(window_open)
        db.session.commit()

        # Fetch all windows in the same room
        windows_in_room = Window.query.filter_by(room_id=window_open.window.room_id).all()

        # Create entries for all other windows with the same timestamp
        for other_window in windows_in_room:
            if other_window.id != window_id:

                other_window_open = WindowOpen(
                    window_id=other_window.id,
                    is_open=other_window.windowOpen[-1].is_open,
                    timestamp=timestamp
                )

                db.session.add(other_window_open)

        db.session.commit()

        response = {'message': f'Ventilator {window_id} is now {status}'}
        return jsonify(response)
    except IntegrityError as integrity_error:
        db.session.rollback()
        print(f"Integrity error occurred: {integrity_error}")
        return jsonify({'error': 'An integrity error occurred'}), 500
    except SQLAlchemyError as sqla_exception:
        print(f"SQLAlchemy error occurred: {sqla_exception}")
        return jsonify({'error': 'A database error occurred'}), 500


@app.route("/import", methods=['POST'])
def import_data():
    """
        function to import data in a xslm
    """
    uploaded_file = request.files['file']
    print(uploaded_file)
    print(uploaded_file.filename)
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)

        file = uploaded_file.filename
        if file:
            rooms = pd.read_excel(
                file,
                sheet_name='Room',
                header=0)

            ventilators = pd.read_excel(
                file,
                sheet_name='Ventilator',
                header=0)

            doors = pd.read_excel(
                file,
                sheet_name='Door',
                header=0)

            windows = pd.read_excel(
                file,
                sheet_name='Window',
                header=0)

            door_connects_room = pd.read_excel(
                file,
                sheet_name='Door_Connects_Room',
                header=0)

            people_in_room = pd.read_excel(
                file,
                sheet_name='PeopleInRoom',
                header=0)

            window_open = pd.read_excel(
                file,
                sheet_name='WindowOpen',
                header=0)

            door_open = pd.read_excel(
                file,
                sheet_name='DoorOpen',
                header=0)

            ventilator_on = pd.read_excel(
                file,
                sheet_name='VentilatorOn',
                header=0)

            rooms.to_sql('room', db.engine, if_exists='append', index=False)
            ventilators.to_sql('ventilator', db.engine, if_exists='append', index=False)
            doors.to_sql('door', db.engine, if_exists='append', index=False)
            windows.to_sql('window', db.engine, if_exists='append', index=False)
            door_connects_room.to_sql('door_connects_room',
            db.engine, if_exists='append', index=False)
            people_in_room.to_sql('people_in_room', db.engine, if_exists='append', index=False)
            window_open.to_sql('window_open', db.engine, if_exists='append', index=False)
            door_open.to_sql('door_open', db.engine, if_exists='append', index=False)
            ventilator_on.to_sql('ventilator_on', db.engine, if_exists='append', index=False)

    return redirect("/")

@app.route("/export", methods=['POST'])
def export_data():
    """
        function to export data in a csv
    """
    with open('exported_data.csv', 'w', newline='', encoding="UTF-8") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(["ROOMS"])
        csvwriter.writerow(["name", "size(m2)"])
        rooms = Room.query.order_by(Room.name).all()
        for element in rooms:
            csvwriter.writerow([element.name, element.size])

        csvwriter.writerow([])
        csvwriter.writerow(["DOORS"])
        csvwriter.writerow(["id"])
        doors = Door.query.order_by(Door.id).all()
        for element in doors:
            csvwriter.writerow([element.id])

        csvwriter.writerow([])
        csvwriter.writerow(["VENTILATORS"])
        csvwriter.writerow(["id","room_id"])
        ventilators = Ventilator.query.order_by(Ventilator.id).all()
        for element in ventilators:
            csvwriter.writerow([element.id, element.room_id])

        csvwriter.writerow([])
        csvwriter.writerow(["WINDOWS"])
        csvwriter.writerow(["id","room_id"])
        windows = Window.query.order_by(Window.id).all()
        for element in windows:
            csvwriter.writerow([element.id, element.room_id])

        csvwriter.writerow([])
        csvwriter.writerow(["LIGHTS"])
        csvwriter.writerow(["id","room_id"])
        lights = Light.query.order_by(Light.id).all()
        for element in lights:
            csvwriter.writerow([element.id, element.room_id])

        csvwriter.writerow([])
        csvwriter.writerow(["DOOR_CONNECTS_ROOM"])
        csvwriter.writerow(["door_id","room_id"])
        door_connects_room = DoorConnectsRoom.query.order_by(DoorConnectsRoom.door_id).all()
        for element in door_connects_room:
            csvwriter.writerow([element.door_id, element.room_id])

    return send_file('exported_data.csv',mimetype='text/csv',as_attachment=True)

@app.route('/update_async_content/<string:room_name>/<string:metric_name>')
def update_async_content(room_name:str, metric_name: str):
    """
        function to update async content
    """
    min_, max_ = 0, -1

    request_dict = {
        ".dynamic-temperature"+room_name: (10.0, 75.0),
        ".dynamic-people"+room_name: (0, 25),
        ".dynamic-co2"+room_name: (400, 1200)
    }

    interval = request_dict[metric_name]
    l_bound, u_bound = interval[min_], interval[max_]

    is_float_range   = isinstance(u_bound, float)

    if is_float_range:
        updated_data = round(random.uniform(l_bound, u_bound), 2)
    else:
        updated_data = 1
        while updated_data == 1:
            updated_data = random.randint(l_bound, u_bound)

    response_dict  = {
        "data": updated_data,
    }

    return jsonify(response_dict)

@app.route('/add_temperature', methods=['POST'])
def add_temperature():
    """
        route to add temperature
    """

    room_name = request.json.get('room_name')
    temperature_data = request.json.get('temperature_data')


    new_temperature = Temperature(room_id=room_name,
                                value=temperature_data,
                                timestamp=datetime.utcnow()\
                                    .strftime("%d-%m-%Y %H:%M:%S"))

    try:
        db.session.add(new_temperature)
        db.session.commit()
        return jsonify({'Success': 'Temperature added successfully'}), 200
    except SQLAlchemyError as sqla_exception:
        print(f"SQLAlchemy error occurred: {sqla_exception}")
        return jsonify({'error': 'A database error occurred'}), 500

@app.route('/add_co2', methods=['POST'])
def add_co2():
    """
        route to add co2
    """

    room_name = request.json.get('room_name')
    co2_data = request.json.get('co2_data')


    new_co2 = CO2(room_id=room_name, value=co2_data, timestamp=datetime.utcnow()\
        .strftime("%d-%m-%Y %H:%M:%S"))

    try:
        db.session.add(new_co2)
        db.session.commit()
        return jsonify({'Success': 'CO2 added successfully'}), 200
    except SQLAlchemyError as sqla_exception:
        print(f"SQLAlchemy error occurred: {sqla_exception}")
        return jsonify({'error': 'A database error occurred'}), 500


@app.route('/add_people', methods=['POST'])
def add_people():
    """
        route to add peple
    """

    room_name = request.json.get('room_name')
    people_data = request.json.get('people_data')

    new_people = PeopleInRoom(room_id=room_name,
                            no_people_in_room=people_data,
                            timestamp=datetime.utcnow()\
                                .strftime("%d-%m-%Y %H:%M:%S"))

    try:
        db.session.add(new_people)
        db.session.commit()
        return jsonify({'Success': 'People added successfully'}), 200
    except SQLAlchemyError as sqla_exception:
        print(f"SQLAlchemy error occurred: {sqla_exception}")
        return jsonify({'error': 'A database error occurred'}), 500

@app.route('/device_status', methods=['GET'])
def get_device_status():
    """
        function get the device status
    """
    room_name = request.args.get('room_name', None)  # Get room_name from query parameters

    device_name = request.args.get('device_name', None)  # Get the device name

    devs_dict = {
        "ventilator" : {
            "dev_obj"  : Ventilator,
            "relation" : VentilatorOn
        },
        "light" : {
            "dev_obj"  : Light,
            "relation" : LightOn
        },
        "door" : {
            "dev_obj"  : DoorConnectsRoom,
            "relation" : DoorOpen
        },
        "window" : {
            "dev_obj"  : Window,
            "relation" : WindowOpen
        },
    }

    device = devs_dict[device_name]

    devices = device["dev_obj"].query.filter_by(room_id=room_name).all()
    if device_name in ["window", "door"]:
        result = {
            'open_count': 0,
            'closed_count': 0
        }
    else:
        result = {
            'on_count': 0,
            'off_count': 0
        }

    dev_relation = device["relation"]

    for dev in devices:
        dev_id = dev.door_id if device_name == "door" else dev.id

        latest_dev_on = dev_relation.query.filter_by(**{f"{device_name}_id": dev_id}).\
            order_by(desc(dev_relation.timestamp)).first()

        if latest_dev_on is not None:

            if device_name in ["window", "door"]:
                if latest_dev_on.is_open:
                    result['open_count'] += 1
                else:
                    result['closed_count'] += 1
            else:
                if latest_dev_on.is_on:
                    result['on_count'] += 1
                else:
                    result['off_count'] += 1

    return jsonify({room_name: result})


@app.route('/update_temperature_chart', methods=['POST'])
def update_temperature_chart():
    """
        function to update the temperature chart
    """
    room_name = request.json.get('room_name')

    # Modify your query to get the last 20 entries for the specified room
    temperatures = Temperature.query.filter_by(room_id=room_name).\
        order_by(desc(Temperature.timestamp)).limit(20).all()

    # Reverse the order to get the oldest entry first
    temperatures.reverse()

    timestamps = [temp.timestamp for temp in temperatures]
    values = [temp.value for temp in temperatures]

    chart_data = {
        'labels': timestamps,
        'data': values
    }

    return jsonify(chart_data)

@app.route('/update_co2_chart', methods=['POST'])
def update_co2_chart():
    """
        function to update the co2 chart
    """
    room_name = request.json.get('room_name')

    # Modify your query to get the last 20 entries for the specified room
    co2 = CO2.query.filter_by(room_id=room_name).order_by(desc(CO2.timestamp)).limit(20).all()

    # Reverse the order to get the oldest entry first
    co2.reverse()

    timestamps = [temp.timestamp for temp in co2]
    values = [temp.value for temp in co2]

    chart_data = {
        'labels': timestamps,
        'data': values
    }

    return jsonify(chart_data)

@app.route('/update_people_chart', methods=['POST'])
def update_people_chart():
    """
        function to update the people chart
    """
    room_name = request.json.get('room_name')

    # Modify your query to get the last 20 entries for the specified room
    people = PeopleInRoom.query.filter_by(room_id=room_name).\
        order_by(desc(PeopleInRoom.timestamp)).limit(20).all()

    # Reverse the order to get the oldest entry first
    people.reverse()

    timestamps = [temp.timestamp for temp in people]
    values = [temp.no_people_in_room for temp in people]

    chart_data = {
        'labels': timestamps,
        'data': values
    }

    return jsonify(chart_data)


@app.route('/update_ventilators_chart', methods=['POST'])
def update_ventilators_chart():
    """
        function to update the ventilators chart
    """
    room_name = request.json.get('room_name')

    ventilators = Ventilator.query.filter_by(room_id=room_name).all()
    if ventilators:
        ventilator_data_list = []

        # Fetch the last 20 unique timestamps across all ventilators
        unique_timestamps = db.session.query(distinct(VentilatorOn.timestamp)).\
            order_by(desc(VentilatorOn.timestamp)).limit(20).all()
        unique_timestamps = [entry[0] for entry in reversed(unique_timestamps)]

        # Check if the length of unique_timestamps is less than 20
        if len(unique_timestamps) < 20:
            # Pad the left side with empty strings to reach length 20
            unique_timestamps = [''] * (20 - len(unique_timestamps)) + unique_timestamps

        for ventilator in ventilators:
            # Fetch last 20 entries for the current ventilator in descending order
            ventilator_data = VentilatorOn.query.filter_by(ventilator_id=ventilator.id).\
                order_by(desc(VentilatorOn.timestamp)).limit(20).all()

            if ventilator_data:
                # Reverse the order of is_on data for the current ventilator
                is_on_data = [entry.is_on for entry in reversed(ventilator_data)]

                # Check if the length of is_on_data is less than 20
                if len(is_on_data) < 20:
                    # Pad the left side with None values to reach length 20
                    is_on_data = [None] * (20 - len(is_on_data)) + is_on_data

                # Append the on/off data for the current ventilator
                ventilator_data_list.append(is_on_data)

        return jsonify({'labels': unique_timestamps, 'data': ventilator_data_list})

    return jsonify({'labels': [], 'data': []})

@app.route('/update_windows_chart', methods=['POST'])
def update_windows_chart():
    """
        function to update the windows chart
    """
    room_name = request.json.get('room_name')

    windows = Window.query.filter_by(room_id=room_name).all()
    if windows:
        window_data_list = []

        # Fetch the last 20 unique timestamps across all windows
        unique_timestamps = db.session.query(distinct(WindowOpen.timestamp)).\
            order_by(desc(WindowOpen.timestamp)).limit(20).all()

        unique_timestamps = [entry[0] for entry in reversed(unique_timestamps)]

        # Check if the length of unique_timestamps is less than 20
        if len(unique_timestamps) < 20:
            # Pad the left side with empty strings to reach length 20
            unique_timestamps = [''] * (20 - len(unique_timestamps)) + unique_timestamps

        for window in windows:
            # Fetch last 20 entries for the current window in descending order
            window_data = WindowOpen.query.filter_by(window_id=window.id).\
                order_by(desc(WindowOpen.timestamp)).limit(20).all()

            if window_data:
                # Reverse the order of is_open data for the current window
                is_open_data = [entry.is_open for entry in reversed(window_data)]

                # Check if the length of is_open_data is less than 20
                if len(is_open_data) < 20:
                    # Pad the left side with None values to reach length 20
                    is_open_data = [None] * (20 - len(is_open_data)) + is_open_data

                # Append the on/off data for the current window
                window_data_list.append(is_open_data)

        return jsonify({'labels': unique_timestamps, 'data': window_data_list})

    return jsonify({'labels': [], 'data': []})


@app.route('/update_lights_chart', methods=['POST'])
def update_lights_chart():
    """
        function to update the lights chart
    """
    room_name = request.json.get('room_name')

    lights = Light.query.filter_by(room_id=room_name).all()
    if lights:
        light_data_list = []

        # Fetch the last 20 unique timestamps across all lights
        unique_timestamps = db.session.query(distinct(LightOn.timestamp)).\
            order_by(desc(LightOn.timestamp)).limit(20).all()
        unique_timestamps = [entry[0] for entry in reversed(unique_timestamps)]

        # Check if the length of unique_timestamps is less than 20
        if len(unique_timestamps) < 20:
            # Pad the left side with empty strings to reach length 20
            unique_timestamps = [''] * (20 - len(unique_timestamps)) + unique_timestamps

        for light in lights:
            # Fetch last 20 entries for the current light in descending order
            light_data = LightOn.query.filter_by(light_id=light.id).\
                order_by(desc(LightOn.timestamp)).limit(20).all()
            if light_data:
                # Reverse the order of is_on data for the current ventilator
                is_on_data = [entry.is_on for entry in reversed(light_data)]

                # Check if the length of is_on_data is less than 20
                if len(is_on_data) < 20:
                    # Pad the left side with None values to reach length 20
                    is_on_data = [None] * (20 - len(is_on_data)) + is_on_data

                # Append the on/off data for the current ventilator
                light_data_list.append(is_on_data)

        return jsonify({'labels': unique_timestamps, 'data': light_data_list})

    return jsonify({'labels': [], 'data': []})

@app.route('/update_doors_chart', methods=['POST'])
def update_doors_chart():
    """
        function to update the doors chart
    """
    room_name = request.json.get('room_name')

    doors = DoorConnectsRoom.query.filter_by(room_id=room_name).all()
    if doors:
        door_data_list = []

        # Fetch the last 20 unique timestamps across all doors
        unique_timestamps = db.session.query(distinct(DoorOpen.timestamp)).\
            order_by(desc(DoorOpen.timestamp)).limit(20).all()

        unique_timestamps = [entry[0] for entry in reversed(unique_timestamps)]

        # Check if the length of unique_timestamps is less than 20
        if len(unique_timestamps) < 20:
            # Pad the left side with empty strings to reach length 20
            unique_timestamps = [''] * (20 - len(unique_timestamps)) + unique_timestamps

        for door in doors:
            # Fetch last 20 entries for the current door in descending order
            door_data = DoorOpen.query.filter_by(door_id=door.door_id).\
                order_by(desc(DoorOpen.timestamp)).limit(20).all()

            if door_data:
                # Reverse the order of is_open data for the current door
                is_open_data = [entry.is_open for entry in reversed(door_data)]

                # Check if the length of is_open_data is less than 20
                if len(is_open_data) < 20:
                    # Pad the left side with None values to reach length 20
                    is_open_data = [None] * (20 - len(is_open_data)) + is_open_data

                # Append the on/off data for the current door
                door_data_list.append(is_open_data)

        return jsonify({'labels': unique_timestamps, 'data': door_data_list})

    return jsonify({'labels': [], 'data': []})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True, port=4000)
    # app.run(debug=False, port=4000)

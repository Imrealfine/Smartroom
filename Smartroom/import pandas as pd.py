import pandas as pd
import sqlite3

def import_data(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)
    
    # 连接到数据库
    conn = sqlite3.connect('rooms.db')
    
    # 将数据导入数据库
    df.to_sql('rooms', conn, if_exists='replace', index=False)
    
    conn.close()

def create_room(id, size, doors, windows, lights, air_conditioners):
    conn = sqlite3.connect('rooms.db')
    cursor = conn.cursor()
    
    cursor.execute('''INSERT INTO rooms (id, size, doors, windows, lights, air_conditioners) 
                      VALUES (?, ?, ?, ?, ?, ?)''', (id, size, doors, windows, lights, air_conditioners))
    
    conn.commit()
    conn.close()

def update_room(id, size, doors, windows, lights, air_conditioners):
    conn = sqlite3.connect('rooms.db')
    cursor = conn.cursor()
    
    cursor.execute('''UPDATE rooms SET size=?, doors=?, windows=?, lights=?, air_conditioners=? 
                      WHERE id=?''', (size, doors, windows, lights, air_conditioners, id))
    
    conn.commit()
    conn.close()

def delete_room(id):
    conn = sqlite3.connect('rooms.db')
    cursor = conn.cursor()
    
    cursor.execute('''DELETE FROM rooms WHERE id=?''', (id,))
    
    conn.commit()
    conn.close()

def list_rooms():
    conn = sqlite3.connect('rooms.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM rooms')
    rooms = cursor.fetchall()
    
    conn.close()
    
    return rooms

import matplotlib.pyplot as plt

def plot_temperature_and_co2(temperature_data, co2_data, timestamps):
    plt.figure(figsize=(10, 5))
    
    plt.plot(timestamps, temperature_data, label='Temperature')
    plt.plot(timestamps, co2_data, label='CO2 Levels')
    
    plt.xlabel('Time')
    plt.ylabel('Values')
    plt.title('Temperature and CO2 Levels Over Time')
    plt.legend()
    
    plt.show()

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/lock_door', methods=['POST'])
def lock_door():
    room_id = request.json.get('room_id')
    action = request.json.get('action')  # 'lock' or 'unlock'
    
    # 假设你有逻辑控制门锁
    if action == 'lock':
        # 这里是锁门逻辑
        return jsonify({'message': f'Room {room_id} is locked.'})
    else:
        # 这里是开门逻辑
        return jsonify({'message': f'Room {room_id} is unlocked.'})

@app.route('/toggle_light', methods=['POST'])
def toggle_light():
    room_id = request.json.get('room_id')
    action = request.json.get('action')  # 'on' or 'off'
    
    # 控制灯光的逻辑
    return jsonify({'message': f'Room {room_id} lights turned {action}.'})

if __name__ == '__main__':
    app.run(debug=True)

def check_temperature(temperature, room_id):
    if temperature > 70:
        # 触发报警系统逻辑
        print(f"Alarm: Room {room_id} temperature exceeds 70°C!")
        # 自动解锁所有门
        unlock_all_doors()

def unlock_all_doors():
    # 假设你有解锁门的逻辑
    print("All doors have been unlocked.")


def energy_saving(room_id, presence):
    if presence:
        print(f"Room {room_id}: Turning on lights.")
        # 控制灯光逻辑
    else:
        print(f"Room {room_id}: No presence detected. Turning off all devices.")
        # 关闭所有设备逻辑

def check_air_quality(co2_level, room_id):
    if co2_level > 1000:
        print(f"Room {room_id}: CO2 levels too high. Ventilating...")
        # 打开窗户和风扇
    elif 800 <= co2_level <= 1000:
        print(f"Room {room_id}: CO2 levels moderate. Room marked yellow.")
    else:
        print(f"Room {room_id}: CO2 levels normal. Room marked green.")
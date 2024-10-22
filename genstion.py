import pandas as pd
import sqlite3


def import_all_sheets(file_path):
    # 读取Excel文件中的所有工作表
    xls = pd.ExcelFile(file_path)
    
    # 连接到SQLite数据库
    conn = sqlite3.connect('smartroom.db')
    
    # 遍历所有工作表，将每个表的数据导入到数据库
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name, header=0)
        
        # 去除列名中的多余空格
        df.columns = df.columns.str.strip()
        
        # 将每张表的数据导入数据库，表名使用工作表名
        df.to_sql(sheet_name, conn, if_exists='replace', index=False)
        print(f"Sheet '{sheet_name}' has been imported.")
    
    conn.close()

# 调用导入函数
import_all_sheets('smartroom_exampledata.xlsx')

def create_or_update_room(room_name, size_m2):
    conn = sqlite3.connect('smartroom.db')
    cursor = conn.cursor()

    # 插入或更新房间基本信息
    cursor.execute('''
        INSERT OR REPLACE INTO Room (name, size_m2)
        VALUES (?, ?)''', (room_name, size_m2))
    
    cursor.execute('''
        INSERT OR REPLACE INTO Ventilator (ID, Room_Id)
        VALUES (?, ?)''', (None, room_name))
    
    cursor.execute('''
        INSERT OR REPLACE INTO Door (ID)
        VALUES (?)''', (99,))
    
    cursor.execute('''
        INSERT OR REPLACE INTO Window (ID, Room_Id)
        VALUES (?, ?)''', (None, room_name))

    cursor.execute('''
        INSERT OR REPLACE INTO Door_Connects_Room (Door_Id, Room_Id)
        VALUES (?, ?)''', (None, room_name))

    conn.commit()
    conn.close()

# 示例调用
#create_or_update_room('Room888', 888)

def delete_room(room_name):
    conn = sqlite3.connect('smartroom.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM Room WHERE Name=?', (room_name,))
    
    conn.commit()
    conn.close()

# 示例调用
#delete_room('room888')

def list_rooms():
    conn = sqlite3.connect('smartroom.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Room')
    rooms = cursor.fetchall()

    conn.close()
    
    return rooms


def query_full_room_info(room_name):
    conn = sqlite3.connect('smartroom.db')
    cursor = conn.cursor()

    # 连接多个表，查询房间的完整信息
    cursor.execute('''
        SELECT Room.name, Room.size_m2, Door.ID AS door_id, Window.ID AS window_id, 
               Ventilator.ID AS ventilator_id
        FROM Room
        LEFT JOIN Door_Connects_Room ON Room.name = Door_Connects_Room.Room_ID
        LEFT JOIN Door ON Door_Connects_Room.Door_ID = Door.ID
        LEFT JOIN Window ON Room.name = Window.Room_Id
        LEFT JOIN Ventilator ON Room.name = Ventilator.Room_Id
        WHERE Room.name = ?
    ''', (room_name,))

    results = cursor.fetchall()
    
    for row in results:
        print(f"Room: {row[0]}, Size: {row[1]} m², Door ID: {row[2]}, "
              f"Window ID: {row[3]}, Ventilator ID: {row[4]}")

    conn.close()
# 示例调用查询完整的房间信息
query_full_room_info('Room101')


# 示例调用
#Rooms = list_rooms()
#for room in Rooms: print(room)

def show_room_info(name):
    conn = sqlite3.connect('smartroom.db')
    cursor = conn.cursor()

    # 调整查询列名为 `name`
    cursor.execute('SELECT * FROM Room WHERE "name"=?', (name,))
    room = cursor.fetchone()

    if room:
        print(f"Room {room[0]}: Size={room[1]} m²")
    else:
        print("Room not found.")

    conn.close()

# 示例调用
#show_room_info('Room888')



import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime
# 获取灯光、空调、窗户和门的状态数据
def get_device_data():
    conn = sqlite3.connect('smartroom.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT Timestamp, isOpen FROM DoorOpen
        UNION ALL
        SELECT Timestamp, isOpen FROM WindowOpen
        UNION ALL
        SELECT Timestamp, isOn FROM VentilatorOn
    ''')
    
    data = cursor.fetchall()
    conn.close()
    
    return data

# 绘制实时折线图
timestamps = []
states = []

# 更新图表的函数，用于实时更新数据
def update_chart(frame):
    data = get_device_data()

    timestamps.clear()
    states.clear()
    
    for entry in data:
        timestamp_str = entry[0].strip()
        
        timestamps.append(datetime.datetime.strptime(entry[0], '%Y-%m-%dT%H:%M:%S%z'))
        states.append(entry[1])

    plt.cla()  # 清除当前图表
    plt.plot(timestamps, states, label='Device State')
    plt.xlabel('Timestamp')
    plt.ylabel('State (On/Off)')
    plt.legend(loc='upper left')
    plt.tight_layout()

# 设置动画，使用 FuncAnimation 实现实时更新
fig = plt.figure()
ani = FuncAnimation(fig, update_chart, interval=1000)  # 每秒更新一次
plt.show()
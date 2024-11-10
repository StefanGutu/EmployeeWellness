import sqlite3


#Function to insert user data when its authenticate for the first time
def add_user(username,password):
    conn = sqlite3.connect('UserData.db')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO UserData (name, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

#Function will give you the id to the user by name 
def get_user_id_by_name(username):
    conn = sqlite3.connect('UserData.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM UserData WHERE name = ?", (username,))
    user_id = cursor.fetchone()
    conn.close()
    
    if user_id is not None:
        return user_id[0]
    else:
        return None

def get_user_password(username):
    conn = sqlite3.connect('UserData.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM UserData where name = ?", (username,))
    user_pass = cursor.fetchone()
    return user_pass[0]

def check_user_exists(username):
    conn = sqlite3.connect('UserData.db')
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT COUNT(*) FROM UserData WHERE name = ?", (username,))
    user_exists = cursor.fetchone()[0]  
    
    conn.close()
    
    if user_exists > 0:
        return True  
    else:
        return False  

#Function will initialize the Stats for the new user
def add_initial_status(id_user):
    conn = sqlite3.connect('UserData.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO UserStats (id_user, head_signal, close_signal, shoulder_signal) VALUES (?, 0, 0, 0)", (id_user,))
    conn.commit()
    conn.close()


#Function will increment the column you give as a param if the column is not present nothing will happen
def increment_signal(id_user, column_name):
    conn = sqlite3.connect('UserData.db')
    cursor = conn.cursor()
  
    if column_name in ["head_signal", "close_signal", "shoulder_signal"]:
        cursor.execute(f'''UPDATE UserStats
                          SET {column_name} = {column_name} + 1
                          WHERE id_user = ?''', (id_user,))
        conn.commit()
        conn.close()
    else:
        conn.close()

#Function will get you all status signals
def get_status(id_user):
    conn = sqlite3.connect('UserData.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM UserStats WHERE id_user = ?", (id_user,))
    results = cursor.fetchall() 
    conn.close()
    return results



#This will create the tables if they dont exists already
def create_base():
    conn = sqlite3.connect('UserData.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS UserData (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(30),
                        password VARCHAR(50)
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS UserStats (
                        id_user INTEGER,
                        head_signal INTEGER,
                        close_signal INTEGER,
                        shoulder_signal INTEGER,
                        FOREIGN KEY (id_user) REFERENCES UserData (id)
                    )''')

    conn.commit()
    conn.close()

#In case something go wrong delete it all 
def drop_tables():
    conn = sqlite3.connect('UserData.db')
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS UserData")
    cursor.execute("DROP TABLE IF EXISTS UserStats")
    
    conn.commit()
    conn.close()


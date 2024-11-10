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
    cursor.execute("SELECT password FROM UserData WHERE name = ?", (username,))
    user_pass = cursor.fetchone()  # Aici va returna fie un tuplu, fie None
    conn.close()

    # Verificăm dacă rezultatul este None
    if user_pass is not None:
        return user_pass[0]  # Accesăm parola
    else:
        return None  # Returnăm None dacă utilizatorul nu există


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
    
def add_number_to_database(user_id, number):
    # Conectăm la baza de date
    conn = sqlite3.connect('UserData.db')
    cursor = conn.cursor()

    # Inserăm numărul pentru un user_id specific
    cursor.execute('''
    INSERT INTO user_data (user_id, number)
    VALUES (?, ?)
    ''', (user_id, number))

    # Confirmăm și salvăm modificările
    conn.commit()
    # Închidem conexiunea
    conn.close()

def get_latest_numbers(user_id):
    # Conectăm la baza de date
    conn = sqlite3.connect('UserData.db')
    cursor = conn.cursor()

    # Selectăm cele mai recente numere adăugate de user_id-ul specificat
    cursor.execute(''' 
    SELECT number, created_at FROM user_data 
    WHERE user_id = ? 
    ORDER BY created_at DESC
    ''', (user_id,))

    # Obținem toate rezultatele
    rows = cursor.fetchall()

    # Închidem conexiunea
    conn.close()

    # Returnează primele 10 înregistrări (sau mai puține, dacă sunt mai puține înregistrări)
    return rows[:10]


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

    # Creăm tabelul UserData
    cursor.execute('''CREATE TABLE IF NOT EXISTS UserData (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name VARCHAR(30),
                        password VARCHAR(50)
                    )''')

    # Creăm tabelul UserStats
    cursor.execute('''CREATE TABLE IF NOT EXISTS UserStats (
                        id_user INTEGER,
                        head_signal INTEGER,
                        close_signal INTEGER,
                        shoulder_signal INTEGER,
                        FOREIGN KEY (id_user) REFERENCES UserData (id)
                    )''')

    # Creăm tabelul user_data fără constrângerea UNIQUE pe user_id
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        number INTEGER NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES UserData(id)
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


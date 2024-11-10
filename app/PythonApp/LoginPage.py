import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import next_page
import dataBaseCode

UserData = {
    "admin": "1111"
}

dataBaseCode.create_base()
# dataBaseCode.drop_tables()  #to reset the database comment create_base and uncomment this
# Function to validate login
def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    checkPassword = dataBaseCode.get_user_password(username)

    if checkPassword == password:
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Invalid username or password")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        return False
    
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    next_page.open_next_page(username, root)

def add_user():
    username = username_entry.get()
    password = password_entry.get()
    
    if username.strip() != "" and password.strip() != "":
        if dataBaseCode.check_user_exists(username) is False:
            dataBaseCode.add_user(username,password)
            temp_id = dataBaseCode.get_user_id_by_name(username)
            dataBaseCode.add_initial_status(temp_id)
            # UserData[username] = password
            # messagebox.showinfo("Auth successful!","Welcome!")
        else:
            messagebox.showerror("Error","User exist!")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            return False
            
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    next_page.open_next_page(username, root)

# Create main window
root = tk.Tk()
root.title("Wellness App")
root.geometry("600x450")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Position the window in the bottom right corner
x_pos = screen_width - 600
y_pos = screen_height - 450
root.geometry(f"600x450+{x_pos}+{y_pos}")
root.configure(bg="#ADE1E7")

# Add a title label
welcome_text = "Welcome!\nAre you ready to conquer the day? 😊"
title_label = ttk.Label(root, text=welcome_text, anchor="center", font=("Helvetica", 20, "bold"), background="#ADE1E7", justify="center")
title_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

# Create and place username label and entry
username_label = ttk.Label(root, text="Username:", anchor="center", font=("Helvetica", 14, "bold"), background="#ADE1E7")
username_label.grid(row=1, column=0, sticky="e", pady=10, padx=20)

username_entry = tk.Entry(root, width=25, font=("Helvetica", 14), bg="#E1E3F0")
username_entry.grid(row=1, column=1, pady=10, padx=20)

# Create and place password label and entry
password_label = ttk.Label(root, text="Password:", anchor="center", font=("Helvetica", 14, "bold"), background="#ADE1E7")
password_label.grid(row=2, column=0, sticky="e", pady=10, padx=20)

password_entry = tk.Entry(root, show="*", width=25, font=("Helvetica", 14), bg="#E1E3F0")
password_entry.grid(row=2, column=1, pady=10, padx=20)

# Bind Enter key to login function
password_entry.bind("<Return>", lambda event: validate_login())

# Create and place login button
login_button = ttk.Button(root, text="Login", command=validate_login, style="TButton")
login_button.grid(row=3, column=0, columnspan=2, pady=20)

# Create and place "Create new account" button
auth_button = ttk.Button(root, text="Create new account", command=add_user, style="TButton")
auth_button.grid(row=4, column=0, columnspan=2, pady=20)

# Start the main event loop
root.mainloop()

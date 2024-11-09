import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


UserData = {
        "admin":"1111"}


# Function to validate login
def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    if username in UserData:
        if UserData[username] == password:
            messagebox.showinfo("Login Successful", "Welcome!")
        else:
            messagebox.showerror("Login Failed", "Password wrong!")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            return False
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        return False
        
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    

def add_user():
    username = username_entry.get()
    password = password_entry.get()
    
    if(username.strip() != "" and password.strip() != ""):
        if username not in UserData:
            UserData[username] = password
            messagebox.showinfo("Auth successful!","Welcome!")
        else:
            messagebox.showerror("User exist","Try again")
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            return False
            
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    
    

            
# Create main window
root = tk.Tk()
root.title("Wellness App")
root.geometry("1920x1080")
root.configure(bg="#B8BCD3")  # Light background color

# Create a frame for the login form
# login_frame = ttk.Frame(root, padding=20)
# login_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

# Add a title label
welcome_text = "Welcome!\nAre you ready to conquer the day? 😊"
title_label = ttk.Label(root, text=welcome_text,anchor="center",font=("Helvetica",35,"bold"),background="#B8BCD3",justify="center")
title_label.grid(row=0, column=0, columnspan=1, pady=10)
title_label.place(relx=0.5, rely=0.3, width=1200, height=150, anchor="center")

# Create and place username label and entry
username_label = ttk.Label(root, text="Username:",anchor="center",font=("Helvetica",16,"bold"),background="#B8BCD3")
username_label.grid(row=1, column=0, sticky="w", pady=5)
username_label.place(relx=0.435,rely=0.4,width=170,height=35,anchor="center")

username_entry = tk.Entry(root, width=25,font=("Helvetica",16),bg="#E1E3F0")
username_entry.grid(row=1, column=1, pady=5)
username_entry.place(relx=0.535,rely=0.4,width=320,height=35,anchor="center")

# Create and place password label and entry
password_label = ttk.Label(root, text="Password:",anchor="center",font=("Helvetica",16,"bold"),background="#B8BCD3")
password_label.grid(row=2, column=0, sticky="w", pady=5)
password_label.place(relx=0.435,rely=0.45,width=170,height=35,anchor="center")

password_entry = tk.Entry(root, show="*", width=25,font=("Helvetica",16),bg="#E1E3F0")
password_entry.grid(row=2, column=1, pady=5)
password_entry.place(relx=0.535,rely=0.45,width=320,height=35,anchor="center")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 16, "bold"),foreground="#7885C5",borderwidth=2)

# Create and place login button
login_button = ttk.Button(root, text="Login", command=validate_login,style="TButton")
login_button.grid(row=3, column=0, columnspan=2, pady=20)
login_button.place(relx=0.445,rely=0.5,width=250,height=60,anchor="center")

auth_button = ttk.Button(root, text="Create new account", command=add_user,style="TButton")
auth_button.grid(row=4, column=0, columnspan=2, pady=20)
auth_button.place(relx=0.548,rely=0.5,width=260,height=60,anchor="center")

# Start the main event loop
root.mainloop()

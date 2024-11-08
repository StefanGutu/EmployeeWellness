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
root.title("Login App")
root.geometry("400x250")
root.configure(bg="#f0f0f0")  # Light background color

# Create a frame for the login form
login_frame = ttk.Frame(root, padding=20)
login_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

# Add a title label
title_label = ttk.Label(login_frame, text="Login", font=("Helvetica", 18, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Create and place username label and entry
username_label = ttk.Label(login_frame, text="Username:")
username_label.grid(row=1, column=0, sticky="w", pady=5)
username_entry = ttk.Entry(login_frame, width=25)
username_entry.grid(row=1, column=1, pady=5)

# Create and place password label and entry
password_label = ttk.Label(login_frame, text="Password:")
password_label.grid(row=2, column=0, sticky="w", pady=5)
password_entry = ttk.Entry(login_frame, show="*", width=25)
password_entry.grid(row=2, column=1, pady=5)

# Create and place login button
login_button = ttk.Button(login_frame, text="Login", command=validate_login)
login_button.grid(row=3, column=0, columnspan=2, pady=20)

auth_button = ttk.Button(login_frame, text="Auth", command=add_user)
auth_button.grid(row=4, column=0, columnspan=2, pady=20)

# Start the main event loop
root.mainloop()

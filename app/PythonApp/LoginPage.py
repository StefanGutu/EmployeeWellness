import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import next_page

UserData = {
    "admin": "1111"
}

# Function to validate login
def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    if username in UserData:
        if UserData[username] != password:
            username_entry.delete(0, tk.END)
            password_entry.delete(0, tk.END)
            return False
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
        if username not in UserData:
            UserData[username] = password
        else:
            messagebox.showerror("Error", "User exists!")
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
title_label.place(relx=0.5, rely=0.1, anchor="center")

# Create and place username label and entry (on the same line)
username_label = ttk.Label(root, text="Username:", anchor="center", font=("Helvetica", 14, "bold"), background="#ADE1E7")
username_label.place(relx=0.3, rely=0.35, anchor="center")

username_entry = tk.Entry(root, width=25, font=("Helvetica", 14), bg="#E1E3F0")
username_entry.place(relx=0.65, rely=0.35, anchor="center")

# Create and place password label and entry (on the same line)
password_label = ttk.Label(root, text="Password:", anchor="center", font=("Helvetica", 14, "bold"), background="#ADE1E7")
password_label.place(relx=0.3, rely=0.45, anchor="center")

password_entry = tk.Entry(root, show="*", width=25, font=("Helvetica", 14), bg="#E1E3F0")
password_entry.place(relx=0.65, rely=0.45, anchor="center")

# Bind Enter key to login function
password_entry.bind("<Return>", lambda event: validate_login())

# Create a style for buttons with matching text and background colors
style = ttk.Style()
style.configure("TButton",
                font=("Helvetica", 14, "bold"),
                foreground="black",  # Darker text color (darker shade of #ADE1E7)
                background="#60B9D4",  # Button background color
                borderwidth=2,         # Small border
                relief="solid",        # Solid border style
                anchor="center",       # Align text in the center
                padding=10)            # Padding inside button to help with alignment

# Create and place login button
login_button = ttk.Button(root, text="Login", command=validate_login, style="TButton")
login_button.place(relx=0.3, rely=0.6, width=220, height=40, anchor="center")

# Create and place "Create new account" button next to the login button
auth_button = ttk.Button(root, text="Create new account", command=add_user, style="TButton")
auth_button.place(relx=0.7, rely=0.6, width=220, height=40, anchor="center")

# Start the main event loop
root.mainloop()

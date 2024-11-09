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
    next_page.open_next_page(username,root) #Aici
    # root.quit()

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
    next_page.open_next_page(username,root) #Aici
    # root.quit()


# Create main window
root = tk.Tk()
root.title("Wellness App")

# Set the size of the window to 600x450
root.geometry("600x450")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Position the window in the bottom right corner
x_pos = screen_width - 600  # width of the window (600px)
y_pos = screen_height - 450  # height of the window (450px)

# Apply the position to the window
root.geometry(f"600x450+{x_pos}+{y_pos}")

root.configure(bg="#B8BCD3")  # Light background color

# Add a title label
welcome_text = "Welcome!\nAre you ready to conquer the day? 😊"
title_label = ttk.Label(root, text=welcome_text, anchor="center", font=("Helvetica", 25, "bold"), background="#B8BCD3", justify="center")
title_label.grid(row=0, column=0, columnspan=2, pady=20, padx=20)

# Create and place username label and entry
username_label = ttk.Label(root, text="Username:", anchor="center", font=("Helvetica", 14, "bold"), background="#B8BCD3")
username_label.grid(row=1, column=0, sticky="e", pady=10, padx=20)

username_entry = tk.Entry(root, width=25, font=("Helvetica", 14), bg="#E1E3F0")
username_entry.grid(row=1, column=1, pady=10, padx=20)

# Create and place password label and entry
password_label = ttk.Label(root, text="Password:", anchor="center", font=("Helvetica", 14, "bold"), background="#B8BCD3")
password_label.grid(row=2, column=0, sticky="e", pady=10, padx=20)

password_entry = tk.Entry(root, show="*", width=25, font=("Helvetica", 14), bg="#E1E3F0")
password_entry.grid(row=2, column=1, pady=10, padx=20)

# Create and place login button
login_button = ttk.Button(root, text="Login", command=validate_login, style="TButton")
login_button.grid(row=3, column=0, columnspan=2, pady=20)

# Create and place "Create new account" button
auth_button = ttk.Button(root, text="Create new account", command=add_user, style="TButton")
auth_button.grid(row=4, column=0, columnspan=2, pady=20)

# Start the main event loop
root.mainloop()

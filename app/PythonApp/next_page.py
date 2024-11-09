import tkinter as tk
from tkinter import ttk
import generateData  # Make sure this module has the `generate_random_numbers` function
import notification

# Function that opens the next page after login
def open_next_page(username, root):
    root.destroy()
    
    # Create a new window for the welcome page
    next_page_window = tk.Tk()  # New welcome window
    next_page_window.title("Welcome Page")

    # Set window size and position
    window_width = 600
    window_height = 450
    screen_width = next_page_window.winfo_screenwidth()
    screen_height = next_page_window.winfo_screenheight()
    x_pos = screen_width - window_width
    y_pos = screen_height - window_height
    next_page_window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

    next_page_window.configure(bg="#ADE1E7")  # Light background for the next page

    # Welcome message with the username
    welcome_message = f"Welcome {username}!\nYou are successfully logged in!"
    welcome_label = ttk.Label(next_page_window, text=welcome_message, font=("Helvetica", 20, "bold"), background="#ADE1E7")
    welcome_label.place(relx=0.5, rely=0.3, anchor="center")

    # Label to display generated value
    my_val = tk.StringVar()
    value_label = ttk.Label(next_page_window, textvariable=my_val, font=("Helvetica", 16), background="#ADE1E7")
    
    # Position the value label below the welcome label
    value_label.place(relx=0.5, rely=0.5, anchor="center")

    # Function to change the element with a generated value
    def change_elem():
        
        my_val.set(str(generateData.generate_random_numbers()))
        notification.send_notification("Test Title", "This is a test message")
        # print(my_val)
        next_page_window.after(10000, change_elem)  # Schedule the next update

    # Start updating the value label after 10 seconds
    next_page_window.after(10000, change_elem)

    # Run the Tkinter main event loop
    next_page_window.mainloop()

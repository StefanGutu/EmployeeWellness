import tkinter as tk
from tkinter import ttk, messagebox
import threading
import ctypes  # For controlling system functions
import generateData
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

    # List to store the last three warning values
    warning_sequence = []
    screen_locked = False

    # Function to lock the entire screen
    def lock_screen():
        lock_window = tk.Toplevel()
        lock_window.attributes("-fullscreen", True)
        lock_window.configure(bg="black")
        lock_window.attributes("-topmost", True)
        
        # Label to instruct the user on how to unlock
        lock_label = ttk.Label(lock_window, text="Screen Locked! Waiting for the correct posture...", font=("Helvetica", 24), background="black", foreground="white")
        lock_label.place(relx=0.5, rely=0.5, anchor="center")

        # Disable keyboard and mouse input
        ctypes.windll.user32.BlockInput(True)

        return lock_window

    # Function to unlock the screen
    def unlock_screen(lock_window):
        lock_window.destroy()
        ctypes.windll.user32.BlockInput(False)

    # Function to change the element with a generated value
    def change_elem():
        my_val.set(str(generateData.generate_random_numbers()))
        threading.Thread(target=show_notification_in_thread).start()
        next_page_window.after(10000, change_elem)  # Schedule the next update

    # Start updating the value label after 10 seconds
    next_page_window.after(10000, change_elem)

    # Function to show notifications in a separate thread
    def show_notification_in_thread():
        nonlocal screen_locked, warning_sequence
        try:
            value = int(my_val.get())

            # Handle warnings for values 1, 2, or 3
            if value in {1, 2, 3}:
                # Send notification based on value
                match value:
                    case 1:
                        notification.send_notification("Bad head!", "Correct your head posture!")
                    case 2:
                        notification.send_notification("Close to monitor!", "Correct your posture!")
                    case 3:
                        notification.send_notification("Bad shoulders!", "Correct your shoulders posture!")

                # Add value to warning sequence
                warning_sequence.append(value)

                # If we have three warnings in sequence, lock the screen
                if len(warning_sequence) == 3:
                    screen_locked = True
                    lock_window = lock_screen()  # Lock the screen

            # If the value is 0, reset the warning sequence
            elif value == 0:
                warning_sequence.clear()

            # If screen is locked and receives 0, unlock
            if screen_locked and value == 0:
                screen_locked = False
                unlock_screen(lock_window)
                warning_sequence.clear()
                messagebox.showinfo("Screen Unlocked", "Screen has been unlocked.")

        except ValueError:
            pass  # Handle cases where my_val is not an integer

    # Run the Tkinter main loop
    next_page_window.mainloop()

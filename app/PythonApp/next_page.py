import tkinter as tk
from tkinter import ttk

def update_font_size(event, label, next_window):
    # Calculate the font size based on the window size
    width = next_window.winfo_width()
    height = next_window.winfo_height()
    
    # Adjust font size based on window size (this is just an example, tweak as needed)
    font_size = int(min(width, height) / 10)  # Set font size proportional to window size
    
    # Update label font size
    label.config(font=("Helvetica", font_size, "bold"))

def draw_dynamic_line(event, canvas, next_window, label):
    # Get the updated width of the window
    width = next_window.winfo_width()
    
    # Get the height of the label (this is used to position the line below the label)
    label_height = label.winfo_height()
    
    # Redraw the line to span the full width and position it below the label
    canvas.delete("line")  # Remove any previous lines
    canvas.create_line(0, label.winfo_y() + label_height + 5, width, label.winfo_y() + label_height + 5, width=2, fill="black", tags="line")  # Line below label

def open_next_page(root, username_entry):
    # Hide the login window
    root.withdraw()

    # Create a new window for the next page
    next_window = tk.Toplevel(root)
    next_window.title("Next Page")
    next_window.geometry("400x250")  # Initial size
    next_window.configure(bg="#f0f0f0")  # Light background color

    # Create a Canvas widget to allow drawing of the line
    canvas = tk.Canvas(next_window, bg="#f0f0f0", height=250)
    canvas.pack(fill="both", expand=True)

    # Customize the user greeting label with a cool design
    greeting_text = f"Welcome {username_entry.get()}!"
    next_label = ttk.Label(next_window, text=greeting_text, font=("Helvetica", 40, "bold"), anchor="center", background="#f0f0f0")
    
    # Position the label at the top of the window, horizontally centered
    next_label.place(relx=0.5, rely=0.05, anchor="center")  # Positioning at the top (5% from top)

    # Bind the window resizing event to update the font size
    next_window.bind("<Configure>", lambda event, label=next_label: update_font_size(event, label, next_window))

    # Bind the window resizing event to redraw the line
    next_window.bind("<Configure>", lambda event, canvas=canvas, next_window=next_window, label=next_label: draw_dynamic_line(event, canvas, next_window, label))

    # Button to close the next page and quit the application
    close_button = ttk.Button(next_window, text="Close", command=root.quit, style="TButton")
    close_button.place(relx=0.5, rely=0.75, anchor="center")

    # Add styling to the close button for a modern look
    style = ttk.Style()
    style.configure("TButton", font=("Helvetica", 12, "bold"), width=10, padding=0)
    style.configure("TButton:hover", background="#4CAF50", foreground="white")

    # Ensure that when the new window is closed, the application will exit
    next_window.protocol("WM_DELETE_WINDOW", lambda: [next_window.destroy(), root.quit()])

root = tk.Tk()
root.geometry("300x200")

# Create a username entry for login
username_entry = ttk.Entry(root)
username_entry.pack(pady=20)

# Button to open the next page
login_button = ttk.Button(root, text="Login", command=lambda: open_next_page(root, username_entry))
login_button.pack()

root.mainloop()
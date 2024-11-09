import tkinter as tk
from tkinter import ttk

# Functia care deschide noua fereastra dupa login
def open_next_page(username, root):
    root.destroy()
    
    # Creăm o fereastră nouă pentru pagina de bun venit
    next_page_window = tk.Tk()  # Noua fereastră de bun venit
    next_page_window.title("Welcome Page")

    # Setăm dimensiunea ferestrei
    window_width = 600
    window_height = 450
    screen_width = next_page_window.winfo_screenwidth()
    screen_height = next_page_window.winfo_screenheight()
    x_pos = screen_width - window_width
    y_pos = screen_height - window_height
    next_page_window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

    next_page_window.configure(bg="#ADE1E7")  # Fundal deschis pentru pagina următoare

    # Mesaj de bun venit cu numele utilizatorului
    welcome_message = f"Welcome {username}!\nYou are successfully logged in!"
    welcome_label = ttk.Label(next_page_window, text=welcome_message, font=("Helvetica", 20, "bold"), background="#ADE1E7")
    welcome_label.place(relx=0.5, rely=0.3, anchor="center")

    # Buton pentru a închide fereastra

    # Lăsăm aplicația să ruleze doar pentru noua fereastră
    next_page_window.mainloop()

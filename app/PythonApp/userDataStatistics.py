import tkinter as tk
from tkinter import ttk

# Creăm fereastra principală Tkinter
root = tk.Tk()
root.title("Statistics")

# Setăm dimensiunea ferestrei
width = 600
height = 450

# Obținem dimensiunea ecranului
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculăm coordonatele pentru a plasa fereastra în partea dreaptă jos
x_pos = screen_width - width
y_pos = screen_height - height
root.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
root.configure(bg="#ADE1E7")

# Funcții pentru butoane
def show_total_statistics():
    print("Total statistics")

def show_latest_statistics():
    print("Latest statistics")

# Adăugăm un titlu centrat pe prima linie
title_label = ttk.Label(
    root, 
    text="Statistics Overview", 
    font=("Helvetica", 20, "bold"), 
    background="#ADE1E7", 
    anchor="center"
)
title_label.grid(row=0, column=0, columnspan=2, pady=40, sticky="ew")
title_label.place(relx=0.5, rely=0.28, width=500, height=70, anchor="center")

# Creăm butoanele și le poziționăm centrat pe linii diferite
button_total = ttk.Button(root, text="Total Statistics", command=show_total_statistics, style="TButton")
button_total.grid(row=1, column=0, columnspan=2, pady=20)
button_total.place(relx=0.5,rely=0.4,width=150, height=30, anchor="center")

button_latest = ttk.Button(root, text="Latest Statistics", command=show_latest_statistics, style="TButton")
button_latest.grid(row=2, column=0, columnspan=2, pady=20)
button_latest.place(relx=0.5,rely=0.48,width=150, height=30, anchor="center")

# Rulăm fereastra principală
root.mainloop()

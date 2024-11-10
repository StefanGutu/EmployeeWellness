import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np

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
    # Creăm date aleatoare pentru grafic (valori între 0 și 100)
    categories = ['Head', 'Shoulders', 'Close to Monitor']
    values = np.random.randint(0, 101, size=3)  # Generăm 3 valori aleatoare între 0 și 100

    # Creăm o fereastră pentru grafic
    fig, ax = plt.subplots()

    # Grafic cu 3 coloane și culori diferite
    colors = ['red', 'green', 'blue']  # Culori pentru coloane
    ax.bar(categories, values, color=colors)

    # Modificăm etichetele axelor și titlul cu font, dimensiune și culoare diferite
    ax.set_xlabel('Categories', fontsize=12, fontweight='bold', color='blue', labelpad=15)
    ax.set_ylabel('Number', fontsize=12, fontweight='bold', color='blue', labelpad=15)
    ax.set_title('Total Statistics', fontsize=14, fontweight='bold', color='darkgreen', pad=20)

    # Setăm intervalul pentru axa Y (de la 0 la 100)
    ax.set_ylim(0, 100)

    # Setăm pozițiile axei X pentru etichete
    ax.set_xticks(np.arange(len(categories)))  # Pozițiile corespunzătoare categoriilor

    # Modificăm etichetele axei X și le facem **bold** și font mai mic
    ax.set_xticklabels(categories, fontweight='bold', fontsize=9)

    # Obținem managerul ferestrei
    manager = plt.get_current_fig_manager()

    # Obținem fereastra și o poziționăm manual
    window = manager.window
    window_width = 800
    window_height = 600
    x_pos = (screen_width - window_width) // 2
    y_pos = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

    # Afișăm graficul
    plt.show()

def show_latest_statistics():
    # Creăm date aleatoare pentru grafic (valori între 0 și 10)
    categories = ['Head', 'Shoulders', 'Close to Monitor']
    values = np.random.randint(0, 11, size=3)  # Generăm 3 valori aleatoare între 0 și 10

    # Calculăm suma totală a valorilor
    total_value = sum(values)

    # Dacă suma totală este 0, setăm un fallback pentru evitarea diviziunii prin 0
    if total_value == 0:
        percentages = [0, 0, 0]
    else:
        # Calculăm procentajele pentru fiecare coloană
        percentages = [(value / total_value) * 100 for value in values]

    # Creăm o fereastră pentru grafic
    fig, ax = plt.subplots()

    # Grafic cu 3 coloane și culori diferite
    colors = ['red', 'green', 'blue']  # Culori pentru coloane
    ax.bar(categories, values, color=colors)

    # Modificăm etichetele axelor și titlul cu font, dimensiune și culoare diferite
    ax.set_xlabel('Categories', fontsize=12, fontweight='bold', color='blue', labelpad=15)
    ax.set_ylabel('Number', fontsize=12, fontweight='bold', color='blue', labelpad=15)
    ax.set_title('Latest Statistics', fontsize=14, fontweight='bold', color='darkgreen', pad=20)

    # Setăm intervalul pentru axa Y (de la 0 la 10)
    ax.set_ylim(0, 10)

    # Setăm pozițiile axei X pentru etichete
    ax.set_xticks(np.arange(len(categories)))  # Pozițiile corespunzătoare categoriilor

    # Modificăm etichetele axei X și le facem **bold** și font mai mic
    ax.set_xticklabels(categories, fontweight='bold', fontsize=9)

    # Afișăm procentele deasupra coloanelor
    for i, (value, percentage) in enumerate(zip(values, percentages)):
        ax.text(i, value + 0.2, f'{percentage:.1f}%', ha='center', fontsize=9, fontweight='bold', color='black')

    # Obținem managerul ferestrei
    manager = plt.get_current_fig_manager()

    # Obținem fereastra și o poziționăm manual
    window = manager.window
    window_width = 800
    window_height = 600
    x_pos = (screen_width - window_width) // 2
    y_pos = (screen_height - window_height) // 2
    window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

    # Afișăm graficul
    plt.show()

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
button_total.place(relx=0.5, rely=0.4, width=150, height=30, anchor="center")

button_latest = ttk.Button(root, text="Latest Statistics", command=show_latest_statistics, style="TButton")
button_latest.grid(row=2, column=0, columnspan=2, pady=20)
button_latest.place(relx=0.5, rely=0.48, width=150, height=30, anchor="center")

# Rulăm fereastra principală
root.mainloop()

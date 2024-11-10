import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import dataBaseCode
import next_page
import importlib 

def open_data_statistics(user_id,old_root):
    
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
        # Închide orice grafic existent înainte de a crea unul nou
        plt.close()  # Sau plt.clf() pentru a curăța figura curentă

        # Creăm date aleatoare pentru grafic (valori între 0 și 100)
        categories = ['Head', 'Shoulders', 'Close to Monitor']

        res = dataBaseCode.get_status(user_id)

        head_signal = res[0][1]  # index 1 is head_signal
        shoulder_signal = res[0][2]  # index 2 is shoulder_signal
        close_signal = res[0][3]  # index 3 is close_signal

        # Creăm o listă cu valorile pentru grafic
        values = [head_signal, shoulder_signal, close_signal]

        # Creăm o fereastră pentru grafic
        fig, ax = plt.subplots()

        # Grafic cu 3 coloane și culori diferite
        colors = ['red', 'green', 'blue']  # Culori pentru coloane
        ax.bar(categories, values, color=colors)

        # Modificăm etichetele axelor și titlul cu font, dimensiune și culoare diferite
        ax.set_xlabel('Categories', fontsize=12, fontweight='bold', color='blue', labelpad=15)
        ax.set_ylabel('Total receive data', fontsize=12, fontweight='bold', color='blue', labelpad=15)
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
        # Categoriile pentru care vrem să calculăm procentele
        categories = ['Head', 'Shoulders', 'Close to Monitor']

        # Obținem valorile din baza de date (aici se presupune că ai funcția care le aduce corect)
        values = dataBaseCode.get_latest_numbers(user_id)
        
        if not values:
            print("Nu au fost găsite valori pentru acest utilizator.")
            return

        # Extragem doar numerele (ignorați data pentru acest calcul)
        numbers = [row[0] for row in values]  # Extragem doar prima coloană care conține numerele

        # Calculăm câte valori sunt de fiecare tip (1, 2 și 3)
        count_1 = numbers.count(1)
        count_2 = numbers.count(2)
        count_3 = numbers.count(3)

        # Calculăm procentele pentru fiecare număr
        total = len(values)
        percentage_1 = (count_1 / total) * 100
        percentage_2 = (count_2 / total) * 100
        percentage_3 = (count_3 / total) * 100

        # Lista cu valorile numărate (count_1, count_2, count_3)
        counts = [count_1, count_2, count_3]

        # Procentele pentru fiecare categorie
        percentages = [percentage_1, percentage_2, percentage_3]

        # Creăm graficul
        fig, ax = plt.subplots(figsize=(8, 6))

        # Culori pentru fiecare coloană
        colors = ['red', 'green', 'blue']

        # Afișăm bara cu valorile pentru 1, 2 și 3
        ax.bar(categories, counts, color=colors)

        # Adăugăm procentele deasupra fiecărei coloane
        for i, (count, percentage) in enumerate(zip(counts, percentages)):
            ax.text(i, count + 0.2, f'{percentage:.1f}%', ha='center', fontsize=9, fontweight='bold', color='black')

        # Modificăm etichetele axelor și titlul
        ax.set_xlabel('Categories', fontsize=12, fontweight='bold', color='blue', labelpad=15)
        ax.set_ylabel('Recent receive data', fontsize=12, fontweight='bold', color='blue', labelpad=15)
        ax.set_title('Latest Statistics', fontsize=14, fontweight='bold', color='darkgreen', pad=20)

        # Setăm intervalul pentru axa Y
        ax.set_ylim(0, max(counts) + 2)

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
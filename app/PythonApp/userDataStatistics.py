import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
import dataBaseCode
import webbrowser

def open_data_statistics(user_id, old_root):
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


    # Funcția pentru afișarea statisticilor totale
    def show_total_statistics():
        plt.close()

        # Date de test pentru grafice
        categories = ['Head', 'Shoulders', 'Close to Monitor']
        res = dataBaseCode.get_status(user_id)

        head_signal = res[0][1]
        shoulder_signal = res[0][2]
        close_signal = res[0][3]
        values = [head_signal, shoulder_signal, close_signal]

        fig, ax = plt.subplots()
        colors = ['red', 'green', 'blue']
        ax.bar(categories, values, color=colors)
        ax.set_xlabel('Categories', fontsize=12, fontweight='bold', color='blue', labelpad=15)
        ax.set_ylabel('Total receive data', fontsize=12, fontweight='bold', color='blue', labelpad=15)
        ax.set_ylabel('Total receive data', fontsize=12, fontweight='bold', color='blue', labelpad=15)
        ax.set_title('Total Statistics', fontsize=14, fontweight='bold', color='darkgreen', pad=20)
        ax.set_ylim(0, 100)
        ax.set_xticks(np.arange(len(categories)))
        ax.set_xticklabels(categories, fontweight='bold', fontsize=9)
        plt.show()

    # Funcția pentru afișarea ultimelor statistici
    def show_latest_statistics():
        # Categoriile pentru care vrem să calculăm procentele
        categories = ['Head', 'Shoulders', 'Close to Monitor']

        # Obținem valorile din baza de date (aici se presupune că ai funcția care le aduce corect)
        values = dataBaseCode.get_latest_numbers(user_id)
        
        if not values:
            print("Nu au fost găsite valori pentru acest utilizator.")
            return

        numbers = [row[0] for row in values]
        count_1 = numbers.count(1)
        count_2 = numbers.count(2)
        count_3 = numbers.count(3)
        total = len(values)
        percentage_1 = (count_1 / total) * 100
        percentage_2 = (count_2 / total) * 100
        percentage_3 = (count_3 / total) * 100

        counts = [count_1, count_2, count_3]
        fig, ax = plt.subplots(figsize=(8, 6))
        colors = ['red', 'green', 'blue']
        ax.bar(categories, counts, color=colors)
        for i, (count, percentage) in enumerate(zip(counts, [percentage_1, percentage_2, percentage_3])):
            ax.text(i, count + 0.2, f'{percentage:.1f}%', ha='center', fontsize=9, fontweight='bold', color='black')
        ax.set_xlabel('Categories', fontsize=12, fontweight='bold', color='blue', labelpad=15)
        ax.set_ylabel('Recent receive data', fontsize=12, fontweight='bold', color='blue', labelpad=15)
        ax.set_ylabel('Recent receive data', fontsize=12, fontweight='bold', color='blue', labelpad=15)
        ax.set_title('Latest Statistics', fontsize=14, fontweight='bold', color='darkgreen', pad=20)
        ax.set_ylim(0, max(counts) + 2)
        plt.show()

    # Funcția pentru recomandări
    def show_recomandations():
        popup = tk.Toplevel(root)
        popup.title("Recomandations")
        
        values = dataBaseCode.get_latest_numbers(user_id)
        
        if not values:
            print("Nu au fost găsite valori pentru acest utilizator.")
            return

        numbers = [row[0] for row in values]
        count_1 = numbers.count(1)
        count_2 = numbers.count(2)
        count_3 = numbers.count(3)
        total = len(values)
        percentage_1 = (count_1 / total) * 100
        percentage_2 = (count_2 / total) * 100
        percentage_3 = (count_3 / total) * 100
        
        popup_width = 600
        popup_height = 450
        x_pos = (screen_width - popup_width) // 2
        y_pos = (screen_height - popup_height) // 2
        popup.geometry(f"{popup_width}x{popup_height}+{x_pos}+{y_pos}")
        popup.configure(bg="#ADE1E7")

        # Adăugăm recomandările
        recommendation_label = ttk.Label(
            popup, 
            text="Here are some recommendations based on your data.\n\n"
                 f"Head Position: {percentage_1}%\n"
                 f"Shoulders Position: {percentage_2}%\n"
                 f"Head Posture: {percentage_3}%\n\n"
                 "Follow these suggestions for better health and comfort.😊",
            font=("Helvetica", 14,"bold"), 
            background="#ADE1E7",
            anchor="center"
        )
        recommendation_label.pack(padx=20, pady=20)

        def open_google(path):
            webbrowser.open(path)

        # Linkuri pentru exerciții
        hyperlinks = [
            ("Exercise for good head posture", "https://backintelligence.com/how-to-fix-forward-head-posture/"),
            ("Exercise for good shoulders posture", "https://www.healthline.com/health/rounded-shoulders-exercises"),
            ("Exercise for good torso posture", "https://www.healthdirect.gov.au/how-to-improve-your-posture")
        ]
        
        for text, url in hyperlinks:
            link = ttk.Label(popup, text=text, foreground="black", font=("Helvetica", 12,"bold","underline"), background="#ADE1E7", cursor="hand2")
            link.pack(pady=10)
            link.bind("<Button-1>", lambda e, u=url: open_google(u))

        close_button = ttk.Button(popup, text="Close", command=popup.destroy, style="TButton")
        close_button.pack(pady=10)
        close_button.place(relx=0.5, rely=0.8, anchor="center")

    # Configurăm interfața grafică
    title_label = ttk.Label(root, text="Statistics Overview", font=("Helvetica", 20, "bold"), background="#ADE1E7", anchor="center")
    title_label.place(relx=0.5, rely=0.28, width=500, height=70, anchor="center")

    button_total = ttk.Button(root, text="Total Statistics", command=show_total_statistics, style="TButton")
    button_total.place(relx=0.5, rely=0.4, width=150, height=30, anchor="center")

    button_latest = ttk.Button(root, text="Latest Statistics", command=show_latest_statistics, style="TButton")
    button_latest.place(relx=0.5, rely=0.48, width=150, height=30, anchor="center")

    button_recomandation = ttk.Button(root, text="Recomandations", command=show_recomandations, style="TButton")
    button_recomandation.place(relx=0.5, rely=0.56, width=150, height=30, anchor="center")

    root.mainloop()

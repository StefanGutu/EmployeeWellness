import random
import time
import subprocess

def generate_random_numbers():
    while True:
        # Generează un număr aleatoriu între 1 și 4
        number = random.randint(1, 4)
        print(f"{number}")
        
        # Așteaptă 1 minut
        time.sleep(10)  # 60 secunde = 1 minut

generate_random_numbers()
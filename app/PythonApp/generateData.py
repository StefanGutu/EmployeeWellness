import random
import asyncio

# Function to generate random numbers continuously
# def generate_random_numbers():
#     return random.randint(0, 3)

class RandomNumberGenerator:
    def __init__(self):
        # Define the sequence
        self.sequence = [1, 1, 1, 2, 3, 0, 0]
        self.index = 0  # Initialize the counter to track the position in the sequence

    def generate_random_number(self):
        # Check if we still have elements left in the sequence
        if self.index < len(self.sequence):
            # Get the next element and increment the index
            number = self.sequence[self.index]
            self.index += 1
            return number
        else:
            # If we have exhausted the sequence, reset the index or return None
            self.index = 0  # You can reset or handle this case however you want
            return None  # or you could raise an exception if you prefer

import cv2
import os
import time
import sys
from datetime import datetime

# Get the folder name from command-line arguments
if len(sys.argv) < 4:
    print("Usage: python script.py <folder_name> <class_code> <first_index> ")
    sys.exit(1)

folder_name = sys.argv[1]
class_code = sys.argv[2]
image_counter = int(sys.argv[3])

# Create the folder if it does not exist
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Initialize the camera
camera = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not camera.isOpened():
    print("Error: Could not open the camera.")
    exit()

# Initialize variable
snapshot_interval = 3    # Time in seconds between each snapshot
start_time = time.time() # Track time for the countdown

try:
    while True:
        # Calculate remaining time for the next snapshot
        elapsed_time = time.time() - start_time
        remaining_time = max(0, snapshot_interval - int(elapsed_time))

        # Capture frame-by-frame
        ret, frame = camera.read()

        # If frame capture was successful
        if ret:
            # Display the countdown on the frame
            countdown_text = f"Next Snap In: {remaining_time}s"
            cv2.putText(frame, countdown_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Display the frame
            cv2.imshow("Camera Feed", frame)

            # Check if it's time to take a snapshot
            if elapsed_time >= snapshot_interval:
                # Reset the timer
                start_time = time.time()

                # Save the frame with the specified filename format
                image_filename = os.path.join(folder_name, f"img{image_counter}_{class_code}.jpg")
                cv2.imwrite(image_filename, frame)
                print(f"Image saved at {image_filename}")

                # Increment the image counter
                image_counter += 1

            # Exit when 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        else:
            print("Error: Could not capture frame.")

except KeyboardInterrupt:
    print("Process interrupted by user.")

finally:
    # Release the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()

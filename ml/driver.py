import pickle 
from image_landmark import get_pose_params
import cv2
import numpy as np
import time
import multiprocessing

SCREEN_TIME_LIMIT  = 180 # in seconds
FRAME_FREQ_RESPOND = 5
# This function handles receiving y_pred and doing something with it, e.g., logging or processing.
def process_predictions(queue):
    while True:
        if not queue.empty():
            y_pred = queue.get()
            print(f"Received y_pred: {y_pred}")  # Do something with the prediction
        time.sleep(0.1)  # Sleep to prevent tight loop that hogs CPU

# Protect entry point with if __name__ == "__main__"
if __name__ == "__main__":

    # Load the model
    with open("model/model.pkl", 'rb') as model_file:
        model = pickle.load(model_file)

    cap = cv2.VideoCapture(0)

    # Create a queue for inter-process communication
    queue = multiprocessing.Queue()

    # Start the process that will handle the predictions
    prediction_process = multiprocessing.Process(target=process_predictions, args=(queue,))
    prediction_process.start()

    last_capture_time = time.time()  # Initialize time control
    time_counter = 0
    screen_frames_limit = SCREEN_TIME_LIMIT/FRAME_FREQ_RESPOND
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            break

        # Get current time
        current_time = time.time()

        # Check if 5 seconds have passed since the last capture
        if current_time - last_capture_time >= FRAME_FREQ_RESPOND:
            last_capture_time = current_time  # Update the last capture time

            # Get pose parameters and annotated frame
            _, params = get_pose_params(frame)

            if params:
                time_counter+=1
                # Predict only if parameters are available
                pred_vec = model.predict_proba(np.array(list(params.values())).reshape(1, -1)).squeeze()
                y_pred = np.argmax(pred_vec)

                # Send y_pred to the other process via the queue
                # if program needs person to leave then it won't resets the counter until 
                # the person is not in the frame
                # We reset it for warning signal transmission
                if time_counter == screen_frames_limit:
                    y_pred = -1
                queue.put(y_pred)
            else:
                time_counter = 0

        # When closing app, close the webcam
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

    # Release the webcam and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

    # Terminate the prediction process when done
    prediction_process.terminate()
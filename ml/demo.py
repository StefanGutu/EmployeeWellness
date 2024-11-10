import pickle 
from image_landmark import get_pose_params
import cv2
import numpy as np

signal2text = {
    0: 'Good Posture',
    1: 'Bad neck posture',
    2: 'Move head back',
    3: 'Bad shoulders placement'
}

# Load the model
with open("model/model.pkl", 'rb') as model_file:
    model = pickle.load(model_file)

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        break

    # Get pose parameters and annotated frame
    annotated_frame, params = get_pose_params(frame)
    display_frame = frame if params is None else annotated_frame

    # Predict only if parameters are available
    if params:
        pred_vec = model.predict_proba(np.array(list(params.values())).reshape(1, -1)).squeeze()
        y_pred = np.argmax(pred_vec)

        # Define color based on y_pred value
        color = (0, 0, 255) if y_pred > 0 else (0, 255, 0)  # Red if y_pred > 0, Green if 0

        # Display y_pred on the left side of the frame
        cv2.putText(display_frame, f'{signal2text[y_pred]}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                    1, color, 2, cv2.LINE_AA)

    # Show the frame
    cv2.imshow("Body Keypoints with Lines", display_frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

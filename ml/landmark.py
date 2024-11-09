import cv2
import mediapipe as mp
import math

# Initialize MediaPipe Pose and Drawing modules
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

params = {
    "Head Ratio" : 0.0,
    "Head Tilt" : 0.0,
    "Shoulders Tilt": 0.0,
    "Neck Tilt" : 0.0,
    "Spine Tilt" : 0.0,
    "Neck Ratio" : 0.0,
    "Spine Ratio" : 0.0
}

# Function to extract and draw keypoints
def extract_and_draw_keypoints(image, pose):
    # Convert image color for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    if not results.pose_landmarks:
        return image

    # Map MediaPipe landmark indices for the relevant points
    landmarks = results.pose_landmarks.landmark
    points = {
        "Nose": landmarks[mp_pose.PoseLandmark.NOSE.value],
        "Right Shoulder": landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
        "Left Shoulder": landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
        "Right Hip": landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
        "Left Hip": landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
        "Right Eye": landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value],
        "Left Eye": landmarks[mp_pose.PoseLandmark.LEFT_EYE.value]
    }

    # Calculate midpoints for the torso center line and approximate neck
    def midpoint(pt1, pt2):
        return (
            (pt1.x + pt2.x) / 2,
            (pt1.y + pt2.y) / 2
        )

    shoulder_midpoint = midpoint(points["Right Shoulder"], points["Left Shoulder"])
    hip_midpoint = midpoint(points["Right Hip"], points["Left Hip"])
    neck_point = shoulder_midpoint  # Approximate neck as the midpoint of shoulders

    # Draw lines between key points
    # color = (0, 255, 0)  # Green color
    # thickness = 2  # Line thickness

    def draw_line(pt1, pt2, color=(0, 255, 0), thickness=2):
        cv2.line(
            image,
            (int(pt1[0] * image.shape[1]), int(pt1[1] * image.shape[0])),
            (int(pt2[0] * image.shape[1]), int(pt2[1] * image.shape[0])),
            color,
            thickness
        )

    # Draw lines for eyes, shoulders, and hips
    draw_line((points["Right Eye"].x, points["Right Eye"].y), (points["Left Eye"].x, points["Left Eye"].y))
    # draw_line((points["Right Shoulder"].x, points["Right Shoulder"].y), (points["Left Shoulder"].x, points["Left Shoulder"].y))
    draw_line((points["Right Hip"].x, points["Right Hip"].y), (points["Left Hip"].x, points["Left Hip"].y))
    draw_line(shoulder_midpoint, hip_midpoint)  # Torso center line

    # Draw the head-to-neck line
    head_point = (points["Nose"].x, points["Nose"].y)
    draw_line(head_point, neck_point, color=(255, 0, 0), thickness=2)  # Red line from head to neck

    # Draw lines from each shoulder to the neck
    draw_line((points["Right Shoulder"].x, points["Right Shoulder"].y), neck_point, color=(0, 0, 255), thickness=2)  # Blue line
    draw_line((points["Left Shoulder"].x, points["Left Shoulder"].y), neck_point, color=(0, 0, 255), thickness=2)  # Blue line

    return image, points

def point_distance(x:tuple, y:tuple)->float:
    return math.sqrt((x[1]-x[0])**2 + (y[1]-y[0])**2)

# Start capturing video from the webcam
cap = cv2.VideoCapture(0)
# Set the resolution (width and height)
# width = 1280  # Set your desired width
# height = 720  # Set your desired height
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Check if the resolution was set correctly
actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"Resolution set to: {actual_width} x {actual_height}")



# Initialize MediaPipe Pose in a context
with mp_pose.Pose(static_image_mode=False) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            break
        
        # Process and draw keypoints on the frame
        annotated_frame, pose_points = extract_and_draw_keypoints(frame, pose)

        head_ratio = point_distance((pose_points["Right Eye"].x, pose_points["Left Eye"].x), (pose_points["Right Eye"].y, pose_points["Left Eye"].y))
        text = f"Head R = {head_ratio}"

        frame_height, frame_width = frame.shape[:2]
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        color = (255, 255, 255)
        thickness = 2
        (text_width, text_height), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        x=frame_width - text_width -10
        y = 10+text_height

        cv2.putText(annotated_frame, text, (x,y), font, font_scale, color, thickness)        


        # Display the resulting frame
        cv2.imshow("Body Keypoints with Lines", annotated_frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

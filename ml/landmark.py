import cv2
import mediapipe as mp
import math
from collections import namedtuple

# Initialize MediaPipe Pose and Drawing modules
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

params = {
    "Head Ratio"     : None,
    "Head Tilt"      : None,
    "Shoulders Tilt" : None,
    "Neck Tilt"      : None,
    "Neck Ratio"     : None,
    "Neck Depth"     : None,
    "Shoulders Depth": None
}

def get_points(image, pose):
    Point = namedtuple("Point", ["x", "y", "z"])
    def midpoint(pt1, pt2):
        return Point(
            (pt1.x + pt2.x) / 2,
            (pt1.y + pt2.y) / 2,
            (pt1.z + pt2.z) / 2
        )

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    results = pose.process(image_rgb)
    if not results.pose_landmarks:
        return image

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

    points['Mid Shoulder'] = midpoint(points["Right Shoulder"], points["Left Shoulder"])
    points['Mid Hip'] = midpoint(points["Right Hip"], points["Left Hip"])
    return points
    # neck_point = shoulder_midpoint  # Approximate neck as the midpoint of shoulders

# Function to extract and draw keypoints
def draw_keypoints(image, pose):
    points = get_points(image, pose)
    
    # Check if points are None (i.e., no pose detected)
    if points is None:
        print("No person detected in the frame.")
        return image  # Return the original image without modifications

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
    draw_line((points["Right Hip"].x, points["Right Hip"].y), (points["Left Hip"].x, points["Left Hip"].y))
    draw_line(points['Mid Shoulder'], points['Mid Hip'])  # Torso center line

    # Draw the head-to-neck line
    head_point = (points["Nose"].x, points["Nose"].y)
    draw_line(head_point, points['Mid Shoulder'], color=(255, 0, 0), thickness=2)  # Red line from head to neck

    # Draw lines from each shoulder to the neck
    draw_line((points["Right Shoulder"].x, points["Right Shoulder"].y), points['Mid Shoulder'], color=(0, 0, 255), thickness=2)  # Blue line
    draw_line((points["Left Shoulder"].x, points["Left Shoulder"].y), points['Mid Shoulder'], color=(0, 0, 255), thickness=2)  # Blue line

    return image


def point_distance(x:tuple, y:tuple)->float:
    return math.sqrt((x[1]-x[0])**2 + (y[1]-y[0])**2)

def get_pose_params():
    return params

def get_tilt(type:str, points:dict) -> float:
    return math.atan(point_distance((points[f'Right {type}'].x, points[f'Right {type}'].x), (points[f"Right {type}"].y, points[f'Left {type}'].y)) / point_distance((points[f'Left {type}'].x, points[f'Right {type}'].x), (points[f"Left {type}"].y, points[f'Left {type}'].y)))

def get_depth(type:str, points:dict, mode='vertical') -> float:
    if mode not in ['vertical', 'horizontal']:
        raise ValueError(f"### No such mode: {mode} ###")
    if mode == 'vertical':
        return math.atan(point_distance((points[f'Right {type}'].z, points[f'Right {type}'].z), (points[f"Right {type}"].y, points[f'Left {type}'].y)) / point_distance((points[f'Left {type}'].z, points[f'Right {type}'].z), (points[f"Left {type}"].y, points[f'Left {type}'].y)))

    elif mode == 'horizontal':
        return math.atan(point_distance((points[f'Right {type}'].z, points[f'Right {type}'].z), (points[f"Right {type}"].x, points[f'Left {type}'].x)) / point_distance((points[f'Left {type}'].z, points[f'Right {type}'].z), (points[f"Left {type}"].x, points[f'Left {type}'].x)))


# Start capturing video from the webcam
cap = cv2.VideoCapture(0)
# Check if the resolution was set correctly
actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
# print(f"Resolution set to: {actual_width} x {actual_height}")

# Initialize MediaPipe Pose in a context
with mp_pose.Pose(static_image_mode=False) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            break

        # Process and draw keypoints on the frame
        pose_points = get_points(frame, pose)

        # Check if pose_points is None or does not contain required points
        required_points = ["Right Eye", "Left Eye", "Right Shoulder", "Left Shoulder", "Nose", "Mid Shoulder"]
        # TODO: bagam in retea doar daca este pose_points != None
        if pose_points is None or not all(key in pose_points for key in required_points):
            annotated_frame = frame  # Show the original frame without modifications
            
            cv2.imshow("Body Keypoints with Lines", annotated_frame)

            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            continue
        else:
            annotated_frame = draw_keypoints(frame, pose)
            # Display the resulting frame

        params["Head Ratio"] = point_distance((pose_points["Right Eye"].x, pose_points["Left Eye"].x), (pose_points["Right Eye"].y, pose_points["Left Eye"].y)) / point_distance((pose_points['Left Shoulder'].x, pose_points['Right Shoulder'].x), (pose_points['Left Shoulder'].y, pose_points['Right Shoulder'].y))
        params['Head Tilt'] = get_tilt("Eye", pose_points)

        params['Shoulders Tilt'] = get_tilt("Shoulder", pose_points)
        params['Neck Tilt'] = math.atan(point_distance((pose_points['Nose'].x, pose_points['Mid Shoulder'].x), (pose_points['Nose'].y, pose_points['Nose'].y)) / point_distance((pose_points['Mid Shoulder'].x, pose_points['Mid Shoulder'].x), (pose_points['Mid Shoulder'].y, pose_points['Nose'].y)))  #math.atan(point_distance((pose_points[f'Right {type}'].x, points[f'Right {type}'].x), (pose_points[f"Right {type}"].y, pose_points[f'Left {type}'].y)) / point_distance((pose_points[f'Left {type}'].x, pose_points[f'Right {type}'].x), (pose_points[f"Left {type}"].y, pose_points[f'Left {type}'].y)))
        params['Neck Ratio'] = point_distance((pose_points["Nose"].x, pose_points["Mid Shoulder"].x), (pose_points["Nose"].y, pose_points["Mid Shoulder"].y)) / point_distance((pose_points['Left Shoulder'].x, pose_points['Right Shoulder'].x), (pose_points['Left Shoulder'].y, pose_points['Right Shoulder'].y))
        params['Neck Depth'] = math.atan(point_distance((pose_points['Nose'].z, pose_points['Nose'].z), (pose_points['Nose'].y, pose_points['Mid Shoulder'].y)) / point_distance((pose_points['Nose'].z, pose_points['Mid Shoulder'].z), (pose_points['Mid Shoulder'].y, pose_points['Mid Shoulder'].y)))
        params['Shoulders Depth'] = get_depth('Shoulder', pose_points, 'horizontal')
        
        # Useful prints for debugging
        head_r_txt = f"Head R = {params["Head Ratio"]}"
        head_t_txt = f"Shoulder D = {params['Shoulders Depth']}"

        frame_height, frame_width = frame.shape[:2]
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.5
        color = (255, 255, 255)
        thickness = 2
        (text_width, text_height), baseline = cv2.getTextSize(head_r_txt, font, font_scale, thickness)
        x=frame_width - text_width -10
        y = 10+text_height

        cv2.putText(annotated_frame, head_r_txt, (x,y), font, font_scale, color, thickness)   

        (text_width, text_height), baseline = cv2.getTextSize(head_t_txt, font, font_scale, thickness)
        x=frame_width - text_width -10
        y = 30+text_height

        cv2.putText(annotated_frame, head_t_txt, (x,y), font, font_scale, color, thickness)  



        # Display the resulting frame
        cv2.imshow("Body Keypoints with Lines", annotated_frame)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()

import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose and Drawing modules
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Function to extract and draw keypoints
def extract_and_draw_keypoints(image, pose):
    """
    Processes a single image to detect and draw keypoints.

    Parameters:
    - image (np.ndarray): The input image in which keypoints will be detected and marked.
    - pose (mp_pose.Pose): An initialized MediaPipe Pose object.

    Returns:
    - edited_image (np.ndarray): The image with keypoints and lines drawn.
    - points (dict): Dictionary of detected keypoints with (x, y) coordinates.
    """
    # Convert image color for MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    # Return the original image if no landmarks are detected
    if not results.pose_landmarks:
        return image, {}

    # Map MediaPipe landmark indices for the relevant points
    landmarks = results.pose_landmarks.landmark
    points = {
        "Nose": (landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y),
        "Right Shoulder": (landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y),
        "Left Shoulder": (landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y),
        "Right Hip": (landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y),
        "Left Hip": (landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y),
        "Right Eye": (landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].x, landmarks[mp_pose.PoseLandmark.RIGHT_EYE.value].y),
        "Left Eye": (landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].x, landmarks[mp_pose.PoseLandmark.LEFT_EYE.value].y)
    }

    # Helper function to calculate midpoint
    def midpoint(pt1, pt2):
        return ((pt1[0] + pt2[0]) / 2, (pt1[1] + pt2[1]) / 2)

    # Calculate midpoints for shoulder and hip, approximate neck
    shoulder_midpoint = midpoint(points["Right Shoulder"], points["Left Shoulder"])
    hip_midpoint = midpoint(points["Right Hip"], points["Left Hip"])
    neck_point = shoulder_midpoint

    # Draw function
    def draw_line(pt1, pt2, color=(0, 255, 0), thickness=2):
        cv2.line(
            image,
            (int(pt1[0] * image.shape[1]), int(pt1[1] * image.shape[0])),
            (int(pt2[0] * image.shape[1]), int(pt2[1] * image.shape[0])),
            color,
            thickness
        )

    # Draw lines for eyes, shoulders, hips, and torso center line
    draw_line(points["Right Eye"], points["Left Eye"])
    draw_line(points["Right Hip"], points["Left Hip"])
    draw_line(shoulder_midpoint, hip_midpoint)  # Torso center line

    # Draw head-to-neck line and shoulder-to-neck lines
    draw_line(points["Nose"], neck_point, color=(255, 0, 0), thickness=2)  # Red line from head to neck
    draw_line(points["Right Shoulder"], neck_point, color=(0, 0, 255), thickness=2)  # Blue line
    draw_line(points["Left Shoulder"], neck_point, color=(0, 0, 255), thickness=2)  # Blue line

    return image, points

# Example usage
if __name__ == "__main__":
    # Load an image (replace 'path/to/image.jpg' with the path to your image)
    input_image = cv2.imread(r"C:\Users\emil.blejdea\Desktop\EmployeeWellness\ml\bad_shoulders\img51_3.jpg")
    alpha = 0.5  # Contrast control (1.0-3.0)
    beta = -5    # Brightness control (0-100)

# Apply brightness and contrast adjustment
    #lighting = cv2.convertScaleAbs(input_image, alpha=alpha, beta=beta)
    lighting = darker_image = cv2.subtract(input_image, (50, 50, 50))
    blurred = cv2.GaussianBlur(lighting, (5, 5), 0)
    sharpening_kernel = np.array([[0, -1, 0], [-1, 6, -1], [0, -1, 0]])

# Apply the kernel using cv2.filter2D
    sharpened = cv2.filter2D(blurred, -1, sharpening_kernel)
    # Initialize MediaPipe Pose in a context
    with mp_pose.Pose(static_image_mode=True) as pose:
        # Process the image and get the edited image and keypoints
        edited_image, keypoints = extract_and_draw_keypoints(input_image, pose)
        #edited_lighting, keypoints = extract_and_draw_keypoints(lighting, pose)
        #edited_blurred, keypoints = extract_and_draw_keypoints(blurred, pose)
        edited_sharpened, keypoints = extract_and_draw_keypoints(sharpened, pose)
        # Show the processed image
        cv2.imshow("Processed Image", edited_image)
        #cv2.imshow("light", edited_lighting)
        #cv2.imshow("blurr", edited_blurred)
        cv2.imshow("sharpen", edited_sharpened)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Print detected keypoints
        print("Detected keypoints:", keypoints)

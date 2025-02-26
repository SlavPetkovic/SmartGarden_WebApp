import cv2
from ultralytics import YOLO
import time

# Load the YOLOv8 model (using a smaller model for faster performance, e.g., "yolo11n.pt")
model = YOLO("yolo11x.pt")  # Switch to "yolo11x.pt" for a larger, more accurate model if needed

# Open the webcam (source="0" for the default camera)
cap = cv2.VideoCapture(0)  # Replace 0 with the index of your camera if you have multiple

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Adjust webcam resolution to reduce latency
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)  # Set width
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)  # Set height

# Initialize variables for FPS calculation
prev_time = time.time()

# Read frames from the webcam and apply YOLO predictions
while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture frame from webcam.")
        break

    # Run YOLO predictions on the current frame with a confidence threshold of 50%
    results = model.predict(source=frame, conf=0.5, show=False)  # Adjust confidence threshold as needed

    # Visualize predictions on the frame
    annotated_frame = results[0].plot()

    # Calculate FPS
    curr_time = time.time()
    fps = 1 / (curr_time - prev_time)
    prev_time = curr_time

    # Display FPS on the frame
    cv2.putText(annotated_frame, f"FPS: {int(fps)}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Display the frame with YOLO predictions
    cv2.imshow("YOLOv8 Webcam", annotated_frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()

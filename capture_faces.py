from picamera2 import Picamera2
import cv2
import time

# Initialize camera
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

count = 0
print("Press SPACE to capture image, ESC to exit")

while count < 15:
    # Capture frame
    frame = picam2.capture_array()
    
    # Display frame
    cv2.imshow("Capture Face Photos", frame)
    
    key = cv2.waitKey(1)
    
    # Press SPACE to save image
    if key == 32:  # SPACE key
        filename = f"face_{count:02d}.jpg"
        cv2.imwrite(filename, frame)
        print(f"Saved {filename}")
        count += 1
        time.sleep(0.5)
    
    # Press ESC to exit
    elif key == 27:  # ESC key
        break

cv2.destroyAllWindows()
picam2.stop()
print(f"Captured {count} images")

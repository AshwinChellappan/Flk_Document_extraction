import cv2
from deepface import DeepFace
import os

def capture_photo(filename):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Could not open video device")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    ret, frame = cap.read()
    if not ret:
        raise Exception("Failed to capture image")

    cv2.imwrite(filename, frame)
    print(f"Captured image saved at {filename}")

    cap.release()
    cv2.destroyAllWindows()
    return filename

def verify_image_readability(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to read image from path: {image_path}")
    print(f"Image at {image_path} is readable and has shape: {img.shape}")
    return img

def compare_faces(img1_path, img2_path):
    try:
        img1 = verify_image_readability(img1_path)
        img2 = verify_image_readability(img2_path)

        print("Both images are readable.")
        print(f"Comparing {img1_path} with {img2_path}")

        result = DeepFace.verify(img1_path, img2_path)
        print(f"DeepFace verification result: {result}")
        return result
    except Exception as e:
        print(f"Error in compare_faces: {e}")
        raise

if __name__ == "__main__":
    local_image_path = "C:/Users/AC16/OneDrive - Capgemini/Desktop/Fortive/POC/Deepface/Photo.jpg"
    captured_image_path = "C:/Users/AC16/OneDrive - Capgemini/Desktop/Fortive/POC/Deepface/captured_image.jpg"
    
    if not os.path.exists(local_image_path):
        print(f"Local image path does not exist: {local_image_path}")
        exit(1)

    try:
        captured_image_path = capture_photo(captured_image_path)
    except Exception as e:
        print(f"Error capturing image: {e}")
        exit(1)
    
    try:
        # Test if DeepFace can process the captured image alone
        verify_image_readability(captured_image_path)
        print("Attempting to process the captured image with DeepFace...")
        deepface_result = DeepFace.analyze(captured_image_path, actions=['age', 'gender', 'race', 'emotion'])
        print(f"DeepFace analysis result: {deepface_result}")
    except Exception as e:
        print(f"Error processing captured image with DeepFace: {e}")
        exit(1)
    
    try:
        comparison_result = compare_faces(captured_image_path, local_image_path)
    except Exception as e:
        print(f"Error comparing images: {e}")
        exit(1)

    if comparison_result["verified"]:
        print("Faces match!")
    else:
        print("Faces do not match!")

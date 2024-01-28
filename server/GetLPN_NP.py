import cv2
import keras_ocr
from ultralytics import YOLO

# Load a pretrained YOLOv8n model
yolo_model = YOLO('server/best.pt')

# Define path to the image file
source = 'server/testing/image1.jpg'
original_image = cv2.imread(source)

# Run YOLOv8n inference on the source
results = yolo_model(source)

for result in results:
    boxes = result.boxes.cpu().numpy()
    for box in boxes:
        xyxy = box.xyxy[0].astype(int)

        # Extract coordinates
        x_min, y_min, x_max, y_max = xyxy

        # Read the original image
        image = cv2.imread(source)


        # Crop the image based on the bounding box
        cropped_image = image[y_min:y_max, x_min:x_max]


        # Load keras-ocr pipeline
        pipeline = keras_ocr.pipeline.Pipeline()


        # Run keras-ocr on the cropped image
        keras_ocr_result = pipeline.recognize([cropped_image])

        # Print the result
        concatenated_text = ' '.join([text for text, _ in keras_ocr_result[0]])
        print("Concatenated Text:", concatenated_text)
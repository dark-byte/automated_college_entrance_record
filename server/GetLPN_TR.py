import cv2
import keras_ocr
from ultralytics import YOLO

# Load a pretrained YOLOv8n model
yolo_model = YOLO('best.pt')

# Define path to the image file
source = '/Users/adrish_mitra/Documents/CODE/automated_college_entrance_record/server/testing/image2.jpg'
original_image = cv2.imread(source)

# Run YOLOv8n inference on the source
results = yolo_model(source)

# Assuming results is a list containing a single tensor
for box in results[0]:
    # Extract coordinates from the tensor
    x_min, y_min, x_max, y_max, confidence, class_idx = box.tolist()

    # Convert to integers for better readability
    x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)

    # Print the coordinates
    print(f"Bounding Box Coordinates: ({x_min}, {y_min}, {x_max}, {y_max})")

    # Crop the region from the original image
    cropped_image = original_image[y_min:y_max, x_min:x_max]

    # Run keras-ocr on the cropped image
    pipeline = keras_ocr.pipeline.Pipeline()
    predictions = pipeline.recognize([cropped_image])

    # Display or process OCR results
    for text, box in predictions[0]:
        # Access box coordinates
        x_min_ocr, y_min_ocr = box[0]
        x_max_ocr, y_max_ocr = box[2]

        # Convert to integers for better readability
        x_min_ocr, y_min_ocr, x_max_ocr, y_max_ocr = (
            int(x_min_ocr), int(y_min_ocr), int(x_max_ocr), int(y_max_ocr)
        )

        # Print the OCR bounding box coordinates
        print(f"OCR Bounding Box Coordinates: ({x_min_ocr}, {y_min_ocr}, {x_max_ocr}, {y_max_ocr})")

        # Print the OCR result
        print(f"OCR Result: {text}")

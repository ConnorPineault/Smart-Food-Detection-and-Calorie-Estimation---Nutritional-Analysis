import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('/Users/zacharyferguson/CMPE452/best (21).pt')

image_path = '/Users/zacharyferguson/CMPE452/images/triple-chocolate-cake-4.jpg'
output_path_with_boundary = '/Users/zacharyferguson/CMPE452/Output_Imgs/output_with_boundary.jpg'

original_image = cv2.imread(image_path)
original_height, original_width, _ = original_image.shape

resized_image = cv2.resize(original_image, (640, 640), interpolation=cv2.INTER_LINEAR)

results = model.predict(source=resized_image, conf=0.5)

if results[0].masks is None:
    print("No masks detected. Ensure the model is trained for instance segmentation.")
else:
    object_counts = {}  

    for mask, box, cls in zip(results[0].masks.data, results[0].boxes.xyxy, results[0].boxes.cls):
        mask_resized = cv2.resize(mask.cpu().numpy(), (original_width, original_height), interpolation=cv2.INTER_NEAREST)
        binary_mask = (mask_resized > 0.5).astype(np.uint8)  

        color = [int(c) for c in np.random.randint(0, 255, size=3)]

        overlay = original_image.copy()
        for i in range(3):  
            overlay[:, :, i] = np.where(binary_mask == 1,
                                        (original_image[:, :, i] * 0.5 + color[i] * 0.5).astype(np.uint8),
                                        original_image[:, :, i])
        original_image = overlay.copy()

  
        x1, y1, x2, y2 = box.cpu().numpy()
        x1 = int(x1 * original_width / 640)  
        y1 = int(y1 * original_height / 640)
        x2 = int(x2 * original_width / 640)
        y2 = int(y2 * original_height / 640)
        cv2.rectangle(original_image, (x1, y1), (x2, y2), color=(255, 0, 0), thickness=2)

        class_id = int(cls)  
        object_name = model.names[class_id] if class_id in model.names else "Unknown"

       
        if object_name in object_counts:
            object_counts[object_name] += 1
        else:
            object_counts[object_name] = 1

   
    for obj, count in object_counts.items():
        print(f"{obj}: {count}")

    
    cv2.imwrite(output_path_with_boundary, original_image)
    print(f"Image with shaded objects and bounding boxes saved as {output_path_with_boundary}")

    print("All Detected Objects:", ", ".join([f"{obj} ({count})" for obj, count in object_counts.items()]))

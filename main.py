import cv2
import numpy as np
from ultralytics import YOLO

model = YOLO('/Users/zacharyferguson/CMPE452/vision.pt')

image_path = '/Users/zacharyferguson/CMPE452/images.jpeg'
output_path_segmented = 'output_segmented_kmeans.jpg'
output_path_filled = 'output_filled_segmented_kmeans.jpg'

image = cv2.imread(image_path)

results = model.predict(source=image_path, conf=0.25)

for result in results[0].boxes:
    x1, y1, x2, y2 = map(int, result.xyxy[0])
    padding = 10
    x1 = max(0, x1 - padding)
    y1 = max(0, y1 - padding)
    x2 = min(image.shape[1], x2 + padding)
    y2 = min(image.shape[0], y2 + padding)

    roi = image[y1:y2, x1:x2]
    ycrcb_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2YCrCb)
    ycrcb_pixels = ycrcb_roi.reshape((-1, 3)).astype(np.float32)

    k = 9  
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(ycrcb_pixels, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    segmented = labels.reshape(roi.shape[:2])


    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    segmented = cv2.morphologyEx(segmented.astype(np.uint8), cv2.MORPH_CLOSE, kernel)

    segmented_vis = np.zeros_like(roi)
    for i in range(k):
        segmented_vis[segmented == i] = (i * 85, i * 85, i * 85)  
    cv2.imwrite(output_path_segmented, segmented_vis)

    apple_cluster = np.argmax(centers[:, 1])  
    apple_mask = (segmented == apple_cluster).astype(np.uint8) * 255
    cv2.imwrite(output_path_filled, apple_mask)

    total_pixels = apple_mask.size
    white_pixel_count = np.sum(apple_mask == 255)

    # Estimate distance and scale
    reference_distance = 2.0
    reference_area = 5000
    if white_pixel_count > 0:
        estimated_distance = reference_distance * np.sqrt(reference_area / white_pixel_count)
        scaling_factor = (estimated_distance / reference_distance) ** 2
        adjusted_apple_size = white_pixel_count * scaling_factor
        print(f"Total Pixels: {total_pixels}")
        print(f"White Pixels (Background): {white_pixel_count}")
        print(f"Black Pixels (Apple Area): {white_pixel_count}")
        print(f"Estimated distance of the apple: {estimated_distance:.2f} feet")
        print(f"Adjusted apple size at 2 feet: {adjusted_apple_size:.2f} pixels")
    else:
        print("No valid apple area detected.")

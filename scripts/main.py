import cv2
import numpy as np
from ultralytics import YOLO






model = YOLO('/Users/connorpineault/Downloads/Smart-Food-Detection-and-Calorie-Estimation---Nutritional-Analysis/models/vision_model.pt')
image_path = ("/Users/connorpineault/Downloads/Smart-Food-Detection-and-Calorie-Estimation---Nutritional-Analysis/images/test.webp")


# image_path = ("/Users/connorpineault/Downloads/Smart-Food-Detection-and-Calorie-Estimation---Nutritional-Analysis/images/testimage2.jpeg")




output_path_with_boundary = '/Users/zacharyferguson/CMPE452/Output_Imgs/output_with_boundary.jpg'

original_image = cv2.imread(image_path)
original_height, original_width, _ = original_image.shape

resized_image = cv2.resize(original_image, (640, 640), interpolation=cv2.INTER_LINEAR)

results = model.predict(source=resized_image, conf=0.5)




food_calories = {
    "apple": 52,
    "banana": 89,
    "orange": 47,
    "strawberry": 33,
    "grapes": 69,
    "carrot": 41,
    "broccoli": 34,
    "potato": 77,
    "chicken Breast": 165,
    "salmon": 208,
    "egg": 155,
    "rice": 130,
    "pasta": 131,
    "cheese": 402,
    "bread": 265,
    "avocado": 160,
    "peanut butter": 588,
    "yogurt": 59,
    "milk": 42,
    "chocolate": 546
}
def get_caloric_value(food_name):

    return food_calories.get(food_name, None)
def getInfo(recognized_food):

    calories = get_caloric_value(recognized_food)
    print('recognized food: ', recognized_food)
    if calories is not None:
        print(f"The caloric value of {recognized_food} is {calories} kcal per 100 grams.")
    else:
        print(f"Caloric data for {recognized_food} is not available.")




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


        print(getInfo(obj))

        print(f"{obj}: {count}")




    
    cv2.imwrite(output_path_with_boundary, original_image)
    print(f"Image with shaded objects and bounding boxes saved as {output_path_with_boundary}")

    print("All Detected Objects:", ", ".join([f"{obj} ({count})" for obj, count in object_counts.items()]))



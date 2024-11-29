food_calories = {
    "Apple": {
        "Honeycrisp": 57,
        "Granny Smith": 58,
        "Default": 52  # Fallback if specific type is not found
    },
    "Pasta": {
        "Pesto": 150,
        "Red Sauce": 131,
        "Alfredo": 200,
        "Default": 131  # Fallback if specific type is not found
    },
    "Banana": {"Default": 89},  # Single value with a "Default" key
    "Orange": {"Default": 47},
    "Chicken Breast": {"Default": 165}

}


def get_caloric_value(food_name, subtype=None):
 
    food_data = food_calories.get(food_name)
    if not food_data:
        return None  
    
    if isinstance(food_data, dict):  # Check for subcategories
        if subtype and subtype in food_data:
            return food_data[subtype]
        return food_data.get("Default")  # Fallback to Default
    return food_data  




def getInfo(recognized_food, subtype):


    calories = get_caloric_value(recognized_food, subtype)

    if calories is not None:
        print(f"The caloric value of {subtype or recognized_food} is {calories} kcal per 100 grams.")
    else:
        print(f"Caloric data for {recognized_food} ({subtype}) is not available.")




def main():

    #from file import file and return food and subtype

    x = "Pasta"
    y = "Alfredo" #if cant find subtype, pass empty string, it will be default val 
    test = getInfo(x, y)


main()
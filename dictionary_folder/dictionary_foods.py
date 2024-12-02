
food_calories = {
    "Apple": 52,
    "Banana": 89,
    "Orange": 47,
    "Strawberry": 33,
    "Grapes": 69,
    "Carrot": 41,
    "Broccoli": 34,
    "Potato": 77,
    "Chicken Breast": 165,
    "Salmon": 208,
    "Egg": 155,
    "Rice": 130,
    "Pasta": 131,
    "Cheese": 402,
    "Bread": 265,
    "Avocado": 160,
    "Peanut Butter": 588,
    "Yogurt": 59,
    "Milk": 42,
    "Chocolate": 546
}


#gets key val pair . returns 
def get_caloric_value(food_name):

    return food_calories.get(food_name, None)





def getInfo(recognized_food):

    calories = get_caloric_value(recognized_food)

    if calories is not None:
        print(f"The caloric value of {recognized_food} is {calories} kcal per 100 grams.")
    else:
        print(f"Caloric data for {recognized_food} is not available.")



def main():

    #from file import file and return food,

    x = "Egg"
    test = getInfo(x)


main()
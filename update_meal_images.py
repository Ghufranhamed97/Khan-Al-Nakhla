import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.models import Meal

def update_meal_images():
    meal_images = {
        "Libn": "meal_images/Libn.jpeg",
        "Hibiscus Tea": "meal_images/Hibiscus-Tea.jpeg",
        "Arabic Coffee": "meal_images/Arabic_Coffee.jpeg",
        "Mint Lemonade": "meal_images/Mint_Lemonade.jpeg",
        "Rice Pudding": "meal_images/Rice_Pudding.jpeg",
        "Knafeh": "meal_images/Knafeh.jpeg",
        "Baklava": "meal_images/Baklava.jpeg",
        "Baba Ghanoush": "meal_images/Baba_Ghanoush.jpeg",
        "Rice Pilaf": "meal_images/Rice_Pilaf.jpeg",
        "Lentil Soup": "meal_images/Lentil_Soup.jpeg",
        "Fattoush": "meal_images/Fattoush.jpeg",
        "Chicken Mandi": "meal_images/Chicken_Mandi.jpeg",
        "Mansaf": "meal_images/Mansaf.jpeg",
        "Lamb Kofta": "meal_images/Lamb_Kofta.jpeg",
        "Maklouba": "meal_images/Maklouba.jpeg",
        "Shawarma": "meal_images/Shawarma.jpeg",
        "Kibbeh": "meal_images/Kibbeh.jpeg",
        "Falafel": "meal_images/Falafel.jpeg",
        "Tabbouleh": "meal_images/Tabbouleh.jpeg",
        "Dolma": "meal_images/Dolma.jpeg",
        "Hummus with Tahini": "meal_images/Hummus_with_Tahini.jpeg",
        "Mixed Grill": "meal_images/Mixed_Grill.jpeg",
        
    }

    for meal_name, image_path in meal_images.items():
        meals = Meal.objects.filter(name=meal_name)
        if meals.exists():
            count = meals.update(image=image_path)
            print(f"Updated image for {count} '{meal_name}' meal(s)")
        else:
            print(f"No meal found with name '{meal_name}'")

update_meal_images()
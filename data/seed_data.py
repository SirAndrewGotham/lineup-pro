from core.models import *

# Universal Fast-Food Assembly Templates
UNIVERSAL_TEMPLATES = [
    SandwichTemplate(
        id="template_001",
        name="Classic Burger",
        station="Grill",
        difficulty=2,
        total_time_target=45,
        steps=[
            AssemblyStep(order=1, ingredient=Ingredient(
                id="ing_001", name="Bottom Bun", type=IngredientType.BREAD,
                image_path="assets/images/bottom_bun.png"
            ), placement="heel", time_target=3),
            AssemblyStep(order=2, ingredient=Ingredient(
                id="ing_002", name="Beef Patty", type=IngredientType.PROTEIN,
                image_path="assets/images/beef_patty.png"
            ), placement="center", time_target=5),
            AssemblyStep(order=3, ingredient=Ingredient(
                id="ing_003", name="Cheese Slice", type=IngredientType.CHEESE,
                image_path="assets/images/cheese.png"
            ), placement="center", time_target=3),
            AssemblyStep(order=4, ingredient=Ingredient(
                id="ing_004", name="Lettuce", type=IngredientType.VEGETABLE,
                image_path="assets/images/lettuce.png"
            ), placement="center", time_target=4),
            AssemblyStep(order=5, ingredient=Ingredient(
                id="ing_005", name="Tomato", type=IngredientType.VEGETABLE,
                image_path="assets/images/tomato.png"
            ), placement="center", time_target=4),
            AssemblyStep(order=6, ingredient=Ingredient(
                id="ing_006", name="Onion", type=IngredientType.VEGETABLE,
                image_path="assets/images/onion.png"
            ), placement="center", time_target=4),
            AssemblyStep(order=7, ingredient=Ingredient(
                id="ing_007", name="Special Sauce", type=IngredientType.SAUCE,
                image_path="assets/images/sauce.png"
            ), placement="center", time_target=3),
            AssemblyStep(order=8, ingredient=Ingredient(
                id="ing_008", name="Top Bun", type=IngredientType.BREAD,
                image_path="assets/images/top_bun.png"
            ), placement="crown", time_target=3, critical=True)
        ],
        description="Classic beef burger with standard toppings",
        common_errors=[
            "Sauce applied to wrong bun",
            "Cheese not properly melted on patty",
            "Uneven topping distribution"
        ]
    ),
    # Add 4 more universal templates here...
]

# Predefined ingredients library
INGREDIENT_LIBRARY = [
    Ingredient(id="ing_001", name="Bottom Bun", type=IngredientType.BREAD,
               image_path="assets/images/bottom_bun.png"),
    Ingredient(id="ing_002", name="Top Bun", type=IngredientType.BREAD,
               image_path="assets/images/top_bun.png"),
    Ingredient(id="ing_003", name="Beef Patty", type=IngredientType.PROTEIN,
               image_path="assets/images/beef_patty.png"),
    Ingredient(id="ing_004", name="Chicken Patty", type=IngredientType.PROTEIN,
               image_path="assets/images/chicken_patty.png"),
    Ingredient(id="ing_005", name="Cheese Slice", type=IngredientType.CHEESE,
               image_path="assets/images/cheese.png"),
    Ingredient(id="ing_006", name="Lettuce", type=IngredientType.VEGETABLE,
               image_path="assets/images/lettuce.png"),
    Ingredient(id="ing_007", name="Tomato", type=IngredientType.VEGETABLE,
               image_path="assets/images/tomato.png"),
    Ingredient(id="ing_008", name="Onion", type=IngredientType.VEGETABLE,
               image_path="assets/images/onion.png"),
    Ingredient(id="ing_009", name="Pickles", type=IngredientType.VEGETABLE,
               image_path="assets/images/pickles.png"),
    Ingredient(id="ing_010", name="Special Sauce", type=IngredientType.SAUCE,
               image_path="assets/images/sauce.png"),
    Ingredient(id="ing_011", name="Ketchup", type=IngredientType.SAUCE,
               image_path="assets/images/ketchup.png"),
    Ingredient(id="ing_012", name="Mustard", type=IngredientType.SAUCE,
               image_path="assets/images/mustard.png"),
    Ingredient(id="ing_013", name="Mayonnaise", type=IngredientType.SAUCE,
               image_path="assets/images/mayonnaise.png"),
]

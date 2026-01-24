"""
Seed data for flashcards feature
"""

from core.models import Flashcard
from datetime import datetime

# Define SEED_FLASHCARDS list at module level
SEED_FLASHCARDS = [
    Flashcard(
        id='flash_001',
        dish_name='Big Hit',
        dish_name_translation_key='dish_big_hit',
        dish_image='assets/images/dishes/big_hit.png',
        ingredients=[
            'Bottom Bun',
            'Beef Patty',
            'Cheese Slice',
            'Lettuce',
            'Pickles',
            'Onions',
            'Ketchup',
            'Mustard',
            'Top Bun'
        ],
        ingredients_translation_keys=[
            'ingredient_bottom_bun',
            'ingredient_beef_patty',
            'ingredient_cheese_slice',
            'ingredient_lettuce',
            'ingredient_pickles',
            'ingredient_onions',
            'ingredient_ketchup',
            'ingredient_mustard',
            'ingredient_top_bun'
        ],
        difficulty='easy',
        category='sandwiches',
        assembly_tips=[
            'Start with bottom bun',
            'Patty goes in the center',
            'Cheese should melt on patty'
        ],
        created_at=datetime.now(),
        times_reviewed=0,
        mastery_level=0.0
    ),
    Flashcard(
        id='flash_002',
        dish_name='Quarter Pounder',
        dish_name_translation_key='dish_quarter_pounder',
        dish_image='assets/images/dishes/quarter_pounder.png',
        ingredients=[
            'Sesame Bun Bottom',
            'Quarter Pound Patty',
            'Two Cheese Slices',
            'Lettuce',
            'Tomato',
            'Onions',
            'Special Sauce'
        ],
        ingredients_translation_keys=[
            'ingredient_sesame_bun_bottom',
            'ingredient_quarter_patty',
            'ingredient_cheese_slice',
            'ingredient_lettuce',
            'ingredient_tomato',
            'ingredient_onions',
            'ingredient_special_sauce'
        ],
        difficulty='medium',
        category='sandwiches',
        assembly_tips=[
            'Use sesame bun',
            'Two cheese slices required',
            'Apply special sauce generously'
        ],
        created_at=datetime.now(),
        times_reviewed=0,
        mastery_level=0.0
    ),
    Flashcard(
        id='flash_003',
        dish_name='Chicken Sandwich',
        dish_name_translation_key='dish_chicken_sandwich',
        dish_image='assets/images/dishes/chicken_sandwich.png',
        ingredients=[
            'Brioche Bun',
            'Chicken Fillet',
            'Lettuce',
            'Mayonnaise',
            'Pickles'
        ],
        ingredients_translation_keys=[
            'ingredient_brioche_bun',
            'ingredient_chicken_fillet',
            'ingredient_lettuce',
            'ingredient_mayonnaise',
            'ingredient_pickles'
        ],
        difficulty='easy',
        category='sandwiches',
        assembly_tips=[],
        created_at=datetime.now(),
        times_reviewed=0,
        mastery_level=0.0
    ),
    Flashcard(
        id='flash_004',
        dish_name='French Fries',
        dish_name_translation_key='dish_french_fries',
        dish_image='assets/images/dishes/french_fries.png',
        ingredients=[
            'Potatoes',
            'Vegetable Oil',
            'Salt'
        ],
        ingredients_translation_keys=[
            'ingredient_potatoes',
            'ingredient_vegetable_oil',
            'ingredient_salt'
        ],
        difficulty='easy',
        category='sides',
        assembly_tips=[
            'Fry at 175°C for 3 minutes',
            'Shake basket halfway through',
            'Salt immediately after frying'
        ],
        created_at=datetime.now(),
        times_reviewed=0,
        mastery_level=0.0
    ),
    Flashcard(
        id='flash_005',
        dish_name='Apple Pie',
        dish_name_translation_key='dish_apple_pie',
        dish_image='assets/images/dishes/apple_pie.png',
        ingredients=[
            'Pie Crust',
            'Apple Filling',
            'Cinnamon Sugar'
        ],
        ingredients_translation_keys=[
            'ingredient_pie_crust',
            'ingredient_apple_filling',
            'ingredient_cinnamon_sugar'
        ],
        difficulty='medium',
        category='desserts',
        assembly_tips=[
            'Heat for 45 seconds',
            'Check for golden brown color',
            'Serve in pie sleeve'
        ],
        created_at=datetime.now(),
        times_reviewed=0,
        mastery_level=0.0
    )
]


def seed_flashcards():
    """Seed initial flashcards data"""
    from data.database import DatabaseManager

    # Save to database
    db = DatabaseManager()
    db.initialize()

    # Ensure flashcards table exists
    db.create_flashcards_table()

    for flashcard in SEED_FLASHCARDS:
        db.save_flashcard(flashcard)

    print(f"Seeded {len(SEED_FLASHCARDS)} flashcards")


if __name__ == '__main__':
    seed_flashcards()

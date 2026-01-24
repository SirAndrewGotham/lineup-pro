"""
Flashcard widget with flip animation
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import (
    StringProperty, ListProperty, NumericProperty,
    BooleanProperty, ObjectProperty
)
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.clock import Clock

Builder.load_string("""
<FlashcardWidget>:
    size_hint: (None, None)
    size: (300, 400)
    canvas.before:
        Color:
            rgba: 0.95, 0.95, 0.95, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20,]
        Color:
            rgba: 0.2, 0.4, 0.8, 1
        Line:
            rounded_rectangle: [self.pos[0], self.pos[1], self.size[0], self.size[1], 20]
            width: 2
    
    # Front side (dish name)
    BoxLayout:
        id: front_side
        orientation: 'vertical'
        padding: 20
        spacing: 10
        opacity: 1 if not root.is_flipped else 0
        
        Label:
            text: root._('Flashcard')
            font_size: '16sp'
            color: 0.4, 0.4, 0.4, 1
            size_hint_y: 0.1
        
        Label:
            id: dish_name_label
            text: root.dish_name
            font_size: '28sp'
            bold: True
            halign: 'center'
            valign: 'middle'
            text_size: self.width, None
            size_hint_y: 0.7
            color: 0.2, 0.2, 0.2, 1
        
        Button:
            text: root._('Flip to see ingredients')
            size_hint_y: 0.2
            background_color: 0.2, 0.6, 0.8, 1
            on_press: root.flip()
    
    # Back side (ingredients)
    BoxLayout:
        id: back_side
        orientation: 'vertical'
        padding: 20
        spacing: 10
        opacity: 0 if not root.is_flipped else 1
        
        Label:
            text: root.dish_name
            font_size: '24sp'
            bold: True
            halign: 'center'
            size_hint_y: 0.15
            color: 0.2, 0.2, 0.2, 1
        
        ScrollView:
            size_hint_y: 0.7
            
            GridLayout:
                id: ingredients_grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: 5
                padding: 10
        
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.15
            spacing: 10
            padding: [0, 5, 0, 0]
            
            Button:
                text: root._('Got it!')
                background_color: 0.1, 0.8, 0.3, 1
                on_press: root.mark_mastered(True)
            
            Button:
                text: root._('Need practice')
                background_color: 0.9, 0.6, 0.1, 1
                on_press: root.mark_mastered(False)
            
            Button:
                text: root._('Flip back')
                background_color: 0.4, 0.4, 0.4, 1
                on_press: root.flip()
""")


class FlashcardWidget(FloatLayout):
    """Interactive flashcard with flip animation"""

    # Properties
    flashcard = ObjectProperty(None)
    dish_name = StringProperty('')
    ingredients = ListProperty([])
    is_flipped = BooleanProperty(False)
    flip_duration = NumericProperty(0.3)

    def __init__(self, flashcard=None, **kwargs):
        super().__init__(**kwargs)
        if flashcard:
            self.set_flashcard(flashcard)

    def set_flashcard(self, flashcard):
        """Set the flashcard data"""
        self.flashcard = flashcard
        self.dish_name = self._(flashcard.dish_name_translation_key)
        self.ingredients = [
            self._(key) for key in flashcard.ingredients_translation_keys
        ]

        # Update ingredients display
        if hasattr(self, 'ids'):
            self.update_ingredients_display()

    def update_ingredients_display(self):
        """Update the ingredients list in the UI"""
        ingredients_grid = self.ids.ingredients_grid
        ingredients_grid.clear_widgets()

        for ingredient in self.ingredients:
            from kivy.uix.label import Label
            label = Label(
                text=f"• {ingredient}",
                font_size='16sp',
                halign='left',
                size_hint_y=None,
                height=30,
                text_size=(self.width - 40, None)
            )
            ingredients_grid.add_widget(label)

        # Set proper height for scroll
        ingredients_grid.height = len(self.ingredients) * 35

    def flip(self):
        """Animate card flip"""
        if self.is_flipped:
            # Flip to front
            anim = Animation(opacity=0, duration=self.flip_duration/2)
            anim += Animation(opacity=1, duration=self.flip_duration/2)
            self.is_flipped = False
        else:
            # Flip to back
            anim = Animation(opacity=0, duration=self.flip_duration/2)
            anim += Animation(opacity=1, duration=self.flip_duration/2)
            self.is_flipped = True

        anim.start(self)

    def mark_mastered(self, mastered):
        """Mark flashcard as mastered or needs practice"""
        if self.flashcard:
            from data.database import DatabaseManager
            db = DatabaseManager()
            db.update_flashcard_progress(self.flashcard.id, mastered)

            # Show feedback
            if mastered:
                print(f"Marked {self.flashcard.dish_name} as mastered")
            else:
                print(f"{self.flashcard.dish_name} needs more practice")

    def _(self, text):
        """Translation shortcut"""
        # Use your existing translation system
        from utils.translation import get_translation
        current_lang = 'en'  # You should get this from your config
        return get_translation(text, current_lang)


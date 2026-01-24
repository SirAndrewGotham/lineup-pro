"""
Flashcards screen for dish memorization
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock

from utils.translation_mixin import TranslatableLabel, TranslatableButton
from ui.widgets.flashcard_widget import FlashcardWidget
from data.database import DatabaseManager


class FlashcardsScreen(Screen):  # REMOVED: , TranslatableMixin
    """Screen for flashcards training"""

    current_category = StringProperty('all')
    current_difficulty = StringProperty('all')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'flashcards'

        # Initialize database properly
        self.db = DatabaseManager()
        self.db.initialize()

        self.current_flashcards = []
        self.current_index = 0

        # Setup UI after a short delay
        Clock.schedule_once(lambda dt: self.setup_ui(), 0.1)

    def setup_ui(self):
        """Setup the screen UI"""
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)

        # Back button
        back_btn = Button(
            text='←',
            size_hint_x=0.1,
            background_color=(0.4, 0.4, 0.4, 1)
        )
        back_btn.bind(on_press=self.go_back)

        # Title
        title = Label(
            text='Flashcards',
            font_size='24sp',
            bold=True,
            size_hint_x=0.8
        )

        # Stats
        stats_btn = Button(
            text='📊',
            size_hint_x=0.1,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        stats_btn.bind(on_press=self.show_stats)

        header.add_widget(back_btn)
        header.add_widget(title)
        header.add_widget(stats_btn)

        # Filters
        filters_layout = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=5)

        # Category filter
        categories = ['all', 'sandwiches', 'sides', 'desserts', 'breakfast']
        for category in categories:
            btn = Button(
                text=category.capitalize(),
                size_hint_x=1/len(categories),
                background_color=(0.3, 0.5, 0.7, 1) if category == 'all' else (0.5, 0.5, 0.5, 1)
            )
            btn.bind(on_press=lambda instance, cat=category: self.filter_by_category(cat))
            filters_layout.add_widget(btn)

        # Difficulty filter
        difficulty_layout = BoxLayout(orientation='horizontal', size_hint_y=0.08, spacing=5)
        difficulties = ['all', 'easy', 'medium', 'hard']
        for diff in difficulties:
            btn = Button(
                text=diff.capitalize(),
                size_hint_x=1/len(difficulties),
                background_color=(0.3, 0.7, 0.5, 1) if diff == 'all' else (0.5, 0.5, 0.5, 1)
            )
            btn.bind(on_press=lambda instance, d=diff: self.filter_by_difficulty(d))
            difficulty_layout.add_widget(btn)

        # Flashcard display area
        self.card_container = BoxLayout(
            orientation='vertical',
            size_hint_y=0.64,
            padding=20
        )

        # Navigation
        nav_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=20)

        prev_btn = Button(
            text='Previous',
            background_color=(0.4, 0.4, 0.4, 1)
        )
        prev_btn.bind(on_press=self.previous_card)

        self.progress_label = Label(
            text='0/0',
            font_size='18sp'
        )

        next_btn = Button(
            text='Next',
            background_color=(0.2, 0.6, 0.8, 1)
        )
        next_btn.bind(on_press=self.next_card)

        nav_layout.add_widget(prev_btn)
        nav_layout.add_widget(self.progress_label)
        nav_layout.add_widget(next_btn)

        # Assemble everything
        main_layout.add_widget(header)
        main_layout.add_widget(filters_layout)
        main_layout.add_widget(difficulty_layout)
        main_layout.add_widget(self.card_container)
        main_layout.add_widget(nav_layout)

        self.add_widget(main_layout)

        # Load initial flashcards
        self.load_flashcards()

    # def load_flashcards(self):
    #     """Load flashcards based on current filters"""
    #     # Build filters
    #     category = None if self.current_category == 'all' else self.current_category
    #     difficulty = None if self.current_difficulty == 'all' else self.current_difficulty
    #
    #     self.current_flashcards = self.db.get_flashcards(
    #         category=category,
    #         difficulty=difficulty
    #     )
    #     self.current_index = 0
    #
    #     self.display_current_card()
    #     self.update_progress()

    def load_flashcards(self):
        """Load flashcards based on current filters"""
        # TEMPORARY: Return empty list until database is fixed
        self.current_flashcards = []
        self.current_index = 0
        self.display_current_card()
        self.update_progress()

        # Comment out the original code:
        # # Build filters
        # category = None if self.current_category == 'all' else self.current_category
        # difficulty = None if self.current_difficulty == 'all' else self.current_difficulty
        #
        # self.current_flashcards = self.db.get_flashcards(
        #     category=category,
        #     difficulty=difficulty
        # )
        # self.current_index = 0
        #
        # self.display_current_card()
        # self.update_progress()






    def display_current_card(self):
        """Display the current flashcard"""
        self.card_container.clear_widgets()

        if not self.current_flashcards:
            # No cards message
            label = Label(
                text='No flashcards found for selected filters',
                font_size='20sp',
                color=(0.5, 0.5, 0.5, 1)
            )
            self.card_container.add_widget(label)
            return

        if self.current_index < len(self.current_flashcards):
            flashcard = self.current_flashcards[self.current_index]
            card_widget = FlashcardWidget(flashcard=flashcard)
            self.card_container.add_widget(card_widget)

    def update_progress(self):
        """Update progress label"""
        total = len(self.current_flashcards)
        current = self.current_index + 1 if total > 0 else 0
        self.progress_label.text = f'{current}/{total}'

    def next_card(self, instance):
        """Show next card"""
        if self.current_flashcards:
            self.current_index = (self.current_index + 1) % len(self.current_flashcards)
            self.display_current_card()
            self.update_progress()

    def previous_card(self, instance):
        """Show previous card"""
        if self.current_flashcards:
            self.current_index = (self.current_index - 1) % len(self.current_flashcards)
            self.display_current_card()
            self.update_progress()

    def filter_by_category(self, category):
        """Filter flashcards by category"""
        self.current_category = category
        self.load_flashcards()

        # Update button colors
        for child in self.children[0].children[3].children:  # filters_layout
            if child.text.lower() == category:
                child.background_color = (0.3, 0.5, 0.7, 1)
            else:
                child.background_color = (0.5, 0.5, 0.5, 1)

    def filter_by_difficulty(self, difficulty):
        """Filter flashcards by difficulty"""
        self.current_difficulty = difficulty
        self.load_flashcards()

        # Update button colors
        for child in self.children[0].children[2].children:  # difficulty_layout
            if child.text.lower() == difficulty:
                child.background_color = (0.3, 0.7, 0.5, 1)
            else:
                child.background_color = (0.5, 0.5, 0.5, 1)

    def show_stats(self, instance):
        """Show flashcards statistics"""
        # This would show mastery statistics
        # For now, just print to console
        flashcards = self.db.get_flashcards()
        mastered = sum(1 for f in flashcards if f.mastery_level > 0.7)

        print(f"Flashcards Statistics:")
        print(f"Total: {len(flashcards)}")
        print(f"Mastered: {mastered} ({mastered/len(flashcards)*100:.1f}%)")
        print(f"Average mastery: {sum(f.mastery_level for f in flashcards)/len(flashcards)*100:.1f}%")

    def go_back(self, instance):
        """Return to main menu"""
        self.manager.current = 'main'

    def on_enter(self, *args):
        """Update translations when screen becomes active"""
        self.update_translations()

    def update_translations(self):
        """Update all text elements with translations"""
        from main import LineUpPro
        app = LineUpPro.get_running_app()

        if app and hasattr(app, 'translation_manager'):
            # Update title if it exists
            for child in self.walk():
                if hasattr(child, 'translation_key') and child.translation_key:
                    translated_text = app.translation_manager.translate(child.translation_key)
                    if hasattr(child, 'text'):
                        child.text = translated_text

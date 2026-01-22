"""
Training Screen - Guided training mode
"""

from kivy.uix.screenmanager import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from ui.widgets.assembly_area import AssemblyArea
from utils.translation_mixin import TranslatableLabel, TranslatableButton

class TrainingScreen(Screen):
    """Guided training mode with step-by-step instructions"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'training'
        self.current_step = 0
        self.total_steps = 0
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the training screen UI"""
        layout = MDBoxLayout(orientation='vertical')
        
        # Header
        header = MDBoxLayout(size_hint=(1, 0.1))
        self.title_label = TranslatableLabel(
            translation_key='training_title',
            font_style='H5',
            halign='center'
        )
        header.add_widget(self.title_label)
        layout.add_widget(header)
        
        # Assembly area (70% of screen)
        self.assembly_area = AssemblyArea()
        layout.add_widget(self.assembly_area)
        
        # Instructions panel (20% of screen)
        instructions_panel = MDBoxLayout(
            orientation='vertical',
            size_hint=(1, 0.2),
            padding=10,
            spacing=10
        )
        
        self.step_label = TranslatableLabel(
            translation_key='step_label',
            font_style='H6'
        )
        instructions_panel.add_widget(self.step_label)
        
        self.instruction_label = MDLabel(
            text='Drag the ingredient to the correct position',
            theme_text_color='Secondary'
        )
        instructions_panel.add_widget(self.instruction_label)
        
        # Navigation buttons
        nav_layout = MDBoxLayout(size_hint=(1, 0.3), spacing=10)
        
        self.prev_button = TranslatableButton(
            translation_key='previous_button',
            size_hint=(0.3, 1),
            disabled=True
        )
        self.prev_button.bind(on_release=self.previous_step)
        
        self.next_button = TranslatableButton(
            translation_key='next_button',
            size_hint=(0.3, 1)
        )
        self.next_button.bind(on_release=self.next_step)
        
        nav_layout.add_widget(self.prev_button)
        nav_layout.add_widget(MDLabel())  # Spacer
        nav_layout.add_widget(self.next_button)
        instructions_panel.add_widget(nav_layout)
        
        layout.add_widget(instructions_panel)
        
        self.add_widget(layout)
    
    def load_training_module(self, module_id):
        """Load a specific training module"""
        # TODO: Implement module loading
        print(f"Loading training module: {module_id}")
        self.current_step = 0
        # self.total_steps = len(module.ingredients)
        self.update_step_display()
    
    def previous_step(self, instance):
        """Go to previous step"""
        if self.current_step > 0:
            self.current_step -= 1
            self.update_step_display()
    
    def next_step(self, instance):
        """Go to next step"""
        if self.current_step < self.total_steps - 1:
            self.current_step += 1
            self.update_step_display()
        else:
            # Training complete
            self.manager.current = 'main'
    
    def update_step_display(self):
        """Update the step display and instructions"""
        self.step_label.text = f"Step {self.current_step + 1} of {self.total_steps}"
        
        # Enable/disable navigation buttons
        self.prev_button.disabled = self.current_step == 0
        self.next_button.disabled = self.current_step == self.total_steps - 1
        
        # TODO: Update instruction text based on current step
        # TODO: Highlight current ingredient in assembly area

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu

from utils.translation_mixin import TranslatableMixin

class TranslatableLabel(MDLabel, TranslatableMixin):
    """Label with translation support"""
    pass

class TranslatableButton(MDRaisedButton, TranslatableMixin):
    """Button with translation support"""
    pass

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        # Header
        header = BoxLayout(orientation='horizontal', size_hint_y=0.15)
        logo = Image(source='assets/images/logo.png', size_hint_x=0.3)
        title = TranslatableLabel(
            translation_key='app.title',
            halign='center',
            font_style='H4',
            size_hint_x=0.7
        )
        subtitle = TranslatableLabel(
            translation_key='app.subtitle',
            halign='center',
            font_style='Subtitle1',
            size_hint_x=0.7
        )

        title_layout = BoxLayout(orientation='vertical')
        title_layout.add_widget(title)
        title_layout.add_widget(subtitle)

        header.add_widget(logo)
        header.add_widget(title_layout)

        # Training modes grid
        modes_grid = GridLayout(cols=1, spacing=15, size_hint_y=0.6)

        modes = [
            ('guided_mode', 'training', 'assets/images/guided.png'),
            ('practice_mode', 'practice', 'assets/images/practice.png'),
            ('exam_mode', 'exam', 'assets/images/exam.png'),
            ('progress', 'progress', 'assets/images/progress.png')
        ]

        for translation_key, screen_name, icon in modes:
            card = MDCard(
                orientation='vertical',
                padding=15,
                size_hint_y=None,
                height=100
            )
            card.add_widget(Image(source=icon, size_hint_y=0.6))

            label = TranslatableLabel(
                translation_key=f'main_menu.{translation_key}',
                halign='center',
                font_style='H6'
            )
            card.add_widget(label)
            card.bind(on_press=lambda x, s=screen_name: self.switch_screen(s))
            modes_grid.add_widget(card)

        # Footer with settings and help
        footer = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=10)

        settings_btn = TranslatableButton(
            translation_key='main_menu.settings',
            size_hint_x=0.5
        )
        settings_btn.bind(on_press=self.open_settings)

        help_btn = TranslatableButton(
            translation_key='main_menu.help',
            size_hint_x=0.5
        )
        help_btn.bind(on_press=self.open_help)

        footer.add_widget(settings_btn)
        footer.add_widget(help_btn)

        layout.add_widget(header)
        layout.add_widget(modes_grid)
        layout.add_widget(footer)
        self.add_widget(layout)

    def switch_screen(self, screen_name):
        self.manager.current = screen_name

    def open_settings(self, instance):
        # Switch to settings screen or open dialog
        # For now, we'll switch to a settings screen
        from ui.screens.settings_screen import SettingsScreen
        if 'settings' not in self.manager.screen_names:
            settings_screen = SettingsScreen(name='settings')
            settings_screen.app = self.app
            self.manager.add_widget(settings_screen)
        self.manager.current = 'settings'

    def open_help(self, instance):
        # Open help dialog
        from utils.translation import translation_manager
        text = translation_manager.translate('app.title') + "\n\n" + \
               translation_manager.translate('app.subtitle')

        dialog = MDDialog(
            title=translation_manager.translate('main_menu.help'),
            text=text,
            size_hint=(0.8, 0.4)
        )
        dialog.open()

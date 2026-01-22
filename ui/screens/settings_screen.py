from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp

from utils.translation_mixin import TranslatableLabel, TranslatableButton

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self):
        # Main layout
        main_layout = BoxLayout(orientation='vertical')

        # Header
        header = BoxLayout(size_hint_y=0.1, padding=[10, 10, 10, 0])
        back_btn = TranslatableButton(
            translation_key='training.back',
            size_hint_x=0.3,
            on_press=lambda x: self.go_back()
        )
        title = TranslatableLabel(
            translation_key='settings.title',
            halign='center',
            font_style='H4',
            size_hint_x=0.7
        )
        header.add_widget(back_btn)
        header.add_widget(title)

        # Scrollable content
        scroll = ScrollView()
        content = BoxLayout(orientation='vertical', spacing=20, padding=20, size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))

        # Language selection
        lang_section = self.create_language_section()
        content.add_widget(lang_section)

        # Theme selection
        theme_section = self.create_theme_section()
        content.add_widget(theme_section)

        # Training settings
        training_section = self.create_training_section()
        content.add_widget(training_section)

        # Buttons
        buttons_section = self.create_buttons_section()
        content.add_widget(buttons_section)

        scroll.add_widget(content)

        main_layout.add_widget(header)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)

    def create_language_section(self):
        """Create language selection section"""
        from utils.translation import translation_manager

        section = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        section.add_widget(TranslatableLabel(
            translation_key='settings.language',
            font_style='H6',
            size_hint_y=None,
            height=dp(30)
        ))

        # Get current language
        current_lang = self.app.config.get('ui.language', 'ru')
        lang_options = self.app.config.get_language_options()

        # Create dropdown button
        lang_btn = TranslatableButton(
            text=lang_options.get(current_lang, 'Русский'),
            size_hint_y=None,
            height=dp(40),
            on_press=self.open_language_menu
        )
        lang_btn.lang_options = lang_options
        self.lang_button = lang_btn

        section.add_widget(lang_btn)
        return section

    def create_theme_section(self):
        """Create theme selection section"""
        section = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        section.add_widget(TranslatableLabel(
            translation_key='settings.theme',
            font_style='H6',
            size_hint_y=None,
            height=dp(30)
        ))

        # Theme buttons
        theme_box = BoxLayout(spacing=10, size_hint_y=None, height=dp(40))

        light_btn = TranslatableButton(
            translation_key='settings.theme_options.light',
            size_hint_x=0.5,
            on_press=lambda x: self.set_theme('light')
        )

        dark_btn = TranslatableButton(
            translation_key='settings.theme_options.dark',
            size_hint_x=0.5,
            on_press=lambda x: self.set_theme('dark')
        )

        theme_box.add_widget(light_btn)
        theme_box.add_widget(dark_btn)
        section.add_widget(theme_box)
        return section

    def create_training_section(self):
        """Create training settings section"""
        section = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        section.add_widget(TranslatableLabel(
            translation_key='training.settings_title',
            font_style='H6',
            size_hint_y=None,
            height=dp(30)
        ))

        # Create checkboxes for various settings
        settings = [
            ('sounds', 'settings.sounds'),
            ('haptic_feedback', 'settings.haptic_feedback'),
            ('voice_guidance', 'settings.voice_guidance'),
            ('show_timer', 'settings.show_timer')
        ]

        for setting_key, translation_key in settings:
            setting_row = self.create_setting_row(setting_key, translation_key)
            section.add_widget(setting_row)

        return section

    def create_setting_row(self, setting_key, translation_key):
        """Create a single setting row with checkbox"""
        row = BoxLayout(size_hint_y=None, height=dp(40))

        label = TranslatableLabel(
            translation_key=translation_key,
            size_hint_x=0.7
        )

        checkbox = MDCheckbox(
            size_hint_x=0.3,
            active=self.app.config.get(f'training.{setting_key}', True)
        )
        checkbox.setting_key = setting_key
        checkbox.bind(active=self.on_setting_changed)

        row.add_widget(label)
        row.add_widget(checkbox)
        return row

    def create_buttons_section(self):
        """Create action buttons section"""
        section = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None, height=dp(100))

        save_btn = TranslatableButton(
            translation_key='settings.save',
            on_press=self.save_settings
        )

        reset_btn = TranslatableButton(
            translation_key='settings.reset',
            on_press=self.reset_settings
        )

        section.add_widget(save_btn)
        section.add_widget(reset_btn)
        return section

    def open_language_menu(self, instance):
        """Open language selection menu"""
        menu_items = []

        for lang_code, lang_name in self.lang_button.lang_options.items():
            item = {
                "text": lang_name,
                "viewclass": "OneLineListItem",
                "height": dp(48),
                "on_release": lambda x=lang_code: self.set_language(x)
            }
            menu_items.append(item)

        self.language_menu = MDDropdownMenu(
            caller=instance,
            items=menu_items,
            width_mult=4
        )
        self.language_menu.open()

    def set_language(self, lang_code):
        """Set application language"""
        self.app.config.set('ui.language', lang_code)
        self.lang_button.text = self.lang_button.lang_options.get(lang_code, lang_code)

        # Show confirmation
        from utils.translation import translation_manager
        message = translation_manager.translate('settings.language_changed')

        dialog = MDDialog(
            title=translation_manager.translate('settings.title'),
            text=message,
            buttons=[
                MDFlatButton(
                    text=translation_manager.translate('training.back'),
                    on_press=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

        if self.language_menu:
            self.language_menu.dismiss()

    def set_theme(self, theme):
        """Set application theme"""
        self.app.config.set('ui.theme', theme)
        # TODO: Implement theme switching

    def on_setting_changed(self, checkbox, value):
        """Handle setting checkbox changes"""
        setting_key = checkbox.setting_key
        self.app.config.set(f'training.{setting_key}', value)

    def save_settings(self, instance):
        """Save all settings"""
        self.app.config.save_config()

        from utils.translation import translation_manager
        dialog = MDDialog(
            title=translation_manager.translate('settings.title'),
            text=translation_manager.translate('settings.saved'),
            buttons=[
                MDFlatButton(
                    text=translation_manager.translate('training.back'),
                    on_press=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def reset_settings(self, instance):
        """Reset settings to defaults"""
        from utils.translation import translation_manager

        dialog = MDDialog(
            title=translation_manager.translate('settings.title'),
            text=translation_manager.translate('settings.reset_confirm'),
            buttons=[
                MDFlatButton(
                    text=translation_manager.translate('settings.cancel'),
                    on_press=lambda x: dialog.dismiss()
                ),
                MDFlatButton(
                    text=translation_manager.translate('settings.reset'),
                    on_press=lambda x: self.confirm_reset(dialog)
                )
            ]
        )
        dialog.open()

    def confirm_reset(self, dialog):
        """Confirm and reset settings"""
        self.app.config.reset_to_defaults()
        dialog.dismiss()

        from utils.translation import translation_manager
        success_dialog = MDDialog(
            title=translation_manager.translate('settings.title'),
            text=translation_manager.translate('settings.reset_complete'),
            buttons=[
                MDFlatButton(
                    text=translation_manager.translate('training.back'),
                    on_press=lambda x: success_dialog.dismiss()
                )
            ]
        )
        success_dialog.open()

    def go_back(self):
        """Return to main screen"""
        self.manager.current = 'main'

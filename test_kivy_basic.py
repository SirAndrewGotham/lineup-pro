# test_kivy_basic.py
import kivy
kivy.require('2.3.0')

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

class TestApp(App):
    def build(self):
        # Set window size (optional)
        Window.size = (400, 300)

        # Create layout
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Add test buttons
        btn1 = Button(text='Test Button 1', size_hint=(1, 0.2))
        btn2 = Button(text='Test Button 2', size_hint=(1, 0.2))
        btn3 = Button(text='Exit', size_hint=(1, 0.2))
        btn3.bind(on_press=lambda x: App.get_running_app().stop())

        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(btn3)

        return layout

if __name__ == '__main__':
    TestApp().run()

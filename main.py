from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label

class AppUI(App):

    def build(self):

        layout = BoxLayout(orientation='vertical')

        self.text = TextInput(hint_text="Enter text")

        self.label = Label(text="Ready")

        btn = Button(text="Click Test")

        btn.bind(on_press=self.test)

        layout.add_widget(self.text)
        layout.add_widget(btn)
        layout.add_widget(self.label)

        return layout

    def test(self, instance):
        self.label.text = "App Working ✔"

AppUI().run()

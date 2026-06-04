from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label

from jnius import autoclass
import os

# Android TTS classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
Locale = autoclass('java.util.Locale')


class TTSApp(App):

    def build(self):

        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        self.text = TextInput(hint_text="Enter text", multiline=True)

        self.language = Spinner(
            text="English",
            values=("English", "Hindi")
        )

        self.speak_btn = Button(text="Speak Text")

        self.status = Label(text="Ready")

        self.speak_btn.bind(on_press=self.speak_text)

        self.layout.add_widget(self.text)
        self.layout.add_widget(self.language)
        self.layout.add_widget(self.speak_btn)
        self.layout.add_widget(self.status)

        return self.layout

    def speak_text(self, instance):

        try:
            activity = PythonActivity.mActivity

            tts = TextToSpeech(activity, None)

            text = self.text.text

            if self.language.text == "Hindi":
                tts.setLanguage(Locale("hi", "IN"))
            else:
                tts.setLanguage(Locale.US)

            tts.speak(text, TextToSpeech.QUEUE_FLUSH, None, None)

            self.status.text = "Speaking..."

        except Exception as e:
            self.status.text = str(e)


TTSApp().run()

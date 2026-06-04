from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label

from jnius import autoclass
import threading


# Android TTS classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
Locale = autoclass('java.util.Locale')


class TTSApp(App):

    def build(self):

        self.layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        self.text = TextInput(
            hint_text="Enter text here",
            multiline=True,
            size_hint=(1, 0.5)
        )

        self.voice = Spinner(
            text="English Female",
            values=("English Female", "English Male")
        )

        self.wpm = TextInput(
            text="80",
            hint_text="Speech Speed (30-150)",
            multiline=False
        )

        self.generate_btn = Button(text="Speak")
        self.stop_btn = Button(text="Stop")

        self.status = Label(text="Ready")

        self.generate_btn.bind(on_press=self.start_speaking)
        self.stop_btn.bind(on_press=self.stop_speaking)

        self.layout.add_widget(self.text)
        self.layout.add_widget(self.voice)
        self.layout.add_widget(self.wpm)
        self.layout.add_widget(self.generate_btn)
        self.layout.add_widget(self.stop_btn)
        self.layout.add_widget(self.status)

        # Init Android TTS
        self.init_tts()

        return self.layout

    def init_tts(self):
        activity = PythonActivity.mActivity

        self.tts = TextToSpeech(activity, None)

        self.tts.setLanguage(Locale.US)

        self.status.text = "TTS Initialized"

    # Convert WPM to speech rate
    def get_rate(self, wpm):
        # Android TTS rate: 0.5 to 2.0
        if wpm < 30:
            wpm = 30
        if wpm > 150:
            wpm = 150

        return wpm / 80.0

    def start_speaking(self, instance):
        threading.Thread(target=self.speak, daemon=True).start()

    def speak(self):

        text = self.text.text.strip()

        if not text:
            self.status.text = "Enter text first"
            return

        try:
            wpm = int(self.wpm.text)
        except:
            self.status.text = "Invalid WPM"
            return

        rate = self.get_rate(wpm)

        self.status.text = "Speaking..."

        self.tts.setSpeechRate(rate)
        self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, None, None)

        self.status.text = "Done"

    def stop_speaking(self, instance):
        try:
            self.tts.stop()
            self.status.text = "Stopped"
        except Exception as e:
            self.status.text = str(e)


TTSApp().run()

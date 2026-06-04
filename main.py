from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label

import asyncio
import edge_tts
import threading
from datetime import datetime
import pygame

pygame.mixer.init()

voice_map = {
    "English Male": "en-US-GuyNeural",
    "English Female": "en-US-AriaNeural",
    "Hindi Male": "hi-IN-MadhurNeural",
    "Hindi Female": "hi-IN-SwaraNeural"
}


class TTSApp(App):

    def build(self):

        layout = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=10
        )

        self.text = TextInput(
            hint_text="Enter text here",
            multiline=True,
            size_hint=(1, 0.5)
        )

        self.voice = Spinner(
            text="English Male",
            values=(
                "English Male",
                "English Female",
                "Hindi Male",
                "Hindi Female"
            )
        )

        self.wpm = TextInput(
            text="80",
            multiline=False,
            hint_text="Enter WPM (30-150)"
        )

        self.generate_btn = Button(
            text="Generate MP3"
        )

        self.play_btn = Button(
            text="▶ Play"
        )

        self.stop_btn = Button(
            text="⏹ Stop"
        )

        self.status = Label(
            text="Ready"
        )

        self.generate_btn.bind(
            on_press=self.start_generation
        )

        self.play_btn.bind(
            on_press=self.play_audio
        )

        self.stop_btn.bind(
            on_press=self.stop_audio
        )

        layout.add_widget(self.text)
        layout.add_widget(self.voice)
        layout.add_widget(self.wpm)
        layout.add_widget(self.generate_btn)
        layout.add_widget(self.play_btn)
        layout.add_widget(self.stop_btn)
        layout.add_widget(self.status)

        return layout

    def start_generation(self, instance):

        threading.Thread(
            target=self.generate_audio,
            daemon=True
        ).start()

    def generate_audio(self):

        try:

            text = self.text.text.strip()

            if not text:
                self.status.text = "Enter some text"
                return

            try:
                wpm = int(self.wpm.text)

                if wpm < 30:
                    wpm = 30

                if wpm > 150:
                    wpm = 150

            except:
                self.status.text = "Enter valid WPM"
                return

            rate_percent = int((wpm - 80) * 1.5)

            if rate_percent >= 0:
                rate = f"+{rate_percent}%"
            else:
                rate = f"{rate_percent}%"

            self.status.text = "Generating..."

            filename = (
                "tts_" +
                datetime.now().strftime("%Y%m%d_%H%M%S")
                + ".mp3"
            )

            path = f"/storage/emulated/0/{filename}"

            self.last_audio = path

            async def create():

                communicate = edge_tts.Communicate(
                    text=text,
                    voice=voice_map[self.voice.text],
                    rate=rate
                )

                await communicate.save(path)

            asyncio.run(create())

            self.status.text = (
                f"Saved Successfully\n{filename}"
            )

        except Exception as e:
            self.status.text = str(e)

    def play_audio(self, instance):

        try:

            if not hasattr(self, "last_audio"):
                self.status.text = "No audio generated"
                return

            pygame.mixer.music.load(
                self.last_audio
            )

            pygame.mixer.music.play()

            self.status.text = "Playing Audio"

        except Exception as e:
            self.status.text = str(e)

    def stop_audio(self, instance):

        try:

            pygame.mixer.music.stop()
            self.status.text = "Stopped"

        except Exception as e:
            self.status.text = str(e)


TTSApp().run()
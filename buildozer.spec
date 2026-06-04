[app]

title = TTS App
package.name = ttsapp
package.domain = org.example

source.dir = .
source.include_exts = py

version = 1.0

requirements = python3,kivy,pyjnius

orientation = portrait
fullscreen = 0

# Android permissions
android.permissions = INTERNET

# (important for modern builds)
android.api = 33
android.minapi = 21

# recommended for stability
log_level = 2

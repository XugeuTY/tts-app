[app]

title = TTS App
package.name = ttsapp
package.domain = org.example

source.dir = .
source.include_exts = py

version = 1.0

# ✅ ONLY Android-compatible requirements
requirements = python3,kivy,pyjnius

orientation = portrait
fullscreen = 0

# Android permissions (needed for TTS engine access)
android.permissions = INTERNET

# Stable Android build settings
android.api = 33
android.minapi = 21

# Optional but recommended
log_level = 2

# Avoid build issues
android.ndk = 25b

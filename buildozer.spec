[app]

title = TTS App
package.name = ttsapp
package.domain = org.example

source.dir = .
source.include_exts = py

version = 1.0

# IMPORTANT: minimal stable requirements
requirements = python3,kivy

orientation = portrait
fullscreen = 0

# Android permissions
android.permissions = INTERNET

# Stable build settings
android.api = 33
android.minapi = 21
android.ndk = 25b

# Use SDL2 backend (IMPORTANT for Kivy APK)
android.bootstrap = sdl2

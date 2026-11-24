[app]
title = Battle Space
package.name = battlespace
package.domain = org.battlespace
source.dir = .
source.include_exts = py,png,jpg,mp3,wav,ogg,json
version = 1.0
requirements = python3,pygame
orientation = landscape
fullscreen = 1
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1

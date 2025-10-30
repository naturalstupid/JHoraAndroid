[app]
title = JHoraApp
icon = assets/app_icon.png
package.domain = org.oat
package.name = jhora
source.dir = .
source.include_patterns = "*.py","*.so","*.se1","*.txt","*.csv","*.ttf","*.png","*.jpg","*.gif","*.json","libs/*", "logs/*","assets/*","jhora/**"
source.include_exts = py,txt,csv,ttf,png,jpg,gif,json,se1,so
version = 2.0
requirements = python3==3.11.0,kivy,ratelim,decorator,geocoder,geopy,python_dateutil,pytz,requests,setuptools,timezonefinder,importlib_resources,numpy
orientation = portrait
fullscreen = 1
android.strip = false

[buildozer]
log_level = 2
warn_on_root = 0

[android]
android.debug = 1
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a
android.permissions = INTERNET, ACCESS_COARSE_LOCATION, ACCESS_FINE_LOCATION


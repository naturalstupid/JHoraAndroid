JHoraAndroid V0.8
=================
![JHoraAndroid](./assets/app_icon.png)

Android App based on [JHora Python Package](https://github.com/naturalstupid/PyJHora/)


Installation Requirements
-------------------------
**You can directly download the Android APK file from the `apks` folder and install it in your android devices.**

If you want to use this app in Windows, then you will have to install python and the below dependent libraries. Then run the `main.py`

This version includes required `jhora` modules. In future versions, you may have to install `PyJHora` using

`pip install PyJHora`

Requirements
-------------

Python interface to Swiss ephemeris and Kivy.

```
	pip install pyswisseph	# OR apt-get install pyswisseph
	pip install kivy       # OR apt-get install kivy
```
There are other dependencies listed in the file `requirements.txt` should be installed using `pip` if not already available.

How to use the App
------------------------------
Enter Name (optional)

Enter Date in the format (YYYY,MM,DD) e.g. 2025,08,07

Enter Time in the format (HH:MM:SS) e.g. 13:04:07

Enter Place with country name (e.g. Chennai, IN)

You can try entering partial string (as many as possible) of the city name. The app will check available city names from the csv data file and show the first 10 names. To get to the precise city name, you may have to try possible names and with correct spelling. (E.g. Thanjavur instead of Tanjore)
If the city is found in the csv data file, you can select it from pop up list. In this case latitude, longitude and timezone hours will automatically filled.

If you are unable to find the city you should enter place, latitude, longitude and time zone manually.
If you want to be precise, enter the lat/long of the exact place (e.g. hospital)
You can use google to find the latitude, longitude, time zone of the place

**Note: Known issue on UI **: As you type in the input fields, Kivy does not seem to keep the keyboard on. To keep the keyboard on, press onto the input field with left hand finger and type with right hand. Once you finish typing, press Enter in the keyboard.

Click **Calculate** to see the results

There will be following tabs of information available in the app.

**Input**, **Panchangam**, **Horoscope**, **Dhasa**, **Options**

You can switch each tab by clicking on the tab name. In each tab, you can click << or >> buttons to see more detailed information for the tab. For example you can scroll through to see Rasi, Hora, ..., D144 charts. Similarly you can scroll through various dhasas, strengths.

** Note: In Android, only English is available.** Glyph rendering requires android compilation of several dependent C-libraries. Other language support for android will be added in future versions. Where as glyph rendering works on Windows and supports Tamil, Kannada, Telugu, Malayalam and Hindi.

**Options Tab** Here you can select language (Windows only), Chart type (South, North, East), Ayanamsa option, Calculation methods for each chart type and whether startup splash is required.

License
-------
See LICENSE file.

Contact
-------
https://github.com/naturalstupid/


#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright (C) Open Astro Technologies, USA.
# Modified by Sundar Sundaresan, USA. carnaticmusicguru2015@comcast.net
# Downloaded from https://github.com/naturalstupid/PyJHora

# This file is part of the "PyJHora" Python library
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from kivy.config import Config
# Disable mouse click even in android - otherwise each button click is registered twice
Config.set('input', 'mtdev_%(name)s', '')
# Disable touch visualization
Config.set('input', 'mouse', 'mouse,disable_multitouch')
# Alternatively, disable touch visualization globally
Config.set('graphics', 'show_touch', '0')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
import os
_DEBUG_ = False
class JHoraMobile(App):
    def build(self):
        try:
            if _DEBUG_: print("JHora: JHoraMobile build entered")
            if _DEBUG_: print("JHora: register_all_resources ")
            self.register_all_resources()
            if _DEBUG_: print("JHora: register_fonts")
            self.register_fonts()
            if _DEBUG_: print("JHora: from config import load_config")
            from config import load_config
            if _DEBUG_: print("JHora: Loading config")
            self.config = load_config()
            if _DEBUG_: print("JHora: config loaded",self.config)
            sm = ScreenManager()
            show_splash = self.config.get("show_splash", "yes")

            if show_splash.lower()=="yes":
                try:
                    if _DEBUG_: print("JHora: JHoraMobile importing PlanetSplashScreen")
                    from jhora_main import PlanetSplashScreen
                    if _DEBUG_: print("JHora: JHoraMobile importing PlanetSplashScreen successful")
                except Exception as e:
                    print("JHora: JHoraMobile importing PlanetSplashScreen failed")
                if _DEBUG_: print("JHora: Adding PlanetSplashScreen")
                sm.add_widget(PlanetSplashScreen(name='splash'))
                sm.current = 'splash'

            main_screen = Screen(name='main')
            try:
                if _DEBUG_: print("JHora: from jhora_main import JHoraApp")
                from jhora_main import JHoraApp
                if _DEBUG_: print("JHora: JHoraApp imported successfully")
            except Exception as e:
                print("JHora: JHoraApp import failed",e)
            if _DEBUG_: print("JHora: Adding JHoraApp to main_screen")
            main_screen.add_widget(JHoraApp(size_hint=(1, 1), pos_hint={'x': 0, 'y': 0}))
            sm.add_widget(main_screen)
            if not show_splash:
                if _DEBUG_: print("JHora: JHoraApp set as main")
                sm.current = 'main'
            return sm
        except Exception as e:
            if _DEBUG_: print("JHora: main Exception")
            try:
                if _DEBUG_: print(f"JHora: importing utils in main")
                from jhora import utils
                if _DEBUG_: print(f"JHora: Showing exception thru utils in main")
                utils.show_exception(e)
            except Exception as e:
                print(f"JHora: unable to import utils in main")
    def register_all_resources(self):
        from kivy.resources import resource_add_path
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        if _DEBUG_: print('ROOT DIR',ROOT_DIR)
        resource_add_path(os.path.join(ROOT_DIR, "assets"))
        resource_add_path(os.path.join(ROOT_DIR, "jhora"))
        resource_add_path(os.path.join(ROOT_DIR,"jhora", "lang"))
        resource_add_path(os.path.join(ROOT_DIR,"jhora", "fonts"))
        resource_add_path(os.path.join(ROOT_DIR,"jhora", "images"))
        resource_add_path(os.path.join(ROOT_DIR,"jhora", "data"))
        resource_add_path(os.path.join(ROOT_DIR,"jhora", "data", "ephe"))
    def register_fonts(self):
        from kivy.resources import resource_find
        from kivy.core.text import LabelBase
        try:
            from jhora import const  # if const is in jhora package
        except Exception as e:
            print(f"JHora: Unable to import const in register_fonts {str(e)}")
        for lang in list(const.available_languages.values()):
            font_path = resource_find(const.FONT_NAMES[lang][1])
            if _DEBUG_: print(f"JHora: Font Path {font_path}")
            if font_path:
                LabelBase.register(name=const.FONT_NAMES[lang][0], fn_regular=font_path)
            else:
                print(f"Font not found in {font_path} for {lang}: {const.FONT_NAMES[lang][1]}")

if __name__ == '__main__':
    if _DEBUG_: print('JHora: Calling JHoraMain Run')
    JHoraMobile().run()

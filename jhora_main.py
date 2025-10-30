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
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from math import sin, cos, radians
from datetime import datetime

from jhora import const, utils
from jhora.panchanga import drik, info
from jhora.horoscope.chart import charts
from jhora.ui.chart_styles import KundaliChart
from jhora.ui.indic_widgets import (IndicScrollSelector, IndicTabWidget, GetButtonWidget, SettingsTab,
                                    GetLabelWidget,ScrollableIndicLabel, IndicTableWidget)
from jhora._package_info import version as _APP_VERSION
from logger import log_error
from error_popup import show_error_popup
from config import load_config

_SPLASH_TEXT_SIZE = '18sp'; _INPUT_FONT_SIZE='16sp';_CALC_FONT_SIZE='18sp';_PANCHANGA_RESULT_FONT_SIZE='12sp'
_splash_app_title = "JHora - Vedic Astrology" + ' - V'+str(_APP_VERSION) + '\n' + \
            "© Open Astro Technologies, USA.\n"+ \
            "https://github.com/naturalstupid/PyJHora"
_DB_RESULT_FONT_SIZE = '12sp'
_SHOW_SPECIAL_TITHIS = False
_KEY_COLOR = '#8B0000'; _VALUE_COLOR = '#00008B'; _HEADER_COLOR='#006400'
_KEY_VALUE_FORMAT = lambda key,value: f"[b][color={_HEADER_COLOR}]{key}[/color][/b]" if value.strip()=='' else \
                f"[b][color={_KEY_COLOR}]{key}[/color][/b]: [color={_VALUE_COLOR}]{value}[/color]"
_BROWN_COLOR = (0.6, 0.3, 0.0, 1); _WHITE_COLOR = (1,1,1,1); _GOLD_COLOR = (1, 0.843, 0, 1); _BUTTON_BG_COLOR=(0.2, 0.6, 0.9, 1)
_DEBUG_PRINT = False
_MAIN_SCREEN_SHOW_TIME = 120
_CHART_LABEL_FONT_SIZE = dp(12); _CHART_CAPTION_FONT_SIZE = dp(12)
_dhasa_names_dict = {'graha':['vimsottari','yoga_vimsottari','rasi_bhukthi_vimsottari','ashtottari','tithi_ashtottari','yogini',
                     'tithi_yogini','shodasottari','dwadasottari','dwisatpathi','panchottari','satabdika','chaturaaseeti_sama',
                     'karana_chaturaaseeti_sama','shashtisama','shattrimsa_sama','naisargika','tara','karaka','buddhi_gathi',
                     'kaala','aayu','saptharishi_nakshathra'],
                'raasi':['narayana','kendraadhi_rasi','sudasa','drig','nirayana','shoola','kendraadhi_karaka',
                'chara','lagnamsaka','padhanadhamsa','mandooka','sthira','tara_lagna','brahma','varnada','yogardha',
                'navamsa','paryaaya','trikona','kalachakra','chakra','sandhya_panchaka'],
                'annual':['patyayini','varsha_vimsottari','varsha_narayana']
                }
_dhasa_names = utils.flatten_list(_dhasa_names_dict.values())
_bala_names_dict = {'vimsopaka_bala':['shadvarga_bala','sapthavarga_bala','dhasavarga_bala','shodhasavarga_bala'],
                    'vaiseshikamsa_bala':['shadvarga_bala','sapthavarga_bala','dhasavarga_bala','shodhasavarga_bala'],
                    'vargeeya_bala':['harsha_bala','pancha_vargeeya_bala','dwadhasa_vargeeya_bala'],
                    '':['shad_bala','bhava_bala']
                    }
_splash_background_image = const.get_resource_path("splash_background_image.png")#"splash_image.jpg")#
_earth_icon = const.get_resource_path("earth.png")
_moon_icon = const.get_resource_path("moon.png")
_sun_icon = const.get_resource_path("sun.png")
_mars_icon = const.get_resource_path("mars.png")
_mercury_icon = const.get_resource_path("mercury.png")
_jupiter_icon = const.get_resource_path("jupiter.png")
_venus_icon = const.get_resource_path("venus.png")
_saturn_icon = const.get_resource_path("saturn.png")
_rahu_icon = const.get_resource_path("rahu.png")
_ketu_icon = const.get_resource_path("ketu.png")

class MyButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(texture_size=self._update_size)
        self.size_hint_x = None  # Important to allow width resizing

    def _update_size(self, instance, value):
        self.width = value[0] + self.padding[0] * 2
        self.height = value[1] + self.padding[1] * 2

class AutoCompleteTextInput(TextInput):
    def __init__(self, update_fields_callback=None, **kwargs):
        super().__init__(**kwargs)
        self.update_fields_callback = update_fields_callback
        self.dropdown = DropDown(auto_dismiss=True)
        self.dropdown_open = False

        # UX settings
        self.hint_text = 'Type Place Name and press Enter to search'
        self.multiline = False
        self.keyboard_suggestions = True
        # Bind Enter key to trigger search
        self.bind(on_text_validate=self.on_enter_pressed)

    def on_enter_pressed(self, instance):
        # Trigger search after a short delay to ensure keyboard input is complete
        Clock.schedule_once(lambda dt: self.search_city(self.text), 0.1)

    def search_city(self, city_name):
        if not city_name.strip():
            return

        # Dismiss any existing dropdown
        if self.dropdown_open:
            self.dropdown.dismiss()
            self.dropdown_open = False

        self.dropdown.clear_widgets()

        try:
            matches = [city for city in utils.world_cities_dict.keys() if city_name.lower() in city.lower()]
        except Exception as e:
            error_msg = f"Error filtering city names: {str(e)}"
            log_error(error_msg)
            show_error_popup(error_msg)
            return

        if matches:
            for city in matches[:10]:
                btn = Button(
                    text=city,
                    size_hint_y=None,
                    height=dp(40),
                    color=_BROWN_COLOR,
                    background_normal='',
                    background_color=_BUTTON_BG_COLOR
                )
                btn.bind(on_release=lambda btn_instance, city_name=city: self.select_city(city_name))
                self.dropdown.add_widget(btn)

            # Open dropdown after a short delay to avoid stealing focus
            Clock.schedule_once(lambda dt: self.open_dropdown(), 0.2)
        else:
            self.show_error_popup("City not found. Please enter latitude, longitude, and timezone manually.")

    def open_dropdown(self):
        self.dropdown.open(self)
        self.dropdown_open = True

        # Reassert focus to keep keyboard active (especially on Android)
        Clock.schedule_once(lambda dt: setattr(self, 'focus', True), 0.1)

    def select_city(self, city_name):
        self.text = city_name
        self.dropdown.dismiss()
        self.dropdown_open = False

        try:
            result = utils.get_location(city_name)
            if self.update_fields_callback and result:
                self.update_fields_callback(result)
        except Exception as e:
            self.show_error_popup(f"Error retrieving location for {city_name}: {str(e)}")

    def show_error_popup(self, message):
        show_error_popup(message, title="Error: City not found in database")

class WhiteBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.size = instance.size
        self.rect.pos = instance.pos
        
# Orbiting planet widget
class OrbitingPlanet(Image):
    def __init__(self, radius, speed, angle=0, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.speed = speed
        self.angle = angle

    def update_position(self, center_x, center_y,scale=1.0):
        self.angle = (self.angle - self.speed) % 360 # negative sign to simulate clockwise
        rad = radians(self.angle)
        self.center_x = center_x + scale * self.radius * cos(rad)
        self.center_y = center_y + scale * self.radius * sin(rad)
# Splash screen with orbit animation
class PlanetSplashScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    def on_enter(self):
        self.layout = FloatLayout()
        # Add background image first
        self.background = Image(
            source=_splash_background_image,
            #allow_stretch=True, # Not Supported in Future versiosn of Kivy
            #keep_ratio=False, # Not Supported in Future versiosn of Kivy
            size_hint=(1, 1),
            pos_hint={'x': 0, 'y': 0}
        )
        self.layout.add_widget(self.background)

        self.earth = Image(source=_earth_icon, size_hint=(None, None), size=(24, 24))
        self.layout.add_widget(self.earth)
        planet_list = [(_moon_icon,0.15,13.37,(8,8)),(_mars_icon,1.2,0.53,(32,32)),(_mercury_icon,0.5,4.15,(32,32)),
                       (_jupiter_icon,1.8,0.084,(32,32)),(_venus_icon,0.7,1.63,(32,32)),(_saturn_icon,2.4,0.033,(32,32)),
                       (_rahu_icon,-2.6,-0.052,(32,32)),(_ketu_icon,2.6,-0.052,(32,32)),(_sun_icon,0.9,1.0,(48,48))]
        self.planets = [
            OrbitingPlanet(source=pl, radius=rad*100, speed=sp, size_hint=(None, None), size=(x, y)) for (pl,rad,sp,(x,y)) in planet_list]
        for planet in self.planets:
            self.layout.add_widget(planet)
        self.label = Label(
            text='',
            font_size=_SPLASH_TEXT_SIZE,
            color=_GOLD_COLOR,
            size_hint=(None, None),
            pos_hint={'center_x': 0.5, 'y': 0.05}  # Bottom of screen
        )
        self.layout.add_widget(self.label)
        self.add_widget(self.layout)
        Clock.schedule_interval(self.animate_orbits, 1/30)
        
        Clock.schedule_once(lambda dt: self.animate_text(_splash_app_title), 0.5)
        
        # Bind input events
        Window.bind(on_key_down=self.on_key_down)
        Window.bind(on_mouse_down=self.on_mouse_down)

        Clock.schedule_once(self.switch_to_main, _MAIN_SCREEN_SHOW_TIME)
    def on_key_down(self, window, key, scancode, codepoint, modifier):
        self.switch_to_main(None)    
    def on_mouse_down(self, window, x, y, button, modifiers):
        self.switch_to_main(None)
    def animate_orbits(self, dt):
        center_x = self.width / 2
        center_y = self.height / 2
        self.earth.center = (center_x, center_y)
        for planet in self.planets:
            planet.update_position(center_x, center_y)
    def animate_text(self, text, index=0):
        if index < len(text):
            self.label.text += text[index]
            anim = Animation(y=self.label.y + 0.05, duration=0.2)
            anim.start(self.label)
            Clock.schedule_once(lambda dt: self.animate_text(text, index + 1), 0.3)
    
    def on_touch_down(self, touch):
        self.switch_to_main(None)
        
    def switch_to_main(self, dt):
        if hasattr(self, '_switched') and self._switched:
            return
        self._switched = True
        Window.unbind(on_key_down=self.on_key_down)
        Window.unbind(on_mouse_down=self.on_mouse_down)
        self.manager.current = 'main'
_DEFAULT_LANG = "English"; _DEFAULT_CHART_TYPE = "south"; _DEFAULT_AYAN="LAHIRI"
class JHoraApp(BoxLayout):
    def _update_label_size(self, instance, value):
        instance.size = instance.texture_size
    def __init__(self,**kwargs):
        try:
            print("JHora: JHoraApp init")
            super().__init__(**kwargs)
            self.config = load_config()
            self.language = const.available_languages[self.config.get("language",_DEFAULT_LANG)]
            self.chart_type = self.config.get("chart_type",_DEFAULT_CHART_TYPE)
            self.last_tab_index = 5
            self.last_selected_tab = 1
            self.chart_info_label = GetLabelWidget(text='',font_name=const.FONT_NAMES[self.language][0])
            self.chart_widget = None
            utils.set_language(self.language)
            Window.softinput_mode = "pan"
            Window.clearcolor = (0, 0, 0, 1)  # RGBA for black
            self.res = utils.resource_strings
            self._chart_names = const._chart_names[:-2]
            self._dhasa_names = _dhasa_names
            self.chart_caption = ''
            self._chart_factors = const.division_chart_factors
            utils.use_database_for_world_cities(const.check_database_for_world_cities)
            current_date_str, current_time_str = datetime.now().strftime('%Y,%m,%d;%H:%M:%S').split(';')
            if const.use_internet_for_location_check:
                try:
                    loc = utils.get_place_from_user_ip_address()
                except:
                    loc = []
                if not loc or len(loc)<4:
                    loc = ['','','','']
            else:
                loc = ['','','','']
                #print('JHora: loc',loc,'use_internet_for_location_check',const.use_internet_for_location_check)
            self._create_app_ui(current_date_str,current_time_str,loc)
        except Exception as e:
            utils.show_exception(e)
    def _validate_input(self):
        try:
            import re
            # Strip all inputs to remove leading/trailing whitespace
            date_str = self.date_input.text.strip()
            time_str = self.time_input.text.strip()
            lat_str = self.lat_input.text.strip()
            lon_str = self.lon_input.text.strip()
            tz_str = self.tz_input.text.strip()
            if not date_str or not re.match(r'^\d{4},\d{1,2},\d{1,2}$', date_str):
                return False
            if not time_str or not re.match(r'^\d{2}:\d{1,2}(?::\d{1,2})?$', time_str):
                return False
            if lat_str:
                lat = float(lat_str)
                if not (-90 <= lat <= 90):
                    return False
            else:
                return False
            if lon_str:
                lon = float(lon_str)
                if not (-180 <= lon <= 180):
                    return False
            else:
                return False
            if tz_str:
                tz = float(tz_str)
                if not (-12 <= tz <= 14):
                    return False
            else:
                return False
            return True
        except Exception as e:
            print("JHora: Error in _validate_input",e)
    def _create_app_ui(self, current_date_str, current_time_str, loc):
        try:
            # Create only the input tab initially
            self.indic_tab_widget = IndicTabWidget(
                tabs=[self.res['input_str']],
                contents=[''],
                font_name=const.FONT_NAMES[self.language][0],
                show_selector=[False],
                widget_classes=[ScrollableIndicLabel]
            )
            # Create input tab content
            self._create_input_tab(current_date_str, current_time_str, loc)
            # Add tab widget to layout
            self.add_widget(self.indic_tab_widget)
            # Select input tab
            self.indic_tab_widget.select_tab(self.input_tab_index)
        except Exception as e:
            print("JHora: Error in _create_app_ui",e)
    def _create_input_tab(self,current_date_str,current_time_str,loc):
        try:
            self.input_tab_index = 0
            input_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            from kivy.uix.scrollview import ScrollView
            scroll = ScrollView(size_hint=(1,1))
            scroll.add_widget(input_layout)
            self.name_input = TextInput(text='',hint_text='Enter your name', multiline=False, font_size=_INPUT_FONT_SIZE)
            self.date_input = TextInput(text=current_date_str, hint_text='Date (YYYY,MM,DD)', multiline=False, font_size=_INPUT_FONT_SIZE)
            self.time_input = TextInput(text=current_time_str, hint_text='Time (HH:MM:SS)', multiline=False, font_size=_INPUT_FONT_SIZE)
            self.place_input = AutoCompleteTextInput(
                text=loc[0], hint_text='Type Place Name and press enter to select available cities', multiline=False, font_size=_INPUT_FONT_SIZE,
                update_fields_callback=self.update_location_fields
            )
            self.lat_input = TextInput(text=str(loc[1]), hint_text='Latitude', multiline=False, font_size=_INPUT_FONT_SIZE)
            self.lon_input = TextInput(text=str(loc[2]), hint_text='Longitude', multiline=False, font_size=_INPUT_FONT_SIZE)
            self.tz_input = TextInput(text=str(loc[3]), hint_text='Timezone Offset (e.g. 5.5)', multiline=False, font_size=_INPUT_FONT_SIZE)
            self.calc_button = GetButtonWidget(text=self.res['calculate_panchangam_str'], size_hint=(1,None),
                                               height = dp(50),
                                           font_size=_CALC_FONT_SIZE,font_name=const.FONT_NAMES[self.language][0],
                                           on_press_callback=self.on_calculate)
            for widget in [self.name_input,self.date_input, self.time_input, self.place_input,
                           self.lat_input, self.lon_input, self.tz_input,
                           self.calc_button]:
                input_layout.add_widget(widget)
            self.indic_tab_widget.content_widgets[0].clear_widgets()
            self.indic_tab_widget.content_widgets[0].add_widget(scroll)
            self.tabs_created = False
            if self._validate_input(): self._create_other_tabs()
        except Exception as e:
            print("JHora: Error in _create_input_tab",e)
    def _create_other_tabs(self):
        try:
            self.panchangam_tab_index = 1
            self.chart_tab_index = 2
            self.dhasa_tab_index = 3
            self.bala_tab_index = 4
            self.options_tab_index = 5
            additional_tabs = ['panchangam','horoscope', 'dhasa', 'strength', 'options'][:self.last_tab_index]
            widget_classes = [ScrollableIndicLabel,ScrollableIndicLabel,ScrollableIndicLabel,
                              IndicTableWidget, ScrollableIndicLabel][:self.last_tab_index]
            show_selector = [True, False, True, True, False][:self.last_tab_index]
            for i, tab in enumerate(additional_tabs):
                self.indic_tab_widget.add_tab(
                    title=self.res[tab + '_str'],
                    content='',
                    widget_class=widget_classes[i],
                    show_selector=show_selector[i]
                )
                eval("self._create_"+tab+"_tab()")
            # 🔔 Assign tab selection callback
            self.indic_tab_widget.on_tab_selected = self.on_tab_change
            self.tabs_created = True  # Mark that tabs have been created
        except Exception as e:
            print("JHora: Error in _create_other_tabs",e)
    def on_tab_change(self,index):
        try:
            if index == self.chart_tab_index and index <= self.last_tab_index:
                self.recreate_chart_widget()
                selected_index = self.chart_selector.selected_index
                selected_item = self.chart_selector.items[selected_index]
                self._on_chart_selected(self.chart_selector,selected_index,selected_item)
        except Exception as e:
            print("JHora: Error in on_tab_change",e)
    def recreate_chart_widget(self):
        try:
            if self.chart_widget and self.chart_widget.parent:
                self.chart_layout.remove_widget(self.chart_widget)
            self.chart_widget = KundaliChart(
                chart_type=self.config.get("chart_type",_DEFAULT_CHART_TYPE),
                font_name=const.FONT_NAMES[self.language][0],
                size_hint=(1, 1),data_font_size=_CHART_LABEL_FONT_SIZE, caption_font_size=_CHART_CAPTION_FONT_SIZE
            )
            # Add the new chart widget to the layout
            self.chart_layout.add_widget(self.chart_widget)
        except Exception as e:
            print("JHora: Error in recreate_chart_widget",e)
    def on_calculate(self, instance):
        try:
            if self._validate_input():
                if not self.tabs_created: self._create_other_tabs()
                self.update_all_tabs(self)
                self.indic_tab_widget.select_tab(self.panchangam_tab_index)
            else:
                show_error_popup(message='Please check if date, time, and location are valid.',title="Invalid Input")
        except Exception as e:
            print("JHora: Error in on_calculate",e)
    def _create_panchangam_tab(self):
        try:
            self.panchangam_tab = self.indic_tab_widget.tabs_widgets[self.panchangam_tab_index]
            self.panchanga_info_types = ['panchangam','special_tithis','gauri_choghadiya','muhurtha','shubha_hora','panchaka_rahitha']
            self.panchanga_menu_items = [{
                'text': self.res[key + '_str'],
                'index': i
            } for i, key in enumerate(self.panchanga_info_types)]
            self.indic_tab_widget.set_selector_items(self.panchangam_tab_index, self.panchanga_menu_items)
            self.indic_tab_widget.set_selector_callback(self.panchangam_tab_index, self._on_panchangam_selected)
        except Exception as e:
            print("JHora: Error in _create_panchangam_tab",e)
    def _create_horoscope_tab(self):
        try:
            self.chart_widget = KundaliChart(chart_type=self.config.get("chart_type",_DEFAULT_CHART_TYPE),
                                             font_name=const.FONT_NAMES[self.language][0],
                                             size_hint=(1,1),data_font_size=_CHART_LABEL_FONT_SIZE,
                                             caption_font_size=_CHART_CAPTION_FONT_SIZE)
            self.chart_layout = BoxLayout(orientation='vertical', padding=10, spacing=10,size_hint=(1,1))
            self.chart_layout.add_widget(self._create_chart_selector())
            self.chart_info_label = GetLabelWidget(text='',font_name=const.FONT_NAMES[self.language][0])
            self.chart_layout.add_widget(self.chart_info_label)
            self.chart_layout.add_widget(self.chart_widget)
            # 1. Switch to the tab to ensure its content is active
            self.indic_tab_widget.content_widgets[self.chart_tab_index].clear_widgets()
            self.indic_tab_widget.content_widgets[self.chart_tab_index].add_widget(self.chart_layout)
            self.indic_tab_widget.select_tab(self.chart_tab_index)
        except Exception as e:
            print("JHora: Error in _create_horoscope_tab",e)
    def _create_dhasa_tab(self):
        try:
            self.db_tab = self.indic_tab_widget.tabs_widgets[self.dhasa_tab_index]
            self.db_menu_items = []
            for i,key in enumerate(_dhasa_names):
                _dhasa_type = utils.get_key_from_list_value(_dhasa_names_dict,key)
                nkey = self.res[_dhasa_type+'_str']+'-'+self.res[key+'_str']
                self.db_menu_items.append({'text':nkey,'index':i}) 
            self.indic_tab_widget.set_selector_items(self.dhasa_tab_index, self.db_menu_items)
            self.indic_tab_widget.set_selector_callback(self.dhasa_tab_index, self._on_dhasa_selected)
        except Exception as e:
            print("JHora: Error in _create_dhasa_tab",e)
    def _create_strength_tab(self):
        try:
            self.bala_tables = []
            self.bala_tab = self.indic_tab_widget.tabs_widgets[self.bala_tab_index]
            self.bala_menu_items = []
            i = 0
            for key,vlist in _bala_names_dict.items():
                _bala_type = self.res[key+"_str"] if key.strip()!="" else ""
                for value in vlist:
                    nkey = _bala_type +" "+self.res[value+'_str']
                    self.bala_menu_items.append({'text':nkey,'index':i})
                    i += 1
            self.indic_tab_widget.set_selector_items(self.bala_tab_index, self.bala_menu_items)
            self.indic_tab_widget.set_selector_callback(self.bala_tab_index, self._on_bala_selected)
        except Exception as e:
            print("JHora: Error in _create_strength_tab",e)
    def _create_options_tab(self):
        try:
            self.settings_widget = SettingsTab(app=self)
            settings_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            settings_layout.add_widget(self.settings_widget)
            self.indic_tab_widget.select_tab(self.options_tab_index)
            self.indic_tab_widget.content_widgets[self.options_tab_index].clear_widgets()
            self.indic_tab_widget.content_widgets[self.options_tab_index].add_widget(settings_layout)
        except Exception as e:
            print("JHora: Error in _create_options_tab",e)
    def update_tab_width(self, *args):
        try:
            self.tab_width = self.width / len(self.tab_list)
        except Exception as e:
            print("JHora: Error in update_tab_width",e)
    def _on_panchangam_selected(self,selector, item_index, selected_item):
        self.last_selected_tab = self.panchangam_tab_index
        try:
            self.calculate_panchangam(panchangam_selected_index=selected_item['index'])
        except Exception as e:
            error_msg = f"Error in {__name__}: {str(e)}"
            log_error(error_msg)
            show_error_popup(error_msg)
            self.indic_tab_widget.update_tab_content(self.panchangam_tab_index, error_msg)
    def _get_bala_tables(self):
        try:
            name_str = self.name_input.text
            date_str = self.date_input.text
            time_str = self.time_input.text
            place_name = self.place_input.text
            lat = float(self.lat_input.text)
            lon = float(self.lon_input.text)
            tz = float(self.tz_input.text)
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y,%m,%d %H:%M:%S")
            dob = drik.Date(dt.year, dt.month, dt.day); tob = (dt.hour, dt.minute, dt.second)
            jd = utils.julian_day_number(dob, tob)
            place = drik.Place(place_name, lat, lon, tz)
            ayanamsa_mode=drik.set_ayanamsa_mode(self.config.get("ayanamsa_mode",_DEFAULT_AYAN))
            from jhora.horoscope import strength_selector
            self.bala_tables = strength_selector._get_bala_tables(dob,tob,place)
        except Exception as e:
            error_msg = f"Error in {__name__}: {str(e)}"
            log_error(error_msg)
            show_error_popup(error_msg)
            self.indic_tab_widget.update_tab_content(self.bala_tab_index, error_msg)            
    def _on_bala_selected(self,selector,item_index, selected_item):
        self.last_selected_tab = self.bala_tab_index
        try:
            if self.bala_tables is None or len(self.bala_tables)==0:
                self._get_bala_tables()
            bala_table = self.bala_tables[item_index]
            self.indic_tab_widget.update_tab_content(self.bala_tab_index, ([], bala_table))
        except Exception as e:
            error_msg = f"Error in {__name__}: {str(e)}"
            log_error(error_msg)
            show_error_popup(error_msg)
            self.indic_tab_widget.update_tab_content(self.bala_tab_index, error_msg)            
    def _on_dhasa_selected(self,selector,item_index, selected_item):
        self.last_selected_tab = self.dhasa_tab_index
        try:
            name_str = self.name_input.text
            date_str = self.date_input.text
            time_str = self.time_input.text
            place_name = self.place_input.text
            lat = float(self.lat_input.text)
            lon = float(self.lon_input.text)
            tz = float(self.tz_input.text)
            dhasa_key = self._dhasa_names[selected_item['index']]
            dhasa_type = utils.get_key_from_list_value(_dhasa_names_dict,dhasa_key)
            dhasa_name = self.res[dhasa_type+'_str']+'-'+self.res[dhasa_key+'_str']
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y,%m,%d %H:%M:%S")
            dob = drik.Date(dt.year, dt.month, dt.day); tob = (dt.hour, dt.minute, dt.second)
            jd = utils.julian_day_number(dob, tob)
            place = drik.Place(place_name, lat, lon, tz)
            ayanamsa_mode=drik.set_ayanamsa_mode(self.config.get("ayanamsa_mode",_DEFAULT_AYAN))
            option_str = ''
            from jhora.horoscope import dhasa_selector
            func_str = 'dhasa_selector._get_'+dhasa_key.lower()+'_dhasa'
            arg_str = 'dob, tob, place,ayanamsa_mode='; option_str = "'"+self.config.get("ayanamsa_mode",_DEFAULT_AYAN)+"'"
            eval_str = func_str+'('+arg_str+option_str+')'
            try:
                retval = eval(eval_str)
                if retval:
                    results_dict = {f"{dhasa_name+' '+self.res['dhasa_bhukthi_str']}":
                                    f"{self.res['starts_at_str']}"}
                    results_dict.update({k:v for (k,v) in retval})
                    #formatted_text = '\n'.join(_KEY_VALUE_FORMAT(k,v) for k,v in results_dict.items())
                    #self.db_results_label.text = formatted_text
                    results_text = '\n'.join(k+':'+v for k,v in results_dict.items())
                else:
                    print(f"JHora: {dhasa_name} returned empty results")
            except Exception as e:
                print(f"JHora: Error getting {dhasa_name} results",e)
            self.indic_tab_widget.update_tab_content(self.dhasa_tab_index, results_text)
        except Exception as e:
            error_msg = f"Error in {__name__}: {str(e)}"
            log_error(error_msg)
            show_error_popup(error_msg)
            self.indic_tab_widget.update_tab_content(self.dhasa_tab_index, error_msg)
    def _create_chart_selector(self):
        try:
            items = [{
                'text': self.res[key],
                'index': i
            } for i, key in enumerate(self._chart_names)]
        
            self.chart_selector = IndicScrollSelector(
                items=items,
                font_name=const.FONT_NAMES[self.language][0],
                on_select=self._on_chart_selected
            )
            self._on_chart_selected(self.chart_selector,items[0]['index'], items[0])
            return self.chart_selector
        except Exception as e:
            print("JHora: Error in _create_chart_selector",e)
    def _on_chart_selected(self,selector,item_index,selected_item):
        self.last_selected_tab = self.chart_tab_index
        try:
            name_str = self.name_input.text
            date_str = self.date_input.text
            time_str = self.time_input.text
            place_name = self.place_input.text
            lat = float(self.lat_input.text)
            lon = float(self.lon_input.text)
            tz = float(self.tz_input.text)
            drik.set_ayanamsa_mode(self.config.get("ayanamsa_mode",_DEFAULT_AYAN))
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y,%m,%d %H:%M:%S")
            jd = utils.julian_day_number(drik.Date(dt.year, dt.month, dt.day), (dt.hour, dt.minute, dt.second))
            place = drik.Place(place_name, lat, lon, tz)
            self.chart_caption = name_str
            year, month, day,birth_time_hrs = utils.jd_to_gregorian(jd)
            date_str = str(day)+'-'+utils.MONTH_SHORT_LIST_EN[month-1]+'-'+str(year)
            time_str = utils.to_dms(birth_time_hrs)
            _lat = utils.to_dms(lat,is_lat_long='lat')
            _long = utils.to_dms(lon,is_lat_long='long')
            place_str2 = ' ('+_lat+', '+_long+', '+str(place.timezone)+')'
            #self.chart_caption += '\n'+date_str+' '+ time_str +'\n'+self.place_input.text+'\n'+place_str2
            chart_index = selected_item['index']
            dcf = self._chart_factors[chart_index]
            chart_key = self._chart_names[chart_index]
            method_index = self.config.get(chart_key.replace("_str",""),1)
            chart_name = self.res[chart_key]; method_name = ''
            if chart_index !=0 and dcf in const.division_chart_factors:
                key = f'd{dcf}_option{method_index}_str'
                method_name = self.res.get(key, 'default-')
            planet_positions = charts.divisional_chart(jd, place, divisional_chart_factor=dcf,chart_method=method_index)
            ascendant_house = planet_positions[0][1][0]
            h_to_p = utils.get_house_planet_list_from_planet_positions(planet_positions)
            #chart_2d = utils._convert_1d_house_data_to_2d(h_to_p)
            chart_1d = utils.convert_h_to_p_to_planet_names(h_to_p)
            #print(chart_1d)
            self.chart_caption += '\n'+chart_name
            if chart_index != 0: self.chart_caption += '\n' + method_name
            #self.chart_widget.draw_data(chart_2d, center_text=self.chart_caption)
            self.chart_widget.set_data(data=chart_1d,chart_caption=self.chart_caption)
            # File planet longitudes
            planet_longitude_info = ''
            for i,(p,(h,long)) in enumerate(planet_positions):
                p_str = self.res['ascendant_str'] if p==const._ascendant_symbol else utils.PLANET_NAMES[p]
                planet_longitude_info += p_str + ': ' + utils.RAASI_SHORT_LIST[h]+'  ' + utils.to_dms(long,is_lat_long='plong')+'  '
                if (i+1)%2==0: planet_longitude_info += '\n'
                if hasattr(self.chart_info_label, 'set_text') and callable(self.chart_info_label.set_text):
                    self.chart_info_label.set_text(planet_longitude_info)
                else:
                    self.chart_info_label.text = planet_longitude_info
        except Exception as e:
            error_msg = f"Error in {__name__}: {str(e)}"
            log_error(error_msg)
            show_error_popup(error_msg)
            self.indic_tab_widget.update_tab_content(self.chart_tab_index, error_msg)
    def update_location_fields(self, location_data):
        try:
            city, lat, lon, tz = location_data
            self.place_input.text = city
            self.lat_input.text = str(lat)
            self.lon_input.text = str(lon)
            self.tz_input.text = str(tz)
        except Exception as e:
            print("JHora: Error in update_location_fields",e)
    def _get_panchangam_results(self,jd,place,resource_type = None):
        try:
            self.chart_caption = self.name_input.text
            year, month, day,birth_time_hrs = utils.jd_to_gregorian(jd)
            date_str = str(day)+'-'+utils.MONTH_SHORT_LIST_EN[month-1]+'-'+str(year)
            time_str = utils.to_dms(birth_time_hrs)
            _lat = utils.to_dms(float(self.lat_input.text),is_lat_long='lat')
            _long = utils.to_dms(float(self.lon_input.text),is_lat_long='long')
            place_str2 = ' ('+_lat+', '+_long+', '+str(place.timezone)+')'
            self.chart_caption += '\n'+date_str+' '+ time_str +'\n'+self.place_input.text+'\n'+place_str2
            info.set_language(self.language)
            results_dict = info.get_panchangam_resources(jd,place,resource_type=resource_type)
            results_dict = {**{utils.resource_strings[self.panchanga_info_types[resource_type-1]+'_str']:''},
                            **results_dict}
            return results_dict
        except Exception as e:
            print("JHora: Error in _get_panchangam_results",e)
    def update_all_tabs(self,instance):
        try:
            for tab_index, layout in enumerate(self.indic_tab_widget.content_widgets):
                selector = getattr(layout, 'selector', None)
                if selector and selector.items:
                    item_index = 0
                    item = selector.items[item_index]
                    if selector.on_select:
                        print("JHora: inside upate_all_tabs calling selector.on_select",selector,item_index,item)
                        selector.on_select(selector, item_index, item)
            if self.last_tab_index > 1:
                self.update_manual_tabs()
            self.indic_tab_widget.select_tab(self.panchangam_tab_index,trigger_callback=False)
        except Exception as e:
            error_msg = f"Error in {__name__}: {str(e)}"
            log_error(error_msg)
            show_error_popup(error_msg)
            self.indic_tab_widget.update_tab_content(tab_index, error_msg)
    def update_manual_tabs(self):
        try:
            items = self.chart_selector.items
            self._on_chart_selected(self.chart_selector,items[0]['index'], items[0])
            self._get_bala_tables()
        except Exception as e:
            print("JHora: Error in update_manual_tabs",e)
    def calculate_panchangam(self,instance=None, panchangam_selected_index=0):
        data_ok = self._validate_input()
        if not data_ok:
            error_msg = f"Input data incomplete. Please fill all data."
            log_error(error_msg)
            show_error_popup(error_msg)
            return
        try:
            name_str = self.name_input
            date_str = self.date_input.text
            time_str = self.time_input.text
            place_name = self.place_input.text
            lat = float(self.lat_input.text)
            lon = float(self.lon_input.text)
            tz = float(self.tz_input.text)
            dt = datetime.strptime(f"{date_str} {time_str}", "%Y,%m,%d %H:%M:%S")
            jd = utils.julian_day_number(drik.Date(dt.year, dt.month, dt.day), (dt.hour, dt.minute, dt.second))
            drik.set_ayanamsa_mode(self.config.get("ayanamsa_mode",_DEFAULT_AYAN))
            place = drik.Place(place_name, lat, lon, tz)
            results_dict = self._get_panchangam_results(jd, place,resource_type=panchangam_selected_index+1)
            results_text = '\n'.join(k+':'+v for k,v in results_dict.items())
            self.indic_tab_widget.update_tab_content(self.panchangam_tab_index, results_text)
        except Exception as e:
            error_msg = f"Error in {__name__}: {str(e)}"
            log_error(error_msg)
            show_error_popup(error_msg)
            self.indic_tab_widget.update_tab_content(self.panchangam_tab_index, error_msg)

class JHoraMain(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def build(self):
        try:
            print("JHora: JHoraMain build entered")
            #from jhora import const
            #const.register_all_resources()
            #const.register_fonts()  # ✅ Register fonts before using them
            return JHoraApp()
        
        except Exception as e:
            log_error(f"App launch failed: {str(e)}")
            show_error_popup("App failed to launch. Please restart or check logs.")
            return None  # Prevent crash
class JHoraWithSplash(App):
    def __init__(self,show_splash_screen = True,language='en', **kwargs):
        super(JHoraWithSplash,self).__init__(**kwargs)
    def build(self):
        self.config = load_config()
        sm = ScreenManager()
        show_splash = self.config.get("show_splash", True)
        # Optionally add splash screen
        if show_splash:
            sm.add_widget(PlanetSplashScreen(name='splash'))
            sm.current = 'splash'
        # Create main screen first
        main_screen = Screen(name='main')
        main_screen.add_widget(JHoraApp())
        sm.add_widget(main_screen)
        if not show_splash:
            sm.current = 'main'
    
        return sm
if __name__ == '__main__':
    #JHoraWithSplash().run()
    JHoraMain().run()

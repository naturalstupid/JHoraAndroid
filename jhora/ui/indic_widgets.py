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
# Add parent directory to sys.path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color, RoundedRectangle
from kivy.properties import (StringProperty, NumericProperty, ListProperty, BooleanProperty, ObjectProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.uix.dropdown import DropDown
from kivy.core.window import Window
# Import the necessary effect for smoother scrolling on mobile
from kivy.effects.dampedscroll import DampedScrollEffect

from jhora.panchanga import info
from jhora import utils, const
#cairo = const.get_cairo()
#hb = const.get_harfbuzz()
from config import save_config

_BROWN_COLOR = (0.6, 0.3, 0.0, 1); _WHITE_COLOR = (1,1,1,1); _GOLD_COLOR = (1, 0.843, 0, 1); _BUTTON_BG_COLOR=(0.2, 0.6, 0.9, 1)
_BLACK_COLOR = (0, 0, 0, 1); _CYAN_COLOR = (0.6,1.0,1.0,1)
_SETTINGS_TAB_COLOR = _CYAN_COLOR; _LABEL_WIDGET_COLOR = _CYAN_COLOR; _BUTTON_WIDGET_COLOR = _BLACK_COLOR
_INDIC_LABEL_FONT_SIZE = dp(14)
_INDIC_BUTTON_FONT_SIZE = dp(14)
_INDIC_TAB_FONT_SIZE = dp(14)
_ENGLISH_TAB_FONT_SIZE = dp(14)
_INDIC_TAB_WIDTH = dp(80)
_ENGLISH_TAB_WIDTH = dp(60)
_INDIC_SCROLL_LABEL_FONT_SIZE = dp(14)
_INDIC_SCROLL_BUTTON_SIZE = dp(14)
_INDIC_SCROLL_SPACING = dp(10)
_INDIC_SCROLL_PADDING = dp(10)
_SPINNER_HEIGHT = dp(40)
_ENABLE_BUTTON_CLOCK_SECONDS = 0.2
_SPINNER_ITEM_HEIGHT = dp(20)
_DROPDOWN_WINDOW_SIZE_FACTOR = 0.75
_DROPDOWN_ITEM_SPACING = dp(10)
_DEBUG_=False
class DropdownSelector(BoxLayout):
    selected_value = StringProperty()

    def __init__(self, label_text, values, initial_value, on_select_callback, **kwargs):
        size_hint_y_val = kwargs.pop('size_hint_y', None) #V0.7.9.2
        super().__init__(orientation='horizontal', size_hint_y=size_hint_y_val, #V0.7.9.2
                         spacing=_DROPDOWN_ITEM_SPACING, **kwargs)
        self.values = values
        self.selected_value = initial_value
        self.on_select_callback = on_select_callback
        self.dropdown_open = False

        # --- Set the max_height based on a percentage of the initial window height ---
        self.dropdown = DropDown(
            max_height=Window.height * _DROPDOWN_WINDOW_SIZE_FACTOR,
            # This is the fix for Android scrolling detection: #V0.7.9.2
            scroll_type=['bars', 'content'], 
            effect_cls=DampedScrollEffect
            )
        self.dropdown.container.size_hint_y = None #V0.7.9.2
        self.dropdown.container.bind(
            minimum_height=self.dropdown.container.setter('height')
        )               #V0.7.9.2
        self.dropdown.bind(on_dismiss=self.on_dropdown_dismiss)
        # --- Bind to the window resize event for dynamic resizing ---
        Window.bind(on_resize=self._update_max_height)

        for value in self.values:
            btn = Button(text=value, size_hint_y=None, height=_SPINNER_ITEM_HEIGHT)
            btn.bind(on_release=lambda instance, btn_text=value: self.select_value(btn_text)) #V0.7.9.2
            self.dropdown.add_widget(btn)

        self.label_button = Button(text=label_text, size_hint_x=0.5, color=_BUTTON_WIDGET_COLOR)
        self.label_button.bind(on_release=self.open_dropdown)

        self.dropdown_button = Button(text=self.selected_value, size_hint_x=0.5, color=_BUTTON_WIDGET_COLOR)
        self.dropdown_button.background_normal = ''
        self.dropdown_button.background_color = (0.9, 0.9, 0.9, 1)
        self.dropdown_button.bind(on_release=self.open_dropdown)

        self.add_widget(self.label_button)
        self.add_widget(self.dropdown_button)
    
    # Method to update the dropdown's max_height dynamically
    def _update_max_height(self, window, width, height):
        self.dropdown.max_height = height * _DROPDOWN_WINDOW_SIZE_FACTOR
        
    def open_dropdown(self, *args):
        if _DEBUG_: print("JHora: Dropdown Left Button pressed")
        if self.dropdown_open:
            if _DEBUG_: print("JHora: Dropdown already open returning")
            return
        self.dropdown_open = True
        self.label_button.disabled = True
        if _DEBUG_: print("JHora: Showing Dropdown")
        self.dropdown.open(self.dropdown_button)

    def select_value(self, value):
        if _DEBUG_: print("JHora: Dropdown Value Selected")
        self.selected_value = value
        self.dropdown_button.text = value
        self.dropdown.dismiss()
        if _DEBUG_: print("JHora: Dropdown dismissed")
        if self.on_select_callback:
            self.on_select_callback(value)

    def on_dropdown_dismiss(self, *args):
        if _DEBUG_: print("JHora: Dropdown dismissed")
        self.dropdown_open = False
        if _DEBUG_: print("JHora: Dropdown Left Button Enabled")
        self.label_button.disabled = False

    def set_values(self, new_values, default_value=None):
        self.values = new_values
        self.dropdown.clear_widgets()
        for value in self.values:
            btn = Button(text=value, size_hint_y=None, height=_SPINNER_ITEM_HEIGHT)
            btn.bind(on_release=lambda instance, btn_text=value: self.select_value(btn_text)) #V0.7.9.2
            self.dropdown.add_widget(btn)
        if default_value:
            self.selected_value = default_value
            self.dropdown_button.text = default_value
class SettingsTab(BoxLayout):
    def __init__(self, app, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.app = app
        self.res = self.app.res
        self.original_config = self.app.config.copy()  # Save original config
        
        layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        layout.size_hint_y = 1

        # Language setting
        _available_languages = list(const.available_languages.keys()) if const._PLATFORM=="win" else ['English']
        self.lang_selector = DropdownSelector(
            label_text="Change Language",
            values=_available_languages,
            initial_value=self.app.config["language"],
            on_select_callback=self.on_language_change,
            size_hint_y = None
        )
        layout.add_widget(self.lang_selector)

        # Chart type setting
        _available_chart_types = ['south', 'east', 'north']
        self.chart_type_selector = DropdownSelector(
            label_text="Change chart_type",
            values=_available_chart_types,
            initial_value=self.app.config["chart_type"],
            on_select_callback=self.on_chart_type_change,
            size_hint_y = None
        )
        layout.add_widget(self.chart_type_selector)

        # Ayanamsa setting
        _ayanamsa_modes = list(const.available_ayanamsa_modes.keys())[:-2]
        self.ayanamsa_selector = DropdownSelector(
            label_text="Ayanamsa Option",
            values=_ayanamsa_modes,
            initial_value=self.app.config["ayanamsa_mode"],
            on_select_callback=self.on_ayanamsa_change,
            size_hint_y = None
        )
        layout.add_widget(self.ayanamsa_selector)

        # Chart spinner
        self.chart_names = [cht.replace("_str", "") for cht in const._chart_names[1:-2]]
        self.chart_selector = DropdownSelector(
            label_text="Divisional Chart",
            values=self.chart_names,
            initial_value=self.chart_names[0],
            on_select_callback=self.on_chart_selected,
            size_hint_y = None
        )
        layout.add_widget(self.chart_selector)

        # Method spinner
        methods, default_index = self.get_varga_methods(1)
        default_method = methods[default_index - 1]# if default_index > 0 else "Select Method"
        self.method_selector = DropdownSelector(
            label_text="Calculation Method",
            values=methods,
            initial_value=default_method,
            on_select_callback=self.on_method_selected,
            size_hint_y = None
        )
        layout.add_widget(self.method_selector)

        # Splash toggle
        self.splash_toggle = DropdownSelector(
            label_text="Show Splash Screen", values = ["yes","no"],
            initial_value = self.app.config["show_splash"].lower(),
            on_select_callback=self.on_splash_toggle,
            size_hint_y = None
        )
        layout.add_widget(self.splash_toggle)

        self.add_widget(layout)

        # Save and Cancel buttons
        button_layout = BoxLayout(orientation="horizontal",height=_SPINNER_HEIGHT,size_hint=(1,None))
        self.save_button = Button(text="Save", on_press=self.on_save,size_hint=(1,None))
        self.cancel_button = Button(text="Cancel", on_press=self.on_cancel,size_hint=(1,None))
        button_layout.add_widget(self.save_button)
        button_layout.add_widget(self.cancel_button)
        self.add_widget(button_layout)

    def get_varga_methods(self, chart_index):
        dcf = const.division_chart_factors[chart_index]
        varga_dict = utils.get_varga_option_dict()
        if dcf not in varga_dict:
            return [], 1

        method_count, default_index, *_ = varga_dict[dcf]
        method_list = []
        if method_count is None:
            return [], 1
        for mc in range(method_count):
            key = f'd{dcf}_option{mc + 1}_str' if dcf in const.division_chart_factors else f'dn_custom_option{mc}_str'
            caption = self.app.res.get(key, f'Method {mc + 1}')
            method_list.append(caption)

        return method_list, default_index

    def on_chart_selected(self, chart_name):
        chart_index = self.chart_names.index(chart_name)
        methods, default_index = self.get_varga_methods(chart_index+1)#+1 to skip Raasi
        if _DEBUG_: print(chart_index,methods,default_index)
        if methods and self.method_selector:
            self.method_selector.set_values(methods,default_index-1)
            self.method_selector.dropdown_button.text = methods[default_index - 1]# if default_index > 0 else "Select Method"
            self.app.config[chart_name] = default_index
            if _DEBUG_: print(chart_name,self.method_selector.values,default_index)
    def on_method_selected(self, method_name):
        chart_name = self.chart_selector.selected_value
        method_index = self.method_selector.values.index(method_name)
        if _DEBUG_: print(chart_name,method_index,method_name,self.method_selector.values)
        self.app.config[chart_name] = method_index + 1
    
    def on_language_change(self, text):
        self.app.config["language"] = text
    
    def on_chart_type_change(self, text):
        self.app.config["chart_type"] = text
    def on_ayanamsa_change(self, text):
        self.app.config["ayanamsa_mode"] = text
    
    def on_splash_toggle(self, text):
        self.app.config["show_splash"] = text.lower()
    
    def on_save(self, instance):
        self.save_button.disabled = True
        save_config(self.app.config)
        self.original_config = self.app.config.copy()  # Update original config
        self.app.indic_tab_widget.select_tab(self.app.last_selected_tab)
        Clock.schedule_once(lambda dt: self.enable_save_button(), _ENABLE_BUTTON_CLOCK_SECONDS)
    def enable_save_button(self):
        self.save_button.disabled = False
    def enable_cancel_button(self):
        self.cancel_button.disabled = False
    def on_cancel(self, instance):
        self.cancel_button.disabled = True
        self.app.config = self.original_config.copy()
        # Revert UI elements
        self.lang_selector.dropdown_button.text = self.app.config["language"]
        self.chart_type_selector.dropdown_button.text = self.app.config["chart_type"]
        self.ayanamsa_selector.dropdown_button.text = self.app.config["ayanamsa_mode"]
        self.splash_toggle.state = "down" if self.app.config["show_splash"] else "normal"
        self.splash_toggle.text = "Show Splash Screen" if self.app.config["show_splash"] else "Skip Splash Screen"
    
        chart_name = self.chart_selector.selected_value
        chart_index = self.chart_names.index(chart_name)+1 # +1 to skip Raasi
        methods, default_index = self.get_varga_methods(chart_index)
        self.method_selector.values = methods
        self.method_selector.dropdown_button.text = methods[default_index - 1]# if default_index > 0 else "Select Method"
        self.app.indic_tab_widget.select_tab(self.app.last_selected_tab)
        Clock.schedule_once(lambda dt: self.enable_save_button(), _ENABLE_BUTTON_CLOCK_SECONDS)
        self.cancel_button.disabled = False

def GetLabelWidget(text, font_name=const.FONT_NAMES[const._DEFAULT_LANGUAGE][0],color=_LABEL_WIDGET_COLOR, **kwargs):
    kwargs['color'] = color  # Ensure color is passed to both types
    if font_name and font_name != const.FONT_NAMES['en'][0]:
        return IndicLabel(text=text, font_name=font_name, **kwargs)
    else:
        kwargs.pop('font_name', None)
        kwargs.pop('font_path', None)
        return Label(text=text,**kwargs)
def GetButtonWidget(text, font_name=None, on_press_callback=None,color=_BUTTON_WIDGET_COLOR, **kwargs):
    kwargs.setdefault('size_hint_x', None)
    kwargs.setdefault('size_hint_y', None)
    kwargs.setdefault('height', dp(40))
    kwargs['color'] = color

    if font_name and font_name != const.FONT_NAMES['en'][0]:
        return IndicButton(text=text, font_name=font_name, on_press_callback=on_press_callback, **kwargs)
    else:
        return LabelButton(text=text,on_press_callback=on_press_callback, **kwargs)

def GetTabButton(text, font_name=None,color=_BLACK_COLOR, **kwargs):
    kwargs['color'] = color  # Ensure color is passed to both types
    kwargs.setdefault('size_hint_x', None)
    kwargs.setdefault('size_hint_y', None)
    kwargs.setdefault('height', dp(40))
    
    if font_name and font_name != const.FONT_NAMES['en'][0]:
        # Only IndicTabButton supports background_color
        kwargs.setdefault('background_color', _BUTTON_BG_COLOR)
        kwargs.setdefault('width', dp(_INDIC_TAB_WIDTH))  # Indic tab
        kwargs.setdefault('font_size',_INDIC_TAB_FONT_SIZE)  # Indic tab
        return IndicTabButton(text=text, font_name=font_name, **kwargs)
    else:
        kwargs.setdefault('width', dp(_ENGLISH_TAB_WIDTH))  # English tab
        kwargs.setdefault('font_size',_ENGLISH_TAB_FONT_SIZE)  # Englis tab
        class StandardTabButton(ButtonBehavior, Label):
            def __init__(self, **kwargs):
                kwargs.setdefault('size_hint_x', None)
                super().__init__(**kwargs)
        kwargs.pop('font_name', None)
        kwargs.pop('font_path', None)
        return StandardTabButton(text=text, **kwargs)
def _resolve_font_path(font_name):
        for lang, (name, path) in const.FONT_NAMES.items():
            if name == font_name:
                return const.get_resource_path(path)
        return None  # fallback if not found

class LabelButton(ButtonBehavior, Label):
    def __init__(self, text, on_press_callback=None,color=_BLACK_COLOR, **kwargs):
        kwargs['text'] = text
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('size', (dp(400), dp(40)))
        kwargs['color'] = color  # Ensure color is passed to both types
        super().__init__(**kwargs)

        self.on_press_callback = on_press_callback
        self.halign = 'center'
        self.valign = 'middle'
        self.pos_hint = {'center_x': 0.5}
        self.text_size = self.size
        self.padding = (dp(10), dp(10))
        self.bind(size=self._update_text_size)

        with self.canvas.before:
            self.bg_color = Color(*_BUTTON_BG_COLOR)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])

        self.bind(pos=self.update_bg, size=self.update_bg)
    def _update_text_size(self, *args):
        self.text_size = self.size

    def update_bg(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_press(self):
        if _DEBUG_: print("JHora: Disabling LabelButton")
        self.disabled = True
        self.bg_color.rgba = [0.1, 0.4, 0.7, 1]  # darker shade
        if self.on_press_callback:
            self.on_press_callback(self.text)
        if _DEBUG_: print("JHora: Enabling LabelButton")
        # Re-enable after short delay
        Clock.schedule_once(lambda dt: self.enable_button(), _ENABLE_BUTTON_CLOCK_SECONDS)

    def enable_button(self):
        self.disabled = False
        
    def on_release(self):
        self.bg_color.rgba = _BUTTON_BG_COLOR  # restore original
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
class IndicLabel(Widget):
    text = StringProperty("வணக்கம்")
    font_path = StringProperty('')
    font_name = StringProperty('')
    font_size = NumericProperty(_INDIC_LABEL_FONT_SIZE)
    text_size = ListProperty([None, None])
    texture_size = ListProperty([0, 0])
    line_spacing = NumericProperty(1.2)
    wrap_width = NumericProperty(600)
    color = ListProperty([0.6, 1.0, 1.0])
    halign = StringProperty("left")
    valign = StringProperty("bottom")
    markup = BooleanProperty(False)
    bold = BooleanProperty(True)
    italic = BooleanProperty(False)
    underline = BooleanProperty(False)
    draw_background = BooleanProperty(False)
    background_color = ListProperty([0, 0, 0, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.font_name != const.FONT_NAMES['en'][0]:
            self.font_path = _resolve_font_path(self.font_name)

        self.bind(size=self._update_text_size)
        self.bind(text=self._schedule_texture_update,
                  font_size=self._schedule_texture_update,
                  pos=self._schedule_texture_update,
                  wrap_width=self._schedule_texture_update)

        if self.text.strip() and self.font_name != const.FONT_NAMES['en'][0]:
            self._schedule_texture_update()

        if self.draw_background:
            with self.canvas.before:
                Color(*self.background_color)
                self._bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.bind(pos=self._update_bg_rect, size=self._update_bg_rect, background_color=self._update_bg_color)

    def _update_bg_rect(self, *args):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size

    def _update_bg_color(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.background_color)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)

    def _update_text_size(self, *args):
        self.text_size = self.size

    def set_text(self, text):
        self.text = text
        self._schedule_texture_update()

    def _shape_line(self, line, hb_font, hb):
        buf = hb.Buffer()
        buf.add_str(line)
        buf.guess_segment_properties()
        hb.shape(hb_font, buf)
        return buf.glyph_infos, buf.glyph_positions

    def _update_texture(self, *args):
        if not self.text.strip():
            return

        if self.font_name == const.FONT_NAMES['en'][0]:
            return  # Skip rendering for English

        # ✅ Safe imports for non-English fonts only
        import uharfbuzz as hb
        import cairo

        try:
            with open(self.font_path, "rb") as fontfile:
                fontdata = fontfile.read()
        except Exception as e:
            print(f"Error loading font:{self.font_name} {self.font_path} {e}")
            return

        hb_blob = hb.Blob(fontdata)
        hb_face = hb.Face(hb_blob)
        hb_font = hb.Font(hb_face)
        hb_font.scale = (self.font_size * 64, self.font_size * 64)

        plain_text = self.text.replace("&lt;br&gt;", "\n")
        avg_char_width = self.font_size * 0.6
        max_chars_per_line = max(1, int(self.wrap_width / avg_char_width))

        import textwrap
        raw_lines = plain_text.split("\n")
        lines = []
        for raw_line in raw_lines:
            wrapped = textwrap.wrap(raw_line, width=max_chars_per_line)
            lines.extend(wrapped if wrapped else [""])

        shaped_lines = []
        max_line_width = 0
        for line in lines:
            infos, positions = self._shape_line(line, hb_font, hb)
            if positions:
                advance_x = sum(pos.x_advance for pos in positions) / 64.0
                max_line_width = max(max_line_width, advance_x)
                shaped_lines.append((infos, positions))

        margin = 10
        line_height = int(self.font_size * self.line_spacing)
        total_text_height = line_height * len(shaped_lines)
        width = int(max_line_width + 2 * margin)
        height = int(total_text_height + 2 * margin)

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        context = cairo.Context(surface)

        context.set_source_rgba(*self.background_color)
        context.rectangle(0, 0, width, height)
        context.fill()

        face = cairo.ToyFontFace(self.font_name, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.set_font_face(face)
        context.set_font_size(self.font_size)

        if self.valign == 'middle':
            y_offset = (height - total_text_height) / 2
        elif self.valign == 'top':
            y_offset = height - total_text_height - margin
        else:
            y_offset = margin

        for line_index, (infos, positions) in enumerate(shaped_lines):
            line_width = sum(pos.x_advance for pos in positions) / 64.0
            if self.halign == 'center':
                x_offset = (width - line_width) / 2
            elif self.halign == 'right':
                x_offset = width - line_width - margin
            else:
                x_offset = margin

            x, y = 0, 0
            glyphs = []
            for info, pos in zip(infos, positions):
                gid = info.codepoint
                gx = x + pos.x_offset / 64.0
                gy = -pos.y_offset / 64.0
                glyphs.append(cairo.Glyph(gid, gx, gy))
                x += pos.x_advance / 64.0
                y += pos.y_advance / 64.0

            context.save()
            context.translate(x_offset, y_offset + line_index * line_height + self.font_size)
            r, g, b = self.color[:3]
            context.set_source_rgb(r, g, b)
            context.show_glyphs(glyphs)
            context.restore()

        buf = surface.get_data()
        from kivy.graphics.texture import Texture
        texture = Texture.create(size=(width, height))
        texture.blit_buffer(buf, colorfmt='bgra', bufferfmt='ubyte')
        texture.flip_vertical()

        self.texture = texture
        self.texture_size = [width, height]
        self.size_hint_y = None
        self.height = height
        self.width = width

        self.canvas.clear()
        with self.canvas:
            Rectangle(texture=self.texture, pos=self.pos, size=self.texture_size)

        if list(self.size) != self.texture_size:
            self.size = self.texture_size

    def _schedule_texture_update(self, *args):
        if self.font_name == const.FONT_NAMES['en'][0]:
            return  # Skip texture update for English
        Clock.unschedule(self._update_texture)
        Clock.schedule_once(self._update_texture, 0)

    
class IndicButton(ButtonBehavior, IndicLabel):
    def __init__(self, text, font_name, on_press_callback=None, **kwargs):
        kwargs['text'] = text
        kwargs['font_name'] = font_name
        kwargs['draw_background'] = True  # ✅ Enable background drawing
        kwargs.setdefault('background_color', _BUTTON_BG_COLOR)
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        #self.size = (dp(150), dp(40))
        #self.background_normal = ''
        #self.background_color = _BUTTON_BG_COLOR
        #self.color = _BROWN_COLOR
        self.on_press_callback = on_press_callback

        #if font_name != const.FONT_NAMES['en'][0]:
        #    self.font_path = _resolve_font_path(font_name)

        #self.bind(background_color=self._update_texture)

    def on_press(self):
        self.background_color = [0.1, 0.4, 0.7, 1]  # darker shade
        if _DEBUG_: print("JHora: Disabling IndicButton")
        self.disabled = True
        if self.on_press_callback:
            self.on_press_callback(self.text)
        if _DEBUG_: print("JHora: Enabling IndicButton")
        # Re-enable after short delay
        Clock.schedule_once(lambda dt: self.enable_button(), _ENABLE_BUTTON_CLOCK_SECONDS)
 
    def enable_button(self):
        self.disabled = False
    def on_release(self):
        self.background_color = _BUTTON_BG_COLOR  # restore original


# Use your existing IndicLabel
class IndicScrollSelector(BoxLayout):
    items = ListProperty([])
    selected_index = NumericProperty(0)
    font_name = StringProperty('')
    font_path = StringProperty('')
    on_select = ObjectProperty(None)

    def __init__(self, items, font_name, on_select=None, **kwargs):
        super().__init__(orientation='horizontal', spacing=10,
                         size_hint=(None, None), size=(dp(300), dp(50)), **kwargs)

        self.font_name = font_name
        self.font_path = _resolve_font_path(font_name) if font_name != const.FONT_NAMES['en'][0] else ""
        self.on_select = on_select
        self.selected_index = 0
        self.spacing = _INDIC_SCROLL_SPACING; self.padding = _INDIC_SCROLL_PADDING
        # Convert items to dict format if needed
        if items and isinstance(items[0], str):
            items = [{'text': key, 'index': i} for i, key in enumerate(items)]
        self.items = items

        left_icon = const.get_resource_path("left_arrow.png")
        right_icon = const.get_resource_path("right_arrow.png")
        self.left_btn = Button(text='', size_hint=(None, None), size=(dp(_INDIC_SCROLL_BUTTON_SIZE), dp(_INDIC_SCROLL_BUTTON_SIZE)),
                               background_normal=left_icon,border=(0,0,0,0))#, background_color=_BUTTON_BG_COLOR, color=_BROWN_COLOR)
        self.right_btn = Button(text='', size_hint=(None, None), size=(dp(_INDIC_SCROLL_BUTTON_SIZE), dp(_INDIC_SCROLL_BUTTON_SIZE)),
                                background_normal=right_icon,border=(0,0,0,0))#, background_color=_BUTTON_BG_COLOR, color=_BROWN_COLOR)

        self.label = GetLabelWidget(
            text=self.items[self.selected_index]['text'] if self.items else '',
            font_name=self.font_name,
            font_path=self.font_path,
            size_hint=(1, 1),
            halign='center', valign='middle',
            color=_LABEL_WIDGET_COLOR,
            font_size = _INDIC_SCROLL_LABEL_FONT_SIZE
        )
        self.label.bind(size=self.update_text_size)

        self.left_btn.bind(on_press=self.scroll_left)
        self.right_btn.bind(on_press=self.scroll_right)

        self.add_widget(self.left_btn)
        self.add_widget(self.label)
        self.add_widget(self.right_btn)

    def update_text_size(self, instance, value):
        self.label.text_size = self.label.size
    def scroll_right(self, *args):
        if _DEBUG_: print("JHora: Disabling Right Button")
        self.right_btn.disabled = True
        if self.selected_index < len(self.items) - 1:
            self.selected_index += 1
            self.update_display()
            if self.on_select and self.items:
                self.on_select(self, self.selected_index, self.items[self.selected_index])
        if _DEBUG_: print("JHora: Enabling Right Button")
        Clock.schedule_once(lambda dt: self.enable_right_button(), _ENABLE_BUTTON_CLOCK_SECONDS)
    def enable_right_button(self):
        self.right_btn.disabled = False
    def scroll_left(self, *args):
        self.left_btn.disabled = True
        if _DEBUG_: print("JHora: Disabling Left Button")
        if self.selected_index > 0:
            self.selected_index -= 1
            self.update_display()
            if self.on_select and self.items:
                self.on_select(self, self.selected_index, self.items[self.selected_index])
        if _DEBUG_: print("JHora: Enabling Left Button")
        Clock.schedule_once(lambda dt: self.enable_left_button(), _ENABLE_BUTTON_CLOCK_SECONDS)
    def enable_left_button(self):
        self.left_btn.disabled = False
    def update_display(self,trigger_callback=True):
        if self.items:
            self.label.text = self.items[self.selected_index]['text']
            if trigger_callback and self.on_select:
                self.on_select(self, self.selected_index, self.items[self.selected_index])

    def set_items(self, items):
        if items and isinstance(items[0], str):
            items = [{'text': key, 'index': i} for i, key in enumerate(items)]
        self.items = items
        self.selected_index = 0
        self.update_display()

    def set_callback(self, callback):
        self.on_select = callback
    def set_selector_callback(self, index, callback):
        if 0 <= index < len(self.content_widgets):
            layout = self.content_widgets[index]
            if hasattr(layout, 'selector') and layout.selector:
                layout.selector.set_callback(callback)
    def on_item_selected(self, index):
        self.selected_index = index  # Update internal state
        if self.on_select:
            self.on_select(self, index, self.items[index])


            
class IndicTabButton(ButtonBehavior, IndicLabel):
    def __init__(self, **kwargs):
        kwargs.setdefault('size_hint_x', None)
        super().__init__(**kwargs)
        self.font_size = _INDIC_BUTTON_FONT_SIZE

# Your existing IndicLabel is used for both tabs and content
class ScrollableIndicLabel(ScrollView):
    text = StringProperty('')
    font_name = StringProperty('')

    def __init__(self, text="", font_name="", **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_name = font_name
        self.do_scroll_x = True
        self.do_scroll_y = True
        self.size_hint = (1, 1)

        self.label = GetLabelWidget(
            text=self.text,
            font_name=self.font_name,
            markup=True,
            size_hint_y=None,
            text_size=(None, None)
        )
        self.label.bind(texture_size=self._update_height)
        self.bind(width=self._update_text_width)

        self.add_widget(self.label)

    def _update_height(self, instance, value):
        self.label.height = value[1]

    def _update_text_width(self, instance, value):
        self.label.text_size = (value, None)

    def set_text(self, text):
        #print(self.label,'scrollableLable setting text',text)
        self.label.text = text

    def set_font(self, font_name):
        self.label.font_name = font_name

class IndicTabWidget(BoxLayout):
    tabs = ListProperty()
    contents = ListProperty()
    font_name = StringProperty()
    show_selector = ListProperty()
    widget_classes = ListProperty()
    on_tab_selected = ObjectProperty()

    def __init__(self, widget_classes=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.widget_classes = widget_classes or [ScrollableIndicLabel] * len(self.tabs)

        self.tab_bar = BoxLayout(size_hint_y=None, height=dp(40))
        self.add_widget(self.tab_bar)

        self.content_area = BoxLayout(orientation='vertical', size_hint=(1, 1))
        self.add_widget(self.content_area)

        self.tabs_widgets = []
        self.content_widgets = []

        self._build_tabs_and_contents()

    def _build_tabs_and_contents(self):
        self.tab_bar.clear_widgets()
        self.content_area.clear_widgets()
        self.tabs_widgets = []
        self.content_widgets = []

        for i, tab_text in enumerate(self.tabs):
            self._create_tab(i, tab_text, self.contents[i], self.widget_classes[i], self.show_selector[i])

        if self.tabs:
            self.select_tab(0)

    def _create_tab(self, index, title, content, widget_class, show_selector):
        tab = GetTabButton(text=title, font_name=self.font_name,size_hint_x=1,
                           size_hint_y=None, height=dp(40))
        tab.font_size = _INDIC_TAB_FONT_SIZE
        with tab.canvas.before:
            tab.bg_color = Color(0.8, 0.8, 0.9, 1)
            tab.bg_rect = Rectangle(pos=tab.pos, size=tab.size)
        tab.bind(pos=self._update_tab_bg, size=self._update_tab_bg)
        tab.bind(on_release=lambda btn, idx=index: self._safe_select_tab(btn, idx))

        self.tab_bar.add_widget(tab)
        self.tabs_widgets.append(tab)

        tab_content_layout = BoxLayout(orientation='vertical', size_hint=(1, 1))

        if show_selector:
            selector = IndicScrollSelector(items=[''], font_name=self.font_name,
                                           size_hint_y=None, height=dp(40))
            tab_content_layout.selector = selector
            tab_content_layout.add_widget(selector)
        else:
            tab_content_layout.selector = None

        if widget_class == ScrollableIndicLabel:
            content_widget = ScrollableIndicLabel(text=content, font_name=self.font_name,
                                                  size_hint=(1, 1))
        elif widget_class == IndicTableWidget:
            content_widget = IndicTableWidget(headers=[], table_data=[], font_name=self.font_name,
                                              size_hint=(1, 1))
        else:
            raise ValueError(f"Unsupported widget class at index {index}: {widget_class}")

        tab_content_layout.widget = content_widget
        tab_content_layout.add_widget(content_widget)

        self.content_widgets.append(tab_content_layout)
    def _safe_select_tab(self, tab_button, index):
        if tab_button.disabled:
            return
        tab_button.disabled = True
        self.select_tab(index)
        Clock.schedule_once(lambda dt: self._enable_tab_button(tab_button), 0.2)
    
    def _enable_tab_button(self, tab_button):
        tab_button.disabled = False
    def add_tab(self, title, content='', widget_class=ScrollableIndicLabel, show_selector=False):
        index = len(self.tabs_widgets)
        self.tabs.append(title)
        self.contents.append(content)
        self.widget_classes.append(widget_class)
        self.show_selector.append(show_selector)
        self._create_tab(index, title, content, widget_class, show_selector)

    def _update_tab_bg(self, instance, *args):
        instance.bg_rect.pos = instance.pos
        instance.bg_rect.size = instance.size

    def select_tab(self, index, trigger_callback=True):
        if 0 <= index < len(self.content_widgets):
            self.content_area.clear_widgets()
            layout = self.content_widgets[index]
            self.content_area.add_widget(layout)

            if hasattr(layout, 'selector') and layout.selector:
                layout.selector.index = 0
                layout.selector.update_display(trigger_callback=trigger_callback)

            # 🔔 Trigger external callback if defined
            if self.on_tab_selected:
                self.on_tab_selected(index)

    def update_tab_content(self, index, new_text_or_data):
        if 0 <= index < len(self.content_widgets):
            layout = self.content_widgets[index]
            widget = getattr(layout, 'widget', None)

            if widget is None:
                return

            if isinstance(widget, ScrollableIndicLabel):
                if hasattr(widget, 'set_text') and callable(widget.set_text):
                    widget.set_text(new_text_or_data)
                else:
                    widget.text = new_text_or_data
                #widget.text = new_text_or_data
                if hasattr(widget.label, 'update_texture'):
                    widget.label.update_texture()

            elif isinstance(widget, IndicTableWidget):
                if isinstance(new_text_or_data, tuple) and len(new_text_or_data) == 2:
                    headers, table_data = new_text_or_data
                    widget.set_data(headers, table_data)

    def set_selector_items(self, index, items):
        if 0 <= index < len(self.content_widgets):
            layout = self.content_widgets[index]
            if hasattr(layout, 'selector') and layout.selector:
                layout.selector.set_items(items)

    def set_selector_callback(self, index, callback):
        if 0 <= index < len(self.content_widgets):
            layout = self.content_widgets[index]
            if hasattr(layout, 'selector') and layout.selector:
                layout.selector.on_select = callback

    def update_selector(self, index, items=None, callback=None):
        if 0 <= index < len(self.content_widgets):
            layout = self.content_widgets[index]
            if hasattr(layout, 'selector') and layout.selector:
                if items is not None:
                    layout.selector.set_items(items)
                if callback is not None:
                    layout.selector.on_select = callback


class IndicTableWidget(ScrollView):
    font_name = StringProperty()
    def __init__(self, headers=None, table_data=None, **kwargs):
        super().__init__(**kwargs)
        self.do_scroll_x = True
        self.do_scroll_y = True
        self.size_hint = (1, 1)

        self.headers = headers or []
        self.table_data = table_data or []

        self.grid = GridLayout(cols=1, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.add_widget(self.grid)

        if self.table_data:
            self.set_data(self.headers, self.table_data)

    def set_data(self, headers, table_data):
        self.headers = headers or []
        self.table_data = table_data or []

        # Clear existing widgets
        self.grid.clear_widgets()

        # Determine number of columns
        num_cols = len(self.headers) if self.headers else max(len(row) for row in self.table_data)
        self.grid.cols = num_cols
        self.grid_rows = len(table_data)
        # Add headers if present
        if self.headers:
            for header in self.headers:
                label = GetLabelWidget(text=str(header), bold=True, size_hint_y=None, height=dp(30),
                                                    font_name=self.font_name)
                # Only bind if it's a standard Label (i.e., English)
                if isinstance(label, Label):
                    label.halign = 'left'; label.valign = 'top'
                    label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
                    label.texture_update()
                    label.height = label.texture_size[1]
                self.grid.add_widget(label)
        # Add table data
        for row in self.table_data:
            for cell in row:
                label = GetLabelWidget(text=str(cell), size_hint_y=None, height=dp(30),
                                                    font_name=self.font_name)
                # Only bind if it's a standard Label (i.e., English)
                if isinstance(label, Label):
                    label.halign = 'left'; label.valign = 'top'
                    label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
                    label.texture_update()
                    label.height = label.texture_size[1]
                self.grid.add_widget(label)

class TableApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.table = IndicTableWidget(font_name=const.FONT_NAMES['en'][0])

        layout.add_widget(self.table)

        # Button to load data
        btn = Button(text="Load Data", size_hint_y=None, height=50)
        btn.bind(on_press=self.load_data_en)
        layout.add_widget(btn)

        return layout

    def load_data(self, instance):
        headers = ['', 'ஷத் வர்க விம்சோபக பலம்']
        table_data = [
            ['சூரியன்', 'கிம்சுகாராம்சம்\n(D1/D3)\n16.6'],
            ['சந்திரன்','அம்சம் இல்லை\n15.0'],
            ['செவ்வாய்','கிம்சுகாராம்சம்\n(D2/D30)\n15.8'],
            ['புதன்','பஞ்சசாராம்சம்\n(D1/D3/D12)\n16.1'],
            ['குரு','அம்சம் இல்லை\n11.0'],
            ['சுக்கிரன்','அம்சம் இல்லை\n9.0'],
            ['சனி','அம்சம் இல்லை\n11.2'],
            ['ராகு','அம்சம் இல்லை\n(D12)\n12.5'],
            ['கேது','அம்சம் இல்லை\n(D9)\n12.8']
        ]
        self.table.set_data(headers, table_data)
    def load_data_en(self, instance):
        headers = ['', 'Table Title']
        table_data = [
            ['Row-1,Column-1', 'Row-1\nColumn-2'],
            ['Row-2,Column-1', 'Row-2\nColumn-2'],
            ['Row-3,Column-1', 'Row-3\nColumn-2'],
            ['Row-4,Column-1', 'Row-4\nColumn-2'],
            ['Row-5,Column-1', 'Row-5\nColumn-2'],
            ['Row-1,Column-6', 'Row-6\nColumn-2'],
            ['Row-1,Column-7', 'Row-7\nColumn-2'],
        ]
        self.table.set_data(headers, table_data)

# --- Main App ---
class IndicTestApp(App):
    def build(self):
        lang = 'ta' # 'ta'#
        root = BoxLayout(orientation='vertical', spacing=10, padding=10)
        """
        # 1. Simple Label
        label = GetLabelWidget(
            text="வணக்கம்! இது ஒரு லேபிள்.",
            font_size=32,
            font_path=const.get_resource_path(const.FONT_NAMES[lang][1]),
            font_name=const.FONT_NAMES[lang][0]
        )
        root.add_widget(label)
        """
        """
        # 2. Scrollable Label
        long_text_str = "தமிழ் ஒரு செழுமையான மொழி.\n"
        long_text = ''.join([f"{i+1} {long_text_str}" for i in range(20)])
        scroll = ScrollView(size_hint=(1, 0.4))
        scroll_label = GetLabelWidget(
            text=long_text,
            font_size=24,
            font_path=const.get_resource_path(const.FONT_NAMES[lang][1]),
            font_name=const.FONT_NAMES[lang][0]
        )
        scroll.add_widget(scroll_label)
        root.add_widget(scroll)
        """
        #"""
        # 3. Button
        button_text = 'Krithika' if lang=='en' else "கிருத்திகை"
        button = GetButtonWidget(
            text=button_text,
            font_size=32,
            size_hint=(1, None),#0.2),
            font_name=const.FONT_NAMES[lang][0],
        )
        root.add_widget(button)
        #"""
        """
        # 4. Tabbed Panel with Scrollable Content
        tab_names = ["ஞாயிற்றுக்கிழமை", "திங்கட்கிழமை"]
        tabs = IndicTabbedPanel(
            tab_names=tab_names,
            font_name=const.FONT_NAMES[lang][0],
            size_hint_y=None
        )

        for t in range(len(tab_names)):
            content_text = tab_names[t] + ' ' + 'கேது☋,அருணா⛢,வருணா♆,குறுகோள்♇'
            scroll = ScrollView()
            content_label = GetLabelWidget(
                text=content_text,
                font_size=18,
                font_name=const.FONT_NAMES[lang][0],
                size_hint_y=0.4
            )
            scroll.add_widget(content_label)
            tabs.tab_list[t].content.clear_widgets()
            tabs.tab_list[t].content.add_widget(scroll)
            tabs.content_labels[t] = content_label
            tabs.content_texts[t] = content_text

        root.add_widget(tabs)
        """
        """
        #5. Radio Button
        rad = IndicRadioButton(text='கேது☋,அருணா⛢,வருணா♆,குறுகோள்♇',font_name=const.FONT_NAMES[lang][0],group='test')
        root.add_widget(rad)
        """
        tabs=["Tithi", "Nakshathram", "Yogam","Table"] if lang== 'en' else ["திதி", "நட்சத்திரம்", "யோகம்","Table"]
        widget_classes = [ScrollableIndicLabel,ScrollableIndicLabel,ScrollableIndicLabel, IndicTableWidget]
        #contents=["இன்று சப்தமி திதி.\nஇது முக்கியமான நாள்.","நட்சத்திரம்: புனர்பூசம்.\nஅதிர்ஷ்டம் அதிகம்.","யோகம்: சித்த யோகம்.\nநல்ல நேரம்."]
        contents = tabs[:]
        indic_tab_widget = IndicTabWidget(tabs=tabs,contents=contents,font_name=const.FONT_NAMES[lang][0],
                                          show_selector=[False,True,True,True],widget_classes=widget_classes)
        root.add_widget(indic_tab_widget)
        def _on_panchangam_selected(widget, item_index, item):
            tab_index = 1  # Panchangam tab
            results_text = f"{item['text']} - Selected Index: {item_index}"
            indic_tab_widget.update_tab_content(tab_index, results_text)
        
        def _on_dhasa_selected(widget, item_index, item):
            tab_index = 2  # Dhasa tab
            results_text = f"{item['text']} - Selected Index: {item_index}"
            indic_tab_widget.update_tab_content(tab_index, results_text)
        #"""
        tab1_items_en = ['Viskamba','Prithi','Ayushmaan']; tab1_items_ta = ['விஸ்கம்பா','ப்ரிதி','ஆயுஷ்மான்']
        tab1_menu_items_en = [{'text': key,'index': i} for i, key in enumerate(tab1_items_en)]
        tab1_menu_items_ta = [{'text': key,'index': i} for i, key in enumerate(tab1_items_ta)]
        indic_tab_widget.set_selector_items(1, tab1_menu_items_en) if lang== 'en' else \
                        indic_tab_widget.set_selector_items(1, tab1_menu_items_ta)
        indic_tab_widget.set_selector_callback(1, _on_panchangam_selected)
        
        tab2_items_en = ['Ashvini','Bharani','Krithika']; tab2_items_ta = ['அஸ்வினி','பரணி','கிருத்திகை']
        tab2_menu_items_en = [{'text': key,'index': i} for i, key in enumerate(tab2_items_en)]
        tab2_menu_items_ta = [{'text': key,'index': i} for i, key in enumerate(tab2_items_ta)]
        indic_tab_widget.set_selector_items(2, tab2_menu_items_en) if lang== 'en' else \
                        indic_tab_widget.set_selector_items(2, tab2_menu_items_ta)
        indic_tab_widget.set_selector_callback(2, _on_dhasa_selected)
        
        indic_tab_widget.update_tab_content(3, (["Planet", "Sign"], [["Sun", "Leo"], ["Moon", "Cancer"]]))

        #"""
        return root
# Dummy app object with config and res
class DummyApp:
    def __init__(self):
        self.config = {
            "language": "en",
            "ayanamsa_mode": "Lahiri",
            "show_splash": True
        }
        self.res = utils.resource_strings

# Now define SettingsTab using the final version from earlier
# Paste the final SettingsTab class here or import it

class TestSettingsApp(App):
    def build(self):
        dummy_app = DummyApp()
        return SettingsTab(app=dummy_app)

if __name__ == '__main__':
    #TableApp().run()
    #TestSettingsApp().run()
    TableApp().run()
    #TestApp().run()
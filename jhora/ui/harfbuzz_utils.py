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
from kivy.graphics.texture import Texture
from kivy.graphics import Rectangle
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.button import Button
from kivy.uix.label import Label
import re
import textwrap
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

from jhora.panchanga import drik, vratha, pancha_paksha,info
from jhora import utils, const
cairo = const.get_cairo()
hb = const.get_harfbuzz()

class IndicWidget(RelativeLayout):
    text = StringProperty("வணக்கம்")
    font_path = StringProperty('')
    font_name = StringProperty('')
    font_size = NumericProperty(24)
    text_size = ListProperty([None, None])  # Add this line
    texture_size = ListProperty([0, 0])
    line_spacing = NumericProperty(1.2)
    wrap_width = NumericProperty(600)
    color = ListProperty([0, 0, 0])  # Default: black (RGB)
    # Other possible common properties
    halign = StringProperty("left")
    valign = StringProperty("bottom")
    text_size = ListProperty([None, None])
    markup = BooleanProperty(False)
    bold = BooleanProperty(False)
    italic = BooleanProperty(False)
    underline = BooleanProperty(False)
    background_color = ListProperty([1, 1, 1, 1])  # For Button compatibility

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.text.strip() == '': return
        self.bind(text=self._update_texture,
                  font_size=self._update_texture,
                  pos=self._update_texture,
                  wrap_width=self._update_texture)
        self._update_texture()

    def _shape_line(self, line, hb_font):
        buf = hb.Buffer()
        buf.add_str(line)
        buf.guess_segment_properties()
        hb.shape(hb_font, buf)
        return buf.glyph_infos, buf.glyph_positions

    def _update_texture(self, *args):
        try:
            with open(self.font_path, "rb") as fontfile:
                fontdata = fontfile.read()
        except Exception as e:
            print(f"Error loading font: {e}")
            return

        hb_blob = hb.Blob(fontdata)
        hb_face = hb.Face(hb_blob)
        hb_font = hb.Font(hb_face)
        hb_font.scale = (self.font_size * 64, self.font_size * 64)
        # Preserve line breaks
        plain_text = self.text.replace("<br>", "\n")

        avg_char_width = self.font_size * 0.6
        max_chars_per_line = max(1, int(self.wrap_width / avg_char_width))

        # Split by line breaks and wrap each line
        raw_lines = plain_text.split("\n")
        lines = []
        for raw_line in raw_lines:
            wrapped = textwrap.wrap(raw_line, width=max_chars_per_line)
            lines.extend(wrapped if wrapped else [""])  # preserve empty lines

        shaped_lines = []
        max_line_width = 0
        for line in lines:
            infos, positions = self._shape_line(line, hb_font)
            #print('harfbuzz',line,infos,positions)
            if positions:
                advance_x = sum(pos.x_advance for pos in positions) / 64.0
                max_line_width = max(max_line_width, advance_x)
                shaped_lines.append((infos, positions))

        margin = 10
        width = int(max_line_width + 2 * margin)
        line_height = int(self.font_size * self.line_spacing)
        height = int(line_height * len(shaped_lines) + 2 * margin)

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        context = cairo.Context(surface)

        context.set_source_rgb(1, 1, 1)
        context.paint()

        face = cairo.ToyFontFace(self.font_name, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.set_font_face(face)
        context.set_font_size(self.font_size)
        r, g, b = self.color[:3]
        context.set_source_rgb(r, g, b)

        context.translate(margin, margin + self.font_size)

        for line_index, (infos, positions) in enumerate(shaped_lines):
            glyphs = []
            x, y = 0, 0
            for info, pos in zip(infos, positions):
                gid = info.codepoint
                x_offset = pos.x_offset / 64.0
                y_offset = -pos.y_offset / 64.0
                x_advance = pos.x_advance / 64.0
                y_advance = -pos.y_advance / 64.0

                gx = x + x_offset
                gy = y + y_offset
                glyphs.append(cairo.Glyph(gid, gx, gy))
                x += x_advance
                y += y_advance

            context.save()
            context.translate(0, line_index * line_height)
            context.show_glyphs(glyphs)
            context.restore()

        buf = surface.get_data()
        texture = Texture.create(size=(width, height))
        texture.blit_buffer(buf, colorfmt='bgra', bufferfmt='ubyte')
        texture.flip_vertical()

        self.texture_size = [width, height]
        self.size_hint_y = None
        self.height = height  # Important for ScrollView

        self.canvas.clear()
        with self.canvas:
            Rectangle(texture=texture, pos=self.pos, size=self.texture_size)

        if list(self.size) != self.texture_size:
            self.size = self.texture_size
    
class IndicTextWidget(Widget):
    text = StringProperty("வணக்கம்")
    font_path = StringProperty(const.get_resource_path(const.FONT_NAMES[const._DEFAULT_LANGUAGE][1]))
    font_name = StringProperty(const.FONT_NAMES[const._DEFAULT_LANGUAGE][0])
    font_size = NumericProperty(48)
    texture_size = ListProperty([0, 0])
    color = ListProperty([0, 0, 0])  # Default: black (RGB)
    # Other possible common properties
    halign = StringProperty("left")
    valign = StringProperty("bottom")
    text_size = ListProperty([None, None])
    markup = BooleanProperty(False)
    bold = BooleanProperty(False)
    italic = BooleanProperty(False)
    underline = BooleanProperty(False)
    background_color = ListProperty([1, 1, 1, 1])  # For Button compatibility

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(text=self._update_texture,
                  font_size=self._update_texture,
                  pos=self._update_texture)
        self._update_texture()

    def _update_texture(self, *args):
        try:
            with open(self.font_path, "rb") as fontfile:
                fontdata = fontfile.read()
        except Exception as e:
            print(f"Error loading font: {e}")
            return

        hb_blob = hb.Blob(fontdata)
        hb_face = hb.Face(hb_blob)
        hb_font = hb.Font(hb_face)
        hb_font.scale = (self.font_size * 64, self.font_size * 64)

        buf = hb.Buffer()
        buf.add_str(self.text)
        buf.guess_segment_properties()
        hb.shape(hb_font, buf)

        infos = buf.glyph_infos
        positions = buf.glyph_positions

        total_advance_x = sum(pos.x_advance for pos in positions) / 64.0
        margin = 10
        width = int(total_advance_x + 2 * margin)
        height = int(self.font_size * 2)

        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
        context = cairo.Context(surface)

        context.set_source_rgb(1, 1, 1)
        context.paint()

        face = cairo.ToyFontFace(self.font_name, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        context.set_font_face(face)
        context.set_font_size(self.font_size)
        r, g, b,_ = self.color
        context.set_source_rgb(r, g, b)

        context.set_source_rgb(0, 0, 0)
        context.translate(margin, self.font_size + margin)

        glyphs = []
        x, y = 0, 0
        for info, pos in zip(infos, positions):
            gid = info.codepoint
            x_offset = pos.x_offset / 64.0
            y_offset = -pos.y_offset / 64.0
            x_advance = pos.x_advance / 64.0
            y_advance = -pos.y_advance / 64.0

            gx = x + x_offset
            gy = y + y_offset
            glyphs.append(cairo.Glyph(gid, gx, gy))
            x += x_advance
            y += y_advance

        context.show_glyphs(glyphs)

        buf = surface.get_data()
        texture = Texture.create(size=(width, height))
        texture.blit_buffer(buf, colorfmt='bgra', bufferfmt='ubyte')
        texture.flip_vertical()

        self.texture_size = [width, height]

        self.canvas.clear()
        with self.canvas:
            Rectangle(texture=texture, pos=self.pos, size=self.texture_size)

        # Only update size if it changed to avoid layout recursion
        if list(self.size) != self.texture_size:
            self.size = self.texture_size

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
_BROWN_COLOR = (0.6, 0.3, 0.0, 1); _WHITE_COLOR = (1,1,1,1); _GOLD_COLOR = (1, 0.843, 0, 1); _BUTTON_BG_COLOR=(0.2, 0.6, 0.9, 1)

class DemoApp(App):
    def build(self):
        layout = BoxLayout()
        jd = utils.julian_day_number(drik.Date(1996,12,7),(10,34,0))
        place = drik.Place('Chennai, India',13.0878,80.2785,5.5)
        lang = 'ta'
        utils.set_language(lang)
        results_dict = info.get_panchangam_resources(jd, place)
        results_text = '\n'.join(k+':'+v for k,v in results_dict.items())
        results_text = "சூரியன்☉\nசந்திரன்☾\nசெவ்வாய்♂"
        label = IndicTextScrollWidget(
                    text=results_text,
                    font_size=12,
                    size_hint=(None, None),
                    color = _BROWN_COLOR,
                    font_name=const.FONT_NAMES[lang][0],font_path=const.get_resource_path(const.FONT_NAMES[lang][1]),
                    #wrap_width=Window.width - 20
                )

        
        scroll = ScrollView(
                    size=(Window.width, Window.height),
                    size_hint=(None, None),
                    pos=(0, 0),
                    do_scroll_y=True,
                    do_scroll_x=False,
                    bar_width=10
                )
        scroll.add_widget(label)
        layout.add_widget(scroll)
        return layout
# --- Main App ---
class IndicTestApp(App):
    def build(self):
        lang = 'ta'
        root = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # 1. Simple Label
        label = IndicWidget(text="வணக்கம்! இது ஒரு லேபிள்.", font_size=32,
                           font_path=const.get_resource_path(const.FONT_NAMES[lang][1]),
                           font_name=const.FONT_NAMES[lang][0])
        root.add_widget(label)

        # 2. Scrollable Label
        long_text_str = "தமிழ் ஒரு செழுமையான மொழி.\n"; long_text = ''
        for i in range(20):
            long_text += str(i+1)+' '+long_text_str
        #long_text = "தமிழ் ஒரு செழுமையான மொழி.\n" * 20
        scroll = ScrollView(size_hint=(1, 0.4))
        scroll_label = IndicWidget(text=long_text, font_size=24,
                           font_path=const.get_resource_path(const.FONT_NAMES[lang][1]),
                           font_name=const.FONT_NAMES[lang][0])
        scroll.add_widget(scroll_label)
        root.add_widget(scroll)

        # 3. Button
        from kivy.uix.button import Button
        button = Button(text="அமுக்கவும்", font_size=32, size_hint=(1, 0.2),font_name=const.FONT_NAMES[lang][0])
        root.add_widget(button)


        # 4. Tabbed Panel
        tabs = TabbedPanel(do_default_tab=False, size_hint=(1, 0.6))
        for name in ["பக்கம் 1", "பக்கம் 2"]:
            tab = TabbedPanelItem(text=name,font_name=const.FONT_NAMES[lang][0])
            content_layout = BoxLayout(orientation='vertical', padding=10)
            content = IndicWidget(text=f"{name} ராகு☊,கேது☋,அருணா⛢,வருணா♆,குறுகோள்♇", font_size=32,
                           font_path=const.get_resource_path(const.FONT_NAMES[lang][1]),
                           font_name=const.FONT_NAMES[lang][0])
            content_layout.add_widget(content)
            tab.add_widget(content_layout)
            tabs.add_widget(tab)
        root.add_widget(tabs)

        return root

    
if __name__ == '__main__':
    #DemoApp().run()
    IndicTestApp().run()
        
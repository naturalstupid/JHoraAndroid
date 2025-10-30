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
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.graphics import Line, Color
from kivy.core.text import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle, Line
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.graphics import Color, Line
from kivy.uix.widget import Widget


from jhora import const
from jhora.ui.indic_widgets import IndicLabel,GetLabelWidget
_ganesha_icon = const.get_resource_path("lord_ganesha.jpg")
_DEFAULT_CHART_ICON_SIZE_FACTOR = 0.5
_DEFAULT_CHART_LABEL_FONT_SIZE = dp(13)
_DEFAULT_CHART_CAPTION_FONT_SIZE = dp(13)
_NORTH_CAPTION_CELL_ROW = -0.25; _NORTH_CAPTION_CELL_COL = 0
_NORTH_CAPTION_XALIGN = 'left'; _NORTH_CAPTION_YALIGN = 'top'
_CHART_GRID_LINE_COLOR = (1,1,1,1)
_CHART_SIZE_FACTOR = 1.0; _CHART_X=dp(10); _CHART_Y=dp(10)
east_house_map = [
            ((0, 1), 'center', 'center', None),      # House 1
            ((0, 0), 'right', 'top', 'Left'),        # House 2
            ((0, 0), 'left', 'bottom', 'Left'),      # House 3
            ((1, 0), 'center', 'center', None),      # House 4
            ((2, 0), 'left', 'top', 'Right'),        # House 5
            ((2, 0), 'right', 'bottom', 'Right'),    # House 6
            ((2, 1), 'center', 'center', None),      # House 7
            ((2, 2), 'left', 'bottom', 'Left'),      # House 8
            ((2, 2), 'right', 'top', 'Left'),        # House 9
            ((1, 2), 'center', 'center', None),      # House 10
            ((0, 2), 'right', 'bottom', 'Right'),    # House 11
            ((0, 2), 'left', 'top', 'Right'),        # House 12
        ]
south_house_map = [
            ((0, 1), 'center', 'center', None),      # House 1
            ((0, 2), 'center', 'center', None),        # House 2
            ((0, 3), 'center', 'center', None),      # House 3
            ((1, 3), 'center', 'center', None),      # House 4
            ((2, 3), 'center', 'center', None),        # House 5
            ((3, 3), 'center', 'center', None),    # House 6
            ((3, 2), 'center', 'center', None),      # House 7
            ((3, 1), 'center', 'center', None),      # House 8
            ((3, 0), 'center', 'center', None),        # House 9
            ((2, 0), 'center', 'center', None),      # House 10
            ((1, 0), 'center', 'center', None),    # House 11
            ((0, 0), 'center', 'center', None),        # House 12
        ]
north_house_map = [
            ((0, 1), 'left', 'center', 'Both'),        # House 1 Always Lagnam Position
            ((0, 0), 'center', 'top', 'Both'),      # House 2
            ((0, 0), 'left', 'center', 'Both'),        # House 3
            ((0, 0), 'center', 'bottom', 'Both'),      # House 4 OR ((0, 1), 'center', 'top', None),
            ((1, 0), 'left', 'center', 'Both'),      # House 5
            ((1, 0), 'center', 'bottom', 'Both'),        # House 6
            ((1, 0), 'right', 'center', 'Both'),    # House 7 OR ((1, 1), 'left', 'center', None),
            ((1, 1), 'center', 'bottom', 'Both'),      # House 8
            ((1, 1), 'right', 'center', 'Both'),      # House 9 
            ((1, 1), 'center', 'top', 'Both'),        # House 10
            ((0, 1), 'right', 'center', 'Both'),      # House 11
            ((0, 1), 'center', 'top', 'Both'),    # House 12
        ]

class BorderedLabel(IndicLabel):
    def __init__(self, draw_border=True, **kwargs):
        kwargs.setdefault('halign', 'center')
        kwargs.setdefault('valign', 'middle')
        kwargs.setdefault('size_hint', (1, 1))
        super().__init__(**kwargs)
        self.draw_border = draw_border
        self.bind(size=self._update_text_size)
        if self.draw_border:
            with self.canvas.after:
                Color(0, 0, 0, 1)
                self.border = Line(rectangle=(self.x, self.y, self.width, self.height), width=1)
            self.bind(pos=self.update_border, size=self.update_border)

    def update_border(self, *args):
        if self.draw_border:
            self.border.rectangle = (self.x, self.y, self.width, self.height)

class CenterCell(FloatLayout):
    def __init__(self, center_text, **kwargs):
        super().__init__(**kwargs)
        label = Label(
            text=center_text,
            size_hint=(1, 1),
            halign='center',
            valign='middle',
            color=(0, 0, 0, 1)  # Optional: set text color
        )
        label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        self.add_widget(label)
        
class RectIcon(Image):
    def __init__(self, rectangle, source='', draw_border=False,
                 x_align='center', y_align='center',icon_size_factor=_DEFAULT_CHART_ICON_SIZE_FACTOR, **kwargs):
        super().__init__(source=source, **kwargs)
        rect_x, rect_y, rect_w, rect_h = rectangle
        self.size_hint = (None, None)
        self.size = (icon_size_factor*rect_w, icon_size_factor*rect_h)
        self.texture_update()
        # Position based on alignment
        if x_align == 'left':
            x = rect_x
        elif x_align == 'right':
            x = rect_x + rect_w - self.width
        else:
            x = rect_x + (rect_w - self.width) / 2

        if y_align == 'top':
            y = rect_y + rect_h - self.height
        elif y_align == 'bottom':
            y = rect_y
        else:
            y = rect_y + (rect_h - self.height) / 2

        self.pos = (x, y)

        if draw_border:
            with self.canvas.before:
                Color(1, 1, 1)
                Line(rectangle=(rect_x, rect_y, rect_w, rect_h), width=1)

class RectLabel(Widget):
    def __init__(self, rectangle, text='', draw_border=True, draw_diagonal_line=None,
                 x_align='center', y_align='center', font_size=20,
                 font_name=const.FONT_NAMES[const._DEFAULT_LANGUAGE][0], **kwargs):
        super().__init__(**kwargs)

        # Store rectangle and drawing options
        self.rect_x, self.rect_y, self.rect_w, self.rect_h = rectangle
        self.x_align = x_align
        self.y_align = y_align
        self.draw_border = draw_border
        self.draw_diagonal_line = draw_diagonal_line

        # Set widget position and size
        self.pos = (self.rect_x, self.rect_y)
        self.size = (self.rect_w, self.rect_h)

        # Create label
        self.label = GetLabelWidget(text=text, font_size=font_size, font_name=font_name, **kwargs)
        self.label.size_hint = (None, None)
        self.label.text_size = (None, None)
        self.add_widget(self.label)

        # Bind updates
        self.label.bind(texture_size=self._update_position)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

        # Initial draw
        self.update_canvas()

    def _update_position(self, *args):
        label_w, label_h = self.label.texture_size
        self.label.size = (label_w, label_h)

        x0, y0 = self.pos
        w, h = self.size

        # Horizontal alignment
        if self.x_align == 'left':
            x = x0
        elif self.x_align == 'right':
            x = x0 + w - label_w
        else:  # center
            x = x0 + (w - label_w) / 2

        # Vertical alignment
        if self.y_align == 'top':
            y = y0 + h - label_h
        elif self.y_align == 'bottom':
            y = y0
        else:  # center
            y = y0 + (h - label_h) / 2

        self.label.pos = (x, y)

    def update_canvas(self, *args):
        self.canvas.before.clear()
        x, y = self.pos
        w, h = self.size

        with self.canvas.before:
            Color(*_CHART_GRID_LINE_COLOR)
            if self.draw_border:
                Line(rectangle=(x, y, w, h), width=1)
            if self.draw_diagonal_line in ['Left', 'Both']:
                Line(points=[x, y + h, x + w, y], width=1)
            if self.draw_diagonal_line in ['Right', 'Both']:
                Line(points=[x + w, y + h, x, y], width=1)


class KundaliChart(Widget):
    def __init__(self, data=None, data_font_size=None, draw_border=True,
                 draw_chart_border=True, chart_type='south',
                 chart_caption='', icon_path=const._IMAGE_ICON_PATH,
                 font_name=const.FONT_NAMES[const._DEFAULT_LANGUAGE][0],
                 caption_font_size=None,
                 **kwargs):
        super().__init__(**kwargs)
        self.chart_type = chart_type if chart_type else 'south'
        self.data_font_size = data_font_size if data_font_size else _DEFAULT_CHART_LABEL_FONT_SIZE
        self.caption_font_size = caption_font_size if caption_font_size else _DEFAULT_CHART_CAPTION_FONT_SIZE
        self.font_name = font_name
        self.draw_border = draw_border
        self.draw_chart_border = draw_chart_border

        self.house_labels = []
        self._data = data
        self._caption = chart_caption
        self._icon_path = icon_path

        #self.cell_size = dp(_DEFAULT_CHART_CELL_SIZE)  # Initial default
        self._init_chart_config()
        self.bind(size=self.on_size)

    def _init_chart_config(self):
        if 'south' in self.chart_type.lower():
            self.grid_dimension = 4
            self.house_map = south_house_map
            self.icon_data = [self._icon_path, (2, 2), ('center', 'center'), _DEFAULT_CHART_ICON_SIZE_FACTOR]
        elif 'north' in self.chart_type.lower():
            self.grid_dimension = 2
            self.house_map = north_house_map
            self.icon_data = [self._icon_path, (1, 1), ('center', 'center'), _DEFAULT_CHART_ICON_SIZE_FACTOR]
            self.draw_border = False
        else:  # East
            self.grid_dimension = 3
            self.house_map = east_house_map
            self.icon_data = [self._icon_path, (1, 1), ('right', 'bottom'), _DEFAULT_CHART_ICON_SIZE_FACTOR]

    def on_size(self, *args):
        #self.cell_size = min(self.width, self.height) / self.grid_dimension
        self.canvas.after.clear()
        #if self.draw_chart_border:
        #    with self.canvas.after:
        #        Line(rectangle=(0, 0, self.cell_size * self.grid_dimension, self.cell_size * self.grid_dimension), width=1)
        if self._data:
            self.set_data(self._data, chart_caption=self._caption, icon_path=self._icon_path)

    def set_data(self, data, chart_caption='', icon_path=const._IMAGE_ICON_PATH):
        self.clear_widgets()
        self.house_labels.clear()
        self._data = data
        self._caption = chart_caption
        self._icon_path = icon_path
        self._init_chart_config()
    
        chart_size = min(self.width, self.height) * _CHART_SIZE_FACTOR
        self.cell_size = chart_size / self.grid_dimension
        x_offset = _CHART_X + (self.width - chart_size) / 2
        y_offset = _CHART_Y + (self.height - chart_size) / 2
    
        def cell_rect(row, col):
            x = x_offset + col * self.cell_size
            y = y_offset + (self.grid_dimension - 1 - row) * self.cell_size
            return (x, y, self.cell_size, self.cell_size)
    
        # Draw chart border
        if self.draw_chart_border:
            with self.canvas.after:
                Color(*_CHART_GRID_LINE_COLOR)
                Line(rectangle=(x_offset, y_offset, chart_size, chart_size), width=1)
    
        # Add house labels
        for i, planets in enumerate(data):
            (row, col), x_align, y_align, diag = self.house_map[i]
            rect = cell_rect(row, col)
            label = RectLabel(
                rectangle=rect,
                text=planets,
                draw_border=self.draw_border,
                draw_diagonal_line=diag,
                x_align=x_align,
                y_align=y_align,
                font_size=self.data_font_size,
                font_name=self.font_name
            )
            self.house_labels.append(label)
            self.add_widget(label)
    
        # Add caption
        caption_rect = cell_rect(1, 1);x_align_caption = 'left';y_align_caption='top'
        if 'north' in self.chart_type.lower():
            caption_rect = cell_rect(_NORTH_CAPTION_CELL_ROW,_NORTH_CAPTION_CELL_COL)
            x_align_caption = _NORTH_CAPTION_XALIGN;y_align_caption=_NORTH_CAPTION_YALIGN
        caption = RectLabel(
            rectangle=caption_rect,
            text=self._caption,
            draw_border=False,
            draw_diagonal_line=None,
            x_align=x_align_caption,
            y_align=y_align_caption,
            font_size=self.caption_font_size,
            font_name=self.font_name
        )
        self.add_widget(caption)
    
        # Add icon
        if self.chart_type.lower() == 'north':
            icon_size = self.cell_size * self.icon_data[3]
            icon_x = (self.width - icon_size) / 2
            icon_y = (self.height - icon_size) / 2
            icon_rect = (icon_x, icon_y, icon_size, icon_size)
        else:
            icon_rect = cell_rect(*self.icon_data[1])
        icon = RectIcon(
            rectangle=icon_rect,
            source=self.icon_data[0],
            x_align=self.icon_data[2][0],
            y_align=self.icon_data[2][1],
            icon_size_factor=self.icon_data[3]
        )
        self.add_widget(icon)


class TestChartApp(App):
    def build(self):
        # Initial data
        data_list2 = [['6/10', '', '9', '4'],
                      ['7', '', '', '3/5'],
                      ['L/11', '', '', '0/8'],
                      ['', '', '1', '2']]
        center_text2 = "2025-08-27\n19:01:53 (GMT -5.0)\nHoffman Estates, US\n42°2'34\" N, -88°4'47\" W"

        # Final data to update
        data_list = [['', '', '1', '2'],
                     ['7', '', '', '3/5'],
                     ['L/11', '', '', '0/8'],
                     ['6/10', '', '9', '4']]
        center_text = "Draw Later 2025-08-27\n19:01:53 (GMT -5.0)\nHoffman Estates, US\n42°2'34\" N, -88°4'47\" W"

        panel = TabbedPanel(do_default_tab=False)
        tab = TabbedPanelItem(text='Chart')
        data = ['லக்னம்', '','செவ்வாய்♂\nபுதன்☿\n','சந்திரன்☾','','','கேது☋','','','','','குரு♃\nசூரியன்☉\nராகு☊\nசனி♄']
        asc_house = 1
        caption = ''
        chart = KundaliChart(chart_type='north',font_name=const.FONT_NAMES['ta'][0])
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(GetLabelWidget('This is the chart below)'))
        layout.add_widget(chart)
        tab.add_widget(layout)
        panel.add_widget(tab)

        # Schedule update after 2 seconds
        Clock.schedule_once(lambda dt: chart.set_data(data, center_text), 2)

        return panel

if __name__ == '__main__':
    TestChartApp().run()
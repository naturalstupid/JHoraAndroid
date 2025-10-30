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
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from jhora import const
_assets_folder = 'assets/'

class SpinnerWidget(Image):
    angle = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.source = const.get_resource_path("spinner.png")
        self.size_hint = (None, None)
        self.size = (64, 64)
        self.allow_stretch = True
        Clock.schedule_interval(self.rotate_spinner, 1/30)

    def rotate_spinner(self, dt):
        self.angle = (self.angle + 5) % 360
        self.canvas.before.clear()
        with self.canvas.before:
            self.canvas.before.rotate(angle=self.angle, origin=self.center)
class SpinnerOverlay(FloatLayout):
    def __init__(self, spinner_path=const.get_resource_path("spinner.png"), **kwargs):
        super().__init__(**kwargs)
        self.spinner = Image(source=spinner_path,
                             size_hint=(None, None),
                             size=(100, 100),
                             pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.add_widget(self.spinner)

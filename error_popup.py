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
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from jhora import utils

def show_error_popup(message,title="Error"):
    try:
        print('JHora: show_error_popup',message,title)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        label = Label(text=message, size_hint=(0.8, 0.3))
        label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
        close_button = Button(text='Close', size_hint=(1, None), height=40)
        layout.add_widget(label)
        layout.add_widget(close_button)
        popup = Popup(title='Error', content=layout, size_hint=(0.8,0.3))
        close_button.bind(on_release=popup.dismiss)
        popup.open()
    except Exception as e:
        utils.show_exception(e)
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
import os
import json
from kivy.app import App
from kivy.utils import platform
from kivy.resources import resource_find
import shutil

CONFIG_FILE_NAME = "user_config.json"
DEFAULT_CONFIG = {
    "language": "English",
    "show_splash": False,
    "ayanamsa_mode": "LAHIRI",
    "chart_type": "south",
}

def get_config_path():
    # This ensures the file is stored in the app's internal storage
    if platform == "android":
        return os.path.join(App.get_running_app().user_data_dir, CONFIG_FILE_NAME)
    else:
        return CONFIG_FILE_NAME  # app folder on Windows

def load_config():
    config_path = get_config_path()
    print(f"JHora: Loading config file {config_path}")

    if not os.path.exists(config_path):
        # First run: copy bundled config to internal storage
        bundled_config_path = resource_find(CONFIG_FILE_NAME)
        if bundled_config_path:
            print(f"JHora: Copying bundled config from {bundled_config_path}")
            shutil.copy(bundled_config_path, config_path)
        else:
            print("JHora: Bundled config not found, using default.")
            return DEFAULT_CONFIG.copy()

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("JHora: Error loading config:", e)

    print("JHora: Loading default config from code.")
    return DEFAULT_CONFIG.copy()

def _load_config():
    config_path = get_config_path()
    print(f"JHora: Loading config file {config_path}")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            print("JHora: unable to find",config_path)
    print("JHora: Loading default config from code.")
    return DEFAULT_CONFIG.copy()

def save_config(config):
    config_path = get_config_path()
    print(f"JHora: Saving config file {config_path}")
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)

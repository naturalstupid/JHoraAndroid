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
import logging
import os
from kivy.utils import platform
from kivy.app import App

def get_log_dir():
    
    default_dir = os.path.join(os.getcwd(), "logs")
    if platform == "android":
        app = App.get_running_app()
        if app:
            return os.path.join(app.user_data_dir, "logs")
        else:
            return default_dir  # fallback
    elif platform == "win":
        return default_dir
    else:
        return default_dir


log_dir = get_log_dir()
os.makedirs(log_dir, exist_ok=True)

# Configure logging
logging.basicConfig(
    filename=os.path.join(log_dir, "app.log"),
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_error(msg):
    logging.error(msg)

# Shortcut functions
def debug(msg): logging.debug(msg)
def info(msg): logging.info(msg)
def warning(msg): logging.warning(msg)
def error(msg): logging.error(msg)
def critical(msg): logging.critical(msg)

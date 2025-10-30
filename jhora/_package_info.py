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

name = "PyJHoraApp"

version = "0.8"

author = "Sundar Sundaresan"

author_email = "carnaticmusicguru2015@comcast.net"

description = "A Python package for generating Indian style calendar, panchang and horoscope"

url = "https://github.com/naturalstupid/PyJHoraApp"

project_urls = {
    "Source Code": "https://github.com/naturalstupid/PyJHoraApp",
    "Documentation": "https://github.com/naturalstupid/PyJHoraApp",
}

#install_requires = ['itertools', "configparser", 'operator', 'collections', 'enum', 'csv', 'scamp', 'math', 're', 'regex', 'random',]
install_requires = ['geopy','pytz']

#extras_require = { }

package_data = {
    'horoscope': ["data/*",'lang/*','images/*']
}

classifiers = [
    "Programming Language :: Python :: 3.6",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
]

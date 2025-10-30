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
try:
    print("JHora: Entered cairo_wrapper.py - importing ctypes")
    import ctypes
except Exception as e:
    print("JHora: Cairo Error importing ctypes",e)
print("JHora: Cairo ctypes imported success")
try:
    from jhora import const
    import os
    lib_path = os.path.join(const._LIBS_PATH,"libcairo.so")
    print("JHora: Loading Cairo",lib_path)
    cairo = ctypes.CDLL(lib_path, mode=ctypes.RTLD_GLOBAL)  # Adjust path as needed
    print("JHora: libcairo loaded success")
except Exception as e:
    print("JHora: Error importing libcairo",e)
print("JHora: Cairo Initiating constants")
from ctypes import c_int, c_double, c_void_p, POINTER, Structure, c_char_p, c_ubyte

# Define necessary Cairo types
class cairo_surface_t(c_void_p): pass
class cairo_t(c_void_p): pass
class cairo_font_face_t(c_void_p): pass

class cairo_glyph_t(Structure):
    _fields_ = [
        ("index", c_int),
        ("x", c_double),
        ("y", c_double),
    ]

# ImageSurface wrapper
class ImageSurface:
    FORMAT_ARGB32 = 0

    def __init__(self, format, width, height):
        cairo.cairo_image_surface_create.restype = cairo_surface_t
        cairo.cairo_image_surface_create.argtypes = [c_int, c_int, c_int]
        self.surface = cairo.cairo_image_surface_create(format, width, height)

    def get_data(self):
        cairo.cairo_image_surface_get_data.restype = POINTER(c_ubyte)
        cairo.cairo_image_surface_get_data.argtypes = [cairo_surface_t]
        return cairo.cairo_image_surface_get_data(self.surface)

# Context wrapper
class Context:
    def __init__(self, surface: ImageSurface):
        cairo.cairo_create.restype = cairo_t
        cairo.cairo_create.argtypes = [cairo_surface_t]
        self.ctx = cairo.cairo_create(surface.surface)

    def set_source_rgb(self, r, g, b):
        cairo.cairo_set_source_rgb.argtypes = [cairo_t, c_double, c_double, c_double]
        cairo.cairo_set_source_rgb(self.ctx, r, g, b)

    def paint(self):
        cairo.cairo_paint.argtypes = [cairo_t]
        cairo.cairo_paint(self.ctx)

    def set_font_face(self, font_face):
        cairo.cairo_set_font_face.argtypes = [cairo_t, cairo_font_face_t]
        cairo.cairo_set_font_face(self.ctx, font_face.face)

    def set_font_size(self, size):
        cairo.cairo_set_font_size.argtypes = [cairo_t, c_double]
        cairo.cairo_set_font_size(self.ctx, size)

    def translate(self, x, y):
        cairo.cairo_translate.argtypes = [cairo_t, c_double, c_double]
        cairo.cairo_translate(self.ctx, x, y)

    def show_glyphs(self, glyphs):
        cairo.cairo_show_glyphs.argtypes = [cairo_t, POINTER(cairo_glyph_t), c_int]
        glyph_array = (cairo_glyph_t * len(glyphs))(*glyphs)
        cairo.cairo_show_glyphs(self.ctx, glyph_array, len(glyphs))

    def save(self):
        cairo.cairo_save.argtypes = [cairo_t]
        cairo.cairo_save(self.ctx)

    def restore(self):
        cairo.cairo_restore.argtypes = [cairo_t]
        cairo.cairo_restore(self.ctx)

# ToyFontFace wrapper
class ToyFontFace:
    FONT_SLANT_NORMAL = 0
    FONT_WEIGHT_NORMAL = 0

    def __init__(self, family, slant=FONT_SLANT_NORMAL, weight=FONT_WEIGHT_NORMAL):
        cairo.cairo_toy_font_face_create.restype = cairo_font_face_t
        cairo.cairo_toy_font_face_create.argtypes = [c_char_p, c_int, c_int]
        self.face = cairo.cairo_toy_font_face_create(family.encode("utf-8"), slant, weight)
print("JHora: Leaving cairo_wrapper")

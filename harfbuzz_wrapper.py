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
    print("JHora: Entered harfbuzz_wrapper.py - importing ctypes")
    import ctypes
except Exception as e:
    print("JHora: Error importing ctypes",e)
print("JHora: ctypes imported success")
try:
    from jhora import const
    import os
    lib_path = os.path.join(const._LIBS_PATH,"libharfbuzz.so")
    print("JHora: Loading ",lib_path)
    libhb = ctypes.CDLL(lib_path, mode=ctypes.RTLD_GLOBAL)  # Adjust path as needed
    print("JHora: libharfbuzz loaded success")
except Exception as e:
    print("JHora: Error importing libharfbuzz",e)
print("JHora: Initiating constants")
# HarfBuzz types
hb_blob_t = ctypes.c_void_p
hb_face_t = ctypes.c_void_p
hb_font_t = ctypes.c_void_p
hb_buffer_t = ctypes.c_void_p

# Constants
HB_MEMORY_MODE_READONLY = 0
print("JHora: GlyphInfo class")
# Structures
class GlyphInfo(ctypes.Structure):
    _fields_ = [("codepoint", ctypes.c_uint), ("cluster", ctypes.c_uint)]
print("JHora: GlyphPosition class")
class GlyphPosition(ctypes.Structure):
    _fields_ = [
        ("x_advance", ctypes.c_int),
        ("y_advance", ctypes.c_int),
        ("x_offset", ctypes.c_int),
        ("y_offset", ctypes.c_int)
    ]
print("JHora:hb_blob_create") 
# Bindings
libhb.hb_blob_create.restype = hb_blob_t
libhb.hb_blob_create.argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.c_int, ctypes.c_void_p, ctypes.c_void_p]

print("JHora:hb_face_create") 
libhb.hb_face_create.restype = hb_face_t
libhb.hb_face_create.argtypes = [hb_blob_t, ctypes.c_uint]

print("JHora:hb_font_create") 
libhb.hb_font_create.restype = hb_font_t
libhb.hb_font_create.argtypes = [hb_face_t]

print("JHora:hb_font_set_scale") 
libhb.hb_font_set_scale.argtypes = [hb_font_t, ctypes.c_int, ctypes.c_int]

print("JHora:hb_buffer_create") 
libhb.hb_buffer_create.restype = hb_buffer_t
libhb.hb_buffer_create.argtypes = []

print("JHora:hb_buffer_add_utf8") 
libhb.hb_buffer_add_utf8.argtypes = [hb_buffer_t, ctypes.c_char_p, ctypes.c_int, ctypes.c_uint, ctypes.c_int]

print("JHora:hb_buffer_guess_segment_properties") 
libhb.hb_buffer_guess_segment_properties.argtypes = [hb_buffer_t]

print("JHora:hb_shape") 
libhb.hb_shape.argtypes = [hb_font_t, hb_buffer_t]

print("JHora:hb_buffer_get_length") 
libhb.hb_buffer_get_length.restype = ctypes.c_uint
libhb.hb_buffer_get_length.argtypes = [hb_buffer_t]

print("JHora:hb_buffer_get_glyph_infos") 
libhb.hb_buffer_get_glyph_infos.restype = ctypes.POINTER(GlyphInfo)
libhb.hb_buffer_get_glyph_infos.argtypes = [hb_buffer_t, ctypes.POINTER(ctypes.c_uint)]

print("JHora:hb_buffer_get_glyph_positions") 
libhb.hb_buffer_get_glyph_positions.restype = ctypes.POINTER(GlyphPosition)
libhb.hb_buffer_get_glyph_positions.argtypes = [hb_buffer_t, ctypes.POINTER(ctypes.c_uint)]

print("JHora: API compatible classes") 
# API-compatible classes
print("JHora: Blob Class") 
class Blob:
    def __init__(self, fontdata: bytes):
        self._blob = libhb.hb_blob_create(fontdata, len(fontdata), HB_MEMORY_MODE_READONLY, None, None)

print("JHora: Face Class") 
class Face:
    def __init__(self, blob: Blob):
        self._face = libhb.hb_face_create(blob._blob, 0)

print("JHora: Font Class") 
class Font:
    def __init__(self, face: Face):
        self._font = libhb.hb_font_create(face._face)
        self.scale = (0, 0)

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        libhb.hb_font_set_scale(self._font, value[0], value[1])

print("JHora: Buffer Class") 
class Buffer:
    def __init__(self):
        self._buf = libhb.hb_buffer_create()
        self.glyph_infos = []
        self.glyph_positions = []

    def add_str(self, text: str):
        libhb.hb_buffer_add_utf8(self._buf, text.encode("utf-8"), -1, 0, -1)

    def guess_segment_properties(self):
        libhb.hb_buffer_guess_segment_properties(self._buf)

def shape(font: Font, buf: Buffer):
    libhb.hb_shape(font._font, buf._buf)

    length = libhb.hb_buffer_get_length(buf._buf)
    infos_ptr = libhb.hb_buffer_get_glyph_infos(buf._buf, None)
    positions_ptr = libhb.hb_buffer_get_glyph_positions(buf._buf, None)

    buf.glyph_infos = [infos_ptr[i] for i in range(length)]
    buf.glyph_positions = [positions_ptr[i] for i in range(length)]

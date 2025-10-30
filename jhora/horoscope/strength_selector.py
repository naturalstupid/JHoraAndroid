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
from jhora.horoscope.chart import charts
from jhora import const,utils

def _get_vimsopaka_bala(dob,tob,place_as_tuple):
    jd_at_dob = utils.julian_day_number(dob, tob)
    sv = charts.vimsopaka_shadvarga_of_planets(jd_at_dob, place_as_tuple)
    sv1 = {}
    for p in range(9):
        sv1[utils.PLANET_NAMES[p]]=utils.SHADVARGAMSA_NAMES[sv[p][0]]+'\n('+sv[p][1]+ ')\n'+str(round(sv[p][2],1))
    sv = charts.vimsopaka_sapthavarga_of_planets(jd_at_dob, place_as_tuple)
    sv2 = {}
    for p in range(9):
        sv2[utils.PLANET_NAMES[p]]=utils.SAPTAVARGAMSA_NAMES[sv[p][0]]+'\n('+sv[p][1]+ ')\n'+str(round(sv[p][2],1))
    sv = charts.vimsopaka_dhasavarga_of_planets(jd_at_dob, place_as_tuple)
    dv = {}
    for p in range(9):
        dv[utils.PLANET_NAMES[p]]=utils.DHASAVARGAMSA_NAMES[sv[p][0]]+'\n('+sv[p][1]+ ')\n'+str(round(sv[p][2],1))
    sv = charts.vimsopaka_shodhasavarga_of_planets(jd_at_dob, place_as_tuple)
    sv3 = {}
    for p in range(9):
        sv3[utils.PLANET_NAMES[p]]=utils.SHODASAVARGAMSA_NAMES[sv[p][0]]+'\n('+sv[p][1]+ ')\n'+str(round(sv[p][2],1))
    return [sv1,sv2,dv,sv3]
def _get_vaiseshikamsa_bala(dob,tob,place_as_tuple):
    jd_at_dob = utils.julian_day_number(dob, tob)
    sv = charts.vaiseshikamsa_shadvarga_of_planets(jd_at_dob, place_as_tuple)
    sv1 = {}
    for p in range(9):
        sv1[utils.PLANET_NAMES[p]]=utils.SHADVARGAMSA_NAMES[sv[p][0]]+'\n('+sv[p][1]+ ')\n'+str(round(sv[p][2],1))
    sv = charts.vaiseshikamsa_sapthavarga_of_planets(jd_at_dob, place_as_tuple)
    sv2 = {}
    for p in range(9):
        sv2[utils.PLANET_NAMES[p]]=utils.SAPTAVARGAMSA_NAMES[sv[p][0]]+'\n('+sv[p][1]+ ')\n'+str(round(sv[p][2],1))
    sv = charts.vaiseshikamsa_dhasavarga_of_planets(jd_at_dob, place_as_tuple)
    dv = {}
    for p in range(9):
        dv[utils.PLANET_NAMES[p]]=utils.DHASAVARGAMSA_NAMES[sv[p][0]]+'\n('+sv[p][1]+ ')\n'+str(round(sv[p][2],1))
    sv = charts.vaiseshikamsa_shodhasavarga_of_planets(jd_at_dob, place_as_tuple)
    sv3 = {}
    for p in range(9):
        sv3[utils.PLANET_NAMES[p]]=utils.SHODASAVARGAMSA_NAMES[sv[p][0]]+'\n('+sv[p][1]+ ')\n'+str(round(sv[p][2],1))
    return [sv1,sv2,dv,sv3]
def _get_other_bala(dob,tob,place):
    #from jhora.horoscope.transit import tajaka
    from jhora.horoscope.chart import strength
    jd = utils.julian_day_number(dob, tob)
    hb = strength.harsha_bala(dob, tob, place)
    hb1 = {utils.PLANET_NAMES[p]:hb[p] for p in range(7)}
    pvb = strength.pancha_vargeeya_bala(jd, place)
    pvb1 = {utils.PLANET_NAMES[p]:pvb[p] for p in range(7)}
    dvb = strength.dwadhasa_vargeeya_bala(jd, place)
    dvb1 = {utils.PLANET_NAMES[p]:dvb[p] for p in range(7)}
    return [hb1, pvb1, dvb1]
def _get_shad_bala(dob,tob,place):
    from jhora.horoscope.chart import strength
    jd = utils.julian_day_number(dob, tob)
    sb = strength.shad_bala(jd, place)
    column_names = [""]+utils.PLANET_SHORT_NAMES[:7]; cmax = len(column_names)
    row_names = ['sthaana_bala_str','kaala_bala_str','dig_bala_str','chesta_bala_str','naisargika_bala_str',
                 'drik_bala_str','shad_bala_str','shad_bala_rupas_str','shad_bala_strength_str']
    rmax = len(row_names)+1
    st = [['' for _ in range(cmax)] for _ in range(rmax)]
    st[0] = column_names
    for r in range(1,rmax):
        st[r] = [utils.resource_strings[row_names[r-1]]]+sb[r-1][:]
    return st
def _get_bhava_bala(dob,tob,place):
    from jhora.horoscope.chart import strength
    jd = utils.julian_day_number(dob, tob)
    bb = strength.bhava_bala(jd, place)
    bb = [list(row) for row in zip(*bb)]

    column_names = [""]+[utils.resource_strings[c] for c in ['bhava_bala_str','bhava_bala_rupas_str','bhava_bala_strength_str']]
    cmax = len(column_names)
    row_names = [utils.resource_strings['house_str']+'-'+str(h+1) for h in range(12)]
    rmax = len(row_names)+1
    st = [['' for _ in range(cmax)] for _ in range(rmax)]
    st[0] = column_names
    for r in range(1,rmax):
        st[r] = [row_names[r-1]]+bb[r-1]
    return st
def _append_bala_tables(data,i_start,bala_table):
    result = bala_table[:]
    for i, d in enumerate(data):
        items = [[k, v] for k, v in d.items()]
        #result.append(i_start + i)
        result.append(items)
    return result
def _get_bala_tables(dob,tob,place):
    jd_at_dob = utils.julian_day_number(dob, tob)
    st = []
    bala_index = 0
    sv = _get_vimsopaka_bala(dob,tob,place)
    st = _append_bala_tables(sv, bala_index, st)
    bala_index += len(sv)
    sv = _get_vaiseshikamsa_bala(dob,tob,place)
    st = _append_bala_tables(sv, bala_index, st)
    bala_index += len(sv)
    sv = _get_other_bala(dob,tob,place)
    st = _append_bala_tables(sv, bala_index, st)
    bala_index += len(sv)
    sb = _get_shad_bala(dob, tob, place)
    st.append(sb)
    bala_index += 1
    bb = _get_bhava_bala(dob, tob, place)
    st.append(bb)
    bala_index += 1
    return st
if __name__ == "__main__":
    from jhora.panchanga import drik
    dob = drik.Date(1996,12,7); tob = (10,34,0); place = drik.Place('Chennai,IN',13.0389, 80.2619, +5.5)
    jd = utils.julian_day_number(dob, tob)
    utils.set_language('en')
    ayanamsa_mode=drik.set_ayanamsa_mode('TRUE_CITRA')
    bt = _get_bala_tables(dob, tob, place)
    print(bt)

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
"""
    TODO: Check use of julian_day vs julian_years if used consistently
    For example: Special Lagna/Ascendant Calculations require jd_years or years/months/60hrs and new tob
"""
"""
    TODO: When selecting Janma, Annual, Tithi Pravesha - which TABS should it be applied and which ones not
    For example only charts? Dhasa Bhukthi as well, how about other TABS line dosha, compatibility etc
    Which TABS should always be based on NATAL CHART?
"""
# Add parent directory to sys.path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from datetime import date
from jhora import const, utils
swe = const.get_swe()
from jhora.panchanga import drik
from jhora.horoscope.chart import house,charts
def _get_graha_dhasa(dob,tob,place):
    _vimsottari_balance,_vimsottari_dhasa_bhkthi_info = _get_vimsottari_dhasa(dob, tob, place)
    _ashtottari_dhasa_bhkthi_info = _get_ashtottari_dhasa(dob, tob, place)
    _yogini_dhasa_bhkthi_info = _get_yogini_dhasa(dob, tob, place)
    return _vimsottari_dhasa_bhkthi_info,_ashtottari_dhasa_bhkthi_info, _yogini_dhasa_bhkthi_info
def _get_rasi_dhasa(dob,tob,place):
    _narayana_dhasa_bhukthi_info = _get_narayana_dhasa(dob,tob,place)
    _kendraadhi_rasi_dhasa_bhukthi_info = _get_kendraadhi_rasi_dhasa(dob,tob,place)
    _sudasa_dhasa_bhukthi_info = _get_sudasa_dhasa(dob,tob,place)
    _drig_dhasa_bhukthi_info = _get_drig_dhasa(dob,tob,place)
    _nirayana_dhasa_bhukthi_info = _get_nirayana_dhasa(dob,tob,place)
    _shoola_dhasa_bhukthi_info = _get_shoola_dhasa(dob,tob,place)
    _kendraadhi_karaka_dhasa_bhukthi_info = _get_kendraadhi_karaka_dhasa(dob,tob,place)
    _chara_dhasa_bhukthi_info = _get_chara_dhasa(dob,tob,place)
    _lagnamsaka_dhasa_bhukthi_info = _get_lagnamsaka_dhasa(dob,tob,place)
    _padhanadhamsa_dhasa_bhukthi_info = _get_padhanadhamsa_dhasa(dob, tob, place)
    _mandooka_dhasa_bhukthi_info = _get_mandooka_dhasa(dob, tob, place)
    _sthira_dhasa_bhukthi_info = _get_sthira_dhasa(dob, tob, place)
    _tara_lagna_dhasa_bhukthi_info = _get_tara_lagna_dhasa(dob, tob, place)
    return [_narayana_dhasa_bhukthi_info, _kendraadhi_rasi_dhasa_bhukthi_info, _sudasa_dhasa_bhukthi_info, \
        _drig_dhasa_bhukthi_info, _nirayana_dhasa_bhukthi_info, _shoola_dhasa_bhukthi_info, \
        _kendraadhi_karaka_dhasa_bhukthi_info, _chara_dhasa_bhukthi_info, _lagnamsaka_dhasa_bhukthi_info, \
        _padhanadhamsa_dhasa_bhukthi_info]
def _get_annual_dhasa(divisional_chart_factor=1):
    _patyayini_dhasa_bhukthi_info = _get_patyayini_dhasa(divisional_chart_factor=divisional_chart_factor)
    _mudda_dhasa_bhukthi_info = _get_varsha_vimsottari_dhasa(julian_day, Place, years-1,divisional_chart_factor=divisional_chart_factor)
    _varsha_narayana_dhasa_bhukthi_info = _get_varsha_narayana_dhasa(Date, birth_time, Place, years,divisional_chart_factor=divisional_chart_factor)
    return [_patyayini_dhasa_bhukthi_info,_mudda_dhasa_bhukthi_info,_varsha_narayana_dhasa_bhukthi_info]
def _get_vimsottari_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):#,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    jd = utils.julian_day_number(dob, tob)
    from jhora.horoscope.dhasa.graha import vimsottari
    _vimsottari_balance,db = vimsottari.get_vimsottari_dhasa_bhukthi(jd, place,ayanamsa_mode=ayanamsa_mode,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_yoga_vimsottari_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    jd = utils.julian_day_number(dob, tob)
    from jhora.horoscope.dhasa.graha import yoga_vimsottari
    _yoga_vimsottari_balance,db = yoga_vimsottari.get_dhasa_bhukthi(jd, place,ayanamsa_mode=ayanamsa_mode,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_rasi_bhukthi_vimsottari_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    jd = utils.julian_day_number(dob, tob)
    from jhora.horoscope.dhasa.graha import vimsottari
    _,db = vimsottari.get_vimsottari_dhasa_bhukthi(jd, place,ayanamsa_mode=ayanamsa_mode,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_ashtottari_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    from jhora.horoscope.dhasa.graha import ashtottari
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    jd = utils.julian_day_number(dob,tob)
    db = ashtottari.get_ashtottari_dhasa_bhukthi(jd, place,ayanamsa_mode=ayanamsa_mode,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        if not db[i]:
            continue
        [dhasa_lord, bukthi_lord,bukthi_start]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_tithi_ashtottari_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    from jhora.horoscope.dhasa.graha import tithi_ashtottari
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    jd = utils.julian_day_number(dob,tob)
    db = tithi_ashtottari.get_ashtottari_dhasa_bhukthi(jd, place,ayanamsa_mode=ayanamsa_mode,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        if not db[i]:
            continue
        [dhasa_lord, bukthi_lord,bukthi_start]=db[i]
        #dhasa_bhukti_info[utils.DHASA_LIST[dhasa_lord]+'-'+utils.BHUKTHI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    #print(dhasa_bhukti_info)
    return dhasa_bhukti_info
def _get_buddhi_gathi_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    from jhora.horoscope.dhasa.graha import buddhi_gathi
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    jd = utils.julian_day_number(dob,tob)
    db = buddhi_gathi.get_dhasa_bhukthi(dob,tob, place,ayanamsa_mode=ayanamsa_mode,include_antardhasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        if not db[i]:
            continue
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_yogini_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    from jhora.horoscope.dhasa.graha import yogini
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    db = yogini.get_dhasa_bhukthi(dob,tob, place,ayanamsa_mode=ayanamsa_mode, include_antardhasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        if not db[i]:
            continue
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_tithi_yogini_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    from jhora.horoscope.dhasa.graha import tithi_yogini
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    db = tithi_yogini.get_dhasa_bhukthi(dob,tob, place,ayanamsa_mode=ayanamsa_mode, include_antardhasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        if not db[i]:
            continue
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_shodasottari_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    from jhora.horoscope.dhasa.graha import shodasottari
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    db = shodasottari.get_dhasa_bhukthi(dob,tob, place,ayanamsa_mode=ayanamsa_mode, include_antardhasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        if not db[i]:
            continue
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_dwadasottari_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    from jhora.horoscope.dhasa.graha import dwadasottari
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    db = dwadasottari.get_dhasa_bhukthi(dob,tob, place,ayanamsa_mode=ayanamsa_mode, include_antardhasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        if not db[i]:
            continue
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_dwisatpathi_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    from jhora.horoscope.dhasa.graha import dwisatpathi
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    db = dwisatpathi.get_dhasa_bhukthi(dob,tob, place,ayanamsa_mode=ayanamsa_mode, include_antardhasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        if not db[i]:
            continue
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_panchottari_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    from jhora.horoscope.dhasa.graha import panchottari
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    db = panchottari.get_dhasa_bhukthi(dob,tob, place,ayanamsa_mode=ayanamsa_mode, include_antardhasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        if not db[i]:
            continue
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_satabdika_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    from jhora.horoscope.dhasa.graha import sataatbika
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    db = sataatbika.get_dhasa_bhukthi(dob,tob, place,ayanamsa_mode=ayanamsa_mode, include_antardhasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        if not db[i]:
            continue
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_chaturaaseeti_sama_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    from jhora.horoscope.dhasa.graha import chathuraaseethi_sama
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    db = chathuraaseethi_sama.get_dhasa_bhukthi(dob,tob, place,ayanamsa_mode=ayanamsa_mode, include_antardhasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        if not db[i]:
            continue
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_karana_chaturaaseeti_sama_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    from jhora.horoscope.dhasa.graha import karana_chathuraaseethi_sama
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    db = karana_chathuraaseethi_sama.get_dhasa_bhukthi(dob,tob, place,ayanamsa_mode=ayanamsa_mode, include_antardhasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        if not db[i]:
            continue
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_shashtisama_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    from jhora.horoscope.dhasa.graha import shastihayani
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    db = shastihayani.get_dhasa_bhukthi(dob,tob, place,ayanamsa_mode=ayanamsa_mode, include_antardhasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        if not db[i]:
            continue
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_shattrimsa_sama_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    from jhora.horoscope.dhasa.graha import shattrimsa_sama
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    db = shattrimsa_sama.get_dhasa_bhukthi(dob,tob, place,ayanamsa_mode=ayanamsa_mode, include_antardhasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        if not db[i]:
            continue
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_saptharishi_nakshathra_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    from jhora.horoscope.dhasa.graha import saptharishi_nakshathra
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    db = saptharishi_nakshathra.get_dhasa_bhukthi(dob,tob, place,ayanamsa_mode=ayanamsa_mode,include_antardhasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        if not db[i]:
            continue
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.NAKSHATRA_LIST[dhasa_lord]+'-'+utils.NAKSHATRA_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_varsha_narayana_dhasa(dob,tob,place,ayanamsa_mode=None,years=1,months=1,sixty_hours=1,divisional_chart_factor=1):
    from jhora.horoscope.dhasa.raasi import narayana
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    db = narayana.varsha_narayana_dhasa_bhukthi(dob, tob, place,ayanamsa_mode=ayanamsa_mode, years=years, months=months, sixty_hours=sixty_hours, divisional_chart_factor=divisional_chart_factor,include_antardhasa=True)
    #print('varsha narayana dhasa',db)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_varsha_vimsottari_dhasa(dob,tob, place,ayanamsa_mode=None, years=1,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    jd = utils.julian_day_number(dob,tob)
    from jhora.horoscope.dhasa.annual import mudda
    md = mudda.varsha_vimsottari_dhasa_bhukthi(jd, place,ayanamsa_mode=ayanamsa_mode, years=years,divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = []
    for pd,pb,bs,_ in md:
        dhasa_lord = utils.PLANET_NAMES[pd]
        bhukthi_lord = utils.PLANET_NAMES[pb]
        dhasa_bhukti_info.append((dhasa_lord+'-'+bhukthi_lord,bs))
    return dhasa_bhukti_info
def _get_patyayini_dhasa(dob,tob,place,ayanamsa_mode=None,years=1,months=1,sixty_hours=1,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    julian_day = utils.julian_day_number(dob,tob)
    from jhora.horoscope.dhasa.annual import patyayini
    julian_years = drik.next_solar_date(julian_day, place, years=years, months=months, sixty_hours=sixty_hours)
    p_d_b = patyayini.patyayini_dhasa(julian_years, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    #print('p_d_b',p_d_b)
    dhasa_bhukti_info = []
    for p,bhukthis,_ in p_d_b:
        #print('p,bhukthis',p,bhukthis)
        if p=='L':
            dhasa_lord = utils.resource_strings['ascendant_str']
        else:
            dhasa_lord = utils.PLANET_NAMES[p]
        for bk,bs in bhukthis:
            #print('bk,bs',bk,bs)
            if bk=='L':
                bhukthi_lord = utils.resource_strings['ascendant_str']
            else:
                bhukthi_lord = utils.PLANET_NAMES[bk]
            dhasa_bhukti_info.append((dhasa_lord+'-'+bhukthi_lord,bs))
            #print('key',dhasa_lord+'-'+bhukthi_lord,'value',bs)
    return dhasa_bhukti_info
def _get_tara_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.graha import tara
    db = tara.get_dhasa_bhukthi(dob, tob, place,ayanamsa_mode=ayanamsa_mode,include_antardasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.DHASA_LIST[dhasa_lord]+'-'+utils.BHUKTHI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_karaka_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    jd = utils.julian_day_number(dob, tob)
    from jhora.horoscope.dhasa.graha import karaka
    planet_positions = charts.rasi_chart(jd, place)
    db = karaka.get_dhasa_antardhasa(dob, tob, place,ayanamsa_mode=ayanamsa_mode,include_antardhasa=True,**kwargs)
    chara_karaka_names = [x+'_str' for x in house.chara_karaka_names]
    chara_karaka_dict = house.chara_karakas(planet_positions)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+' ('+utils.resource_strings[chara_karaka_names[chara_karaka_dict[dhasa_lord]]]+') '
                                  +'-'+utils.PLANET_NAMES[bukthi_lord]+' ('+utils.resource_strings[chara_karaka_names[chara_karaka_dict[bukthi_lord]]]+') ',bukthi_start))
    return dhasa_bhukti_info
def _get_naisargika_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.graha import naisargika
    db = naisargika.get_dhasa_bhukthi(dob, tob, place,ayanamsa_mode=ayanamsa_mode,include_antardhasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_str=utils.resource_strings['ascendant_str'] if dhasa_lord == const._ascendant_symbol else utils.PLANET_NAMES[dhasa_lord]
        bukthi_str=utils.resource_strings['ascendant_str'] if bukthi_lord == const._ascendant_symbol else utils.PLANET_NAMES[bukthi_lord]
        dhasa_bhukti_info.append((dhasa_str+'-'+bukthi_str,bukthi_start))
    return dhasa_bhukti_info
def _get_aayu_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    jd = utils.julian_day_number(dob, tob)
    from jhora.horoscope.dhasa.graha import aayu
    _aayu_dhasa_type,db = aayu.get_dhasa_antardhasa(jd, place,ayanamsa_mode=ayanamsa_mode,include_antardhasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_str=utils.resource_strings['ascendant_str'] if dhasa_lord==const._ascendant_symbol else utils.PLANET_NAMES[dhasa_lord]
        bukthi_str=utils.resource_strings['ascendant_str'] if bukthi_lord==const._ascendant_symbol else utils.PLANET_NAMES[bukthi_lord]                
        dhasa_bhukti_info.append((dhasa_str+'-'+bukthi_str,bukthi_start))
    return dhasa_bhukti_info
def _get_kaala_dhasa(dob,tob,place,ayanamsa_mode=None,**kwargs):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.graha import kaala
    _kaala_dhasa_type,db = kaala.get_dhasa_antardhasa(dob,tob, place,ayanamsa_mode=ayanamsa_mode,include_antardhasa=True,**kwargs)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.PLANET_NAMES[dhasa_lord]+'-'+utils.PLANET_NAMES[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_chakra_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import chakra
    db = chakra.get_dhasa_antardhasa(dob,tob, place,ayanamsa_mode=ayanamsa_mode,include_antardhasa=True,divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_sandhya_panchaka_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import sandhya
    db = sandhya.get_dhasa_antardhasa(dob,tob, place,ayanamsa_mode=ayanamsa_mode,use_panchaka_variation=True,divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_narayana_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import narayana
    db = narayana.narayana_dhasa_for_rasi_chart(dob, tob, place,ayanamsa_mode=ayanamsa_mode,include_antardhasa=True)
    dhasa_bhukti_info = [] #{}
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_kendraadhi_rasi_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import kendradhi_rasi
    db = kendradhi_rasi.kendradhi_rasi_dhasa(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_sudasa_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import sudasa
    db = sudasa.sudasa_dhasa_bhukthi(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_drig_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import drig
    db = drig.drig_dhasa_bhukthi(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_nirayana_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import nirayana
    db = nirayana.nirayana_shoola_dhasa_bhukthi(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_shoola_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import shoola
    db = shoola.shoola_dhasa_bhukthi(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_kendraadhi_karaka_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import kendradhi_rasi
    db = kendradhi_rasi.karaka_kendradhi_rasi_dhasa(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor, karaka_index=1)
    dhasa_bhukti_info = []
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_chara_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import chara
    db = chara.get_dhasa_antardhasa(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor, chara_method=1)
    #print('chara dasa',db)
    dhasa_bhukti_info = []
    for _dhasa,_bhukthi,dhasa_start,_ in db:
        dhasa_lord = utils.RAASI_LIST[_dhasa]
        bukthi_lord = utils.RAASI_LIST[_bhukthi]
        #dhasa_start = '%04d-%02d-%02d' %(y,m,d) +' '+utils.to_dms(fh, as_string=True)
        dhasa_bhukti_info.append((dhasa_lord+'-'+bukthi_lord,dhasa_start))
    return dhasa_bhukti_info
def _get_lagnamsaka_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import lagnamsaka
    db = lagnamsaka.get_dhasa_antardhasa(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = [] #{}
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_padhanadhamsa_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import padhanadhamsa
    db = padhanadhamsa.get_dhasa_antardhasa(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = [] #{}
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_mandooka_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import mandooka
    db = mandooka.get_dhasa_antardhasa(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = [] #{}
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_sthira_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import sthira
    db = sthira.get_dhasa_antardhasa(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = [] #{}
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_tara_lagna_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import tara_lagna
    db = tara_lagna.get_dhasa_antardhasa(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = [] #{}
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_brahma_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import brahma
    db = brahma.get_dhasa_antardhasa(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = [] #{}
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_varnada_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import varnada
    db = varnada.get_dhasa_antardhasa(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = [] #{}
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_yogardha_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import yogardha
    db = yogardha.get_dhasa_antardhasa(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = [] #{}
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_navamsa_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import navamsa
    db = navamsa.get_dhasa_antardhasa(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    dhasa_bhukti_info = [] #{}
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        #dhasa_bhukti_info[utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord]]=bukthi_start
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_paryaaya_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import paryaaya
    db = paryaaya.get_dhasa_antardhasa(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    #print('paryaaya dhasa',db)
    dhasa_bhukti_info = [] #{}
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
        #dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_trikona_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import trikona
    db = trikona.get_dhasa_antardhasa(dob, tob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    #print('trikona dhasa',db)
    dhasa_bhukti_info = [] #{}
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
        #dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
def _get_kalachakra_dhasa(dob,tob,place,ayanamsa_mode=None,divisional_chart_factor=1):
    if ayanamsa_mode is None: ayanamsa_mode=const._DEFAULT_AYANAMSA_MODE
    from jhora.horoscope.dhasa.raasi import kalachakra
    jd_at_dob = utils.julian_day_number(dob, tob)
    pp = charts.divisional_chart(jd_at_dob, place,ayanamsa_mode=ayanamsa_mode, divisional_chart_factor=divisional_chart_factor)
    moon_long = pp[2][1][0]*30+pp[2][1][1]
    db = kalachakra.kalachakra_dhasa(moon_long, jd_at_dob)
    dhasa_bhukti_info = [] #{}
    for i in range(len(db)):
        [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
        dhasa_bhukti_info.append((utils.RAASI_LIST[dhasa_lord]+'-'+utils.RAASI_LIST[bukthi_lord],bukthi_start))
    return dhasa_bhukti_info
if __name__ == "__main__":
    dob = drik.Date(1996,12,7); tob = (10,34,0); place = drik.Place('Chennai,IN',13.0389, 80.2619, +5.5)
    jd = utils.julian_day_number(dob, tob)
    utils.set_language('en')
    ayanamsa_mode=drik.set_ayanamsa_mode('TRUE_CITRA')
    option_str = ''
    _dhasa_names = ['vimsottari','yoga_vimsottari','rasi_bhukthi_vimsottari','ashtottari','tithi_ashtottari','yogini',
                     'tithi_yogini','shodasottari','dwadasottari','dwisatpathi','panchottari','satabdika','chaturaaseeti_sama',
                     'karana_chaturaaseeti_sama','shashtisama','shattrimsa_sama','naisargika','tara','karaka','buddhi_gathi',
                     'kaala','aayu','saptharishi_nakshathra',
                     'narayana','kendraadhi_rasi','sudasa','drig','nirayana','shoola','kendraadhi_karaka',
                'chara','lagnamsaka','padhanadhamsa','mandooka','sthira','tara_lagna','brahma','varnada','yogardha',
                'navamsa','paryaaya','trikona','kalachakra','chakra','sandhya_panchaka',
                'patyayini','varsha_vimsottari','varsha_narayana',
                ]
    for dhasa_key in _dhasa_names:
        func_str = '_get_'+dhasa_key.lower()+'_dhasa'
        arg_str = "dob, tob, place,ayanamsa_mode='TRUE_CITRA'";option_str=''
        eval_str = func_str+'('+arg_str+option_str+')'
        print(eval_str)
        retval = eval(eval_str)

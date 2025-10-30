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
_DEBUG_APP = False
try:
    if _DEBUG_APP: print("JHora: Entered swisseph.py - importing ctypes")
    import ctypes
except Exception as e:
    print("JHora: Error importing ctypes",e)
if _DEBUG_APP: print("JHora: ctypes imported success")
try:
    import os
    from jhora import const
    lib_path = lib_path = os.path.join(const._LIBS_PATH,"swisseph_android.so")
    if _DEBUG_APP: print("JHora: Loading ",lib_path)
    # Load the shared library
    swe = ctypes.CDLL(lib_path, mode=ctypes.RTLD_GLOBAL)
except Exception as e:
    print("JHora: Error loading ",lib_path,e)
if _DEBUG_APP: print("JHora: Loading constants")
# Constants
JUL_CAL = 0
GREG_CAL = 1
AUNIT_TO_KM = 149597870.7
AUNIT_TO_LIGHTYEAR = 1.5812507409819728e-05
AUNIT_TO_PARSEC = 4.848136811095274e-06
ECL_NUT = -1
SUN = 0
MOON = 1
MERCURY = 2
VENUS = 3
MARS = 4
JUPITER = 5
SATURN = 6
URANUS = 7
NEPTUNE = 8
PLUTO = 9
MEAN_NODE = 10
TRUE_NODE = 11
MEAN_APOG = 12
OSCU_APOG = 13
EARTH = 14
CHIRON = 15
PHOLUS = 16
CERES = 17
PALLAS = 18
JUNO = 19
VESTA = 20
INTP_APOG = 21
INTP_PERG = 22
NPLANETS = 23
PLMOON_OFFSET = 9000
AST_OFFSET = 10000
VARUNA = AST_OFFSET + 20000
FICT_OFFSET = 40
FICT_OFFSET_1 = 39
FICT_MAX = 999
NFICT_ELEM = 15
COMET_OFFSET = 1000
NALL_NAT_POINTS = NPLANETS + NFICT_ELEM
CUPIDO = 40
HADES = 41
ZEUS = 42
KRONOS = 43
APOLLON = 44
ADMETOS = 45
VULKANUS = 46
POSEIDON = 47
ISIS = 48
NIBIRU = 49
HARRINGTON = 50
NEPTUNE_LEVERRIER = 51
NEPTUNE_ADAMS = 52
PLUTO_LOWELL = 53
PLUTO_PICKERING = 54
VULCAN = 55
WHITE_MOON = 56
PROSERPINA = 57
WALDEMATH = 58
FIXSTAR = -10
ASC = 0
MC = 1
ARMC = 2
VERTEX = 3
EQUASC = 4
COASC1 = 5
COASC2 = 6
POLASC = 7
NASCMC = 8
FLG_JPLEPH = 1
FLG_SWIEPH = 2
FLG_MOSEPH = 4
FLG_HELCTR = 8
FLG_TRUEPOS = 16
FLG_J2000 = 32
FLG_NONUT = 64
FLG_SPEED3 = 128
FLG_SPEED = 256
FLG_NOGDEFL = 512
FLG_NOABERR = 1024
FLG_ASTROMETRIC = FLG_NOABERR|FLG_NOGDEFL
FLG_EQUATORIAL = 2048
FLG_XYZ = 4096
FLG_RADIANS = 8192
FLG_BARYCTR = 16384
FLG_TOPOCTR = 32768
FLG_ORBEL_AA = FLG_TOPOCTR
FLG_TROPICAL = 0
FLG_SIDEREAL = 65536
FLG_ICRS = 131072
FLG_DPSIDEPS_1980 = 262144
FLG_JPLHOR = FLG_DPSIDEPS_1980
FLG_JPLHOR_APPROX = 524288
FLG_CENTER_BODY = 1048576
FLG_TEST_PLMOON = 2*1024*1024 | FLG_J2000 | FLG_ICRS | FLG_HELCTR | FLG_TRUEPOS
SIDBITS = 256
SIDBIT_ECL_T0 = 256
SIDBIT_SSY_PLANE = 512
SIDBIT_USER_UT = 1024
SIDBIT_ECL_DATE = 2048
SIDBIT_NO_PREC_OFFSET = 4096
SIDBIT_PREC_ORIG = 8192
SIDM_FAGAN_BRADLEY = 0
SIDM_LAHIRI = 1
SIDM_DELUCE = 2
SIDM_RAMAN = 3
SIDM_USHASHASHI = 4
SIDM_KRISHNAMURTI = 5
SIDM_DJWHAL_KHUL = 6
SIDM_YUKTESHWAR = 7
SIDM_JN_BHASIN = 8
SIDM_BABYL_KUGLER1 = 9
SIDM_BABYL_KUGLER2 = 10
SIDM_BABYL_KUGLER3 = 11
SIDM_BABYL_HUBER = 12
SIDM_BABYL_ETPSC = 13
SIDM_ALDEBARAN_15TAU = 14
SIDM_HIPPARCHOS = 15
SIDM_SASSANIAN = 16
SIDM_GALCENT_0SAG = 17
SIDM_J2000 = 18
SIDM_J1900 = 19
SIDM_B1950 = 20
SIDM_SURYASIDDHANTA = 21
SIDM_SURYASIDDHANTA_MSUN = 22
SIDM_ARYABHATA = 23
SIDM_ARYABHATA_MSUN = 24
SIDM_SS_REVATI = 25
SIDM_SS_CITRA = 26
SIDM_TRUE_CITRA = 27
SIDM_TRUE_REVATI = 28
SIDM_TRUE_PUSHYA = 29
SIDM_GALCENT_RGILBRAND = 30
SIDM_GALEQU_IAU1958 = 31
SIDM_GALEQU_TRUE = 32
SIDM_GALEQU_MULA = 33
SIDM_GALALIGN_MARDYKS = 34
SIDM_TRUE_MULA = 35
SIDM_GALCENT_MULA_WILHELM = 36
SIDM_ARYABHATA_522 = 37
SIDM_BABYL_BRITTON = 38
SIDM_TRUE_SHEORAN = 39
SIDM_GALCENT_COCHRANE = 40
SIDM_GALEQU_FIORENZA = 41
SIDM_VALENS_MOON = 42
SIDM_LAHIRI_1940 = 43
SIDM_LAHIRI_VP285 = 44
SIDM_KRISHNAMURTI_VP291 = 45
SIDM_LAHIRI_ICRC = 46
SIDM_MANJULA = 43
SIDM_USER = 255
NSIDM_PREDEF = 47
NODBIT_MEAN = 1
NODBIT_OSCU = 2
NODBIT_OSCU_BAR = 4
NODBIT_FOPOINT = 256
FLG_DEFAULTEPH = FLG_SWIEPH
MAX_STNAME = 256
ECL_CENTRAL = 1
ECL_NONCENTRAL = 2
ECL_TOTAL = 4
ECL_ANNULAR = 8
ECL_PARTIAL = 16
ECL_ANNULAR_TOTAL = 32
ECL_HYBRID = 32
ECL_PENUMBRAL = 64
ECL_ALLTYPES_SOLAR = ECL_CENTRAL|ECL_NONCENTRAL|ECL_TOTAL|ECL_ANNULAR|ECL_PARTIAL|ECL_ANNULAR_TOTAL
ECL_ALLTYPES_LUNAR = ECL_TOTAL|ECL_PARTIAL|ECL_PENUMBRAL
ECL_VISIBLE = 128
ECL_MAX_VISIBLE = 256
ECL_1ST_VISIBLE = 512
ECL_PARTBEG_VISIBLE = 512
ECL_2ND_VISIBLE = 1024
ECL_TOTBEG_VISIBLE = 1024
ECL_3RD_VISIBLE = 2048
ECL_TOTEND_VISIBLE = 2048
ECL_4TH_VISIBLE = 4096
ECL_PARTEND_VISIBLE = 4096
ECL_PENUMBBEG_VISIBLE = 8192
ECL_PENUMBEND_VISIBLE = 16384
ECL_OCC_BEG_DAYLIGHT = 8192
ECL_OCC_END_DAYLIGHT = 16384
ECL_ONE_TRY = 32768
CALC_RISE = 1
CALC_SET = 2
CALC_MTRANSIT = 4
CALC_ITRANSIT = 8
BIT_DISC_CENTER = 256
BIT_DISC_BOTTOM = 8192
BIT_GEOCTR_NO_ECL_LAT = 128
BIT_NO_REFRACTION = 512
BIT_CIVIL_TWILIGHT = 1024
BIT_NAUTIC_TWILIGHT = 2048
BIT_ASTRO_TWILIGHT = 4096
BIT_FIXED_DISC_SIZE = 16384
BIT_FORCE_SLOW_METHOD = 32768
BIT_HINDU_RISING = BIT_DISC_CENTER|BIT_NO_REFRACTION|BIT_GEOCTR_NO_ECL_LAT
ECL2HOR = 0
EQU2HOR = 1
HOR2ECL = 0
HOR2EQU = 1
TRUE_TO_APP = 0
APP_TO_TRUE = 1
DE_NUMBER = 431
FNAME_DE200 = "de200.eph"
FNAME_DE403 = "de403.eph"
FNAME_DE404 = "de404.eph"
FNAME_DE405 = "de405.eph"
FNAME_DE406 = "de406.eph"
FNAME_DE431 = "de431.eph"
FNAME_DFT = FNAME_DE431
FNAME_DFT2 = FNAME_DE406
STARFILE_OLD = "fixstars.cat"
STARFILE = "sefstars.txt"
ASTNAMFILE = "seasnam.txt"
FICTFILE = "seorbel.txt"
HELIACAL_RISING = 1
HELIACAL_SETTING = 2
MORNING_FIRST = HELIACAL_RISING
EVENING_LAST = HELIACAL_SETTING
EVENING_FIRST = 3
MORNING_LAST = 4
ACRONYCHAL_RISING = 5
ACRONYCHAL_SETTING = 6
COSMICAL_SETTING = ACRONYCHAL_SETTING
HELFLAG_LONG_SEARCH = 128
HELFLAG_HIGH_PRECISION = 256
HELFLAG_OPTICAL_PARAMS = 512
HELFLAG_NO_DETAILS = 1024
HELFLAG_SEARCH_1_PERIOD = 2048
HELFLAG_VISLIM_DARK = 4096
HELFLAG_VISLIM_NOMOON = 8192
HELFLAG_VISLIM_PHOTOPIC = 16384
HELFLAG_VISLIM_SCOTOPIC = 32768
HELFLAG_AV = 65536
HELFLAG_AVKIND_VR = 65536
HELFLAG_AVKIND_PTO = 131072
HELFLAG_AVKIND_MIN7 = 262144
HELFLAG_AVKIND_MIN9 = 524288
HELFLAG_AVKIND = HELFLAG_AVKIND_VR|HELFLAG_AVKIND_PTO|HELFLAG_AVKIND_MIN7|HELFLAG_AVKIND_MIN9
TJD_INVALID = 99999999.0
SIMULATE_VICTORVB = 1
HELIACAL_LONG_SEARCH = 128
HELIACAL_HIGH_PRECISION = 256
HELIACAL_OPTICAL_PARAMS = 512
HELIACAL_NO_DETAILS = 1024
HELIACAL_SEARCH_1_PERIOD = 2048
HELIACAL_VISLIM_DARK = 4096
HELIACAL_VISLIM_NOMOON = 8192
HELIACAL_VISLIM_PHOTOPIC = 16384
HELIACAL_AVKIND_VR = 32768
HELIACAL_AVKIND_PTO = 65536
HELIACAL_AVKIND_MIN7 = 131072
HELIACAL_AVKIND_MIN9 = 262144
HELIACAL_AVKIND = HELFLAG_AVKIND_VR|HELFLAG_AVKIND_PTO|HELFLAG_AVKIND_MIN7|HELFLAG_AVKIND_MIN9
PHOTOPIC_FLAG = 0
SCOTOPIC_FLAG = 1
MIXEDOPIC_FLAG = 2
TIDAL_DE200 = -23.8946
TIDAL_DE403 = -25.58
TIDAL_DE404 = -25.58
TIDAL_DE405 = -25.826
TIDAL_DE406 = -25.826
TIDAL_DE421 = -25.85
TIDAL_DE422 = -25.85
TIDAL_DE430 = -25.82
TIDAL_DE431 = -25.8
TIDAL_DE441 = -25.936
TIDAL_26 = -26.0
TIDAL_STEPHENSON_2016 = -25.85
TIDAL_DEFAULT = TIDAL_DE431
TIDAL_AUTOMATIC = 999999
TIDAL_MOSEPH = TIDAL_DE404
TIDAL_SWIEPH = TIDAL_DEFAULT
TIDAL_JPLEPH = TIDAL_DEFAULT
DELTAT_AUTOMATIC = -1e-10
MODEL_DELTAT = 0
MODEL_PREC_LONGTERM = 1
MODEL_PREC_SHORTTERM = 2
MODEL_NUT = 3
MODEL_BIAS = 4
MODEL_JPLHOR_MODE = 5
MODEL_JPLHORA_MODE = 6
MODEL_SIDT = 7
NSE_NMODELS = 8
MOD_NPREC = 11
MOD_PREC_IAU_1976 = 1
MOD_PREC_LASKAR_1986 = 2
MOD_PREC_WILL_EPS_LASK = 3
MOD_PREC_WILLIAMS_1994 = 4
MOD_PREC_SIMON_1994 = 5
MOD_PREC_IAU_2000 = 6
MOD_PREC_BRETAGNON_2003 = 7
MOD_PREC_IAU_2006 = 8
MOD_PREC_VONDRAK_2011 = 9
MOD_PREC_OWEN_1990 = 10
MOD_PREC_NEWCOMB = 11
MOD_PREC_DEFAULT = MOD_PREC_VONDRAK_2011
MOD_PREC_DEFAULT_SHORT = MOD_PREC_VONDRAK_2011
MOD_NNUT = 5
MOD_NNUT_IAU_1980 = 1
MOD_NUT_IAU_CORR_1987 = 2
MOD_NUT_IAU_2000A = 3
MOD_NUT_IAU_2000B = 4
MOD_NUT_WOOLARD = 5
MOD_NUT_DEFAULT = MOD_NUT_IAU_2000B
MOD_NSIDT = 4
MOD_SIDT_IAU_1976 = 1
MOD_SIDT_IAU_2006 = 2
MOD_SIDT_IERS_CONV_2010 = 3
MOD_SIDT_LONGTERM = 4
MOD_SIDT_DEFAULT = MOD_SIDT_IERS_CONV_2010
MOD_NBIAS = 3
MOD_BIAS_NONE = 1
MOD_BIAS_IAU2000 = 2
MOD_BIAS_IAU2006 = 3
MOD_BIAS_DEFAULT = MOD_BIAS_IAU2006
MOD_NJPLHOR = 2
MOD_JPLHOR_LONG_AGREEMENT = 1
MOD_JPLHOR_DEFAULT = MOD_JPLHOR_LONG_AGREEMENT
MOD_NJPLHORA = 3
MOD_JPLHORA_1 = 1
MOD_JPLHORA_2 = 2
MOD_JPLHORA_3 = 3
MOD_JPLHORA_DEFAULT = MOD_JPLHORA_3
MOD_NDELTAT = 5
MOD_DELTAT_STEPHENSON_MORRISON_1984 = 1
MOD_DELTAT_STEPHENSON_1997 = 2
MOD_DELTAT_STEPHENSON_MORRISON_2004 = 3
MOD_DELTAT_ESPENAK_MEEUS_2006 = 4
MOD_DELTAT_STEPHENSON_ETC_2016 = 5
MOD_DELTAT_DEFAULT = MOD_DELTAT_STEPHENSON_ETC_2016
#CALL_CONV = "#define EXP32"
#EXP32 = "__declspec( dllexport )"

# Default swe_wrapper constants for Swiss Ephemeris
HINDU_FLAGS = BIT_HINDU_RISING | FLG_TRUEPOS | FLG_SPEED
SIDEREAL_FLAGS = FLG_SWIEPH | FLG_SIDEREAL | HINDU_FLAGS
# FLG_DEFAULTEPH = FLG_SWIEPH # Already assigned earlier - this is just for reference

if _DEBUG_APP: print("JHora: Constants Loaded")
if _DEBUG_APP: print("JHora: Loading function signatures")
# Function signatures
if _DEBUG_APP: print("JHora: Loading swe_revjul")
"""
void swe_revjul(
    double tjd,       /* Julian day number */
    int gregflag,     /* Gregorian calendar: 1, Julian calendar: 0 */
    int *year,        /* target addresses for year, etc. */
    int *month,
    int *day,
    double *hour);
"""
swe.swe_revjul.argtypes = [
    ctypes.c_double,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_int),
    ctypes.POINTER(ctypes.c_double)
]
swe.swe_revjul.restype = None
# Wrapper function
def revjul(jd, gregflag=GREG_CAL):
    if _DEBUG_APP: print("JHora: Calling revjul", jd, gregflag)
    year = ctypes.c_int()
    month = ctypes.c_int()
    day = ctypes.c_int()
    hour = ctypes.c_double()
    swe.swe_revjul(jd, gregflag,
                   ctypes.byref(year),
                   ctypes.byref(month),
                   ctypes.byref(day),
                   ctypes.byref(hour))
    if _DEBUG_APP: print("JHora: revjul return", year.value, month.value, day.value, hour.value)
    return year.value, month.value, day.value, hour.value

if _DEBUG_APP: print("JHora: Loading swe_julday")
if _DEBUG_APP: print("JHora: Loading swe_julday")
"""
double swe_julday(
    int year,
    int month,
    int day,
    double hour,
    int gregflag);
"""
swe.swe_julday.argtypes = [
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_double,
    ctypes.c_int
]
swe.swe_julday.restype = ctypes.c_double
# Wrapper function
"""
double swe_julday(
int year,
int month,
int day,
double hour,
int gregflag);
"""
def julday(year, month, day, hour=0.0, gregflag=GREG_CAL):
    if _DEBUG_APP: print("JHora: Calling julday",year, month, day, hour, gregflag)
    jday = swe.swe_julday(year, month, day, hour, gregflag)
    if _DEBUG_APP: print("JHora: julday return",jday)
    return jday

if _DEBUG_APP: print("JHora: Loading swe_get_ayanamsa")
swe.swe_get_ayanamsa.argtypes = [ctypes.c_double]
swe.swe_get_ayanamsa.restype = ctypes.c_double
# Wrapper function
"""
double swe_get_ayanamsa(
double tjd_et);     /* input: Julian day number in ET/TT */
"""
def get_ayanamsa(jd):
    if _DEBUG_APP: print("JHora: Calling get_ayanamsa",jd)
    ret = swe.swe_get_ayanamsa(jd)
    if _DEBUG_APP: print("JHora: get_ayanamsa return",ret)
    return ret

if _DEBUG_APP: print("JHora: Loading swe_set_sid_mode")
swe.swe_set_sid_mode.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double]
swe.swe_set_sid_mode.restype = None
# Wrapper function
"""
void swe_set_sid_mode(
int32 sid_mode,
double t0,               /* reference epoch */
double ayan_t0);    /* initial ayanamsha at t0 *//* The function calculates ayanamsha for a given date in UT.
* The return value is either the ephemeris flag used or ERR (-1) */
"""
def set_sid_mode(sid_mode, t0=0, ayan_t0=0):
    if _DEBUG_APP: print("JHora: Calling set_sid_mode",sid_mode,t0,ayan_t0,'returns nothing')
    swe.swe_set_sid_mode(sid_mode, t0, ayan_t0)

if _DEBUG_APP: print("JHora: Loading swe_calc_ut")
swe.swe_calc_ut.argtypes = [
    ctypes.c_double,                      # tjdut
    ctypes.c_int,                         # planet id
    ctypes.c_int,                         # flags
    ctypes.POINTER(ctypes.c_double),      # result[6]
    ctypes.POINTER(ctypes.c_char)         # error buffer
]
swe.swe_calc_ut.restype = ctypes.c_int

def calc_ut(jd_ut, planet_id, flags=SIDEREAL_FLAGS):
    if _DEBUG_APP: print("JHora: Calling calc_ut",jd_ut,planet_id,flags)
    result = (ctypes.c_double * 6)()
    err_msg = ctypes.create_string_buffer(256)

    ret = swe.swe_calc_ut(jd_ut, planet_id, flags, result, err_msg)
    if _DEBUG_APP: print("JHora: calc_ut return",tuple(result),ret)
    if ret < 0:
        raise ValueError(err_msg.value.decode())
    return tuple(result), ret

if _DEBUG_APP: print("JHora: Loading swe_rise_trans")
""" 
int32 swe_rise_trans(
double tjd_ut,      /* search after this time (UT) */
int32 ipl,               /* planet number, if planet or moon */
char *starname,     /* star name, if star; must be NULL or empty, if ipl is used */
int32 epheflag,     /* ephemeris flag */
int32 rsmi,              /* integer specifying that rise, set, or one of the two meridian transits is wanted. see definition below */
double *geopos,     /* array of three doubles containing
                        * geograph. long., lat., height of observer */
double atpress      /* atmospheric pressure in mbar/hPa */
double attemp,      /* atmospheric temperature in deg. C */
double *tret,            /* return address (double) for rise time etc. */
char *serr);             /* return address for error message */
"""
swe.swe_rise_trans.argtypes = [
    ctypes.c_double,                # tjdut
    ctypes.c_int,                   # planet id/body
    ctypes.c_char_p,                # star name (NULL if planet)
    ctypes.c_int,                   # epheflag
    ctypes.c_int,                   # rsmi
    ctypes.POINTER(ctypes.c_double),# geopos[3]
    ctypes.c_double,                # atpress
    ctypes.c_double,                # attemp
    ctypes.POINTER(ctypes.c_double),# tret[10]
    ctypes.POINTER(ctypes.c_char)         # error buffer
]
swe.swe_rise_trans.restype = ctypes.c_int

def rise_trans(jd_ut, body=SUN, rsmi=HINDU_FLAGS+CALC_RISE, geopos=(0,0,0), atpress=0.0, attemp=0.0, flags=FLG_DEFAULTEPH):

    """
    Calculate times of rising, setting, or meridian transits.

    Parameters:
        jd_ut (float): Julian day number (UT)
        body (int or str): Planet ID or fixed star name
        rsmi (int): Rise/set/transit mode flags
        geopos (list of float): [longitude, latitude, altitude] in degrees/meters
        atpress (float): Atmospheric pressure in mbar/hPa
        attemp (float): Atmospheric temperature in Celsius
        flags (int): Ephemeris flags (e.g., FLG_SWIEPH | FLG_TOPOCTR)

    Returns:
        tuple: (result_code, (tret0, tret1, ..., tret9))
            result_code: 0 if event found, -2 if object is circumpolar
            tret: list of 10 event times (Julian days)
    """
    if _DEBUG_APP: print("JHora: Calling rise_trans",jd_ut, body, rsmi, geopos, atpress, attemp, flags)
    # Determine if body is planet ID or star name
    if isinstance(body, int):
        planet_id = body
        star_name = None
    elif isinstance(body, str):
        planet_id = FIXSTAR  # or -10
        star_name = body.encode('utf-8')
    else:
        raise TypeError("body must be int (planet) or str (star name)")

    geo = (ctypes.c_double * 3)(*geopos)
    tret = (ctypes.c_double * 10)()
    err_msg = ctypes.create_string_buffer(256)

    # ✅ Set topocentric parameters if needed
    if flags & FLG_TOPOCTR:
        swe.swe_set_topo(geo[0], geo[1], geo[2])

    ret = swe.swe_rise_trans(jd_ut, planet_id, star_name, flags, rsmi, geo, atpress, attemp, tret, err_msg)
    if _DEBUG_APP: print("JHora: rise_transe return",ret,tuple(tret))
    if ret == -1:
        raise ValueError(err_msg.value.decode())
    return ret, tuple(tret)

swe.swe_rise_trans_true_hor.argtypes = [
    ctypes.c_double,                 # tjdut
    ctypes.c_int,                    # planet id
    ctypes.c_char_p,                 # star name (NULL if planet)
    ctypes.c_int,                    # epheflag
    ctypes.c_int,                    # rsmi
    ctypes.POINTER(ctypes.c_double), # geopos[3]
    ctypes.c_double,                 # atpress
    ctypes.c_double,                 # attemp
    ctypes.c_double,                 # horhgt
    ctypes.POINTER(ctypes.c_double), # tret[10]
    ctypes.POINTER(ctypes.c_char)         # error buffer
]
swe.swe_rise_trans_true_hor.restype = ctypes.c_int

def rise_trans_true_hor(jd_ut, body=SUN, rsmi=HINDU_FLAGS+CALC_RISE, geopos=(0,0,0), atpress=0.0, attemp=0.0, horhgt=0.0, flags=FLG_DEFAULTEPH):
    """
    Calculate times of rising, setting, or meridian transits with horizon height.

    Parameters:
        jd_ut (float): Julian day number (UT)
        body (int or str): Planet ID or fixed star name
        rsmi (int): Rise/set/transit mode flags
        geopos (list of float): [longitude, latitude, altitude] in degrees/meters
        atpress (float): Atmospheric pressure in mbar/hPa
        attemp (float): Atmospheric temperature in Celsius
        horhgt (float): Local horizon height in degrees
        flags (int): Ephemeris flags (e.g., FLG_SWIEPH | FLG_TOPOCTR)

    Returns:
        tuple: (result_code, (tret0, tret1, ..., tret9))
            result_code: 0 if event found, -2 if object is circumpolar
            tret: list of 10 event times (Julian days)
    """
    if _DEBUG_APP: print("JHora: calling rise_trans_true_hor",jd_ut, body, rsmi, geopos, atpress, attemp, horhgt, flags)
    if isinstance(body, int):
        planet_id = body
        star_name = None
    elif isinstance(body, str):
        planet_id = FIXSTAR
        star_name = body.encode('utf-8')
    else:
        raise TypeError("body must be int (planet) or str (star name)")

    geo = (ctypes.c_double * 3)(*geopos)
    tret = (ctypes.c_double * 10)()
    err_msg = ctypes.create_string_buffer(256)

    # ✅ Set topocentric parameters if needed
    if flags & FLG_TOPOCTR:
        swe.swe_set_topo(geo[0], geo[1], geo[2])

    ret = swe.swe_rise_trans_true_hor(jd_ut, planet_id, star_name, flags, rsmi, geo, atpress, attemp, horhgt, tret, err_msg)
    if _DEBUG_APP: print("JHora: swe_rise_trans_true_hor return",ret, tuple(tret))
    if ret == -1:
        raise ValueError(err_msg.value.decode())
    return ret, tuple(tret)
if _DEBUG_APP: print("JHora: Loading swe_houses_ex")
"""
/* extended function; to compute tropical or sidereal positions of house cusps */
int swe_houses_ex(
double tjd_ut,      /* Julian day number, UT */
int32 iflag,        /* 0 or SEFLG_SIDEREAL or SEFLG_RADIANS or SEFLG_NONUT */
double geolat,      /* geographic latitude, in degrees */
double geolon,      /* geographic longitude, in degrees
                   * eastern longitude is positive,
                   * western longitude is negative,
                   * northern latitude is positive,
                   * southern latitude is negative */
int hsys,                /* house method, one-letter case sensitive code (list, see further below) */
double *cusps,      /* array for 13 (or 37 for hsys G) doubles, explained further below */
double *ascmc);     /* array for 10 doubles, explained further below */
"""
swe.swe_houses_ex.argtypes = [
    ctypes.c_double,                # tjd_ut
    ctypes.c_int,                   # iflag
    ctypes.c_double,                # geolat
    ctypes.c_double,                # geolon
    ctypes.c_char,                  # hsys (char code)
    ctypes.POINTER(ctypes.c_double),# cusps[13]
    ctypes.POINTER(ctypes.c_double) # ascmc[10]
]
swe.swe_houses_ex.restype = ctypes.c_int
def houses_ex(jd_ut, geolat, geolon, hsys='P', flags=SIDEREAL_FLAGS):
    if _DEBUG_APP: print("JHora: Calling houses_ex",jd_ut,geolat,geolon,hsys,flags)
    cusps = (ctypes.c_double * 13)()
    ascmc = (ctypes.c_double * 10)()
    hsys_char = hsys.encode('ascii')[0]
    ret = swe.swe_houses_ex(jd_ut, flags, geolat, geolon, hsys_char, cusps, ascmc)
    if _DEBUG_APP: print("JHora: houses_ex return ",list(cusps), list(ascmc))
    if ret < 0:
        raise ValueError("Error computing houses")
    return list(cusps), list(ascmc)

if _DEBUG_APP: print("JHora: Loading swe_sol_eclipse_how")
"""
int32 swe_sol_eclipse_how(
double tjd_ut,      /* time, Jul. day UT */
int32 ifl,          /* ephemeris flag */
double *geopos,     /* geogr. longitude, latitude, height */
                   * eastern longitude is positive,
                   * western longitude is negative,
                   * northern latitude is positive,
                   * southern latitude is negative */
double *attr,       /* return array, 20 doubles, see below */
char *serr);        /* return error string */
"""
swe.swe_sol_eclipse_how.argtypes = [ctypes.c_double, ctypes.c_int, ctypes.POINTER(ctypes.c_double),
                                    ctypes.POINTER(ctypes.c_double), ctypes.c_char_p]
swe.swe_sol_eclipse_how.restype = ctypes.c_int
def sol_eclipse_how(jd_ut, iflag, geopos):
    if _DEBUG_APP: print("JHora: Calling sol_eclipse_how",jd_ut, iflag, geopos)
    geo = (ctypes.c_double * 3)(*geopos)
    attr = (ctypes.c_double * 20)()
    err_msg = ctypes.create_string_buffer(256)
    # ✅ Set topocentric parameters if needed
    if iflag & FLG_TOPOCTR:
        swe.swe_set_topo(geo[0], geo[1], geo[2])
    ret = swe.swe_sol_eclipse_how(jd_ut, iflag, geo, attr, err_msg)
    if _DEBUG_APP: print("JHora: sol_eclipse_how",list(attr))
    if ret < 0:
        raise ValueError(err_msg.value.decode())
    return ret,list(attr)

if _DEBUG_APP: print("JHora: Loading swe_sol_eclipse_when_loc")
"""
int32 swe_sol_eclipse_when_loc(
double tjd_start,   /* start date for search, Jul. day UT */
int32 ifl,          /* ephemeris flag */
double *geopos,     /* 3 doubles for geo. lon, lat, height */
                   * eastern longitude is positive,
                   * western longitude is negative,
                   * northern latitude is positive,
                   * southern latitude is negative */
double *tret,       /* return array, 10 doubles, see below */
double *attr,       /* return array, 20 doubles, see below */
AS_BOOL backward,   /* TRUE, if backward search */
char *serr);        /* return error string */
"""
swe.swe_sol_eclipse_when_loc.argtypes = [
    ctypes.c_double,                # tjd_ut
    ctypes.c_int,                   # flags
    ctypes.POINTER(ctypes.c_double),# geopos[3]
    ctypes.POINTER(ctypes.c_double),# tret[10]
    ctypes.POINTER(ctypes.c_double),# attr[20]
    ctypes.c_int,                   # backward
    ctypes.POINTER(ctypes.c_char)         # error buffer
]
swe.swe_sol_eclipse_when_loc.restype = ctypes.c_int

def sol_eclipse_when_loc(jd_ut, geopos, flags=FLG_SIDEREAL, backward=False):
    if _DEBUG_APP: print("JHora: Calling sol_eclipse_when_loc",jd_ut, geopos, flags, backward)
    geo = (ctypes.c_double * 3)(*geopos)
    tret = (ctypes.c_double * 10)()
    attr = (ctypes.c_double * 20)()
    err_msg = ctypes.create_string_buffer(256)

    # ✅ Set topocentric parameters if needed
    if flags & FLG_TOPOCTR:
        swe.swe_set_topo(geo[0], geo[1], geo[2])

    ret = swe.swe_sol_eclipse_when_loc(jd_ut, flags, geo, tret, attr, int(backward), err_msg)
    if _DEBUG_APP: print("JHora: sol_eclipse_when_loc",ret, tuple(tret), tuple(attr))
    if ret < 0:
        raise ValueError(err_msg.value.decode())
    return ret, tuple(tret), tuple(attr)


if _DEBUG_APP: print("JHora: Loading swe_lun_eclipse_how")
"""
int32 swe_lun_eclipse_how(
double tjd_ut,      /* time, Jul. day UT */
int32 ifl,          /* ephemeris flag */
double *geopos,     /* input array, geopos, geolon, geoheight */
                   * eastern longitude is positive,
                   * western longitude is negative,
                   * northern latitude is positive,
                   * southern latitude is negative */
double *attr,       /* return array, 20 doubles, see below */
char *serr);        /* return error string */
"""
swe.swe_lun_eclipse_how.argtypes = [
    ctypes.c_double,                # tjd_ut
    ctypes.c_int,                   # flags
    ctypes.POINTER(ctypes.c_double),# geopos[3]
    ctypes.POINTER(ctypes.c_double),# attr[20]
    ctypes.POINTER(ctypes.c_char)         # error buffer
]
swe.swe_lun_eclipse_how.restype = ctypes.c_int

def lun_eclipse_how(jd_ut, geopos, flags=FLG_SIDEREAL):
    if _DEBUG_APP: print("JHora: lun_eclipse_how",jd_ut, geopos, flags)
    geo = (ctypes.c_double * 3)(*geopos)
    attr = (ctypes.c_double * 20)()
    err_msg = ctypes.create_string_buffer(256)

    # ✅ Set topocentric parameters if needed
    if flags & FLG_TOPOCTR:
        swe.swe_set_topo(geo[0], geo[1], geo[2])

    ret = swe.swe_lun_eclipse_how(jd_ut, flags, geo, attr, err_msg)
    if _DEBUG_APP: print("JHora: lun_eclipse_how",ret, tuple(attr))
    if ret < 0:
        raise ValueError(err_msg.value.decode())
    return ret, tuple(attr)

if _DEBUG_APP: print("JHora: Loading swe_lun_eclipse_when_loc")
"""
int32 swe_lun_eclipse_when_loc(
double tjd_start,   /* start date for search, Jul. day UT */
int32 ifl,          /* ephemeris flag */
double *geopos,     /* 3 doubles for geo. lon, lat, height
                   * eastern longitude is positive,
                   * western longitude is negative,
                   * northern latitude is positive,
                   * southern latitude is negative */
double *tret,       /* return array, 10 doubles, see below */
double *attr,       /* return array, 20 doubles, see below */
AS_BOOL backward,   /* TRUE, if backward search */
char *serr);        /* return error string */
"""
swe.swe_lun_eclipse_when_loc.argtypes = [
    ctypes.c_double,                # tjd_ut
    ctypes.c_int,                   # flags
    ctypes.POINTER(ctypes.c_double),# geopos[3]
    ctypes.POINTER(ctypes.c_double),# tret[10]
    ctypes.POINTER(ctypes.c_double),# attr[20]
    ctypes.c_int,                   # backward
    ctypes.POINTER(ctypes.c_char)         # error buffer
]
swe.swe_lun_eclipse_when_loc.restype = ctypes.c_int

def lun_eclipse_when_loc(jd_ut, geopos, flags=FLG_SIDEREAL, backward=False):
    geo = (ctypes.c_double * 3)(*geopos)
    tret = (ctypes.c_double * 10)()
    attr = (ctypes.c_double * 20)()
    err_msg = ctypes.create_string_buffer(256)

    # ✅ Set topocentric parameters if needed
    if flags & FLG_TOPOCTR:
        swe.swe_set_topo(geo[0], geo[1], geo[2])

    ret = swe.swe_lun_eclipse_when_loc(jd_ut, flags, geo, tret, attr, int(backward), err_msg)
    if _DEBUG_APP: print("JHora: lun_eclipse_when_loc",ret, tuple(tret), tuple(attr))
    if ret < 0:
        raise ValueError(err_msg.value.decode())
    return ret, tuple(tret), tuple(attr)

if _DEBUG_APP: print("JHora: Loading swe_set_ephe_path")
swe.swe_set_ephe_path.argtypes = [ctypes.c_char_p]
swe.swe_set_ephe_path.restype = None

def set_ephe_path(path):
    swe.swe_set_ephe_path(path.encode('utf-8'))

if _DEBUG_APP: print("JHora: Loading swe_fixstar_ut")
swe.swe_fixstar_ut.argtypes = [
    ctypes.c_char_p,                 # star name
    ctypes.c_double,                 # tjdut
    ctypes.c_int,                    # flags
    ctypes.POINTER(ctypes.c_double),# xx[6]
    ctypes.POINTER(ctypes.c_char)         # error buffer
]
swe.swe_fixstar_ut.restype = ctypes.c_int

def fixstar_ut(star_name, jd_ut, flags=FLG_SWIEPH):
    """
    Calculate fixed star positions (UT).

    Parameters:
        star_name (str): Name of the fixed star
        jd_ut (float): Julian day number (UT)
        flags (int): Ephemeris flags (e.g., FLG_SWIEPH | FLG_SIDEREAL)

    Returns:
        tuple: (position_data, star_name, retflags)
            position_data: tuple of 6 floats
            star_name: possibly corrected star name returned by Swiss Ephemeris
            retflags: bit flags indicating what computation was done
    """
    xx = (ctypes.c_double * 6)()
    err_msg = ctypes.create_string_buffer(256)

    ret = swe.swe_fixstar_ut(star_name.encode('utf-8'), jd_ut, flags, xx, err_msg)
    if _DEBUG_APP: print("JHora: swe_fixstar_ut",tuple(xx), star_name, ret)
    if ret < 0:
        raise ValueError(err_msg.value.decode())
    return tuple(xx), star_name, ret


if _DEBUG_APP: print("JHora: Loading swe_utc_time_zone")
swe.swe_utc_time_zone.argtypes = [
    ctypes.c_int, ctypes.c_int, ctypes.c_int,  # year, month, day
    ctypes.c_int, ctypes.c_int, ctypes.c_double,  # hour, minute, second
    ctypes.c_double,  # timezone offset
    ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int),  # year, month, day out
    ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_double)  # hour, minute, second out
]
swe.swe_utc_time_zone.restype = None

def utc_time_zone(iyear, imonth, iday, ihour, imin, dsec, timezone):
    """
    Convert UTC time with time zone to UTC time without time zone.

    Parameters:
        iyear, imonth, iday (int): Input date
        ihour, imin (int): Input time
        dsec (float): Seconds
        timezone (float): Time zone offset in hours

    Returns:
        tuple: (year, month, day, hour, minute, second) in UTC
    """
    y_out = ctypes.c_int()
    m_out = ctypes.c_int()
    d_out = ctypes.c_int()
    h_out = ctypes.c_int()
    min_out = ctypes.c_int()
    sec_out = ctypes.c_double()

    swe.swe_utc_time_zone(
        iyear, imonth, iday, ihour, imin, dsec, timezone,
        ctypes.byref(y_out), ctypes.byref(m_out), ctypes.byref(d_out),
        ctypes.byref(h_out), ctypes.byref(min_out), ctypes.byref(sec_out)
    )
    if _DEBUG_APP: print("JHora: swe_utc_time_zone",y_out.value, m_out.value, d_out.value, h_out.value, min_out.value, sec_out.value)
    return y_out.value, m_out.value, d_out.value, h_out.value, min_out.value, sec_out.value



if _DEBUG_APP: print("JHora: Loading swe_utc_to_jd")
swe.swe_utc_to_jd.argtypes = [
    ctypes.c_int, ctypes.c_int, ctypes.c_int,  # year, month, day
    ctypes.c_int, ctypes.c_int, ctypes.c_double,  # hour, minute, second
    ctypes.c_int,  # gregflag
    ctypes.POINTER(ctypes.c_double),  # dret[2]
    ctypes.POINTER(ctypes.c_char)         # error buffer
]
swe.swe_utc_to_jd.restype = ctypes.c_int

def utc_to_jd(iyear, imonth, iday, ihour, imin, dsec, gregflag=GREG_CAL):
    """
    Convert UTC date and time to Julian day number.

    Parameters:
        iyear, imonth, iday (int): Input date
        ihour, imin (int): Input time
        dsec (float): Seconds
        gregflag (int): Calendar flag (GREG_CAL or JUL_CAL)

    Returns:
        tuple: (jd_et, jd_ut)
    """
    dret = (ctypes.c_double * 2)()
    err_msg = ctypes.create_string_buffer(256)

    ret = swe.swe_utc_to_jd(iyear, imonth, iday, ihour, imin, dsec, gregflag, dret, err_msg)
    if _DEBUG_APP: print("JHora: swe_utc_to_jd",dret[0], dret[1])
    if ret < 0:
        raise ValueError(err_msg.value.decode())
    return dret[0], dret[1]
if _DEBUG_APP: print("JHora: Done loading wrapper functions - End of swisseph.py")
import pandas as pd

sats = pd.read_excel("UCS-Satellite-Database-5-1-2022.xls")

sites = sats["Launch Site"].unique()
sitedict = {
    'Satish Dhawan Space Centre': 'India',
    'Guiana Space Center': 'France',
    'Cape Canaveral': 'USA',
    'Baikonur Cosmodrome': 'Russia',
    'Vandenberg AFB': 'USA',
    'Cygnus': None,
    'Rocket Lab Launch Complex 1': 'New Zealand',
    'Dombarovsky Air Base': 'Russia',
    'Wallops Island Flight Facility': 'USA',
    'Xichang Satellite Launch Center': 'China',
    'Vostochny Cosmodrome': 'Russia',
    'Uchinoura Space Center': 'Japan',
    'Jiuquan Satellite Launch Center': 'China',
    'Plesetsk Cosmodrome': 'Russia',
    'Taiyuan Launch Center': 'China',
    'Virgin Orbit': None,
    'Yellow Sea Launch Platform': 'China',
    'FANTM-RAiL [Xtenti]': 'USA',
    'Wenchang Space Center': 'China',
    'Orbital ATK L-1011': None,
    'Tanegashima Space Center': 'Japan',
    'International Space Station': None,
    'Antares': None,
    'Sea Launch Odyssey': None,
    'Svobodny Cosmodrome': 'Russia',
    'Kodiak Launch Complex': 'USA',  # duplicate
    'Stargazer L-1011': None,
    'Kwajalein Island': 'USA',
    'International Space Station - Cygnus': None,  # duplicate
    'Shahroud Missile Range': 'Iran',
    'Palmachim Launch Complex': 'Israel',
    'Kodiak Island': 'USA',
    'nan': None,
    'FANTM-RAiL (Xtenti)': 'USA',  # duplicate
    'Wenchang Satellite Launch Center': 'China',
    'Dragon CRS-17': None,
    'International Space Station - Antares': None,  # duplicate
    'Satish Dhawan': 'India',  # duplicate
    'Rocket Lab Launch Complex 1B': 'New Zealand',  # duplicate
    'Naro Space Center': 'South Korea'
}

# for site in sites:
#     if site

from pathlib import Path

###############################################################################
# APPLICATION DIRS
###############################################################################

BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent

CITY_DATA_DIR: Path = BASE_DIR / 'data'

FILENAME: str = 'fifty_biggest_cities_by_population.csv'

CITY_DATA_FILE: Path = CITY_DATA_DIR / FILENAME

###############################################################################
# APPLICATION INFO
###############################################################################

TITLE_APP: str = 'Weather Collector'

DESCRIPTION_APP: str = 'Weather Collector'

###############################################################################
# CITIES INFO
###############################################################################

CITIES_NUMBER: int = 50

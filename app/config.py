import os

from dotenv import load_dotenv

load_dotenv()

TMAP_APP_KEY = os.getenv("TMAP_APP_KEY")
TMAP_BASE_URL = "https://apis.openapi.sk.com/tmap"

STOP_CANDIDATE_COUNT = 3

POI_INITIAL_RADIUS_KM = 3
POI_MAX_INITIAL_RADIUS_KM = 3
POI_MAX_RADIUS_KM = 33
POI_RADIUS_EXPAND_FACTOR = 2.0
POI_CANDIDATE_COUNT = 3
POI_FETCH_COUNT = 30

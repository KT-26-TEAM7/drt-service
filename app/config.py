import os

from dotenv import load_dotenv

load_dotenv()

TMAP_APP_KEY = os.getenv("TMAP_APP_KEY")
TMAP_BASE_URL = "https://apis.openapi.sk.com/tmap"

NEARBY_STOP_CANDIDATE_COUNT = 3
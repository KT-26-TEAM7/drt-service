import os

from dotenv import load_dotenv

load_dotenv()

TMAP_APP_KEY = os.getenv("TMAP_APP_KEY")
TMAP_BASE_URL = "https://apis.openapi.sk.com/tmap"

if not TMAP_APP_KEY:
    raise RuntimeError("TMAP_APP_KEY 환경변수가 설정되지 않았습니다.")

"""출발 정류장과 하차 정류장 사이의 DRT 경로 계산."""

from app.clients.tmap import TMapClient
from app.schemas.route import DrtRouteSummary
from app.schemas.stop import DRTStop


async def calculate_drt_route(
    boarding_stop: DRTStop,
    dropoff_stop: DRTStop,
    client: TMapClient | None = None,
) -> DrtRouteSummary:
    # TODO: DRT 이동시간 산정 
    pass

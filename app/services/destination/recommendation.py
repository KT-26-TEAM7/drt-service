"""대분류 목적지별 이동 비용을 비교해 최종 목적지를 추천한다."""

from app.schemas.destination import DestinationCandidate
from app.schemas.route import DestinationRecommendationResponse
from app.schemas.stop import StopWalkingRoute


async def recommend_destination(
    destinations: list[DestinationCandidate],
    boarding_stop: StopWalkingRoute,
) -> DestinationRecommendationResponse:
    # TODO: 목적지별 최적 하차 정류장과 DRT 경로를 계산한다.
    # TODO: evaluate_destination_route()로 전체 시간과 거리를 합산한다.
    # TODO: 일부 목적지 실패 시 나머지 목적지 평가를 계속한다.
    # TODO: 총 이동시간, 총 이동거리, 목적지명 순으로 최종 후보를 선택한다.
    pass

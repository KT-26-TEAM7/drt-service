from app.schemas.destination import (
    DestinationCandidate,
    DestinationConfirmationRequest,
    DestinationConfirmationResponse,
    DestinationConfirmationStatus,
    DestinationSearchResponse,
    DestinationSearchType,
)

class DestinationConfirmationError(ValueError):
    """목적지 확인 요청 처리 중 발생한 오류."""

def _build_destination_description(destination: DestinationCandidate) -> str:
    location = destination.neighborhood or destination.district
    category = destination.category or destination.detail_category

    if location and category:
        return (
            f"{location}에 위치한 "
            f"{category} {destination.name}"
        )

    if location:
        return f"{location}에 위치한 {destination.name}"

    if category:
        return f"{category} {destination.name}"

    return destination.name


def build_destination_confirmation(destinations: list[DestinationCandidate]) -> DestinationSearchResponse:
    total_count = len(destinations)

    if total_count == 0:
        return DestinationSearchResponse(
            total_count=0,
            search_type=DestinationSearchType.NOT_FOUND,
            message=("검색된 장소가 없습니다. 정확한 장소명을 다시 한 번 말씀해주세요."),
            destinations=[],
        )

    if total_count == 1:
        destination = destinations[0]
        description = _build_destination_description(destination)

        return DestinationSearchResponse(
            total_count=1,
            search_type=DestinationSearchType.SINGLE,
            message=(f"검색된 장소는 {description}입니다. 이곳으로 이동하시겠습니까?"),
            destinations=destinations,
        )

    return DestinationSearchResponse(
        total_count=total_count,
        search_type=DestinationSearchType.MULTIPLE,
        message=("검색된 장소가 여러 개 있습니다. 주소를 확인하고 이동할 장소를 선택해주세요."),
        destinations=destinations,
    )

def confirm_destination(request: DestinationConfirmationRequest) -> DestinationConfirmationResponse:
    if not request.confirmed:
        return DestinationConfirmationResponse(
            status=DestinationConfirmationStatus.CANCELLED,
            message=("목적지 선택을 취소했습니다. 다른 목적지를 말씀해주세요."),
            destination=None,
        )

    if request.destination is None:
        raise DestinationConfirmationError("확인할 목적지 정보가 없습니다.")

    destination = request.destination

    return DestinationConfirmationResponse(
        status=DestinationConfirmationStatus.CONFIRMED,
        message=(f"{destination.name}을 목적지로 설정했습니다."),
        destination=destination,
    )
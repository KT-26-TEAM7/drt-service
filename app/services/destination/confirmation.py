"""사용자의 목적지 확정 또는 취소 요청을 처리한다."""

from app.schemas.destination import (
    DestinationConfirmationRequest,
    DestinationConfirmationResponse,
    DestinationConfirmationStatus,
)


class DestinationConfirmationError(ValueError):
    """목적지 확인 요청 처리 중 발생한 오류."""


def confirm_destination(
    request: DestinationConfirmationRequest,
) -> DestinationConfirmationResponse:
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

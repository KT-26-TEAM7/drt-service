from typing import Any

from app.clients.tmap import TMapClient
from app.schemas.destination import DestinationCandidate, DestinationSearchResponse


class DestinationSearchError(RuntimeError):
    """목적지 검색 응답 처리 중 발생한 오류."""


def _normalize_text(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).strip()
    return text or None


def _extract_coordinates(raw_destination: dict[str, Any],) -> tuple[float, float] | None:
    coordinate_pairs = [
        ("pnsLat", "pnsLon"),
        ("frontLat", "frontLon"),
        ("noorLat", "noorLon"),
    ]

    for latitude_key, longitude_key in coordinate_pairs:
        latitude = raw_destination.get(latitude_key)
        longitude = raw_destination.get(longitude_key)

        if latitude in (None, "") or longitude in (None, ""):
            continue

        try:
            return float(latitude), float(longitude)
        except (TypeError, ValueError):
            continue

    return None


def _extract_road_address(raw_destination: dict[str, Any],) -> str | None:
    new_address_list = raw_destination.get("newAddressList") or {}

    if not isinstance(new_address_list, dict):
        return None

    new_addresses = new_address_list.get("newAddress") or []

    if isinstance(new_addresses, dict):
        new_addresses = [new_addresses]

    if not isinstance(new_addresses, list):
        return None

    for new_address in new_addresses:
        if not isinstance(new_address, dict):
            continue

        full_address = _normalize_text(
            new_address.get("fullAddressRoad")
        )

        if full_address:
            return full_address

    return None


def _extract_lot_address(raw_destination: dict[str, Any]) -> str | None:
    address_parts = [
        _normalize_text(raw_destination.get("upperAddrName")),
        _normalize_text(raw_destination.get("middleAddrName")),
        _normalize_text(raw_destination.get("lowerAddrName")),
    ]

    address_parts = [
        part for part in address_parts if part
    ]

    first_number = _normalize_text(
        raw_destination.get("firstNo")
    )
    second_number = _normalize_text(
        raw_destination.get("secondNo")
    )

    if first_number:
        lot_number = first_number

        if second_number and second_number != "0":
            lot_number += f"-{second_number}"

        address_parts.append(lot_number)

    detail_address = _normalize_text(
        raw_destination.get("detailAddrName")
    )

    if detail_address:
        address_parts.append(detail_address)

    return " ".join(address_parts) or None


def _parse_destination(raw_destination: dict[str, Any]) -> DestinationCandidate | None:
    tmap_id = _normalize_text(raw_destination.get("id"))
    name = _normalize_text(raw_destination.get("name"))
    coordinates = _extract_coordinates(raw_destination)

    if not tmap_id or not name or coordinates is None:
        return None

    latitude, longitude = coordinates

    address = (
        _extract_road_address(raw_destination)
        or _extract_lot_address(raw_destination)
    )

    return DestinationCandidate(
        tmap_id=tmap_id,
        name=name,
        phone=_normalize_text(raw_destination.get("telNo")),
        latitude=latitude,
        longitude=longitude,
        address=address,
        district=_normalize_text(
            raw_destination.get("middleAddrName")
        ),
        neighborhood=_normalize_text(
            raw_destination.get("lowerAddrName")
        ),
        category=_normalize_text(
            raw_destination.get("lowerBizName")
        ),
        detail_category=_normalize_text(
            raw_destination.get("detailBizName")
        ),
    )


async def search_destinations(keyword: str, client: TMapClient | None = None) -> DestinationSearchResponse:
    normalized_keyword = keyword.strip()

    if not normalized_keyword:
        raise ValueError("검색어를 입력해주세요.")

    tmap_client = client or TMapClient()

    params = {
        "version": "1",
        "searchKeyword": normalized_keyword,
        "searchType": "name",
        "areaLLCode": "11",
        "areaLMCode": "590",
        "searchtypCd": "A",
        "resCoordType": "WGS84GEO",
        "page": "1",
        "count": "10",
        "multiPoint": "Y",
    }

    data = await tmap_client.get(
        path="/pois",
        params=params,
    )

    search_info = data.get("searchPoiInfo")

    if not isinstance(search_info, dict):
        raise DestinationSearchError(
            "TMAP 응답에 searchPoiInfo가 없습니다."
        )

    pois_container = search_info.get("pois") or {}

    if not isinstance(pois_container, dict):
        raise DestinationSearchError(
            "TMAP 응답의 pois 형식이 올바르지 않습니다."
        )

    raw_destinations = pois_container.get("poi") or []

    if isinstance(raw_destinations, dict):
        raw_destinations = [raw_destinations]

    if not isinstance(raw_destinations, list):
        raise DestinationSearchError(
            "TMAP 응답의 poi 형식이 올바르지 않습니다."
        )

    destinations: list[DestinationCandidate] = []
    seen_ids: set[str] = set()

    for raw_destination in raw_destinations:
        if not isinstance(raw_destination, dict):
            continue

        destination = _parse_destination(raw_destination)

        if destination is None:
            continue

        if destination.tmap_id in seen_ids:
            continue

        seen_ids.add(destination.tmap_id)
        destinations.append(destination)

    total_count = len(destinations)

    return DestinationSearchResponse(
        total_count=total_count,
        requires_confirmation=total_count > 1,
        destinations=destinations,
    )
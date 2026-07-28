from typing import Any

import httpx

from app.config import TMAP_APP_KEY, TMAP_BASE_URL


class TMapAPIError(RuntimeError):
    """TMAP API 요청 중 발생한 오류."""


class TMapClient:
    def __init__(
        self, app_key: str | None = TMAP_APP_KEY, base_url: str = TMAP_BASE_URL
    ) -> None:
        if not app_key:
            raise TMapAPIError("TMAP_APP_KEY 환경변수가 설정되지 않았습니다.")

        self.base_url = base_url.rstrip("/")
        self.headers = {
            "appKey": app_key,
            "Accept": "application/json",
        }

    async def get(
        self, path: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        return await self._request(
            method="GET",
            path=path,
            params=params,
        )

    async def post(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return await self._request(
            method="POST",
            path=path,
            params=params,
            json=json,
        )

    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"

        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    params=params,
                    json=json,
                )

                response.raise_for_status()

        except httpx.TimeoutException as error:
            raise TMapAPIError("TMAP API 요청 시간이 초과되었습니다.") from error

        except httpx.HTTPStatusError as error:
            status_code = error.response.status_code

            try:
                detail = error.response.json()
            except ValueError:
                detail = error.response.text

            raise TMapAPIError(
                f"TMAP API 요청에 실패했습니다. status={status_code}, detail={detail}"
            ) from error

        except httpx.RequestError as error:
            raise TMapAPIError("TMAP API에 연결할 수 없습니다.") from error

        try:
            data = response.json()
        except ValueError as error:
            raise TMapAPIError(
                "TMAP API 응답이 올바른 JSON 형식이 아닙니다."
            ) from error

        if not isinstance(data, dict):
            raise TMapAPIError("TMAP API 응답의 최상위 값이 객체가 아닙니다.")

        return data

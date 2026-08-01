"""대분류 목적지 선정 API."""

from fastapi import APIRouter

router = APIRouter(
    prefix="/api/category-destinations",
    tags=["category-destinations"],
)

# TODO: 목적지 선정 서비스 구현 후 POST /select 엔드포인트를 추가한다.
# TODO: 요청·응답 스키마와 외부 API 오류 매핑을 추가한다.
# TODO: 엔드포인트 구현 이후 app/main.py에 이 라우터를 등록한다.

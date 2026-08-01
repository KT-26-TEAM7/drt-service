import csv
from pathlib import Path

from app.schemas.stop import DRTStop


DEFAULT_STOP_CSV_PATH = (
    Path(__file__).resolve().parents[1]
    / "data"
    / "drt_stops.csv"
)


class StopRepositoryError(RuntimeError):
    """정류장 CSV를 읽는 중 발생한 오류."""


class CsvStopRepository:
    def __init__(self, file_path: Path = DEFAULT_STOP_CSV_PATH) -> None:
        self.file_path = file_path

    def get_all(self) -> list[DRTStop]:
        if not self.file_path.exists():
            raise StopRepositoryError(
                f"정류장 CSV 파일을 찾을 수 없습니다: "
                f"{self.file_path}"
            )

        stops: list[DRTStop] = []

        try:
            with self.file_path.open(
                mode="r",
                encoding="utf-8-sig",
                newline="",
            ) as csv_file:
                reader = csv.DictReader(csv_file)

                for line_number, row in enumerate(reader, start=2):
                    try:
                        stop = DRTStop(
                            id=int(row["id"]),
                            name=row["name"].strip(),
                            type=row["type"].strip(),
                            ext_id=(row["ext_id"].strip() or None),
                            latitude=float(row["latitude"]),
                            longitude=float(row["longitude"]),
                        )
                    except (
                        KeyError,
                        TypeError,
                        ValueError,
                    ) as error:
                        raise StopRepositoryError(
                            f"정류장 CSV의 {line_number}번째 행 형식이 올바르지 않습니다."
                        ) from error

                    stops.append(stop)

        except OSError as error:
            raise StopRepositoryError("정류장 CSV 파일을 읽을 수 없습니다.") from error

        return stops
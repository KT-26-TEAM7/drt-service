# DRT Route Assistant Backend

DRT 호출 서비스를 위한 FastAPI 백엔드입니다.

## 프로젝트 구조

```text
drt-service/
├── app/
│   ├── __init__.py
│   ├── config.py
│   └── main.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 실행 방법

### 1. 가상환경 생성 및 활성화

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정

```bash
cp .env.example .env
```

`.env`에 실제 TMAP 앱 키를 입력합니다.

```env
TMAP_APP_KEY=your_TMAP_APP_KEY
```

### 4. 서버 실행

```bash
uvicorn app.main:app --reload
```

## 테스트

### 기본 API

```bash
curl http://127.0.0.1:8000/
```

예상 응답:

```json
{
  "message": "DRT Route Assistant API"
}
```

### 헬스체크

```bash
curl http://127.0.0.1:8000/health
```

예상 응답:

```json
{
  "status": "ok"
}
```

### Swagger 문서

```text
http://127.0.0.1:8000/docs
```

서버 종료는 실행 중인 터미널에서 `Ctrl + C`를 누릅니다.

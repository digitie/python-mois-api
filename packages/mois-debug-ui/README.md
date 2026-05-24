# python-mois-debug-ui

`python-mois-debug-ui`는 `python-mois-api`로 만든 SQLite localdata DB를 점검하기 위한 개발/디버그용 웹 UI 패키지입니다.

## 문서 언어 원칙

사용자 대상 문서는 한국어로 작성합니다. 패키지명, 명령어, 환경변수, URL, 표준 기술명처럼 코드나 공식 명칭으로 식별해야 하는 값은 원문 표기를 유지합니다.

## 설치

저장소 루트에서 다음처럼 수정 가능 모드로 설치합니다.

```bash
pip install -e . -e packages/mois-debug-ui
```

## 실행

```bash
export MOIS_SQLITE_PATH=artifacts/mois.sqlite
export MOIS_WEB_HOST=127.0.0.1
export MOIS_WEB_PORT=8611
mois-debug-ui
```

프론트엔드 개발 서버는 `frontend` 디렉터리에서 실행합니다.

```bash
cd packages/mois-debug-ui/frontend
npm ci
npm run dev -- --host localhost --port 8610 --strictPort
```

## 적재 CLI

```bash
mois-debug-ui-load-sqlite --file artifacts/localdata/hospitals_info.bin --slug hospitals --replace-slug
```

# 칼셀바도르 2

브라우저에서 돌아가는 고딕 웹게임. 「칼셀바도르」(https://github.com/ghostlight000/kalselbador)와 같은 세계의 후속작.

- `index.html` — 게임 (HTML 파일 하나, v0.1 뼈대)
- `proto/` — 턴제 + 타이밍 전투 시제품
- `tests/` — Playwright 자동 테스트
  - `python3 tests/skel.py` — 뼈대 전체 경로 (만들기 → 1편 기록 → 이동 → 파견 → 가르침 → 첫 번째 밤 → 기록 코드 → 저장 이전)
  - `python3 tests/shots.py <폴더>` — 두 테마·두 폭 스크린샷
  - `python3 tests/t3.py` — 시제품 가르침·밤길

테스트는 `index.html?test`를 내 컴퓨터 파일로 열 때만 실제 시간을 줄인다. 배포 사이트에서는 켜지지 않는다.

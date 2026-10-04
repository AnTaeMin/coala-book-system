# 6차시 순서도 제작 명세

대상은 원고의 ch06-branch 한 곳이다. 입력값을 0~10의 정수로 검증한 **다음**의 조건 판단을 표현한다.
원고의 노드와 연결 데이터는 준비되어 있다. 아래는 Canva 편집기에서 완성할 명세이며 완성 순서도 이미지가 아니다.

## 노드와 연결

| 노드 | 문구 | Canva 네이티브 요소 | 채우기 / 테두리 |
|---|---|---|---|
| input | 현재 대출 수 | [Input-Output](https://www.canva.com/graphics/MAGpWHDxa1c/) | #DFF1FE / #1800AD |
| check | 3 미만인가? | [Decision](https://www.canva.com/graphics/MAGpWETGMb4/) | #FFDEE7 / #FF5757 |
| yes | 추가 대출 가능 | [Document](https://www.canva.com/graphics/MAGpWDtQbCc/) | #FFF3E8 / #F3B96B |
| no | 추가 대출 불가 | [Document](https://www.canva.com/graphics/MAGpWDtQbCc/) | #FFF3E8 / #F3B96B |

- input → check: 아래 방향.
- check —YES→ yes: 왼쪽 아래 방향.
- check —NO→ no: 오른쪽 아래 방향.
- if-else 분기는 [Process 컨테이너](https://www.canva.com/graphics/MAGpWHT7x4M/)로 감싼다. 채우기 #FFDEE7, 테두리 #FF5757.
- 판단 도형을 컨테이너 왼쪽 위에 겹쳐 놓고 판단 도형이 앞쪽에 오게 한다.
- 연결선은 Canva 네이티브 선·커넥터, 색 #737373, 방향 화살표를 사용한다.
- 모든 내부 문구와 YES/NO는 Hakgyoansim Chilpanjiugae OTF, 줄 간격 2, 자간 0이다.
- 내부 글자 크기·연결선 굵기는 확정값이 없어 임의의 고정값을 명세하지 않는다.

## 판단 검수

| 검증된 입력 | 분기 | 출력 |
|---:|---|---|
| 0 | YES | 추가 대출 가능 |
| 2 | YES | 추가 대출 가능 |
| 3 | NO | 추가 대출 불가 |
| 10 | NO | 추가 대출 불가 |

빈 입력, 음수, 문자, 10보다 큰 수는 순서도 진입 전 입력 검증에서 안내한다.

## 남은 Canva 작업

Coala Book Builder는 위 라이브러리 도형을 직접 삽입하지 못하고 회색 작업 영역을 만든다. 해당 영역에 네이티브 요소를 배치하고 안내 문구와 회색 상자를 삭제해야 한다.
PDF의 기존 순서도나 새 PNG를 최종 도형 대신 넣으면 편집 가능성 규칙을 충족하지 못한다.
정확한 요구 사항: [flowcharts.md](../../skill/coala-canva-textbook/references/flowcharts.md).
최종 Canva 순서도는 아직 제작되지 않았다.

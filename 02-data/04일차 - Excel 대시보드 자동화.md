# 04일차 (후반부) - Excel 대시보드 자동화

> **🎯 오늘의 목표**: xlwings로 Excel을 제어하여 게임 판매 데이터를 전문적인 대시보드로 자동 생성합니다!

```table-of-contents
```

---

# 🤔 프로젝트 준비: Excel 자동화, 어떻게 시작할까요? (10분)

## 🎯 코딩 전에 먼저 생각해보기

> **핵심 질문**: "Excel 보고서, 매번 수동으로 만들고 계신가요?"

**질문 1: Excel 보고서, 얼마나 자주 만드나요?**
```
- 매일? 매주? 매월?
- 데이터만 바뀌고 구조는 같은가요?
- 같은 작업을 반복하고 계신가요?

💭 [30초 생각해보기]
```

**질문 2: Excel 수동 작업, 어떤 게 번거로웠나요?**
```
- 차트 하나씩 만들기?
- 데이터 복사/붙여넣기?
- 색상 하나씩 설정하기?
- 실수로 수식 깨뜨리기?

💭 [짝꿍과 1분 이야기하기]
```

**질문 3: 자동화하면 어떤 업무에 적용하고 싶나요?**
```
예시:
- 월간 매출 보고서
- 프로젝트 진행 현황 대시보드
- 재고 현황 리포트
- 성과 측정 보고서

✍️ [내 관심사 1가지 적어보기]
```

---

## 💡 Why Excel 자동화인가?

**시간 절약의 마법**:
```
수동 작업: 30분
  ↓
자동화: 10초

월 20회 → 월 10시간 절약!
```

**에러 제로**:
- 복사/붙여넣기 실수 없음
- 수식 깨짐 없음
- 일관된 품질 보장

**재사용성**:
- 한 번 만들면 계속 사용
- 데이터만 바꿔서 즉시 생성

**💡 오늘의 핵심**:
```
❌ Excel 전문가가 되기
✅ 반복 작업을 자동화하여 시간 절약하기
```

---

## 📌 Why Excel 대시보드 자동화?

**실무에서 이런 경우가 있습니다**:
- 매주/매월 반복적으로 Excel 보고서를 만들어야 함
- 데이터만 바뀌고 차트 구조는 동일한 보고서
- 수동으로 하면 30분 걸리는 작업을 10초로 단축!

**이번 실습에서 배울 것**:
1. xlwings로 Excel을 프로그래밍 방식으로 제어
2. pandas와 xlwings 연동하여 데이터 처리
3. 4개 차트가 포함된 전문 대시보드 자동 생성
4. 재사용 가능한 테마 시스템 구축

**다음 시간(Day 3) 예고**:
- 이번 시간에 만든 Excel 대시보드를 Streamlit 웹 대시보드로 재구현
- 같은 데이터, 같은 차트 구조를 웹으로 전환하는 과정 학습

---

## 📦 xlwings 설치 및 설정 (14:00 시작)

> **⏱️ 목표**: 기초 실습(-3)을 14:45까지 완료하기

```bash
pip install xlwings pandas openpyxl
```

**xlwings란?**:
- Python에서 Excel을 제어하는 라이브러리
- Windows와 Mac 모두 지원
- Excel의 모든 기능을 Python 코드로 조작 가능

**pandas vs xlwings**:
| 기능 | pandas | xlwings |
|------|--------|---------|
| 데이터 읽기 | ✅ 빠름 | ⚠️ 느림 |
| 데이터 쓰기 | ✅ 간단 | ✅ 간단 |
| 차트 생성 | ❌ 불가 | ✅ 가능 |
| 스타일링 | ❌ 제한적 | ✅ 완벽 제어 |
| 용도 | 데이터 분석 | Excel 자동화 |

---

## 🎮 실습 프로젝트: 게임 판매 대시보드

**최종 결과물**:
```
┌────────────────────────────────────────┐
│   🎮 글로벌 게임 판매 대시보드          │
├──────────────────┬─────────────────────┤
│ 📊 장르별 판매량  │  🏆 Top 10 배급사   │
│  (세로 막대형)   │   (가로 막대형)     │
│                 │                     │
├──────────────────┼─────────────────────┤
│ 📅 연도별 추이   │  🎯 플랫폼별 분포   │
│   (꺾은선형)     │     (원형)          │
│                 │                     │
└──────────────────┴─────────────────────┘
```

**데이터셋**: 글로벌 게임 판매 Top 50
- Rank, 게임명, 플랫폼, 발행년도, 장르, 배급사, 판매량

---

## 실습 . xlwings 기초 - Excel 제어하기

**목표**: Excel 워크북을 생성하고 데이터를 입력해봅니다.

**코드**:
```python
import xlwings as xw

# Excel 앱 시작 (visible=True: 창이 보임)
app = xw.App(visible=True)

# 새 워크북 생성
wb = app.books.add()

# 첫 번째 시트 가져오기
sheet = wb.sheets[0]

# 데이터 입력
sheet.range('A1').value = "안녕하세요!"
sheet.range('A2').value = [1, 2, 3, 4, 5]  # 가로로 입력
sheet.range('A3').value = [[1], [2], [3]]  # 세로로 입력

# 저장
wb.save('test.xlsx')

# 워크북 닫기 (Excel은 열린 상태 유지)
wb.close()

# Excel 앱 종료
app.quit()
```

**설명**:
- `xw.App(visible=True)`: Excel 프로그램 실행
- `books.add()`: 새 워크북 생성
- `range('A1').value`: 셀에 값 입력
- 리스트는 가로, 리스트의 리스트는 세로로 입력됨

**AI 활용 프롬프트**:
+ xlwings로 기존 Excel 파일을 여는 방법을 알려줘
+ 여러 시트를 한 번에 생성하는 방법을 알려줘
+ 셀 범위를 선택하고 값을 읽는 방법을 알려줘

---

## 실습 . pandas 데이터를 Excel로 내보내기

**목표**: pandas DataFrame을 Excel 시트에 붙여넣습니다.

**코드**:
```python
import xlwings as xw
import pandas as pd

# 샘플 데이터
data = {
    "이름": ["홍길동", "김철수", "이영희"],
    "나이": [25, 30, 28],
    "직업": ["개발자", "디자이너", "기획자"]
}
df = pd.DataFrame(data)

# Excel 생성
app = xw.App(visible=True)
wb = app.books.add()
sheet = wb.sheets[0]

# DataFrame 붙여넣기 (A1부터)
sheet.range('A1').value = df

# 헤더 스타일링
header_range = sheet.range('A1:C1')
header_range.color = (0, 112, 192)  # 파란색 배경
header_range.api.Font.Color = 0xFFFFFF  # 흰색 텍스트
header_range.api.Font.Bold = True

# 열 너비 자동 조정
sheet.autofit('c')  # 'c' = columns

wb.save('dataframe_output.xlsx')
```

**설명**:
- `range('A1').value = df`: DataFrame을 통째로 붙여넣기
- `color = (R, G, B)`: RGB 색상 (0-255)
- `api.Font`: Excel COM API 직접 접근
- `autofit('c')`: 열 너비 자동 조정

**색상 코드 팁**:
- RGB 값: (255, 0, 0) = 빨강
- HEX 값 변환:  → (46, 89, 132)
- 온라인 변환기: https://www.rapidtables.com/convert/color/hex-to-rgb.html

**AI 활용 프롬프트**:
+ xlwings에서 HEX 색상 코드를 사용하는 방법을 알려줘
+ 특정 행만 스타일을 다르게 적용하는 방법을 알려줘
+ Excel에서 데이터를 읽어와서 DataFrame으로 변환하는 방법을 알려줘

---

## 실습 . 차트 생성 기초

**목표**: 막대 차트를 만들어봅니다.

**코드**:
```python
import xlwings as xw
import pandas as pd

app = xw.App(visible=True)
wb = app.books.add()
sheet = wb.sheets[0]

# 샘플 데이터 입력
data = {
    "과목": ["국어", "영어", "수학", "과학"],
    "점수": [85, 92, 78, 88]
}
df = pd.DataFrame(data)
sheet.range('A1').value = df

# 차트 생성
chart = sheet.charts.add(
    left=sheet.range('D2').left,  # 위치
    top=sheet.range('D2').top,
    width=400,  # 너비
    height=250  # 높이
)

# 데이터 범위 설정
chart.set_source_data(sheet.range('A1:B5'))

# 차트 타입 설정
chart.chart_type = 'column_clustered'  # 세로 막대형

# 차트 제목
chart.api[1].HasTitle = True
chart.api[1].ChartTitle.Text = "과목별 점수"

wb.save('chart_example.xlsx')
```

**차트 타입**:
| 타입 | 이름 | 용도 |
|------|------|------|
| `column_clustered` | 세로 막대형 | 항목별 비교 |
| `bar_clustered` | 가로 막대형 | 순위, Top N |
| `line` | 꺾은선형 | 시간 추이 |
| `pie` | 원형 | 비율 분석 |

**AI 활용 프롬프트**:
+ 차트의 범례 위치를 변경하는 방법을 알려줘
+ 차트 축의 최소값/최대값을 설정하는 방법을 알려줘
+ 여러 개의 차트를 한 시트에 배치하는 방법을 알려줘

---

---

## ⏸️ 중간 체크포인트 (14:45)

**여기까지 완료했나요?**
- ✅ xlwings로 Excel 제어 성공
- ✅ DataFrame을 Excel에 붙여넣기 성공
- ✅ 차트 생성 기초 이해
- ✅ 차트 타입 4가지 기억 (세로막대/가로막대/꺾은선/원형)

**15분 휴식 후, 본격적인 대시보드 프로젝트를 시작합니다!** ☕

---

## 실습 . 샘플 데이터 생성 (15:00 시작)

> **⏱️ 목표**: 완성된 대시보드를 16:30까지 생성하기

**목표**: 실습용 게임 판매 데이터를 생성합니다.

**💾 완전한 코드**: [GitHub Gist](https://gist.github.com/allieus/1bccc34e941dc783ab2144bc3b8367a5)

**코드**:
```python
import pandas as pd

# 게임 판매 데이터 (Top 50)
data = {
    "Rank": list(range(1, 51)),
    "게임명": [
        "Minecraft", "Grand Theft Auto V", "Tetris (EA)", "Wii Sports", "PUBG: Battlegrounds",
        "Super Mario Bros.", "Mario Kart 8", "Red Dead Redemption 2", "Pokémon Red/Blue/Yellow", "Terraria",
        # ... (총 50개)
    ],
    "플랫폼": [
        "Multi-platform", "Multi-platform", "Mobile", "Wii", "PC",
        # ...
    ],
    "발행년도": [2011, 2013, 2006, 2006, 2017, ...],
    "장르": ["Sandbox", "Action", "Puzzle", "Sports", "Shooter", ...],
    "배급사": ["Mojang", "Rockstar Games", "Electronic Arts", "Nintendo", ...],
    "판매량_백만": [238.0, 185.0, 100.0, 82.9, 75.0, ...]
}

df = pd.DataFrame(data)
df.to_excel("game_sales_data.xlsx", index=False, sheet_name="게임판매데이터")

print(f"✅ 샘플 데이터 생성 완료: game_sales_data.xlsx")
print(f"📊 총 {len(df)}개 게임 데이터")
```

**실행 후**:
- `game_sales_data.xlsx` 파일 생성됨
- 이 파일을 다음 실습들에서 사용

---

## 실습 . 대시보드 템플릿 생성

**목표**: 4개 차트를 위한 레이아웃을 만듭니다.

**코드**:
```python
import xlwings as xw

app = xw.App(visible=True)
wb = app.books.add()
sheet = wb.sheets[0]
sheet.name = "대시보드"

# 헤더 영역 (A1:H1)
header_range = sheet.range('A1:H1')
header_range.merge()
header_range.value = "🎮 글로벌 게임 판매 대시보드"
header_range.color = (46, 89, 132)  # 진한 파란색
header_range.api.Font.Color = 0xFFFFFF  # 흰색
header_range.api.Font.Size = 20
header_range.api.Font.Bold = True
header_range.api.HorizontalAlignment = -4108  # 가운데 정렬
sheet.range('A1').row_height = 40

# 차트 제목 영역들
chart_titles = {
    'A3:D3': '📊 장르별 판매량',
    'E3:H3': '🏆 Top 10 배급사',
    'A13:D13': '📅 연도별 판매 추이',
    'E13:H13': '🎯 플랫폼별 분포'
}

for cell_range, title in chart_titles.items():
    title_cell = sheet.range(cell_range)
    title_cell.merge()
    title_cell.value = title
    title_cell.color = (68, 114, 196)  # 밝은 파란색
    title_cell.api.Font.Color = 0xFFFFFF
    title_cell.api.Font.Size = 14
    title_cell.api.Font.Bold = True
    title_cell.api.HorizontalAlignment = -4108

wb.save('dashboard_template.xlsx')
```

**레이아웃 구조**:
```
Row 1:  [────────── 헤더 ──────────]
Row 3:  [차트1 제목] [차트2 제목]
Row 4-12: [차트1] [차트2]
Row 13: [차트3 제목] [차트4 제목]
Row 14-22: [차트3] [차트4]
```

---

## 실습 . 데이터 처리 및 피벗 시트 생성

**목표**: 차트용 집계 데이터를 별도 시트에 준비합니다.

**코드** (장르별 판매량 집계):
```python
import xlwings as xw
import pandas as pd

# 데이터 로드
df = pd.read_excel("game_sales_data.xlsx")

# 장르별 판매량 집계
genre_sales = df.groupby('장르')['판매량_백만'].sum().sort_values(ascending=False)

# Excel 열기
app = xw.App(visible=True)
wb = app.books.open("dashboard_template.xlsx")

# 피벗 시트 생성
pivot_sheet = wb.sheets.add("피벗_장르", after=wb.sheets[-1])
pivot_sheet.range('A1').value = "장르"
pivot_sheet.range('B1').value = "판매량"
pivot_sheet.range('A2').value = genre_sales.index.tolist()
pivot_sheet.range('B2').value = [[v] for v in genre_sales.values.tolist()]

wb.save()
```

**pandas 집계 문법**:
```python
# GroupBy 집계
df.groupby('컬럼')['값컬럼'].sum()      # 합계
df.groupby('컬럼')['값컬럼'].mean()     # 평균
df.groupby('컬럼')['값컬럼'].count()    # 개수

# 정렬
.sort_values(ascending=False)  # 내림차순
.sort_values(ascending=True)   # 오름차순

# Top N
.head(10)  # 상위 10개
```

**AI 활용 프롬프트**:
+ 여러 컬럼으로 GroupBy하는 방법을 알려줘
+ 배급사별로 게임 수와 평균 판매량을 함께 구하는 방법을 알려줘

---

## 실습 . 완성된 대시보드 생성기

**목표**: 전체 프로세스를 클래스로 구조화합니다.

**💾 완전한 코드**: [GitHub Gist](https://gist.github.com/allieus/c82e974a807075940e99728e71ea2f27)

**핵심 구조**:
```python
class ExcelDashboardGenerator:
    def __init__(self, data_path):
        self.data_path = data_path
        self.app = None
        self.wb = None
        self.df = None

    def load_data(self):
        """데이터 로드"""
        self.df = pd.read_excel(self.data_path)

    def create_workbook(self, visible=True):
        """새 워크북 생성"""
        self.app = xw.App(visible=visible)
        self.wb = self.app.books.add()

    def create_dashboard_template(self):
        """대시보드 템플릿 생성"""
        # 헤더, 제목 영역 설정

    def create_genre_chart(self):
        """장르별 판매량 차트 (세로 막대형)"""
        # GroupBy 집계 → 피벗 시트 → 차트 생성

    def create_publisher_chart(self):
        """Top 10 배급사 차트 (가로 막대형)"""
        # ...

    def create_year_chart(self):
        """연도별 추이 차트 (꺾은선형)"""
        # ...

    def create_platform_chart(self):
        """플랫폼별 분포 차트 (원형)"""
        # ...

    def save_dashboard(self, output_path):
        """대시보드 저장"""
        self.wb.save(output_path)

    def generate(self, output_path, visible=True):
        """전체 프로세스 실행"""
        self.load_data()
        self.create_workbook(visible=visible)
        self.create_dashboard_template()
        self.add_data_sheet()
        self.create_genre_chart()
        self.create_publisher_chart()
        self.create_year_chart()
        self.create_platform_chart()
        self.save_dashboard(output_path)

# 사용
generator = ExcelDashboardGenerator("game_sales_data.xlsx")
generator.generate("게임판매_대시보드.xlsx", visible=True)
```

**실행 결과**:
- `게임판매_대시보드.xlsx` 생성
- 4개 차트가 포함된 전문 대시보드 완성!

---

## 🎉 축하합니다! 대시보드 완성 (16:30 목표)

**여기까지 오셨다면**:
- ✅ 30분 걸리던 작업을 10초로 단축하는 자동화 구현
- ✅ Python으로 Excel을 완벽하게 제어하는 방법 습득
- ✅ 실무에 바로 적용 가능한 템플릿 확보

**남은 시간(16:30-17:00)**: 테마 시스템으로 색상 커스터마이징 배우기 (선택)

---

## 🎨 고급 실습: 테마 시스템 (선택)

**목표**: 색상 테마를 외부 파일로 관리합니다.

**💾 완전한 코드**: [GitHub Gist](https://gist.github.com/allieus/86109c5f51045488f54f97ce1cc32ab6)

**config.py**:
```python
# 기본 테마
DEFAULT_THEME = {
    "header_bg": "",
    "header_text": "",
    "title_bg": "",
    "chart_color1": "",
    "chart_color2": "",
}

# 다크 테마
DARK_THEME = {
    "header_bg": "",
    "header_text": "",
    # ...
}

def get_theme(theme_name="default"):
    themes = {
        "default": DEFAULT_THEME,
        "dark": DARK_THEME,
    }
    return themes.get(theme_name, DEFAULT_THEME)
```

**사용**:
```python
from config import get_theme

theme = get_theme("dark")
header_range.color = theme["header_bg"]
```

---

## 💡 Claude Code 활용 전략

**이번 실습에서 Claude Code를 이렇게 활용하세요**:

**1. 기초 학습 단계**:
```
"xlwings로 A1:C10 범위를 읽어서 pandas DataFrame으로 변환하는 코드를 작성해줘"
"Excel 차트를 생성할 때 사용 가능한 chart_type 목록을 알려줘"
```

**2. 문제 해결 단계**:
```
"xlwings에서 색상을 설정할 때 HEX 코드를 사용하는 방법을 알려줘"
"차트의 범례 위치를 변경하는 방법을 알려줘"
```

**3. 기능 확장 단계**:
```
"이 대시보드에 슬라이서(필터)를 추가하는 방법을 알려줘"
"차트에 데이터 레이블을 표시하는 코드를 작성해줘"
```

**4. 코드 개선 단계**:
```
"이 코드의 에러 처리를 개선해줘"
"차트 생성 코드를 더 모듈화하는 방법을 알려줘"
```

---

## 🚀 실무 확장 아이디어

**1. 판매 리포트 자동화**:
- 매월 CSV 파일을 받으면 자동으로 대시보드 생성
- 여러 지점의 데이터를 통합하여 전국 현황 대시보드

**2. 재무 보고서 생성**:
- 회계 시스템에서 데이터 추출
- 손익계산서, 재무상태표를 시각화
- 경영진 보고용 요약 대시보드

**3. 인사 데이터 분석**:
- 부서별 인원 현황
- 연차/휴가 사용 통계
- 채용/퇴사 트렌드 분석

**4. 마케팅 성과 추적**:
- 캠페인별 ROI 분석
- 채널별 전환율 비교
- 시계열 성과 추이

---

## 📊 다음 시간 예고: 웹 대시보드로 전환

**Day 3에서 할 일**:
1. 이번 시간에 만든 Excel 대시보드 구조를 그대로 가져감
2. Streamlit으로 동일한 4개 차트 구현
3. 웹 브라우저에서 인터랙티브하게 동작

**Excel vs Streamlit 비교**:
| 특징 | Excel | Streamlit |
|------|-------|-----------|
| 배포 | ❌ 파일 공유 | ✅ URL 공유 |
| 인터랙션 | ⚠️ 제한적 | ✅ 풍부함 |
| 접근성 | ⚠️ Excel 필요 | ✅ 브라우저만 |
| 익숙함 | ✅ 매우 익숙 | ⚠️ 학습 필요 |

**이번 실습의 장점**:
- Excel로 먼저 프로토타입을 만들어보고
- 웹으로 전환할 때 이미 구조를 알고 있어서
- 학습 곡선이 완만함!

---

## 🎯 실습 완료 체크리스트

### 📚 기초 개념 이해
- [ ] xlwings가 무엇이고 왜 사용하는지 설명할 수 있다
- [ ] Excel 자동화로 절약할 수 있는 시간을 계산해봤다
- [ ] pandas vs xlwings의 차이점을 이해했다
- [ ] 4가지 차트 타입(세로막대/가로막대/꺾은선/원형)의 용도를 안다

### 🛠️ 기술 실습 완료
- [ ] xlwings로 Excel 워크북을 생성하고 데이터를 입력했다
- [ ] pandas DataFrame을 Excel에 붙여넣고 스타일링을 적용했다
- [ ] 헤더 셀의 배경색과 글자색을 변경해봤다
- [ ] 막대 차트를 생성하고 제목을 설정했다
- [ ] 차트의 위치와 크기를 조정해봤다

### 📊 대시보드 프로젝트 완성
- [ ] 게임 판매 샘플 데이터(50개)를 생성했다
- [ ] 4개 차트를 위한 레이아웃 템플릿을 만들었다
- [ ] GroupBy로 장르별 판매량을 집계했다
- [ ] 피벗 시트를 생성하고 차트 데이터 소스로 연결했다
- [ ] `ExcelDashboardGenerator` 클래스를 실행했다
- [ ] 완성된 `게임판매_대시보드.xlsx` 파일을 확인했다

### 💡 추가 학습 (선택)
- [ ] 테마 시스템 코드를 읽고 이해했다
- [ ] config.py로 색상을 분리하는 이점을 이해했다
- [ ] 다른 색상 테마로 대시보드를 재생성해봤다

### 🚀 실무 적용 계획
- [ ] 내 업무에서 자동화할 수 있는 보고서를 1개 찾았다
- [ ] 어떤 데이터를 어떤 차트로 보여줄지 계획했다
- [ ] 이번 코드를 내 업무에 맞게 수정할 아이디어가 있다

### ✅ 최종 확인
- [ ] AI(Claude)에게 xlwings 관련 질문을 1개 이상 했다
- [ ] 에러가 발생했을 때 스스로 또는 AI의 도움으로 해결했다
- [ ] 같은 구조를 Streamlit으로 어떻게 만들지 기대된다

**모두 체크하셨다면 축하합니다! 🎉**

**✨ 오늘의 핵심 성과**:
```
수동 30분 → 자동 10초
반복 작업 → 재사용 가능한 템플릿
Excel 파일 → 코드로 제어 가능
```

**🔜 내일 예고**: 이 구조를 Streamlit으로 재구현하면서 웹 대시보드의 세계로 들어갑니다!

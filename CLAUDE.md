# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an educational bootcamp repository for **Euclidsoft ABC Bootcamp 2025** (유클리드소프트 ABC 부트캠프 2025), containing instructor guides and curriculum materials for teaching Python programming and data analysis to beginners in Korean.

**Instructors**: 이진석, 오소진

**Target Audience**: Complete beginners with no coding experience who will learn to develop with AI assistance (ChatGPT/Codex)

## Repository Structure

```
abc-bootcamp-202510/
├── 01-python/          # Python Programming & AI Project Bootcamp (5 days, 30 hours)
│   ├── README.md       # Instructor guide with day-by-day curriculum
│   ├── 소개.md         # Pre-course introduction (students must read before Day 1)
│   ├── 01일차 - AI와 함께 첫 웹 앱 만들기.md
│   ├── 02일차 - 실생활 자동화 앱 만들기.md
│   ├── 03일차 - AI 슈퍼파워 앱 만들기.md
│   ├── 04일차 - 프로젝트 개발.md
│   ├── 05일차 - 프로젝트 공유.md
│   ├── 파이썬 활용 사례 모음.md
│   └── 파이썬 문법 치트 시트.md
│
└── 02-data/           # Data Analysis & Visualization Bootcamp (6 days, 36 hours)
    ├── README.md       # Instructor guide with day-by-day curriculum
    ├── 소개.md         # Pre-course introduction
    ├── 01일차 - 인구 및 교통사고 데이터 분석.md
    ├── 02일차 - 텍스트 데이터 분석 및 시각화.md
    ├── 03일차 - pandas 기초.md
    ├── 04일차 - 데이터 시각화.md
    ├── 04일차 - Excel 대시보드 자동화.md
    ├── 05일차 - 웹 대시보드.md
    └── 데이터분석 프로젝트 - 가계부 앱.md
```

## Course Architecture

### 01-python: Python Programming & AI Project (5 days)
- **Day 1**: AI-powered first web app (Streamlit, DuckDuckGo image search, OpenAI API)
- **Day 2**: Real-life automation apps (QR code generation, web crawling with BeautifulSoup)
- **Day 3**: AI superpower apps (OpenWeatherMap API, OpenAI/Claude API)
- **Day 4-5**: Student-driven projects with AI pair programming

**Key Libraries**: `streamlit`, `duckduckgo-search`, `openai`, `anthropic`, `qrcode`, `pillow`, `beautifulsoup4`, `requests`

**Philosophy**: 80% hands-on practice, 20% theory. Prioritize "working code" over perfection. ChatGPT/Codex as "AI pair programmer".

### 02-data: Data Analysis & Visualization (6 days)
- **Day 1-2**: Data analysis with pandas, matplotlib visualization
- **Day 2**: Excel dashboard automation with xlwings
- **Day 3**: Web dashboard with Streamlit
- **Day 4-6**: Household budget app project (income/expense management with statistics and visualization)

**Key Libraries**: `pandas`, `matplotlib`, `plotly`, `xlwings`, `streamlit`, `openpyxl`

**Philosophy**: Business-focused data analysis, visualization-first approach (graphs over numbers), progressive learning (Excel → Web dashboards).

## Important Context

### Educational Approach
1. **AI-First Learning**: Students use shared ChatGPT accounts or GitHub Copilot provided by instructors
2. **Standardized Workspace**: All students use `C:\Work\abc-bootcamp-202510` folder for consistency
3. **Instant Gratification**: Emphasis on seeing working results quickly (especially with Streamlit's hot-reloading)
4. **Error as Learning**: Experiencing and solving errors is part of the pedagogy

### Language and Localization
- **Primary Language**: Korean (all documentation, comments, and student materials)
- **Code Comments**: Should be in Korean for student accessibility
- **Variable Names**: Can be English (following Python conventions) but explanatory comments should be Korean
- **Error Messages**: Should be clear and actionable in Korean

### Python Environment
- **Version**: Python 3.10+ recommended (3.13 latest stable)
- **Package Manager**: pip (no conda or poetry)
- **Virtual Environments**: Not emphasized in beginner courses (instructors may use, but not taught to students)

## Working with This Repository

### When Creating Example Code
1. **Keep it simple**: Beginners with zero coding experience
2. **Add Korean comments**: Explain what each section does
3. **Use Streamlit**: Most student projects will be Streamlit web apps
4. **API Keys**: Never hardcode; use `.env` files and demonstrate `.gitignore` usage
5. **Error Handling**: Keep it minimal but functional (avoid complex try-except for beginners)

### When Modifying Curriculum Materials
1. **Preserve the teaching flow**: Each day builds on previous days
2. **Maintain time estimates**: E.g., "11:30 완성 목표" (completion target: 11:30)
3. **Keep instructor tips**: Notes marked with ⚡ are critical teaching reminders
4. **Update both README and daily files**: Changes should be reflected in curriculum overview

### Sample Data Files
Referenced external resources (GitHub Gists):
- `game_sales_data.xlsx`: https://gist.github.com/allieus/1bccc34e941dc783ab2144bc3b8367a5
- `dashboard_generator.py`: https://gist.github.com/allieus/c82e974a807075940e99728e71ea2f27

## Common Patterns

### Streamlit App Structure
```python
import streamlit as st

# 페이지 설정
st.title("앱 제목")
st.write("설명")

# 사용자 입력
user_input = st.text_input("입력 라벨")
if st.button("버튼 텍스트"):
    # 처리 로직
    st.success("완료 메시지")
```

### API Key Management
```python
import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드
api_key = os.getenv("OPENAI_API_KEY")
```

### pandas Data Analysis Pattern
```python
import pandas as pd

# 데이터 읽기
df = pd.read_csv("data.csv", encoding="utf-8-sig")  # 한글 인코딩 주의

# 기본 분석
print(df.head())
print(df.info())
print(df.describe())
```

### matplotlib Korean Font Setup
```python
import matplotlib.pyplot as plt

# Windows
plt.rcParams['font.family'] = 'Malgun Gothic'
# Mac
# plt.rcParams['font.family'] = 'AppleGothic'

plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지
```

## Critical Teaching Points

### Python Course (01-python)
- ⚡ **Day 1**: Environment setup should take <30 min; AI account distribution before class
- ⚡ **Day 2**: Emphasize Streamlit's hot-reload "magic"; explain `st.session_state` clearly
- ⚡ **Day 3**: Security emphasis on API key management; cost awareness for AI APIs

### Data Analysis Course (02-data)
- ⚡ **Day 1**: DataFrame as "Excel sheet" analogy; always `print()` results
- ⚡ **Day 2**: Korean font setup for matplotlib; xlwings requires Excel installed
- ⚡ **Day 3**: Streamlit instant reflection demonstration; compare with Excel dashboard structure
- ⚡ CSV encoding issues: Use `encoding='utf-8-sig'` or `encoding='cp949'` for Korean data

## External API Keys Required

Instructors must prepare:
- OpenAI API Key (Day 3, LLM practice)
- Anthropic API Key (Day 3, alternative to OpenAI)
- OpenWeatherMap API Key (Day 3, weather app)
- Kakao/Naver Map API Keys (optional)
- ChatGPT shared accounts (distributed to students on Day 1)

## Frequently Asked Questions (from Instructor Guide)

**Q: Can students use folders other than `C:\Work\abc-bootcamp-202510`?**
A: Yes, but using the standard folder is recommended for consistency with instructor screen sharing.

**Q: ChatGPT vs Codex - which to use?**
A: Beginners should start with ChatGPT web browser. Advanced users can upgrade to Codex (GitHub Copilot).

**Q: What if xlwings doesn't work?**
A: Excel program must be installed. If unavailable, skip Excel dashboard and proceed directly to web dashboard.

**Q: pandas CSV Korean characters broken?**
A: Use `encoding='utf-8-sig'` or `encoding='cp949'` when reading CSV files.

**Q: matplotlib Korean characters showing as ???**
A: Configure font settings (Windows: 'Malgun Gothic', Mac: 'AppleGothic').

## Educational Philosophy

From instructor guides:
- **Evidence-based learning**: Students see results immediately
- **AI as partner**: ChatGPT/Codex as "AI pair programmer", not just a tool
- **Completion over perfection**: Working code is better than perfect code
- **Error experience**: Learning to debug is as important as writing code
- **Progressive enhancement**: Excel → Web dashboards (from familiar to new)

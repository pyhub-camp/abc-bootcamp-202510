# 데이터 분석 & 시각화 부트캠프

> **👨‍🏫 강사용 가이드**

```table-of-contents
```

---

## 📋 과정 개요

**기간**: 6일 (총 36시간)
- 데이터 분석 기초: 3일 (18시간)
- 프로젝트: 3일 (18시간)

**목표**:
1. pandas를 활용한 데이터 분석 기초 이해
2. matplotlib/plotly를 활용한 데이터 시각화 능력 습득
3. Streamlit으로 데이터 분석 결과를 웹 대시보드로 구현
4. 실전 데이터 분석 프로젝트를 통한 문제 해결 능력 향상

---

## 🎯 일차별 커리큘럼

| 일차 | 주제 | 핵심 내용 | 결과물 |
|------|------|-----------|--------|
| **1일차** | [pandas 기초](01%EC%9D%BC%EC%B0%A8%20-%20pandas%20%EA%B8%B0%EC%B4%88.md) | pandas DataFrame 기초<br>데이터 읽기/쓰기, 필터링, 정렬, 집계 | CSV 데이터 분석 |
| **2일차 (전반부)** | [matplotlib 시각화](02%EC%9D%BC%EC%B0%A8%20-%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EC%8B%9C%EA%B0%81%ED%99%94.md) | matplotlib 기초<br>막대/선/파이 그래프, 서브플롯 | 다양한 차트 |
| **2일차 (후반부)** | [Excel 대시보드](02%EC%9D%BC%EC%B0%A8%20-%20Excel%20%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C%20%EC%9E%90%EB%8F%99%ED%99%94.md) | xlwings로 Excel 자동화<br>4개 차트 대시보드 생성 | Excel 대시보드 |
| **3일차** | [웹 대시보드](03%EC%9D%BC%EC%B0%A8%20-%20%EC%9B%B9%20%EB%8C%80%EC%8B%9C%EB%B3%B4%EB%93%9C.md) | Streamlit 기초<br>웹 대시보드 배포 | 인터랙티브 웹 앱 |
| **4-6일차** | [가계부 프로젝트](%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D%20%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%20-%20%EA%B0%80%EA%B3%84%EB%B6%80%20%EC%95%B1.md) | 수입/지출 관리<br>통계, 그래프 시각화 | 완성된 가계부 앱 |

---

## 📚 교육 자료

### 교육생용 문서
- **[소개](../01-python/%EC%86%8C%EA%B0%9C.md)**: 사전 학습 자료 (왜 데이터 분석인가?, pandas/matplotlib의 가치)
  - **중요**: 1일차 수업 전에 읽어오도록 안내

### 샘플 데이터 파일
- **employees.csv**: pandas 기초 실습용 (1일차)
- **game_sales_data.xlsx**: 게임 판매 데이터 (2일차 시각화 & 대시보드)
  - GitHub Gist: https://gist.github.com/allieus/1bccc34e941dc783ab2144bc3b8367a5
- **dashboard_generator.py**: Excel 대시보드 생성 스크립트 (2일차)
  - GitHub Gist: https://gist.github.com/allieus/c82e974a807075940e99728e71ea2f27

### 참고 자료
- pandas 공식 문서: https://pandas.pydata.org/docs/
- matplotlib 튜토리얼: https://matplotlib.org/stable/tutorials/index.html
- xlwings 문서: https://docs.xlwings.org/
- Streamlit 문서: https://docs.streamlit.io/

---

## 준비 사항

### 강사 준비
- [ ] 샘플 CSV/Excel 데이터 파일 준비
- [ ] Python 환경 (pandas, matplotlib, xlwings, streamlit 설치 확인)
- [ ] Excel 프로그램 설치 확인 (xlwings 실습용)
- [ ] 프로젝터 및 화면 공유 환경 확인
- [ ] GitHub Gist 샘플 데이터 접근 확인

### 교육생 준비 (사전 안내)
- [ ] 노트북 (Windows/Mac 무관)
- [ ] Python 기초 문법 이해 (변수, 함수, 리스트, 딕셔너리)
- [ ] Excel 기본 사용법 (차트 보는 정도)
- [ ] [소개](../01-python/%EC%86%8C%EA%B0%9C.md) 문서 읽어오기 (필수!)

---

## 💡 강의 팁

### 전체 진행 원칙
- **실무 중심**: 실제 업무에서 활용 가능한 분석 기법 강조
- **시각화 우선**: 숫자보다 그래프로 이해하기
- **점진적 학습**: Excel → Web 대시보드로 단계적 발전
- **AI 협업**: Claude Code를 적극 활용한 데이터 분석

### 일차별 주안점

**1일차**:
- ⚡ pandas 설치 확인 먼저 (pip install pandas)
- ⚡ DataFrame을 "엑셀 시트"로 비유하여 설명
- ⚡ 실습 데이터는 5-10행 정도로 작게 시작
- ⚡ 결과를 항상 print()로 확인하는 습관 강조

**2일차 (전반부)**:
- ⚡ matplotlib 한글 폰트 설정 미리 안내
- ⚡ 차트는 "메시지를 전달하는 도구"임을 강조
- ⚡ 같은 데이터를 다양한 그래프로 그려보기

**2일차 (후반부)**:
- ⚡ xlwings는 Excel이 설치되어 있어야 작동 (사전 확인!)
- ⚡ Excel 대시보드의 "자동화" 가치 강조
- ⚡ Python으로 생성한 Excel 파일을 직접 열어보며 감탄 유도

**3일차**:
- ⚡ Streamlit의 "즉시 반영" 마법 체험시키기
- ⚡ Excel 대시보드와 구조를 비교하며 학습
- ⚡ 웹 URL로 공유 가능한 점 강조 (배포 데모)

**4-6일차**:
- ⚡ 개별 프로젝트 진행 속도 차이 고려
- ⚡ 막힌 사람 우선 지원
- ⚡ 발표는 "배운 점"과 "활용 계획" 위주로

### 자주 나오는 질문

**Q: pandas 한글이 깨져요**
A: CSV 읽을 때 `encoding='utf-8-sig'` 또는 `encoding='cp949'` 옵션 사용

**Q: matplotlib 한글이 ???로 나와요**
A: 폰트 설정 필요. Windows: 'Malgun Gothic', Mac: 'AppleGothic'
```python
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'  # Windows
plt.rcParams['axes.unicode_minus'] = False
```

**Q: xlwings가 작동하지 않아요**
A: Excel 프로그램이 설치되어 있어야 함. 없으면 Excel 대시보드 스킵하고 웹 대시보드로 진행

**Q: Streamlit 배포는 어떻게 하나요?**
A: Streamlit Community Cloud 무료 배포 (GitHub 연동). 시간 여유 있으면 데모

**Q: 데이터 분석 경험이 전혀 없는데 괜찮나요?**
A: 전혀 문제없음. pandas는 엑셀과 비슷한 개념이라 쉽게 적응 가능

---

## 🎓 수료 후 추천 학습 경로

**데이터 분석 심화**:
1. pandas 고급 기능 (merge, pivot_table, datetime)
2. numpy (수치 계산)
3. 통계 기초 (scipy, statsmodels)

**시각화 고급**:
1. seaborn (고급 통계 시각화)
2. plotly (인터랙티브 차트)
3. folium (지도 시각화)

**데이터 과학 방향**:
1. scikit-learn (머신러닝 입문)
2. 데이터 전처리 심화
3. 예측 모델링

**업무 자동화 방향**:
1. openpyxl (Excel 자동화 심화)
2. selenium (웹 스크래핑)
3. schedule (정기 실행 자동화)

---

## 📞 문의 및 피드백

**강의 개선 아이디어**:
- 실습 난이도 조정이 필요한 부분
- 추가하면 좋을 데이터셋이나 분석 예제
- 교육생 피드백 및 질문 패턴

**버전 정보**:
- 최종 업데이트: 2025-01-10
- 작성자: AI 교육팀

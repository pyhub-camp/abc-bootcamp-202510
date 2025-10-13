# 03일차 - pandas 기초

> **🎯 오늘의 목표**: 데이터 분석의 핵심 라이브러리 pandas를 배워, 데이터를 읽고 가공하고 분석합니다!

```table-of-contents
```

---

# 🌟 오늘 무엇을 만들까요?

## 완성 화면 미리보기

**프로젝트 1: 직원 데이터 분석 시스템** (11:30 완성 목표)
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 직원 데이터 분석 시스템
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 데이터 미리보기
┌─────┬────┬────────┬────┐
│ 이름 │나이│  직업  │연봉│
├─────┼────┼────────┼────┤
│홍길동│ 25 │ 개발자 │5000│
│김철수│ 30 │디자이너│4500│
│이영희│ 22 │ 기획자 │4000│
└─────┴────┴────────┴────┘

📈 통계 요약
• 평균 나이: 28.0세
• 평균 연봉: 4,860만원
• 총 직원 수: 5명

🔍 필터링 결과
30세 이상 & 연봉 5000 이상
→ 2명 발견!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**프로젝트 2: 직업별 통계 분석** (16:00 완성 목표)
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 직업별 통계 대시보드
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

직업별 평균 연봉
개발자    : 5,500만원 ████████████
디자이너  : 4,500만원 █████████
기획자    : 4,000만원 ████████

직업별 인원 수
개발자    : 2명
디자이너  : 1명
기획자    : 1명
마케터    : 1명
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

# 💡 시작하기 전에: 왜 pandas인가요?

## "엑셀로 충분한데, 왜 pandas를 배워야 하나요?"

**답은 "YES!"입니다.** 특히 데이터가 중요한 시대에는 더욱 그렇습니다.

### 📊 엑셀 vs pandas

많은 분들이 이렇게 생각합니다:
> "나는 엑셀로도 잘 하고 있어. 왜 pandas를 배워야 하지?"

하지만 **pandas ≠ 엑셀의 대체**입니다!

**pandas가 엑셀보다 강력한 이유**:
- **자동화**: 매달 반복되는 데이터 분석을 버튼 하나로 완성
- **대용량 데이터**: 엑셀 100만 행 제한 없이 수천만 행도 처리 가능
- **복잡한 분석**: 다중 조건, 그룹별 집계, 피벗 등 고급 분석
- **재사용성**: 한 번 작성한 분석 코드를 계속 활용
- **AI 연동**: AI에게 분석 요청 시 더 정확한 결과

### 🚀 실제 시나리오: 엑셀 vs pandas

**시나리오**: 매월 100개 지점의 매출 데이터를 분석해야 하는 마케터

```
[엑셀 사용자]
1. 100개 CSV 파일을 하나씩 열기
2. 수작업으로 복사/붙여넣기
3. 피벗 테이블 수동 생성
4. 차트 수동 업데이트
5. 실수로 수식이 깨지면 처음부터 다시
⏱️ 소요 시간: 3-4시간

[pandas 사용자]
1. Python 스크립트 실행
2. 100개 파일 자동 병합
3. 통계 자동 계산
4. 차트 자동 생성
⚡ 소요 시간: 30초
```

**결과**: 월 20시간 → 1분으로 단축 (99.9% 시간 절감!)

### 💼 pandas로 할 수 있는 것

**데이터 처리**:
- 여러 파일을 하나로 병합
- 결측치 자동 처리
- 데이터 타입 자동 변환

**데이터 분석**:
- 복잡한 조건으로 필터링
- 그룹별 통계 자동 계산
- 시계열 데이터 분석

**자동화**:
- 매일/매주/매달 반복 작업 자동화
- 실시간 데이터 모니터링
- 리포트 자동 생성

> 💡 **핵심**: "엑셀 전문가"가 아니라,
> "데이터로 인사이트를 발견하는 사람"이 되는 것!

---

# 🤔 프로젝트 준비: 데이터 분석, 어떻게 시작할까요? (10분)

## 🎯 코딩 전에 먼저 생각해보기

> **핵심 질문**: "데이터는 도구입니다. 여러분이 **무엇을 알고 싶은지** 정하는 게 먼저!"

**질문 1: 엑셀에서 데이터 분석, 어떻게 했나요?**
```
- 필터 기능으로 특정 조건 찾기?
- 피벗 테이블로 요약?
- VLOOKUP으로 데이터 조회?

💭 [30초 생각해보기]
```

**질문 2: pandas로 하면 뭐가 더 좋을까요?**
```
- 자동화: 매번 반복하지 않아도 됨
- 복잡한 조건: 여러 조건을 쉽게 결합
- 재사용: 한 번 작성한 코드를 계속 활용

💭 [짝꿍과 1분 이야기하기]
```

**질문 3: 내가 정말 분석하고 싶은 데이터는?**
```
예시:
- 회사 매출 데이터
- 개인 가계부 데이터
- 학교 성적 데이터
- SNS 통계 데이터

✍️ [내 관심사 1가지 적어보기]
```

---

## 💡 왜 직원 데이터 분석인가?

**실생활 활용**:
- 📊 인사 데이터 분석
- 💰 급여 통계 계산
- 📈 부서별 현황 파악
- 🔍 특정 조건의 직원 찾기

**학습 포인트**:
- CSV 파일 읽기/쓰기
- 조건 필터링
- 그룹별 집계
- 통계 요약

**💡 오늘의 핵심**:
```
❌ pandas를 완벽하게 마스터하기
✅ 데이터로 인사이트를 빠르게 찾는 방법 배우기
```

---

## 📋 Overview

**왜 데이터 분석을 배워야 할까요?**
- 본격적인 수업에 앞서, [과정 소개 문서](../01-python/%EC%86%8C%EA%B0%9C.md)를 먼저 읽어보세요!
- "왜 데이터 분석인가?", "pandas/matplotlib의 가치" 등을 다룹니다.

**오늘 배울 내용**:
1. pandas 라이브러리 기초
2. CSV 파일 읽기/쓰기
3. 데이터 탐색 및 통계 요약
4. 데이터 필터링 및 정렬
5. 새로운 열 추가 및 데이터 가공
6. 그룹별 집계

---

## 📦 pandas 설치

```bash
pip install pandas
```

---

## pandas 기초 - 데이터 분석의 핵심 라이브러리

**필요한 문법**:
```python
import pandas as pd

# CSV 파일 읽기
df = pd.read_csv("data.csv")

# 데이터 확인
print(df.head())        # 처음 5행
print(df.tail())        # 마지막 5행
print(df.info())        # 데이터 정보
print(df.describe())    # 통계 요약

# 특정 열 선택
names = df["이름"]
print(names)

# 여러 열 선택
subset = df["이름", "나이"](%22%EC%9D%B4%EB%A6%84%22%2C%20%22%EB%82%98%EC%9D%B4%22.md)

# 조건 필터링
adults = df[df["나이"] >= 20]
print(adults)

# 정렬
sorted_df = df.sort_values("나이", ascending=False)

# 새로운 열 추가
df["나이그룹"] = df["나이"].apply(lambda x: "성인" if x >= 20 else "미성년")

# CSV로 저장
df.to_csv("output.csv", index=False)
```

**설명**:
- **pandas**: 데이터 분석을 위한 강력한 라이브러리
- **DataFrame**: 표 형태의 데이터 구조 (행과 열로 구성)
- **read_csv()**: CSV 파일 읽기
- **head/tail()**: 데이터 일부 확인
- **info()**: 데이터 타입, 결측치 정보
- **describe()**: 평균, 표준편차 등 통계 요약
- **[]**: 열 선택
- **조건 필터링**: 특정 조건에 맞는 행만 추출
- **sort_values()**: 정렬
- **apply()**: 각 행에 함수 적용

**주요 작업 패턴**:
```python
# 데이터 읽기
df = pd.read_csv("data.csv")

# 열 선택
df["컬럼명"]

# 조건 필터링
df[df["나이"] >= 20]

# 정렬
df.sort_values("컬럼명")

# 새 열 추가
df["새열"] = df["A"] + df["B"]

# 저장
df.to_csv("output.csv")
```

**AI 활용 프롬프트**:
```
"pandas에서 결측치(NaN)를 처리하는 방법들을 알려줘"
"여러 CSV 파일을 하나로 합치는 방법을 알려줘"
"그룹별로 집계하는 groupby() 사용법을 예제와 함께 보여줘"
```

---

## 실습 . CSV 파일 다루기

**실습 데이터 생성**:
```python
import pandas as pd

# 샘플 데이터 생성
data = {
    '이름': ['홍길동', '김철수', '이영희', '박민수', '최지은'],
    '나이': [25, 30, 22, 35, 28],
    '직업': ['개발자', '디자이너', '기획자', '개발자', '마케터'],
    '연봉': [5000, 4500, 4000, 6000, 4800]
}

df = pd.DataFrame(data)

# CSV로 저장
df.to_csv('employees.csv', index=False, encoding='utf-8-sig')
print("샘플 데이터 생성 완료!")
```

**실습 . 데이터 읽기 및 탐색**:
```python
import pandas as pd

# CSV 파일 읽기
df = pd.read_csv('employees.csv')

# 기본 정보 확인
print("=== 데이터 미리보기 ===")
print(df.head())

print("\n=== 데이터 정보 ===")
print(df.info())

print("\n=== 통계 요약 ===")
print(df.describe())

print("\n=== 열 이름 ===")
print(df.columns.tolist())

print("\n=== 데이터 크기 ===")
print(f"행 개수: {len(df)}")
print(f"열 개수: {len(df.columns)}")
```

**실습 . 데이터 필터링**:
```python
import pandas as pd

df = pd.read_csv('employees.csv')

# 조건 필터링
print("=== 30세 이상 ===")
adults_30 = df[df['나이'] >= 30]
print(adults_30)

print("\n=== 개발자만 ===")
developers = df[df['직업'] == '개발자']
print(developers)

print("\n=== 연봉 5000만원 이상 ===")
high_salary = df[df['연봉'] >= 5000]
print(high_salary)

# 복합 조건 (AND)
print("\n=== 30세 이상이면서 연봉 5000 이상 ===")
condition = (df['나이'] >= 30) & (df['연봉'] >= 5000)
filtered = df[condition]
print(filtered)

# 복합 조건 (OR)
print("\n=== 개발자이거나 디자이너 ===")
condition = (df['직업'] == '개발자') | (df['직업'] == '디자이너')
filtered = df[condition]
print(filtered)
```

**실습 . 데이터 정렬**:
```python
import pandas as pd

df = pd.read_csv('employees.csv')

# 나이 오름차순
print("=== 나이 오름차순 ===")
sorted_age = df.sort_values('나이')
print(sorted_age)

# 연봉 내림차순
print("\n=== 연봉 내림차순 ===")
sorted_salary = df.sort_values('연봉', ascending=False)
print(sorted_salary)

# 다중 정렬 (직업 오름차순 → 연봉 내림차순)
print("\n=== 직업별 정렬 후 연봉 내림차순 ===")
sorted_multi = df.sort_values(['직업', '연봉'], ascending=[True, False])
print(sorted_multi)
```

**실습 . 데이터 가공 및 새로운 열 추가**:
```python
import pandas as pd

df = pd.read_csv('employees.csv')

# 새로운 열 추가: 나이 그룹
def age_group(age):
    if age < 25:
        return '20대 초반'
    elif age < 30:
        return '20대 후반'
    else:
        return '30대 이상'

df['나이그룹'] = df['나이'].apply(age_group)

# 새로운 열 추가: 연봉 등급
df['연봉등급'] = df['연봉'].apply(lambda x: '상' if x >= 5000 else ('중' if x >= 4500 else '하'))

print("=== 가공된 데이터 ===")
print(df)

# 결과 저장
df.to_csv('employees_processed.csv', index=False, encoding='utf-8-sig')
print("\n가공된 데이터 저장 완료!")
```

**실습 . 그룹별 집계**:
```python
import pandas as pd

df = pd.read_csv('employees.csv')

# 직업별 평균 연봉
print("=== 직업별 평균 연봉 ===")
avg_salary = df.groupby('직업')['연봉'].mean()
print(avg_salary)

# 직업별 인원 수
print("\n=== 직업별 인원 수 ===")
job_count = df.groupby('직업').size()
print(job_count)

# 직업별 통계 요약
print("\n=== 직업별 통계 요약 ===")
job_stats = df.groupby('직업')['연봉'].agg(['count', 'mean', 'min', 'max'])
print(job_stats)

# 여러 열에 대한 집계
print("\n=== 직업별 나이와 연봉 평균 ===")
multi_stats = df.groupby('직업')['나이', '연봉'](%27%EB%82%98%EC%9D%B4%27%2C%20%27%EC%97%B0%EB%B4%89%27.md).mean()
print(multi_stats)
```

---

## 💡 pandas 핵심 정리

### 데이터 읽기/쓰기
```python
df = pd.read_csv('file.csv')              # CSV 읽기
df = pd.read_excel('file.xlsx')           # Excel 읽기
df.to_csv('output.csv', index=False)      # CSV로 저장
df.to_excel('output.xlsx', index=False)   # Excel로 저장
```

### 데이터 탐색
```python
df.head(n)          # 처음 n행 (기본 5)
df.tail(n)          # 마지막 n행
df.info()           # 데이터 정보
df.describe()       # 통계 요약
df.shape            # (행, 열) 개수
df.columns          # 열 이름
```

### 데이터 선택
```python
df['컬럼명']                    # 단일 열 선택
df['컬럼1', '컬럼2'](%27%EC%BB%AC%EB%9F%BC1%27%2C%20%27%EC%BB%AC%EB%9F%BC2%27.md)         # 여러 열 선택
df[df['나이'] > 30]            # 조건 필터링
df.loc[행_인덱스, '컬럼명']     # 라벨 기반 선택
df.iloc[행_번호, 열_번호]       # 위치 기반 선택
```

### 데이터 정렬 및 집계
```python
df.sort_values('컬럼명')                    # 정렬
df.groupby('컬럼명').mean()                 # 그룹별 평균
df.groupby('컬럼명').agg(['min', 'max'])   # 여러 집계 함수
```

### 데이터 가공
```python
df['새열'] = df['A'] + df['B']         # 새 열 추가
df['새열'] = df['열'].apply(함수)       # 함수 적용
df.drop('컬럼명', axis=1)              # 열 삭제
df.rename(columns={'옛이름': '새이름'}) # 열 이름 변경
```

---

## AI 활용 프롬프트 모음

**기초 학습**:
```
"pandas DataFrame의 기본 구조를 설명해줘"
"pandas에서 데이터를 필터링하는 다양한 방법을 알려줘"
"loc와 iloc의 차이점을 예제와 함께 설명해줘"
```

**실무 활용**:
```
"pandas에서 결측치를 처리하는 방법을 알려줘"
"여러 CSV 파일을 하나로 병합하는 방법을 알려줘"
"날짜/시간 데이터를 다루는 방법을 알려줘"
"두 개의 DataFrame을 조인(merge)하는 방법을 알려줘"
```

**성능 최적화**:
```
"pandas 연산 속도를 높이는 방법을 알려줘"
"대용량 CSV 파일을 효율적으로 읽는 방법을 알려줘"
"메모리 사용량을 줄이는 방법을 알려줘"
```

---

## 🎓 3일차 학습 완료!

**오늘 배운 것**:
1. ✅ pandas 기초 문법
2. ✅ CSV 파일 읽기/쓰기
3. ✅ 데이터 탐색 및 통계 요약
4. ✅ 데이터 필터링 및 정렬
5. ✅ 새로운 열 추가 및 데이터 가공
6. ✅ 그룹별 집계

**다음 학습**:
- matplotlib을 사용한 데이터 시각화
- 다양한 그래프 그리기
- 시각화 베스트 프랙티스

---

## ✅ 학습 완료 체크리스트

**기초 개념**:
- [ ] pandas가 엑셀보다 강력한 이유를 3가지 이상 설명할 수 있다
- [ ] DataFrame이 무엇인지 이해했다
- [ ] CSV 파일을 읽고 쓸 수 있다

**데이터 탐색**:
- [ ] head(), tail()로 데이터를 미리볼 수 있다
- [ ] info()로 데이터 타입과 결측치를 확인할 수 있다
- [ ] describe()로 통계 요약을 볼 수 있다

**데이터 필터링**:
- [ ] 단일 조건으로 데이터를 필터링할 수 있다
- [ ] 복합 조건 (AND, OR)으로 필터링할 수 있다
- [ ] 특정 열만 선택할 수 있다

**데이터 가공**:
- [ ] sort_values()로 데이터를 정렬할 수 있다
- [ ] apply()로 새로운 열을 추가할 수 있다
- [ ] groupby()로 그룹별 통계를 계산할 수 있다

**실전 활용**:
- [ ] 직원 데이터 분석 시스템을 완성했다
- [ ] 직업별 통계 분석을 완성했다
- [ ] AI에게 pandas 관련 질문을 효과적으로 할 수 있다

**모두 체크하셨다면 축하합니다! 🎉**

내일은 matplotlib으로 데이터를 그래프로 시각화하는 방법을 배웁니다!

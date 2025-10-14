# 파이썬 문법 치트 노트 (factorial.py 기반)

## 1. 함수 정의와 호출

### 기본 함수 정의
```python
def 함수이름(매개변수1, 매개변수2):
    """함수 설명을 여기에 작성 (독스트링)"""
    # 코드 실행
    return 결과값
```

### 타입 힌트 (선택사항)
```python
def factorial(n: int) -> int:
    # n은 정수를 받고, 정수를 반환한다는 힌트
    return result
```

### 선택적 매개변수 (None 기본값)
```python
def main(argv: list[str] | None = None):
    # argv가 주어지지 않으면 None이 기본값
```

### 초초보 예시 코드

**예시 1: 인사 함수**
```python
def greet(name):
    """이름을 받아서 인사말을 출력하는 함수"""
    print(f"안녕하세요, {name}님!")

# 함수 호출
greet("철수")  # 출력: 안녕하세요, 철수님!
greet("영희")  # 출력: 안녕하세요, 영희님!
```

**예시 2: 더하기 함수 (값을 반환)**
```python
def add(a, b):
    """두 숫자를 더한 결과를 반환하는 함수"""
    result = a + b
    return result

# 반환값을 변수에 저장
total = add(5, 3)
print(f"5 + 3 = {total}")  # 출력: 5 + 3 = 8

# 바로 출력
print(add(10, 20))  # 출력: 30
```

**예시 3: 기본값이 있는 함수**
```python
def make_coffee(size="중간"):
    """커피를 만드는 함수 (기본 사이즈는 중간)"""
    print(f"{size} 사이즈 커피를 만들었습니다.")

make_coffee()          # 출력: 중간 사이즈 커피를 만들었습니다.
make_coffee("큰")      # 출력: 큰 사이즈 커피를 만들었습니다.
make_coffee("작은")    # 출력: 작은 사이즈 커피를 만들었습니다.
```

---

## 2. 조건문 (if-elif-else)

### 기본 구조
```python
if 조건1:
    # 조건1이 참일 때 실행
elif 조건2:
    # 조건1이 거짓이고 조건2가 참일 때
else:
    # 모든 조건이 거짓일 때
```

### 실제 예시
```python
if args.n is None:
    # 사용자가 숫자를 안 줬을 때
    user_input = input("숫자 입력: ")
else:
    # 사용자가 숫자를 줬을 때
    n = args.n
```

### 초초보 예시 코드

**예시 1: 나이 확인**
```python
age = 15

if age >= 18:
    print("성인입니다.")
else:
    print("미성년자입니다.")

# 출력: 미성년자입니다.
```

**예시 2: 성적 등급 매기기 (elif 사용)**
```python
score = 85

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(f"당신의 등급은 {grade}입니다.")
# 출력: 당신의 등급은 B입니다.
```

**예시 3: 비밀번호 확인**
```python
password = "abc123"

if password == "abc123":
    print("로그인 성공!")
    print("환영합니다.")
else:
    print("비밀번호가 틀렸습니다.")
    print("다시 시도해주세요.")

# 출력:
# 로그인 성공!
# 환영합니다.
```

---

## 3. 반복문 (for)

### range()와 함께 사용
```python
for i in range(2, n + 1):
    # 2부터 n까지 반복 (n+1은 포함 안 됨)
    result *= i
```

### range() 이해하기
- `range(5)` → 0, 1, 2, 3, 4
- `range(2, 5)` → 2, 3, 4
- `range(2, 10, 2)` → 2, 4, 6, 8

### 초초보 예시 코드

**예시 1: 1부터 10까지 출력**
```python
for i in range(1, 11):
    print(i)

# 출력:
# 1
# 2
# 3
# ...
# 10
```

**예시 2: 과일 목록 출력**
```python
fruits = ["사과", "바나나", "딸기", "포도"]

for fruit in fruits:
    print(f"내가 좋아하는 과일: {fruit}")

# 출력:
# 내가 좋아하는 과일: 사과
# 내가 좋아하는 과일: 바나나
# 내가 좋아하는 과일: 딸기
# 내가 좋아하는 과일: 포도
```

**예시 3: 구구단 3단**
```python
dan = 3

for i in range(1, 10):
    result = dan * i
    print(f"{dan} x {i} = {result}")

# 출력:
# 3 x 1 = 3
# 3 x 2 = 6
# ...
# 3 x 9 = 27
```

---

## 4. 예외 처리 (try-except)

### 기본 구조
```python
try:
    # 에러가 날 수 있는 코드
    n = int(user_input)
except ValueError:
    # ValueError 발생 시 실행
    print("잘못된 입력!")
except EOFError:
    # EOFError 발생 시 실행
    print("입력 없음!")
```

### 예외 발생시키기
```python
if n < 0:
    raise ValueError("음수는 안 됩니다")
```

### 여러 예외 한 번에 처리
```python
except (TypeError, ValueError) as e:
    # TypeError 또는 ValueError 발생 시
    print(f"에러: {e}")
```

### 초초보 예시 코드

**예시 1: 나눗셈 에러 처리**
```python
try:
    num = 10
    result = num / 0  # 0으로 나누기는 에러!
    print(result)
except ZeroDivisionError:
    print("0으로 나눌 수 없습니다!")

# 출력: 0으로 나눌 수 없습니다!
```

**예시 2: 숫자 변환 에러 처리**
```python
user_input = "abc"  # 숫자가 아님

try:
    age = int(user_input)
    print(f"나이: {age}")
except ValueError:
    print("숫자를 입력해주세요!")

# 출력: 숫자를 입력해주세요!
```

**예시 3: 파일 읽기 에러 처리**
```python
try:
    file = open("없는파일.txt", "r")
    content = file.read()
    print(content)
except FileNotFoundError:
    print("파일이 존재하지 않습니다.")
except PermissionError:
    print("파일을 읽을 권한이 없습니다.")

# 출력: 파일이 존재하지 않습니다.
```

---

## 5. 타입 검사와 유효성 검증

### isinstance() - 타입 확인
```python
if not isinstance(n, int):
    # n이 정수가 아니면
    raise TypeError("정수를 입력하세요")
```

### 값 범위 검사
```python
if n < 0:
    # 음수 체크
    raise ValueError("0 이상의 숫자만 가능")
```

### 초초보 예시 코드

**예시 1: 나이 유효성 검사**
```python
age = -5

if age < 0:
    print("나이는 음수가 될 수 없습니다.")
elif age > 150:
    print("나이가 너무 많습니다.")
else:
    print(f"당신의 나이는 {age}살입니다.")

# 출력: 나이는 음수가 될 수 없습니다.
```

**예시 2: 타입 검사**
```python
value = "123"

if isinstance(value, int):
    print("정수입니다.")
elif isinstance(value, str):
    print("문자열입니다.")
else:
    print("다른 타입입니다.")

# 출력: 문자열입니다.
```

**예시 3: 비밀번호 강도 검사**
```python
password = "abc"

if len(password) < 8:
    print("비밀번호는 8자 이상이어야 합니다.")
elif password.isdigit():
    print("숫자만으로는 안전하지 않습니다.")
else:
    print("비밀번호가 생성되었습니다.")

# 출력: 비밀번호는 8자 이상이어야 합니다.
```

---

## 6. 사용자 입력 받기

### input() 함수
```python
user_input = input("프롬프트 메시지: ")
# 항상 문자열(str)로 반환됨

# 공백 제거
user_input = input("숫자: ").strip()

# 빈 문자열 체크
if user_input == "":
    print("입력이 없습니다")
```

### 문자열을 숫자로 변환
```python
try:
    n = int(user_input)  # 정수 변환
    # f = float(user_input)  # 실수 변환
except ValueError:
    print("숫자가 아닙니다")
```

### 초초보 예시 코드

**예시 1: 이름 입력받기**
```python
name = input("이름을 입력하세요: ")
print(f"안녕하세요, {name}님!")

# 실행 예시:
# 이름을 입력하세요: 철수
# 안녕하세요, 철수님!
```

**예시 2: 나이 입력받고 계산하기**
```python
age_str = input("나이를 입력하세요: ")
age = int(age_str)  # 문자열을 숫자로 변환
next_year_age = age + 1
print(f"내년에는 {next_year_age}살이 되시네요!")

# 실행 예시:
# 나이를 입력하세요: 25
# 내년에는 26살이 되시네요!
```

**예시 3: 간단한 계산기**
```python
num1 = int(input("첫 번째 숫자: "))
num2 = int(input("두 번째 숫자: "))
result = num1 + num2
print(f"{num1} + {num2} = {result}")

# 실행 예시:
# 첫 번째 숫자: 10
# 두 번째 숫자: 20
# 10 + 20 = 30
```

---

## 7. 출력하기 (print)

### 기본 출력
```python
print(value)  # 화면에 출력
```

### 표준 에러로 출력
```python
import sys
print("에러 메시지", file=sys.stderr)
# 에러 메시지는 stderr로 출력
```

### f-string (포맷 문자열)
```python
name = "홍길동"
age = 25
print(f"이름: {name}, 나이: {age}")
# 출력: 이름: 홍길동, 나이: 25

print(f"에러: {e}")  # 변수 값 삽입
```

### 초초보 예시 코드

**예시 1: 여러 줄 출력**
```python
print("안녕하세요!")
print("파이썬을 배우는 중입니다.")
print("반갑습니다!")

# 출력:
# 안녕하세요!
# 파이썬을 배우는 중입니다.
# 반갑습니다!
```

**예시 2: f-string으로 계산 결과 출력**
```python
price = 1000
quantity = 3
total = price * quantity

print(f"가격: {price}원")
print(f"수량: {quantity}개")
print(f"총 금액: {total}원")

# 출력:
# 가격: 1000원
# 수량: 3개
# 총 금액: 3000원
```

**예시 3: 소수점 출력 제어**
```python
pi = 3.141592

print(f"원주율: {pi}")
print(f"소수점 2자리: {pi:.2f}")
print(f"소수점 4자리: {pi:.4f}")

# 출력:
# 원주율: 3.141592
# 소수점 2자리: 3.14
# 소수점 4자리: 3.1416
```

---

## 8. 모듈 임포트 (import)

### 기본 import
```python
import sys          # sys 모듈 전체 가져오기
import argparse     # argparse 모듈 가져오기
```

### from import
```python
from __future__ import annotations
# __future__ 모듈에서 annotations만 가져오기
```

### 초초보 예시 코드

**예시 1: 랜덤 숫자 생성**
```python
import random

# 1부터 10까지 랜덤 숫자
number = random.randint(1, 10)
print(f"랜덤 숫자: {number}")

# 출력 예시: 랜덤 숫자: 7
```

**예시 2: 날짜와 시간 출력**
```python
import datetime

# 현재 날짜와 시간
now = datetime.datetime.now()
print(f"현재 시간: {now}")
print(f"년도: {now.year}")
print(f"월: {now.month}")
print(f"일: {now.day}")

# 출력 예시:
# 현재 시간: 2025-10-14 14:30:00
# 년도: 2025
# 월: 10
# 일: 14
```

**예시 3: 수학 함수 사용**
```python
import math

# 제곱근
print(f"9의 제곱근: {math.sqrt(9)}")

# 원의 넓이 (반지름 5)
radius = 5
area = math.pi * radius ** 2
print(f"원의 넓이: {area:.2f}")

# 출력:
# 9의 제곱근: 3.0
# 원의 넓이: 78.54
```

---

## 9. 명령행 인자 처리 (argparse)

### 기본 구조
```python
import argparse

parser = argparse.ArgumentParser(description="프로그램 설명")
parser.add_argument("인자이름", type=int, help="도움말")
args = parser.parse_args()

# 인자 접근
value = args.인자이름
```

### 선택적 인자
```python
parser.add_argument("n", nargs="?", type=int)
# nargs="?" → 선택적 인자 (없어도 됨)
# args.n이 None일 수 있음
```

### 초초보 예시 코드

**예시 1: 간단한 인사 프로그램**
```python
# 파일명: greet.py
import argparse

parser = argparse.ArgumentParser(description="인사 프로그램")
parser.add_argument("name", help="이름을 입력하세요")
args = parser.parse_args()

print(f"안녕하세요, {args.name}님!")

# 실행: python greet.py 철수
# 출력: 안녕하세요, 철수님!
```

**예시 2: 계산기 프로그램**
```python
# 파일명: calculator.py
import argparse

parser = argparse.ArgumentParser(description="간단한 계산기")
parser.add_argument("num1", type=int, help="첫 번째 숫자")
parser.add_argument("num2", type=int, help="두 번째 숫자")
args = parser.parse_args()

result = args.num1 + args.num2
print(f"{args.num1} + {args.num2} = {result}")

# 실행: python calculator.py 10 20
# 출력: 10 + 20 = 30
```

**예시 3: 선택적 인자가 있는 프로그램**
```python
# 파일명: greeting.py
import argparse

parser = argparse.ArgumentParser(description="인사 프로그램")
parser.add_argument("name", help="이름")
parser.add_argument("--lang", default="ko", help="언어 (ko/en)")
args = parser.parse_args()

if args.lang == "ko":
    print(f"안녕하세요, {args.name}님!")
else:
    print(f"Hello, {args.name}!")

# 실행 1: python greeting.py 철수
# 출력: 안녕하세요, 철수님!

# 실행 2: python greeting.py John --lang en
# 출력: Hello, John!
```

---

## 10. 메인 프로그램 패턴

### 표준 패턴
```python
def main():
    # 메인 로직
    return 0  # 성공 시 0 반환

if __name__ == "__main__":
    # 이 파일이 직접 실행될 때만 실행됨
    # import될 때는 실행 안 됨
    sys.exit(main())
```

### 반환 코드 (Exit Code)
- `0`: 정상 종료
- `1`: 일반적인 에러
- `2`: 잘못된 사용법/입력

### 초초보 예시 코드

**예시 1: 기본 메인 패턴**
```python
# 파일명: hello.py
def main():
    print("안녕하세요!")
    print("파이썬 프로그램입니다.")
    return 0

if __name__ == "__main__":
    main()

# 실행: python hello.py
# 출력:
# 안녕하세요!
# 파이썬 프로그램입니다.
```

**예시 2: 계산 프로그램**
```python
# 파일명: calculate.py
def add(a, b):
    return a + b

def main():
    result = add(10, 20)
    print(f"10 + 20 = {result}")
    return 0

if __name__ == "__main__":
    main()

# 실행: python calculate.py
# 출력: 10 + 20 = 30
```

**예시 3: 여러 함수를 사용하는 프로그램**
```python
# 파일명: program.py
def greet(name):
    print(f"안녕하세요, {name}님!")

def show_menu():
    print("1. 새 게임")
    print("2. 불러오기")
    print("3. 종료")

def main():
    greet("플레이어")
    show_menu()
    return 0

if __name__ == "__main__":
    main()

# 실행: python program.py
# 출력:
# 안녕하세요, 플레이어님!
# 1. 새 게임
# 2. 불러오기
# 3. 종료
```

---

## 11. 독스트링 (Docstring)

### 모듈 독스트링
```python
"""
파일 맨 위에 작성하는 모듈 설명

여러 줄로 작성 가능
"""
```

### 함수 독스트링
```python
def function():
    """함수가 하는 일을 간단히 설명

    Args:
        param1: 매개변수 설명

    Returns:
        반환값 설명

    Raises:
        ValueError: 언제 이 에러가 발생하는지
    """
```

### 초초보 예시 코드

**예시 1: 간단한 함수 독스트링**
```python
def greet(name):
    """사용자에게 인사말을 출력하는 함수"""
    print(f"안녕하세요, {name}님!")

# help() 함수로 독스트링 확인
help(greet)
# 출력: 사용자에게 인사말을 출력하는 함수
```

**예시 2: 매개변수 설명이 있는 독스트링**
```python
def calculate_area(width, height):
    """
    직사각형의 넓이를 계산합니다.

    매개변수:
        width: 가로 길이
        height: 세로 길이

    반환값:
        직사각형의 넓이
    """
    return width * height

area = calculate_area(5, 10)
print(f"넓이: {area}")  # 출력: 넓이: 50
```

**예시 3: 모듈 독스트링**
```python
"""
계산기 프로그램 v1.0

이 모듈은 기본적인 산술 연산을 제공합니다.
더하기, 빼기, 곱하기, 나누기 기능이 있습니다.
"""

def add(a, b):
    """두 숫자를 더합니다."""
    return a + b

def subtract(a, b):
    """두 숫자를 뺍니다."""
    return a - b

print(add(10, 5))       # 출력: 15
print(subtract(10, 5))  # 출력: 5
```

---

## 12. 주요 내장 함수

### isinstance() - 타입 체크
```python
isinstance(5, int)      # True
isinstance("hello", str) # True
isinstance(5, str)      # False
```

### range() - 숫자 시퀀스
```python
range(시작, 끝, 간격)
# 끝 값은 포함 안 됨!
```

### int() - 정수 변환
```python
int("123")    # 123
int("3.14")   # ValueError!
int(3.14)     # 3 (소수점 버림)
```

### 초초보 예시 코드

**예시 1: len() - 길이 구하기**
```python
# 문자열 길이
name = "홍길동"
print(f"이름 길이: {len(name)}")  # 출력: 이름 길이: 3

# 리스트 길이
fruits = ["사과", "바나나", "딸기"]
print(f"과일 개수: {len(fruits)}")  # 출력: 과일 개수: 3
```

**예시 2: max(), min() - 최대값, 최소값**
```python
numbers = [10, 5, 8, 20, 3]

highest = max(numbers)
lowest = min(numbers)

print(f"가장 큰 수: {highest}")  # 출력: 가장 큰 수: 20
print(f"가장 작은 수: {lowest}")  # 출력: 가장 작은 수: 3
```

**예시 3: sum() - 합계 구하기**
```python
scores = [85, 90, 78, 92, 88]

total = sum(scores)
average = total / len(scores)

print(f"총점: {total}")        # 출력: 총점: 433
print(f"평균: {average}")      # 출력: 평균: 86.6
```

---

## 13. 연산자

### 산술 연산
```python
result = 1
result *= i    # result = result * i (복합 할당)
result += 1    # result = result + 1
result -= 1    # result = result - 1
```

### 비교 연산
```python
n < 0      # ~보다 작다
n <= 0     # 작거나 같다
n == 0     # 같다
n != 0     # 같지 않다
```

### 논리 연산
```python
not isinstance(n, int)  # not (부정)
a and b                  # and (그리고)
a or b                   # or (또는)
```

### 초초보 예시 코드

**예시 1: 산술 연산**
```python
a = 10
b = 3

print(f"더하기: {a + b}")    # 출력: 더하기: 13
print(f"빼기: {a - b}")      # 출력: 빼기: 7
print(f"곱하기: {a * b}")    # 출력: 곱하기: 30
print(f"나누기: {a / b}")    # 출력: 나누기: 3.333...
print(f"몫: {a // b}")       # 출력: 몫: 3
print(f"나머지: {a % b}")    # 출력: 나머지: 1
print(f"거듭제곱: {a ** 2}") # 출력: 거듭제곱: 100
```

**예시 2: 비교 연산**
```python
age = 20
adult_age = 18

print(f"성인인가요? {age >= adult_age}")  # 출력: 성인인가요? True

score = 85
if score >= 90:
    print("A등급")
elif score >= 80:
    print("B등급")  # 출력: B등급
else:
    print("C등급")
```

**예시 3: 논리 연산**
```python
age = 25
has_license = True

# and 연산 (둘 다 참이어야 함)
if age >= 18 and has_license:
    print("운전 가능합니다.")  # 출력: 운전 가능합니다.

# or 연산 (하나만 참이면 됨)
is_student = False
is_senior = False
if is_student or is_senior:
    print("할인 대상입니다.")
else:
    print("정상 요금입니다.")  # 출력: 정상 요금입니다.

# not 연산 (반대로)
is_raining = False
if not is_raining:
    print("우산이 필요 없습니다.")  # 출력: 우산이 필요 없습니다.
```

---

## 💡 초보자 팁

1. **들여쓰기 중요**: 파이썬은 들여쓰기로 코드 블록 구분 (보통 4칸 공백)
2. **타입 힌트는 선택**: 없어도 코드는 동작함 (가독성을 위한 것)
3. **에러는 친구**: try-except로 예상되는 에러 처리
4. **독스트링 습관**: 함수마다 설명 작성하면 나중에 편함
5. **`if __name__ == "__main__":`**: 파일이 직접 실행될 때만 실행되는 코드 블록

---

## 📚 더 공부하면 좋은 것들

이 코드에는 없지만 자주 쓰이는 것들:
- 리스트, 딕셔너리 (자료구조)
- while 반복문
- 리스트 컴프리헨션
- 람다 함수
- 클래스와 객체

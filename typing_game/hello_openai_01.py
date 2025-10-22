import random
from openai import OpenAI

# 누가 돈을 낼래? - 인증 (Authentication)
#  - 요청자가 누구인지를 증명 => 식별
OPENAI_API_KEY = ""

# 파이썬에서는 쌍따옴표 혹은 홑따옴표 3개를 통해 여러 줄 문자열을 쉽게 정의할 수 있습니다.
# 쌍따옴표 혹은 홑따옴표 1개는 소스코드에서 1줄로만 문자열을 정의할 수 있어요.
PROMPT = """단어 타이핑 게임에 사용할 단어들을 생성해줘.

- 언어 : 영어
- 생성 개수 : 100개
- 주제 : "해리포터" 소설에 나오는 단어
- 레벨 : 대한민국 중학생
- 출력 포맷 : 설명을 제외하고, 단어만 줄 단위로 줄번호 없이 출력"""

client = OpenAI(api_key=OPENAI_API_KEY)

# API 요청 시에 지정 api key가 OpenAI API 서버로 자동 전달
# 그 api key가 유효하다면, API 요청을 처리하고 응답을 합니다.
response = client.responses.create(
    model="gpt-4o-mini",
    input=PROMPT,
)

# print(response)
# print(response.output_text)  # 타입 : 문자열

# 1) 우리가 AI응답을 직접 가공
words_str: str = response.output_text  # 타입 : 문자열
# 통 문자열 -> 여러 개의 문자열 (개행문자를 기준으로 나눠봅시다.)
word_list: list[str] = words_str.splitlines()  # 타입 : 문자열로 구성된 리스트(list)
print(word_list)
random.shuffle(word_list)  # 리스트 내 요소들의 순서를 랜덤으로 변경

print("랜덤으로 뽑은 10개 단어 :", word_list[0:10])

# 2) OpenAI AI가 알아서 가공해주는 방법도 있어요.

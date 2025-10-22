# OpenAI, Stuructured Model Output
#  - 원하는 타입(포맷)으로 정확하게 AI가 맞춰서 응답을 줍니다.
#  - 후가공이 필요없이, 간단하게 AI 응답을 활용할 수 있습니다.

from openai import OpenAI
from pydantic import BaseModel

OPENAI_API_KEY = ""

client = OpenAI(api_key=OPENAI_API_KEY)  # 클라이언트 객체 생성

class WordListResponse(BaseModel):
    word_list: list[str]

# 인자 (Arguments)
#  - 함수를 수행하기 위해 필요한 사전 정보
def make_word_list(language: str, size: int, subject: str, level: str):
    # 함수 내에서의 변수 선언은 지역변수(local variable)로서
    # 항상 소문자로 쓰셔야 합니다. (파이썬 스타일 가이드)
    # 파이썬의 f-string 문법을 활용
    prompt = f"""단어 타이핑 게임에 사용할 단어들을 생성해줘.

- 언어 : {language}
- 생성 개수 : {size}
- 주제 : {subject}
- 레벨 : {level}
- 출력 포맷 : 설명을 제외하고, 단어만 줄 단위로 줄번호 없이 출력"""

    print(prompt)

    response = client.responses.parse(
        model="gpt-4o-mini",
        input=prompt,
        text_format=WordListResponse,
    )

    word_list_response: WordListResponse = response.output_parsed
    return word_list_response.word_list

print(make_word_list("일본어", 10, "아이언맨", "초급"))

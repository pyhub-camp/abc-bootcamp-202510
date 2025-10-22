from openai import OpenAI

OPENAI_API_KEY = ""

client = OpenAI(api_key=OPENAI_API_KEY)  # 클라이언트 객체 생성

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

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
    )
    # 각 단어 끝에 공백이 포함된 리스트
    word_list = response.output_text.splitlines()  # 응답 뭉치 (str) -> list[str]

    # AI 응답 + 후처리
    new_word_list = []
    for word in word_list:  # word : str 타입
        # 문자열의 좌/우의 연속된 white spaces들을 제거한 문자열을 반환
        word = word.strip()  # 같은 이름의 변수에 다시 저장
        new_word_list.append(word)

    return new_word_list

print(make_word_list("일본어", 10, "아이언맨", "초급"))

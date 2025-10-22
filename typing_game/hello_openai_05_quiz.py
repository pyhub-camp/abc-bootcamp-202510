# 방금 전과 같이 VSCode의 자동완성 기능이 제대로 동작할려면
# 가상환경과 VSCode의 "Python: Select Interpreter" 설정를 통해 생성한 가상환경을
# 올바르게 지정해주셔야 합니다.
from openai import OpenAI
from pydantic import BaseModel


OPENAI_API_KEY = "..."
client = OpenAI(api_key=OPENAI_API_KEY)

class QuizPair(BaseModel):
    description: str
    answer: str

# 함수 (Function)
#  - 어떤 일을 수행하는 코드 묶음
#  - 가급적 작게, 하나의 일만 수행하도록 구성을 권장.

def make_quiz(주제: str) -> tuple[str, str]:
    """
    인자로 퀴즈 주제를 받아서, OpenAI API를 활용해서
    해당 주제의 퀴즈 설명/답변을 1개 생성한 뒤에
    퀴즈 설명과 답변을 반환(Return)합니다.
    """

    prompt = f"""퀴즈 설명/답변 생성해줘.

    - 주제 : {주제}
    - 주의 : 모든 답변은 한국어로 생성합니다.
    """
    # print("디버깅 목적 :", prompt)

    # client.responses.create()  # 응답이 문자열 뭉치 (str 타입) - ex) AI 대화 응답 생성
    # response.output_text

    # 응답이 여러 요소여야할 경우에 유용
    response = client.responses.parse(
        model="gpt-4o-mini",
        input=prompt,  # 지침 (Instruction)
        text_format=QuizPair,
    )

    # 지침에 따라 설명/답변이 잘 생성되었는 지를, 프로그램 초기에 확인할 목적
    # print("디버깅 목적 :", response.output_parsed)

    설명 = response.output_parsed.description  # 설명
    답변 = response.output_parsed.answer  # 답변
    # 설명 = "..."
    # 답변 = "..."
    return 설명, 답변

# make_quiz 함수가 2개를 반환하니까, 반환값을 받을 때에도 꼭 2개로 받아야 합니다.
퀴즈_설명, 퀴즈_답변 = make_quiz("대한민국 2000년대 영화 제목 맞추기")

print("퀴즈를 맞춰보세요.")
print(퀴즈_설명)
유저가_입력한_답변 = input("당신의 답은? ")

if 퀴즈_답변 == 유저가_입력한_답변:  # 띄워쓰기, 콤마 하나까지 모두 같은지 비교
    print("정답입니다!!")
else:  # 앞선 조건이 모두 거짓이라면
    print("오답이구요. 정답은", 퀴즈_답변, "입니다.")

# 각자의 주제로 작은 파이썬 프로그램을 만들기
#  1) 지금까지 내용을 복습
#  2) 각자의 주제/기능개선 계획을 Padlet에게 포스팅
#  3) 기능 만들기 하신 후에, 조금 전 Padlet 포스팅의 댓글로
#     스샷과 만든 기능에 대한 대략적인 설명과 코드를 공유

# 퀴즈 개선 아이디어
#  1) 재시도를 지원 (최대 10번)
#  2) 한 번에 1개의 퀴즈가 아닌 10개의 퀴즈를 생성하고, 퀴즈 진행 후에 스코어를 알려준다.
#  3) "힌트주세요." 명령을 지원. => 힌트를 AI를 통해서 생성해서 제공.
#  4) Network 대전

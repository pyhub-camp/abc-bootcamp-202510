
# 함수 정의만 했을 뿐, 아직 작업을 지시하지는 X.
def make_word_list():
    return ["단어1", "단어2", "단어3"]

# 함수 이름만 출력(print)했을 뿐, 실제 작업 지시 X
print(make_word_list)

# 작업 지시 문법 : 함수이름()  => 함수를 호출(Call)한다.
print(make_word_list())
print(make_word_list())

# 함수를 사용하는 사람 입장에서는
# 이제 make_word_list 함수 호출방법만 알면, 단어 목록을 생성받을 수 있게 됩니다.
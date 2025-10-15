
print("2 * 1 = 2")
print("2 * 2 = 4")
print("2 * 3 = 6")
print("2 * 4 = 8")
print("2 * 5 = 10")
print("2 * 6 = 12")
print("2 * 7 = 14")
print("2 * 8 = 16")
print("2 * 9 = 18")
print("----")

# 주석 (Comments) - 프로그래밍 언어가 무시하는 코드.
# 반복문 (for loop)
# range : 1 이상 10 미만 범위에서 1씩 증가
for i in range(1, 10, 3):
    print("2 * {} = {}".format(i, 2*i))

# 파이썬에서는 들여쓰기를 맞추지 않으면
# IndentationError 예외가 발생한다.

print("---")

for number in range(2, 10):
    print("### {}단 ###".format(number))
    for i in range(1, 10, 1):
        # 파이썬에서는 문자열의 format 함수를 통해
        # 출력 양식을 지정할 수 있습니다.
        # 값이 들어갈 위치(placeholder)는 중괄호를 통해 지정
        print("{} * {} = {}".format(number, i, number * i))
    print()

n = int(input("피라미드 높이를 입력하세요: "))
for i in range(1, n + 1):
    print(" " * (n - i) + "*" * (2 * i - 1))

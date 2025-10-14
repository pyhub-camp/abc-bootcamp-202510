def pyramid(n, mode='center'):
    for i in range(1, n+1):
        if mode == 'left':
            print('*' * i)
        elif mode == 'right':
            print(' ' * (n - i) + '*' * i)
        elif mode == 'diamond':
            print(' ' * (n - i) + '*' * (2 * i - 1))
        else:  # center
            print(' ' * (n - i) + '*' * (2 * i - 1))
    if mode == 'diamond':  # 아래쪽 반 추가
        for i in range(n-1, 0, -1):
            print(' ' * (n - i) + '*' * (2 * i - 1))

try:
    n = int(input("숫자를 입력하세요: "))
    mode = input("모드를 선택하세요 (left, center, right, diamond) [기본: center]: ") or 'center'
    pyramid(n, mode)
except ValueError:
    print("정수를 입력해주세요!")

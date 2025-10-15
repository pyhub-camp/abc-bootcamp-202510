# Visual Studio Code를 활용한 파이썬 소스코드 디버깅

## Python 확장 설치

Visual Studio Code 내에서 Microsoft의 다음 [Python](https://marketplace.visualstudio.com/items?itemName=ms-python.python) 확장을 설치합니다.
![](./assets/Pasted%20image%2020251015221830.png)

## Python 소스파일 하나 열기

디버깅할 Python 소스파일을 하나 활성화합니다.
![](./assets/Pasted%20image%2020251015221931.png)

## 디버거 실행 설정 파일 만들기

툴바에서 4번째 아이콘 "실행 및 디버그" 패널에서 `launch.json 파일 만들기` 링크를 클릭합니다.
![](./assets/Pasted%20image%2020251015223306.png)

위와 같이 "Show automatic Python configurations" 버튼이 있다면, 이를 클릭해주세요.

다음과 같이"Python Debugger: Python File (텐트메이커1기)" 팝업이 뜨면 선택합니다.
![](./assets/Pasted%20image%2020251015223328.png)

아래 아래와 같이 디버그 메뉴가 활성화되었습니다.
![](./assets/Pasted%20image%2020251015223438.png)

## 중단점 설정하기

에디터 패널에서 줄번호 왼쪽에 마우스를 올려 "중단점 (Break Point)"를 Toggle할 수 있습니다.
![](./assets/Pasted%20image%2020251015223616.png)

디버거 구동 중에 멈춰야할 줄(Line)에 중단점을 설정합니다.
![](./assets/Pasted%20image%2020251015223744.png)

## 디버거 시작

"디버깅 시작" 녹색 버튼을 눌러, 디버깅을 시작합니다.
![](./assets/Pasted%20image%2020251015223756.png)

디버거가 구동되고, 지정된 중단점에서 실행이 멈춤을 확인하실 수 있습니다.
![](./assets/Pasted%20image%2020251015223838.png)

디버거 메뉴는 아래와 같습니다.
![](./assets/Pasted%20image%2020251015223919.png)
1. 계속 (Continue) : 다음 중단점까지 실행
2. 단위 실행 (Step Over) : 현재 줄 실행하고, 다음 줄에서 멈춤
3. 단계 정보 (Step In) : 함수 안으로 들어갑니다.
4. 단계 출력 (Step Out) : 현재 함수 밖으로 1 depth 나갑니다.
5. 다시 시작 (Restart) : 처음부터 다시 시작합니다.
6. 중지 (Stop) : 디버거를 중지합니다.

## 변수값 모니터링

실행이 멈춘 상황에서의 변수 현황을 모니터링할 수 있습니다. 실시간으로 반영됩니다.
![](./assets/Pasted%20image%2020251015224150.png)

디버거 메뉴를 통해, 줄 단위로 실행하시며 변수값을 변화를 확인하며 버그를 찾아 해결하실 수 있습니다.

# 파이썬 프로그래밍 & AI 프로젝트 부트캠프

> **👨‍🏫 강사용 가이드**

```table-of-contents
```

---

## 📋 과정 개요

**기간**: 5일 (총 30시간)
- 파이썬 프로그래밍: 3일 (18시간)
- 프로젝트: 2일 (12시간)

**목표**:
1. 파이썬 기초 문법 이해
2. AI(ChatGPT/Codex)와 함께 다양한 애플리케이션을 만들 수 있는 자신감 확보
3. 실전 프로젝트를 통한 문제 해결 능력 향상

---

## 🎯 일차별 커리큘럼

| 일차 | 주제 | 핵심 내용 | 결과물 |
|------|------|-----------|--------|
| **1일차** | [AI와 함께 첫 웹 앱 만들기](01%EC%9D%BC%EC%B0%A8---AI%EC%99%80-%ED%95%A8%EA%BB%98-%EC%B2%AB-%EC%9B%B9-%EC%95%B1-%EB%A7%8C%EB%93%A4%EA%B8%B0%5C.md) | Python, VSCode, Streamlit 설치<br>DuckDuckGo 이미지 검색<br>OpenAI API 사용 | 이미지 검색 앱, AI 질문 도우미 |
| **2일차** | [실생활 자동화 앱 만들기](02%EC%9D%BC%EC%B0%A8---%EC%8B%A4%EC%83%9D%ED%99%9C-%EC%9E%90%EB%8F%99%ED%99%94-%EC%95%B1-%EB%A7%8C%EB%93%A4%EA%B8%B0%5C.md) | QR 코드 생성 (qrcode, pillow)<br>웹 크롤링 (BeautifulSoup) | QR 코드 생성기, 뉴스 크롤러 |
| **3일차** | [AI 슈퍼파워 앱 만들기](03%EC%9D%BC%EC%B0%A8---AI-%EC%8A%88%ED%8D%BC%ED%8C%8C%EC%9B%8C-%EC%95%B1-%EB%A7%8C%EB%93%A4%EA%B8%B0%5C.md) | API 연동 (requests)<br>OpenWeatherMap API<br>OpenAI/Claude API | 날씨 앱, AI 챗봇 |
| **4일차** | [내 문제 해결하는 앱 만들기](04%EC%9D%BC%EC%B0%A8---%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EA%B0%9C%EB%B0%9C%5C.md) | 문제 정의 및 아이디어 구체화<br>AI와 협업 개발 | 개인 프로젝트 (자유 주제) |
| **5일차** | [프로젝트 완성](05%EC%9D%BC%EC%B0%A8---%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8-%EC%99%84%EC%84%B1-%EB%B0%8F-%EB%B0%9C%ED%91%9C%5C.md) | 마무리 및 발표<br>피드백 및 학습 정리 | 완성된 프로젝트 |

---

## 📚 교육 자료

### 교육생용 문서
- **[소개](%EC%86%8C%EA%B0%9C.md)**: 사전 학습 자료 (왜 Python인가?, AI 시대 개발자의 역할)
  - **중요**: 1일차 수업 전에 읽어오도록 안내
- **[파이썬 활용 사례 모음](%ED%8C%8C%EC%9D%B4%EC%8D%AC-%ED%99%9C%EC%9A%A9-%EC%82%AC%EB%A1%80-%EB%AA%A8%EC%9D%8C.md)**: 실전 예시 20+ 가지

### 참고 자료
- ChatGPT: https://chat.openai.com
- GitHub Copilot (Codex): https://github.com/features/copilot
- Python 공식 튜토리얼: https://docs.python.org/ko/3/tutorial/
- Streamlit 문서: https://docs.streamlit.io/

---

## 준비 사항

### 강사 준비
- [ ] **AI 계정 준비** (교육생 수만큼)
  - ChatGPT 계정 (권장) 또는 GitHub Copilot 라이선스
  - 계정 정보 리스트 (이메일/비밀번호)
  - 교육용 공유 계정으로 사용
- [ ] OpenAI API KEY 또는 Anthropic API KEY (3일차 LLM 실습용)
- [ ] OpenWeatherMap API KEY (3일차 날씨 앱 실습용)
- [ ] 카카오/네이버 지도 API KEY (선택사항)
- [ ] 샘플 코드 및 데이터 파일 준비
- [ ] 프로젝터 및 화면 공유 환경 확인

### 교육생 준비 (사전 안내)
- [ ] 노트북 (Windows/Mac 무관)
- [ ] 개인 이메일 계정 (선택사항)
- [ ] [소개](%EC%86%8C%EA%B0%9C.md) 문서 읽어오기 (필수!)
- [ ] Python 사전 설치 (권장)

---

## 💡 강의 팁

### 전체 진행 원칙
- **AI 협업 강조**: ChatGPT/Codex를 "AI 페어 프로그래머"로 활용
- **실습 중심**: 이론 20%, 실습 80%
- **완성 우선**: 완벽함보다 동작하는 코드 만들기
- **에러 경험**: 에러를 겪고 해결하는 과정도 중요한 학습

### 일차별 주안점

**1일차**:
- ⚡ 환경 구축에 30분 이상 쓰지 않기 (사전 준비 강조)
- ⚡ **AI 계정 배포**: 수업 시작 전 계정 정보 배포 및 로그인 확인
- ⚡ **작업 폴더 통일**: `C:\Work\abc-bootcamp-202510` 폴더 사용
- ⚡ 문법보다 "코드가 동작한다"는 성취감 제공
- ⚡ AI 사용법을 충분히 시연 (ChatGPT 또는 Codex)

**2일차**:
- ⚡ Streamlit의 "즉시 반영" 마법 체험시키기
- ⚡ 상태 관리(st.session_state) 개념 명확히
- ⚡ 웹 앱 배포까지 체험하면 동기부여 극대화

**3일차**:
- ⚡ API 키 관리 보안 강조 (.env, .gitignore)
- ⚡ AI API 비용 안내 (무료 크레딧, 사용량 모니터링)
- ⚡ 프로젝트 아이디어 브레인스토밍 시간 확보

**4-5일차**:
- ⚡ 개별 프로젝트 진행 속도 차이 고려
- ⚡ 막힌 사람 우선 지원
- ⚡ 발표는 "배운 점"과 "느낀 점" 위주로

### 자주 나오는 질문

**Q: Python 버전은 어떤 걸 쓰나요?**
A: 3.10 이상 권장 (3.13 최신 안정화 버전)

**Q: AI 계정은 개인이 준비해야 하나요?**
A: 아니요, 교육팀에서 준비한 공용 계정을 사용합니다. 수업 시작 시 배포합니다.

**Q: AI 계정을 개인적으로 사용해도 되나요?**
A: 교육용 공용 계정이므로 수업 중에만 사용하세요. 개인 용도로는 사용할 수 없습니다.

**Q: ChatGPT와 Codex 중 어떤 걸 써야 하나요?**
A: 초보자는 ChatGPT 웹 브라우저로 시작하는 것을 권장합니다. 익숙해지면 Codex(GitHub Copilot)로 업그레이드하세요.

**Q: API 키가 없으면 못 하나요?**
A: 1-2일차는 API 키 불필요. 3일차 날씨 앱과 AI 챗봇은 강사가 준비한 API 키 공유

**Q: Mac과 Windows 차이가 있나요?**
A: Python/VS Code 모두 동일. 단, 터미널 명령어 일부 차이 (cd, mkdir 등은 동일)

**Q: 코딩 경험이 전혀 없는데 괜찮나요?**
A: 전혀 문제없음. 오히려 선입견 없이 AI와 협업하는 방법을 배우기 좋음

**Q: 작업 폴더를 다른 곳에 만들어도 되나요?**
A: 가능하지만 `C:\Work\abc-bootcamp-202510` 사용 권장 (강사 화면과 동일하게 진행)

---

## 🎓 수료 후 추천 학습 경로

**업무 자동화에 집중**:
1. openpyxl, pandas 심화 (엑셀 자동화)
2. selenium, playwright (웹 자동화)
3. schedule, APScheduler (작업 스케줄링)

**데이터 분석 방향**:
1. pandas, numpy 심화
2. matplotlib, seaborn, plotly (시각화)
3. scikit-learn (머신러닝 입문)

**웹 개발 방향**:
1. Flask, FastAPI 백엔드
2. SQLAlchemy (데이터베이스)
3. JavaScript 기초 (프론트엔드 이해)

---

## 📞 문의 및 피드백

**강의 개선 아이디어**:
- 실습 난이도 조정이 필요한 부분
- 추가하면 좋을 예제나 프로젝트
- 교육생 피드백 및 질문 패턴

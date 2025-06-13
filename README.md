# 뉴스 수집기 및 Gmail API 연동

이 프로젝트는 네이버와 다음의 주요 뉴스를 자동으로 수집하여 CSV 파일로 저장하고, 수집 결과 요약을 Gmail API를 통해 이메일로 전송할 수 있습니다.

## 주요 기능
- 네이버/다음 뉴스 자동 수집 (news_collector.py)
- 수집 결과 CSV 저장 (news_data.csv 등)
- Gmail API를 통한 이메일 전송 (send_summary.py)
- 중복 저장 방지

## 설치 및 준비

### 1. 패키지 설치
```bash
pip install -r requirements.txt
```

### 2. 구글 클라우드 콘솔에서 Gmail API 설정
1. [Google Cloud Console](https://console.cloud.google.com/)에서 새 프로젝트 생성
2. "API 및 서비스" > "사용자 인증 정보"에서 OAuth 클라이언트 ID 생성 (데스크톱 앱)
3. 생성된 `credentials.json`(여기서는 `sans_seesunny_gmailtest.json`) 파일을 프로젝트 폴더에 저장
4. 최초 실행 시 구글 계정 인증 후 `token.pickle`이 자동 생성됨

### 3. .gitignore 설정
- `token.pickle` 등 민감 파일은 반드시 .gitignore에 추가하여 깃허브에 업로드하지 않도록 주의

## 사용 방법

### 1. 뉴스 수집
```bash
python news_collector.py
```
- 수집된 뉴스는 `news_data.csv` 등으로 저장됩니다.

### 2. 이메일로 요약 전송
```bash
python send_summary.py
```
- `send_summary.py`는 프로젝트 요약을 지정한 이메일로 전송합니다.
- 수신자, 제목, 본문 등은 코드 내에서 수정 가능합니다.

## 주요 파일 설명
- `news_collector.py`: 뉴스 크롤러 메인 스크립트
- `send_summary.py`: Gmail API로 이메일 전송
- `sans_seesunny_gmailtest.json`: 구글 OAuth 클라이언트 인증 파일
- `token.pickle`: 인증 토큰(자동 생성, 깃허브 업로드 금지)
- `news_data.csv`: 수집된 뉴스 데이터

## requirements.txt 예시
```
google-auth
google-auth-oauthlib
google-api-python-client
pandas
beautifulsoup4
requests
```

## 보안 및 주의사항
- `token.pickle` 등 민감 정보는 절대 공개 저장소에 올리지 마세요.
- 구글 인증은 최초 1회만 필요하며, 이후에는 자동으로 토큰이 갱신됩니다.
- 웹사이트 구조 변경 시 크롤러 코드도 함께 수정해야 할 수 있습니다.

## 참고
- Gmail API 공식 문서: https://developers.google.com/gmail/api/quickstart/python
- 구글 클라우드 콘솔: https://console.cloud.google.com/

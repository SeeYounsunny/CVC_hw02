import os
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
PORT = 8080  # 고정된 포트 번호 사용

def get_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'sans_seesunny_gmailtest.json', SCOPES)
            creds = flow.run_local_server(port=PORT)  # 고정된 포트 사용
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()
        print(f'Message Id: {message["id"]}')
        return message
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

def main():
    # 프로젝트 요약 작성
    summary = """
    프로젝트 요약: 뉴스 수집기

    1. 주요 파일:
    - news_collector.py: 네이버 뉴스를 수집하는 메인 스크립트
    - news_data.csv: 수집된 뉴스 데이터
    - README.md: 프로젝트 설명 문서

    2. 주요 기능:
    - 네이버 뉴스 자동 수집
    - CSV 형식으로 데이터 저장
    - 중복 뉴스 제거
    - 에러 처리 및 로깅

    3. 사용된 기술:
    - Python
    - BeautifulSoup4
    - Pandas
    - Git/GitHub

    4. 프로젝트 상태:
    - Private 저장소로 설정
    - Personal Access Token으로 인증
    - 정상적으로 푸시/풀 가능

    이 프로젝트는 자동화된 뉴스 수집 시스템을 구현한 것으로,
    네이버 뉴스를 주기적으로 수집하여 CSV 파일로 저장합니다.
    """

    # Gmail 서비스 설정
    service = get_gmail_service()
    
    # 메시지 생성
    message = create_message(
        'me',
        # TODO: Add recipient email address here
        '프로젝트 요약: 뉴스 수집기',
        summary
    )
    
    # 메시지 전송
    send_message(service, 'me', message)

if __name__ == '__main__':
    main() 
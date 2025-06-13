import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
PORT = 8080

class NewsCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # AI/Tech 관련 키워드
        self.keywords = ['AI', '인공지능', '머신러닝', '딥러닝', 'GPT', '챗GPT', '로봇', '빅데이터', 
                        '클라우드', '블록체인', '메타버스', '스마트폰', '반도체', 'IT', '기술']
    
    def get_gmail_service(self):
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
                creds = flow.run_local_server(port=PORT)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('gmail', 'v1', credentials=creds)

    def create_news_email(self, news_list, stage):
        today = datetime.now().strftime('%Y년 %m월 %d일')
        
        # 단계별 제목과 설명
        stage_info = {
            1: {
                'title': '1단계: 뉴스 수집 시작',
                'description': 'AI/Tech 뉴스 수집 프로세스가 시작되었습니다.',
                'emoji': '🚀'
            },
            2: {
                'title': '2단계: 뉴스 데이터 처리',
                'description': '수집된 뉴스 데이터가 처리되었습니다.',
                'emoji': '⚙️'
            },
            3: {
                'title': '3단계: 최종 뉴스 클리핑',
                'description': 'AI/Tech 뉴스 클리핑이 완료되었습니다.',
                'emoji': '📊'
            }
        }
        
        # HTML 템플릿 생성
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ 
                    background-color: #f8f9fa;
                    padding: 20px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }}
                .news-item {{
                    margin-bottom: 15px;
                    padding: 10px;
                    border-left: 4px solid #007bff;
                    background-color: #f8f9fa;
                }}
                .news-title {{
                    color: #007bff;
                    text-decoration: none;
                    font-weight: bold;
                }}
                .news-title:hover {{
                    text-decoration: underline;
                }}
                .news-source {{
                    color: #6c757d;
                    font-size: 0.9em;
                }}
                .news-date {{
                    color: #6c757d;
                    font-size: 0.9em;
                }}
                .section-header {{
                    background-color: #e9ecef;
                    padding: 10px;
                    margin: 20px 0 10px 0;
                    border-radius: 5px;
                }}
                .stage-info {{
                    background-color: #e3f2fd;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>{stage_info[stage]['emoji']} {today} {stage_info[stage]['title']}</h2>
                <p>{stage_info[stage]['description']}</p>
            </div>
            <div class="stage-info">
                <h3>프로세스 단계 정보</h3>
                <p>현재 단계: {stage}/3</p>
                <p>수집된 뉴스: {len(news_list)}건</p>
            </div>
        """
        
        # 네이버 뉴스 섹션
        naver_news = [news for news in news_list if news['source'] == 'Naver']
        if naver_news:
            html_content += '<div class="section-header"><h3>📰 네이버 AI/Tech 뉴스</h3></div>'
            for news in naver_news:
                html_content += f"""
                <div class="news-item">
                    <a href="{news['link']}" class="news-title">{news['title']}</a>
                    <div class="news-source">출처: {news['source']}</div>
                    <div class="news-date">수집시간: {news['date']}</div>
                </div>
                """
        
        # 다음 뉴스 섹션
        daum_news = [news for news in news_list if news['source'] == 'Daum']
        if daum_news:
            html_content += '<div class="section-header"><h3>📰 다음 AI/Tech 뉴스</h3></div>'
            for news in daum_news:
                html_content += f"""
                <div class="news-item">
                    <a href="{news['link']}" class="news-title">{news['title']}</a>
                    <div class="news-source">출처: {news['source']}</div>
                    <div class="news-date">수집시간: {news['date']}</div>
                </div>
                """
        
        html_content += """
        </body>
        </html>
        """
        
        return html_content

    def send_news_email(self, news_list, stage, recipient):
        service = self.get_gmail_service()
        
        # HTML 형식의 이메일 생성
        message = MIMEMultipart('alternative')
        message['to'] = recipient
        message['from'] = 'me'
        
        # 단계별 제목
        stage_titles = {
            1: '1단계: 뉴스 수집 시작',
            2: '2단계: 뉴스 데이터 처리',
            3: '3단계: 최종 뉴스 클리핑'
        }
        
        message['subject'] = f'AI/Tech 뉴스 클리핑 - {stage_titles[stage]} - {datetime.now().strftime("%Y년 %m월 %d일")}'
        
        # HTML 내용 추가
        html_content = self.create_news_email(news_list, stage)
        message.attach(MIMEText(html_content, 'html'))
        
        # 이메일 전송
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        try:
            message = service.users().messages().send(
                userId='me',
                body={'raw': raw_message}
            ).execute()
            print(f'AI/Tech 뉴스 클리핑 이메일이 {recipient}에게 전송되었습니다. (Message Id: {message["id"]})')
        except Exception as e:
            print(f'이메일 전송 중 오류 발생: {str(e)}')

    def is_tech_news(self, title):
        """제목에 AI/Tech 관련 키워드가 포함되어 있는지 확인"""
        return any(keyword.lower() in title.lower() for keyword in self.keywords)

    def collect_naver_news(self):
        # 네이버 IT/과학 섹션 URL
        url = "https://news.naver.com/section/105"
        news_list = []
        
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.select('a.sa_text_title, a.news_tit')
            
            for article in articles:
                title = article.text.strip()
                # AI/Tech 관련 뉴스만 필터링
                if self.is_tech_news(title):
                    link = article.get('href', '')
                    if link.startswith('/'):
                        link = 'https://news.naver.com' + link
                    elif link.startswith('//'):
                        link = 'https:' + link
                    
                    news_data = {
                        'title': title,
                        'link': link,
                        'source': 'Naver',
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    news_list.append(news_data)
                    
                    # 최대 10개까지만 수집
                    if len(news_list) >= 10:
                        break
            
            return news_list
            
        except Exception as e:
            print(f"네이버 뉴스 수집 중 오류 발생: {str(e)}")
            return []

    def collect_daum_news(self):
        # 다음 IT/과학 섹션 URL
        url = "https://news.daum.net/digital"
        news_list = []
        
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.select('a.link_txt')
            
            for article in articles:
                title = article.text.strip()
                # AI/Tech 관련 뉴스만 필터링
                if self.is_tech_news(title):
                    link = article.get('href', '')
                    
                    news_data = {
                        'title': title,
                        'link': link,
                        'source': 'Daum',
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    news_list.append(news_data)
                    
                    # 최대 10개까지만 수집
                    if len(news_list) >= 10:
                        break
            
            return news_list
            
        except Exception as e:
            print(f"다음 뉴스 수집 중 오류 발생: {str(e)}")
            return []

    def save_to_csv(self, news_list, filename='news_data.csv'):
        try:
            df = pd.DataFrame(news_list)
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"뉴스가 {filename}에 저장되었습니다.")
        except Exception as e:
            print(f"CSV 저장 중 오류 발생: {str(e)}")

def main():
    collector = NewsCollector()
    
    # 수신자 목록
    recipients = [
        'jayleekr0125@gmail.com',
        'jysin0102@gmail.com',
        'jkimak1124@gmail.com'
    ]
    
    # 네이버 뉴스 수집
    naver_news = collector.collect_naver_news()
    collector.save_to_csv(naver_news, 'naver_tech_news.csv')
    
    # 다음 뉴스 수집
    daum_news = collector.collect_daum_news()
    collector.save_to_csv(daum_news, 'daum_tech_news.csv')
    
    # 각 수신자에게 단계별로 이메일 전송
    all_news = naver_news + daum_news
    for i, recipient in enumerate(recipients, 1):
        collector.send_news_email(all_news, i, recipient)
        time.sleep(1)  # 이메일 전송 간 1초 대기
    
    print("AI/Tech 뉴스 수집 및 이메일 전송이 완료되었습니다.")

if __name__ == "__main__":
    main() 
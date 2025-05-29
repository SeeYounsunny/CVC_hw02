import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def test_news_collection():
    """테스트용 뉴스 수집 함수"""
    url = "https://news.naver.com/section/100"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 첫 번째 뉴스만 가져오기
        article = soup.select_one('a.sa_text_title, a.news_tit')
        
        if article:
            title = article.text.strip()
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
            
            # CSV 파일로 저장
            df = pd.DataFrame([news_data])
            df.to_csv('test_news.csv', index=False, encoding='utf-8-sig')
            print(f"테스트 뉴스가 test_news.csv에 저장되었습니다.")
            return True
            
    except Exception as e:
        print(f"테스트 뉴스 수집 중 오류 발생: {str(e)}")
        return False

if __name__ == "__main__":
    test_news_collection() 
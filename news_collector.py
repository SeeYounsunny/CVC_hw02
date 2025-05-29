import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import os

class NewsCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
    def collect_naver_news(self):
        """네이버 뉴스 수집"""
        url = "https://news.naver.com/section/100"
        news_list = []
        
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = soup.select('a.sa_text_title, a.news_tit')
            
            for article in articles[:10]:  # 상위 10개 뉴스만 수집
                title = article.text.strip()
                link = article.get('href', '')
                if link.startswith('/'):
                    link = 'https://news.naver.com' + link
                elif link.startswith('//'):
                    link = 'https:' + link
                
                news_list.append({
                    'title': title,
                    'link': link,
                    'source': 'Naver',
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
        except Exception as e:
            print(f"네이버 뉴스 수집 중 오류 발생: {str(e)}")
            
        return news_list
    
    def collect_daum_news(self):
        """다음 뉴스 수집"""
        url = "https://news.daum.net/"
        news_list = []
        
        try:
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            articles = soup.select('a.link_txt')
            
            for article in articles[:10]:  # 상위 10개 뉴스만 수집
                title = article.text.strip()
                link = article.get('href', '')
                if link.startswith('/'):
                    link = 'https://news.daum.net' + link
                elif link.startswith('//'):
                    link = 'https:' + link
                
                news_list.append({
                    'title': title,
                    'link': link,
                    'source': 'Daum',
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
        except Exception as e:
            print(f"다음 뉴스 수집 중 오류 발생: {str(e)}")
            
        return news_list
    
    def save_to_csv(self, news_list, filename='news_data.csv'):
        """수집된 뉴스를 CSV 파일로 저장"""
        df = pd.DataFrame(news_list)
        
        # 파일이 이미 존재하면 추가 모드로 저장
        if os.path.exists(filename):
            df.to_csv(filename, mode='a', header=False, index=False, encoding='utf-8-sig')
        else:
            df.to_csv(filename, index=False, encoding='utf-8-sig')
            
        print(f"뉴스가 {filename}에 저장되었습니다.")

def main():
    collector = NewsCollector()
    
    # 네이버 뉴스 수집
    naver_news = collector.collect_naver_news()
    collector.save_to_csv(naver_news)
    
    # 다음 뉴스 수집
    daum_news = collector.collect_daum_news()
    collector.save_to_csv(daum_news)
    
    print("뉴스 수집이 완료되었습니다.")

if __name__ == "__main__":
    main() 
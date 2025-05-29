import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
import json
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SportsCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36'
        }
        # Selenium 설정
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-infobars')
        options.add_argument('--start-maximized')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--allow-running-insecure-content')
        options.add_argument('--disable-web-security')
        options.add_argument(f'--user-agent={self.headers["User-Agent"]}')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-sync')
        options.add_argument('--no-first-run')
        options.add_argument('--no-default-browser-check')
        options.add_argument('--password-store=basic')
        options.add_argument('--use-mock-keychain')
        
        # 브라우저 실행 설정
        self.driver = uc.Chrome(
            options=options,
            headless=False,  # 브라우저를 보이게 실행
            use_subprocess=True  # 서브프로세스로 실행
        )
        self.driver.set_page_load_timeout(30)
        self.wait = WebDriverWait(self.driver, 20)

    def __del__(self):
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
            except:
                pass

    def get_kbo_news(self):
        url = "https://sports.daum.net/baseball/"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = []
        articles = soup.select('a.link_txt')
        for article in articles[:10]:
            title = article.text.strip()
            link = article['href']
            if not link.startswith('http'):
                link = 'https://sports.daum.net' + link
            news_list.append({
                'title': title,
                'link': link,
                'source': 'KBO',
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        return news_list

    def get_mlb_news(self):
        url = "https://sports.daum.net/worldbaseball/"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = []
        articles = soup.select('a.link_txt')
        for article in articles[:10]:
            title = article.text.strip()
            link = article['href']
            if not link.startswith('http'):
                link = 'https://sports.daum.net' + link
            news_list.append({
                'title': title,
                'link': link,
                'source': 'MLB',
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        return news_list

    def get_kbl_news(self):
        url = "https://sports.daum.net/basketball/"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = []
        articles = soup.select('a.link_txt')
        for article in articles[:10]:
            title = article.text.strip()
            link = article['href']
            if not link.startswith('http'):
                link = 'https://sports.daum.net' + link
            news_list.append({
                'title': title,
                'link': link,
                'source': 'KBL',
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        return news_list

    def get_nba_news(self):
        url = "https://sports.daum.net/worldbasketball/"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_list = []
        articles = soup.select('a.link_txt')
        for article in articles[:10]:
            title = article.text.strip()
            link = article['href']
            if not link.startswith('http'):
                link = 'https://sports.daum.net' + link
            news_list.append({
                'title': title,
                'link': link,
                'source': 'NBA',
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        return news_list

    def get_kbo_standings(self):
        url = "https://sports.news.naver.com/kbaseball/record/index"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        standings = []
        rows = soup.select('.tb_wrap tbody tr')
        
        for row in rows:
            cols = row.select('td')
            if len(cols) >= 8:
                standings.append({
                    'rank': cols[0].text.strip(),
                    'team': cols[1].text.strip(),
                    'games': cols[2].text.strip(),
                    'wins': cols[3].text.strip(),
                    'losses': cols[4].text.strip(),
                    'draws': cols[5].text.strip(),
                    'win_rate': cols[6].text.strip(),
                    'games_behind': cols[7].text.strip()
                })
        return standings

    def get_mlb_standings(self):
        url = "https://sports.news.naver.com/wbaseball/record/index"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        standings = []
        rows = soup.select('.tb_wrap tbody tr')
        
        for row in rows:
            cols = row.select('td')
            if len(cols) >= 8:
                standings.append({
                    'rank': cols[0].text.strip(),
                    'team': cols[1].text.strip(),
                    'games': cols[2].text.strip(),
                    'wins': cols[3].text.strip(),
                    'losses': cols[4].text.strip(),
                    'win_rate': cols[5].text.strip(),
                    'games_behind': cols[6].text.strip()
                })
        return standings

    def get_kbl_standings(self):
        url = "https://sports.news.naver.com/basketball/record/index"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        standings = []
        rows = soup.select('.tb_wrap tbody tr')
        
        for row in rows:
            cols = row.select('td')
            if len(cols) >= 7:
                standings.append({
                    'rank': cols[0].text.strip(),
                    'team': cols[1].text.strip(),
                    'games': cols[2].text.strip(),
                    'wins': cols[3].text.strip(),
                    'losses': cols[4].text.strip(),
                    'win_rate': cols[5].text.strip(),
                    'games_behind': cols[6].text.strip()
                })
        return standings

    def get_nba_standings(self):
        url = "https://sports.news.naver.com/basketball/nba/record/index"
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        standings = []
        rows = soup.select('.tb_wrap tbody tr')
        
        for row in rows:
            cols = row.select('td')
            if len(cols) >= 7:
                standings.append({
                    'rank': cols[0].text.strip(),
                    'team': cols[1].text.strip(),
                    'games': cols[2].text.strip(),
                    'wins': cols[3].text.strip(),
                    'losses': cols[4].text.strip(),
                    'win_rate': cols[5].text.strip(),
                    'games_behind': cols[6].text.strip()
                })
        return standings

    def get_kbo_results(self):
        print("KBO 경기 결과 수집 시작...")
        results = []
        
        try:
            for i in range(7):
                date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                print(f"날짜 {date} 처리 중...")
                
                url = f"https://www.koreabaseball.com/Schedule/Schedule.aspx"
                print(f"URL 접속 시도: {url}")
                
                try:
                    self.driver.get(url)
                    time.sleep(10)  # 페이지 로딩 대기
                    print("페이지 로딩 완료")
                    
                    # 날짜 선택
                    date_input = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input#txtSearchDate"))
                    )
                    date_input.clear()
                    date_input.send_keys(date)
                    
                    # 검색 버튼 클릭
                    search_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "input#btnSearch"))
                    )
                    search_button.click()
                    time.sleep(5)  # 검색 결과 로딩 대기
                    
                    # 경기 결과 요소 대기
                    games = self.wait.until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.tblSchedule tr"))
                    )
                    
                    print(f"경기 수: {len(games)}")
                    
                    for game in games[1:]:  # 첫 번째 행은 헤더이므로 제외
                        try:
                            cols = game.find_elements(By.TAG_NAME, "td")
                            if len(cols) >= 4:
                                teams = cols[1].text.strip().split('vs')
                                scores = cols[2].text.strip().split('-')
                                
                                if len(teams) == 2 and len(scores) == 2:
                                    away_team = teams[0].strip()
                                    home_team = teams[1].strip()
                                    away_score = scores[0].strip()
                                    home_score = scores[1].strip()
                                    
                                    result = {
                                        'date': date.replace('-', ''),
                                        'league': 'KBO',
                                        'home_team': home_team,
                                        'away_team': away_team,
                                        'home_score': home_score,
                                        'away_score': away_score
                                    }
                                    results.append(result)
                                    print(f"경기 결과 추가: {away_team} {away_score} - {home_score} {home_team}")
                        except Exception as e:
                            print(f"경기 데이터 추출 중 오류: {str(e)}")
                            continue
                    
                    time.sleep(2)  # 다음 날짜로 넘어가기 전 대기
                
                except Exception as e:
                    print(f"페이지 로딩 중 오류 ({date}): {str(e)}")
                    continue
                
        except Exception as e:
            print(f"KBO 결과 수집 중 오류: {str(e)}")
        
        print(f"KBO 경기 결과 수집 완료. 총 {len(results)}개의 경기 결과 수집됨.")
        return results

    def get_mlb_results(self):
        print("MLB 경기 결과 수집 시작 (Yahoo Sports)...")
        results = []
        try:
            for i in range(7):
                date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                print(f"날짜 {date} 처리 중...")
                url = f"https://sports.yahoo.com/mlb/scoreboard/?date={date}"
                print(f"URL 접속 시도: {url}")
                try:
                    response = requests.get(url, headers=self.headers)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    games = soup.select('li.js-stream-content')
                    print(f"경기 수: {len(games)}")
                    for game in games:
                        try:
                            teams = game.select('span.Fw\(600\)')
                            scores = game.select('div.D\(f\).Jc\(c\).Ai\(c\) span')
                            if len(teams) == 2 and len(scores) == 2:
                                away_team = teams[0].text.strip()
                                home_team = teams[1].text.strip()
                                away_score = scores[0].text.strip()
                                home_score = scores[1].text.strip()
                                result = {
                                    'date': date.replace('-', ''),
                                    'league': 'MLB',
                                    'home_team': home_team,
                                    'away_team': away_team,
                                    'home_score': home_score,
                                    'away_score': away_score
                                }
                                results.append(result)
                                print(f"경기 결과 추가: {away_team} {away_score} - {home_score} {home_team}")
                        except Exception as e:
                            print(f"경기 데이터 추출 중 오류: {str(e)}")
                            continue
                except Exception as e:
                    print(f"페이지 로딩 중 오류 ({date}): {str(e)}")
                    continue
        except Exception as e:
            print(f"MLB 결과 수집 중 오류: {str(e)}")
        print(f"MLB 경기 결과 수집 완료. 총 {len(results)}개의 경기 결과 수집됨.")
        return results

    def get_kbl_results(self):
        print("KBL 경기 결과 수집 시작...")
        results = []
        
        try:
            for i in range(7):
                date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                print(f"날짜 {date} 처리 중...")
                
                url = f"https://www.kbl.or.kr/schedule/result"
                print(f"URL 접속 시도: {url}")
                
                try:
                    self.driver.get(url)
                    time.sleep(10)  # 페이지 로딩 대기
                    print("페이지 로딩 완료")
                    
                    # 날짜 선택
                    date_input = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input#searchDate"))
                    )
                    date_input.clear()
                    date_input.send_keys(date)
                    
                    # 검색 버튼 클릭
                    search_button = self.wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn_search"))
                    )
                    search_button.click()
                    time.sleep(5)  # 검색 결과 로딩 대기
                    
                    # 경기 결과 요소 대기
                    games = self.wait.until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table.schedule_result tbody tr"))
                    )
                    
                    print(f"경기 수: {len(games)}")
                    
                    for game in games:
                        try:
                            cols = game.find_elements(By.TAG_NAME, "td")
                            if len(cols) >= 4:
                                away_team = cols[1].text.strip()
                                home_team = cols[3].text.strip()
                                away_score = cols[2].text.strip()
                                home_score = cols[4].text.strip()
                                
                                result = {
                                    'date': date.replace('-', ''),
                                    'league': 'KBL',
                                    'home_team': home_team,
                                    'away_team': away_team,
                                    'home_score': home_score,
                                    'away_score': away_score
                                }
                                results.append(result)
                                print(f"경기 결과 추가: {away_team} {away_score} - {home_score} {home_team}")
                        except Exception as e:
                            print(f"경기 데이터 추출 중 오류: {str(e)}")
                            continue
                    
                    time.sleep(2)  # 다음 날짜로 넘어가기 전 대기
                
                except Exception as e:
                    print(f"페이지 로딩 중 오류 ({date}): {str(e)}")
                    continue
                
        except Exception as e:
            print(f"KBL 결과 수집 중 오류: {str(e)}")
        
        print(f"KBL 경기 결과 수집 완료. 총 {len(results)}개의 경기 결과 수집됨.")
        return results

    def get_nba_results(self):
        print("NBA 경기 결과 수집 시작 (Yahoo Sports)...")
        results = []
        try:
            for i in range(7):
                date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                print(f"날짜 {date} 처리 중...")
                url = f"https://sports.yahoo.com/nba/scoreboard/?date={date}"
                print(f"URL 접속 시도: {url}")
                try:
                    response = requests.get(url, headers=self.headers)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    games = soup.select('li.js-stream-content')
                    print(f"경기 수: {len(games)}")
                    for game in games:
                        try:
                            teams = game.select('span.Fw\(600\)')
                            scores = game.select('div.D\(f\).Jc\(c\).Ai\(c\) span')
                            if len(teams) == 2 and len(scores) == 2:
                                away_team = teams[0].text.strip()
                                home_team = teams[1].text.strip()
                                away_score = scores[0].text.strip()
                                home_score = scores[1].text.strip()
                                result = {
                                    'date': date.replace('-', ''),
                                    'league': 'NBA',
                                    'home_team': home_team,
                                    'away_team': away_team,
                                    'home_score': home_score,
                                    'away_score': away_score
                                }
                                results.append(result)
                                print(f"경기 결과 추가: {away_team} {away_score} - {home_score} {home_team}")
                        except Exception as e:
                            print(f"경기 데이터 추출 중 오류: {str(e)}")
                            continue
                except Exception as e:
                    print(f"페이지 로딩 중 오류 ({date}): {str(e)}")
                    continue
        except Exception as e:
            print(f"NBA 결과 수집 중 오류: {str(e)}")
        print(f"NBA 경기 결과 수집 완료. 총 {len(results)}개의 경기 결과 수집됨.")
        return results

    def collect_all_data(self):
        try:
            # 뉴스 수집
            kbo_news = self.get_kbo_news()
            mlb_news = self.get_mlb_news()
            kbl_news = self.get_kbl_news()
            nba_news = self.get_nba_news()

            # 순위 수집
            kbo_standings = self.get_kbo_standings()
            mlb_standings = self.get_mlb_standings()
            kbl_standings = self.get_kbl_standings()
            nba_standings = self.get_nba_standings()

            # 경기 결과 수집
            kbo_results = self.get_kbo_results()
            mlb_results = self.get_mlb_results()
            kbl_results = self.get_kbl_results()
            nba_results = self.get_nba_results()

            # 데이터 저장
            data = {
                'news': {
                    'KBO': kbo_news,
                    'MLB': mlb_news,
                    'KBL': kbl_news,
                    'NBA': nba_news
                },
                'standings': {
                    'KBO': kbo_standings,
                    'MLB': mlb_standings,
                    'KBL': kbl_standings,
                    'NBA': nba_standings
                },
                'results': {
                    'KBO': kbo_results,
                    'MLB': mlb_results,
                    'KBL': kbl_results,
                    'NBA': nba_results
                }
            }

            # JSON 파일로 저장
            with open('sports_data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

            # CSV 파일로도 저장
            all_news = []
            for league in ['KBO', 'MLB', 'KBL', 'NBA']:
                for news in data['news'][league]:
                    all_news.append(news)
            
            pd.DataFrame(all_news).to_csv('sports_news.csv', index=False, encoding='utf-8-sig')

            # 경기 결과를 CSV로 저장
            all_results = []
            for league in ['KBO', 'MLB', 'KBL', 'NBA']:
                for result in data['results'][league]:
                    all_results.append(result)
            
            pd.DataFrame(all_results).to_csv('sports_results.csv', index=False, encoding='utf-8-sig')
            
        except Exception as e:
            print(f"데이터 수집 중 오류 발생: {str(e)}")
        finally:
            if hasattr(self, 'driver'):
                try:
                    self.driver.quit()
                except:
                    pass

if __name__ == "__main__":
    collector = SportsCollector()
    collector.collect_all_data()
    print("스포츠 뉴스, 순위, 경기 결과 데이터가 성공적으로 수집되었습니다.") 
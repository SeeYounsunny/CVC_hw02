from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import requests
import pandas as pd
import json
from datetime import datetime
from bs4 import BeautifulSoup
import time

class StandingsCollector:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(service=Service('chromedriver-mac-arm64/chromedriver'), options=chrome_options)

    def is_valid_team_name(self, name):
        if not name:
            return False
        if name.isdigit():
            return False
        if len(name) < 2:
            return False
        if name.upper() in ['W', 'L', 'PCT', 'GB', 'HOME', 'AWAY', 'RS', 'RA', 'DIV', 'CONF', 'PF', 'PA', 'STRK', 'STREAK', 'WIN', 'LOSS', 'WIN%', 'GB', 'LAST 10']:
            return False
        return True

    def collect_kbo_standings(self):
        try:
            url = 'https://www.koreabaseball.com/Record/TeamRank/TeamRankDaily.aspx'
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            standings = []
            rows = soup.select('table.tData01 tbody tr')
            for row in rows:
                cols = row.select('td')
                if len(cols) >= 8:
                    team_data = {
                        'rank': cols[0].text.strip(),
                        'team': cols[1].text.strip(),
                        'games': cols[2].text.strip(),
                        'wins': cols[3].text.strip(),
                        'losses': cols[4].text.strip(),
                        'draws': cols[5].text.strip(),
                        'win_rate': cols[6].text.strip(),
                        'games_behind': cols[7].text.strip()
                    }
                    standings.append(team_data)
            return standings
        except Exception as e:
            print(f"KBO standings collection error: {str(e)}")
            return []

    def collect_kbl_standings(self):
        try:
            url = 'https://www.kbl.or.kr/record/team_standing.asp'
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            standings = []
            rows = soup.select('table.tbl_01 tbody tr')
            for row in rows:
                cols = row.select('td')
                if len(cols) >= 8:
                    team_data = {
                        'rank': cols[0].text.strip(),
                        'team': cols[1].text.strip(),
                        'games': cols[2].text.strip(),
                        'wins': cols[3].text.strip(),
                        'losses': cols[4].text.strip(),
                        'win_rate': cols[5].text.strip(),
                        'games_behind': cols[6].text.strip(),
                        'streak': cols[7].text.strip()
                    }
                    standings.append(team_data)
            return standings
        except Exception as e:
            print(f"KBL standings collection error: {str(e)}")
            return []

    def collect_mlb_standings(self):
        try:
            self.driver.get('https://www.espn.com/mlb/standings')
            time.sleep(5)  # Increased wait time for page load
            
            # Save page source for debugging
            with open('mlb_standings.html', 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            
            standings = []
            # Find all division tables
            tables = self.driver.find_elements(By.CSS_SELECTOR, 'div.Table__Scroller table.Table')
            
            for table in tables:
                rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')
                for row in rows:
                    try:
                        cols = row.find_elements(By.TAG_NAME, 'td')
                        if len(cols) >= 8:
                            team_cell = cols[1]
                            # Try different methods to get team name
                            team_name = None
                            
                            # Method 1: Check for span with hide-mobile class
                            spans = team_cell.find_elements(By.CSS_SELECTOR, 'span.hide-mobile')
                            if spans:
                                team_name = spans[0].text.strip()
                            
                            # Method 2: Check for anchor tag
                            if not team_name:
                                anchors = team_cell.find_elements(By.TAG_NAME, 'a')
                                if anchors:
                                    team_name = anchors[0].text.strip()
                            
                            # Method 3: Get direct text
                            if not team_name:
                                team_name = team_cell.text.strip()
                            
                            if not self.is_valid_team_name(team_name):
                                continue
                                
                            team_data = {
                                'rank': cols[0].text.strip(),
                                'team': team_name,
                                'wins': cols[2].text.strip(),
                                'losses': cols[3].text.strip(),
                                'win_rate': cols[4].text.strip(),
                                'games_behind': cols[5].text.strip(),
                                'last_10': cols[6].text.strip(),
                                'streak': cols[7].text.strip()
                            }
                            standings.append(team_data)
                            print(f"Added team: {team_name}")
                    except Exception as e:
                        print(f"Error processing row: {str(e)}")
                        continue
            
            print(f"Total teams found: {len(standings)}")
            return standings
            
        except Exception as e:
            print(f"MLB standings collection error: {str(e)}")
            return []

    def collect_nba_standings(self):
        try:
            self.driver.get('https://www.espn.com/nba/standings')
            time.sleep(3)
            standings = []
            tables = self.driver.find_elements(By.CSS_SELECTOR, 'table.Table')
            for table in tables:
                rows = table.find_elements(By.CSS_SELECTOR, 'tbody tr')
                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, 'td')
                    if len(cols) >= 8:
                        team_cell = cols[1]
                        span = team_cell.find_elements(By.CSS_SELECTOR, 'span.hide-mobile')
                        if span:
                            team_name = span[0].text.strip()
                        elif team_cell.find_elements(By.TAG_NAME, 'a'):
                            team_name = team_cell.find_elements(By.TAG_NAME, 'a')[0].text.strip()
                        else:
                            team_name = team_cell.text.strip()
                        if not self.is_valid_team_name(team_name):
                            continue
                        team_data = {
                            'rank': cols[0].text.strip(),
                            'team': team_name,
                            'wins': cols[2].text.strip(),
                            'losses': cols[3].text.strip(),
                            'win_rate': cols[4].text.strip(),
                            'games_behind': cols[5].text.strip(),
                            'last_10': cols[6].text.strip(),
                            'streak': cols[7].text.strip()
                        }
                        standings.append(team_data)
            return standings
        except Exception as e:
            print(f"NBA standings collection error: {str(e)}")
            return []

    def collect_all_standings(self):
        standings_data = {
            'kbo': self.collect_kbo_standings(),
            'mlb': self.collect_mlb_standings(),
            'kbl': self.collect_kbl_standings(),
            'nba': self.collect_nba_standings(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        # Save to JSON
        with open('standings_data.json', 'w', encoding='utf-8') as f:
            json.dump(standings_data, f, ensure_ascii=False, indent=2)
        # Save to CSV for each league
        for league in ['kbo', 'mlb', 'kbl', 'nba']:
            if standings_data[league]:
                df = pd.DataFrame(standings_data[league])
                df.to_csv(f'{league}_standings.csv', index=False, encoding='utf-8-sig')
        return standings_data

    def close(self):
        self.driver.quit()

if __name__ == "__main__":
    collector = StandingsCollector()
    try:
        standings = collector.collect_all_standings()
        print("Standings data collection completed successfully!")
    except Exception as e:
        print(f"Error during standings collection: {str(e)}")
    finally:
        collector.close() 
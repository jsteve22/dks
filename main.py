from selenium import webdriver
from bs4 import BeautifulSoup
import time

def get_dk_html():
  # open browser driver and connect to website
  driver = webdriver.Firefox()
  driver.get('https://sportsbook.draftkings.com/leagues/basketball/nba')

  # sleep to load webpage... idk if it's necessary but I'll have it for now
  # for i in range(10):
  #   time.sleep(1)
  #   print(f'{i+1} seconds have passed')

  # get page source and close driver
  source = driver.page_source
  driver.close()

  return source

def main():

  # get draftkings webpage
  html = get_dk_html()

  soup = BeautifulSoup(html, 'lxml' )

  tables = soup.find_all('table', class_='sportsbook-table')
  
  print(len(tables))
  for t in tables:
    print(type(t))
    print(t.attrs)
  return


if __name__ == '__main__':
  main()
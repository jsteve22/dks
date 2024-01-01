from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import time
import os

def get_dk_html():
  # open browser driver and connect to website
  driver = webdriver.Firefox()
  driver.get('https://sportsbook.draftkings.com/leagues/basketball/nba')
  # driver.get('https://sportsbook.draftkings.com/leagues/football/nfl')

  # sleep to load webpage... idk if it's necessary but I'll have it for now
  # for i in range(10):
  #   time.sleep(1)
  #   print(f'{i+1} seconds have passed')
  time.sleep(1)

  # get page source and close driver
  source = driver.page_source
  driver.close()

  return source

def get_date(date_elem):
  # date_soup = BeautifulSoup(str(date_elem), 'lxml')
  # inner = date_soup.select('div.sportsbook-table-header__title')
  inner = date_elem.select('div.sportsbook-table-header__title')

  if len(inner) == 0:
    return ''

  inner = inner[0]

  date = inner.findChildren()[-1].string

  if date.lower() == 'today':
    return f'{datetime.date.today()}'
  elif date.lower() == 'tomorrow':
    return f'{datetime.date.today() + datetime.timedelta(days=1)}'

  return date

def get_team_odds(team_elem):
  team = get_team(team_elem)
  spread, spread_odds = get_spread(team_elem)
  over_under, over_under_odds = get_over_under(team_elem)
  moneyline_odds = get_moneyline(team_elem)

  return (team, spread, spread_odds, over_under, over_under_odds, moneyline_odds)

def get_team(team_elem):
  name = team_elem.select('div.event-cell__name-text')[0].string
  return name

def get_spread(team_elem):
  spread = team_elem.select('span.sportsbook-outcome-cell__line')[0].string
  spread_odds = team_elem.select('span.sportsbook-odds.american.default-color')[0].string

  return (spread, spread_odds)

def get_over_under(team_elem):
  over_under = team_elem.select('span.sportsbook-outcome-cell__line')[1].string
  over_under_odds = team_elem.select('span.sportsbook-odds.american.default-color')[1].string

  return (over_under, over_under_odds)

def get_moneyline(team_elem):
  moneyline_odds = team_elem.select('span.sportsbook-odds.american.default-color')[2].string

  return moneyline_odds

def construct_line(game, date, name, spread, spread_odds, over_under, over_under_odds, moneyline_odds):
  return f'{game}, {date}, {name}, {spread}, {spread_odds}, {over_under}, {over_under_odds}, {moneyline_odds}'

def get_game(team_elems):
  team_a, team_b = team_elems

  team_odds_a = get_team_odds(team_a)
  team_odds_b = get_team_odds(team_b)

  name_a, spread_a, spread_odds_a, over_under_a, over_under_odds_a, moneyline_odds_a = team_odds_a
  name_b, spread_b, spread_odds_b, over_under_b, over_under_odds_b, moneyline_odds_b = team_odds_b

  game = f'{name_a} at {name_b}'

  return game, team_odds_a, team_odds_b

def read_table(table_elem):

  # extract the rows from the table elements
  # table_soup = BeautifulSoup(str(table_elem), 'lxml')
  # rows = table_soup.select('tr')
  rows = table_elem.select('tr')


  # first row gives the date and rest give the games
  date_elem = rows[0]
  games = rows[1:]

  date = get_date(date_elem)

  for i in range(0, len(games), 2):
    game, team_odds_a, team_odds_b = get_game(games[i:i+2])

    name_a, spread_a, spread_odds_a, over_under_a, over_under_odds_a, moneyline_odds_a = team_odds_a
    name_b, spread_b, spread_odds_b, over_under_b, over_under_odds_b, moneyline_odds_b = team_odds_b

    line_a = construct_line(game, date, name_a, spread_a, spread_odds_a, over_under_a, over_under_odds_a, moneyline_odds_a)
    line_b = construct_line(game, date, name_b, spread_b, spread_odds_b, over_under_b, over_under_odds_b, moneyline_odds_b)
    print(line_a)
    print(line_b)

  return

def main():
  # add test data to speed up extracting sports table data
  path = './test.tmp'

  # get draftkings webpage
  if os.path.isfile(path):
    with open(path, 'rb') as f:
      html_bytes = f.read()
      html = html_bytes.decode('utf-8')
  else:
    html = get_dk_html()
    with open(path, 'wb') as f:
      f.write(bytes(f'{html}','utf-8'))

  soup = BeautifulSoup(html, 'lxml' )

  tables = soup.select('table.sportsbook-table')
  
  for t in tables:
    read_table(t)
    print()

  return


if __name__ == '__main__':
  main()
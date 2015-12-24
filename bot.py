from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pystockfish import *
import time

driver = None

def main():
  global driver
  driver = webdriver.Chrome()
  driver.get("http://www.chess.com")
  #assert "Python" in driver.title
  print "Please log in and start a game to continue..."  # login process - user input required
  while True:
    try:
      draw = driver.find_element_by_class_name("drawResignButtons")  # game start if draw/resign buttons exist
      break
    except NoSuchElementException:  # continuously check until draw/resign buttons are found
      time.sleep(5)
      aw = driver.window_handles
      if (len(aw)> 1):  # chess.com sometimes opens a new tab when playing live
        driver.switch_to_window(aw[1])
        print "Switched to latest window."
      continue
  print "Started game."
  play_game()

def play_game():
  turn_count = 0
  game_state = {}
  move_list = []
  player_color = 1  # 1:black 0:white
  ### color initialization ###
  color_element = driver.find_element_by_xpath("//a[contains(@id, '_player_name_')]")
  color = color_element.get_attribute("id")[:5] # color of the opponent
  if (color == "black"):
    player_color = 0
  ### game loop ###
  while True:  # TODO - replace true with endgame condition
    board_element = driver.find_element_by_xpath("//div[contains(@id, '_boardarea')]")
    squares_list = board_element.find_elements_by_tag_name("img")
    board = {}
    for square in squares_list[:-4]:
      coord = square.get_attribute("id")[-2:]
      board[coord] = square.get_attribute("src")[-5]
    if (len(game_state) == 0):
      game_state = board
    diff_set = set(board.items()) ^ set(game_state.items())  # compare game state and current board
    if (len(diff_set) != 0 or (turn_count + player_color == 0)): # move has been made, or first turn as white
      print diff_set
      if (turn_count % 2 == player_color):
        print ""
        # TODO - make move
      turn_count += 1
    game_state = board  # update gamestate

if __name__ == "__main__":
    main()
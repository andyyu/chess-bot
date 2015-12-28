from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pystockfish import *
import time

driver = None
engine_depth = 15
engine = Engine(depth=engine_depth)

def main():
  global driver
  driver = webdriver.Chrome()
  driver.get("http://www.chess.com")
  #assert "Python" in driver.title
  print "Please log in and start a game to continue..."  # login process - user input required
  while True:
    try:
      draw = driver.find_element_by_class_name("drawResignButtons")  # game start if draw/resign buttons exist
    except NoSuchElementException:  # continuously check until draw/resign buttons are found
      aw = driver.window_handles
      if (len(aw)> 1):  # chess.com sometimes opens a new tab when playing live
        driver.switch_to_window(aw[1])
        print "Switched to latest window."
      continue
    draw2 = driver.find_elements_by_class_name("drawResignButtons")  # find_elements doesn't return exception if NSE
    print len(draw2)
    print draw2[1].get_attribute("class")
    if (len(draw2) == 2 and draw2[1].get_attribute("class").find("hidden") == -1):
      break
    continue
  print "Started game."
  play_game()

def play_game():
  turn_count = 0
  game_state = {}
  move_list = []
  next_move = None
  player_color = 0  # 1:black 0:white
  ### color initialization ###
  board = driver.find_element_by_class_name("boardDummy")
  board_element_1 = board.find_element_by_class_name("bs")
  board_element_2 = board_element_1.find_element_by_class_name("boardBottomPlayer")
  color_element = board_element_2.find_element_by_xpath("//input[contains(@id, '_timer_dummy')]")
  color = color_element.get_attribute("id")[:5]
  if (color == "black"):
    player_color = 1
  ### game loop ###
  while True:  # TODO - replace true with endgame condition
    '''
    board_element = driver.find_element_by_xpath("//div[contains(@id, '_boardarea')]")
    squares_list = board_element.find_elements_by_tag_name("img")
    board = {}
    for square in squares_list[:-4]:
      coord = square.get_attribute("id")[-2:]
      board[coord] = square.get_attribute("src")[-5]
    if (len(game_state) == 0):
      game_state = board
    diff_set = set(board.items()) ^ set(game_state.items())  # compare game state and current board
    print board.keys()
    '''
    temp_move_list = []
    if (turn_count + player_color == 0): # first turn as white
      play_move(move_list)
    try:
      moves_element = driver.find_element_by_xpath("//div[contains(@id, 'notation_')]")
    except NoSuchElementException:
      continue   
    moves = moves_element.find_elements_by_class_name("notationVertical")
    for move in moves:
      blah = move.find_elements_by_xpath("//span[contains(@id, 'movelist_')]")
      for ble in blah:
        m = ble.find_element_by_tag_name("a").text  # move in chess notation e.g. "e4"
        if (m != ""):
          temp_move_list.append(str(m))
    if (len(temp_move_list) != len(move_list)):
      new_move = [m for m in temp_move_list if m not in move_list]
      move_list += new_move
      if (len(new_move) == 1): # move has been made
        if (turn_count % 2 != player_color):
          print move_list
          play_move(move_list)
          # TODO - make move
        turn_count += 1
    #game_state = board  # update gamestate

def play_move(state):
  engine.setposition(state)
  next_move = engine.bestmove()
  print "played move: %s" % (next_move)

if __name__ == "__main__":
    main()
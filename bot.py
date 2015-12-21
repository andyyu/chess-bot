from selenium import webdriver
from selenium.common.exceptions import *
from selenium.webdriver.common.keys import Keys
import time

def main():
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
  board = driver.find_element_by_id("chess_board")

if __name__ == "__main__":
    main()
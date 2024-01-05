from DashboardLogin import *
chooseClientElement=elementWait(driver,timeOut=50,byWhat="css selector", selector="#clientSelect_chosen") #waits for the search client textbox to appear for max 50 sec
  # asks for the client name to pass it the SelectClent.py
driver.minimize_window()
clientName=getClientName(driver)
driver.maximize_window()
clientSelect(driver,clientName)
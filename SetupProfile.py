#import packages , DO NOT DELETE ANY!!!!!! , they are used in all the other files
from  Methods import *




#directing chrome to my instashop profile

chrome_options = Options()
chrome_options.add_argument("--user-data-dir=C:\\Users\\Instashop\\AppData\\Local\\Google\\Chrome\\User Data\\")
chrome_options.add_argument("--profile-directory=Default")
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

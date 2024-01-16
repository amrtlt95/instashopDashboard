from SetupProfile import *
driver.get("") #open the dashboard
try: #handle the login screen if it appeared
    # try to find the element by its CSS selector
    element = WebDriverWait(driver,5).until(
        EC.invisibility_of_element((By.ID,"login"))
    )
    productsButton = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[8]/div[1]/div/div[2]/ul/li[2]/a")))
    productsButton.click()

except:
    print("Logged out\n")
    userName = driver.find_element(By.CSS_SELECTOR, "#login > form > div:nth-child(1) > div > input")
    password = driver.find_element(By.CSS_SELECTOR, "#login > form > div:nth-child(2) > div > input")
    loginButton = driver.find_element(By.CSS_SELECTOR, "#login > form > div.submit.text-right > button")
    userName.send_keys("")#your instashop email
    password.send_keys("")#your instashop password
    loginButton.click()
    element = WebDriverWait(driver, 5).until(
        EC.invisibility_of_element((By.ID, "login"))
    )
    productsButton = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[8]/div[1]/div/div[2]/ul/li[2]/a")))
    productsButton.click()

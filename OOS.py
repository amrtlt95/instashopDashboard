from SetupProfile import *
clientList=[
"Max Muscle - Miami",
"Choco Rico - Sporting",
"Imtenan - Miami",
"AbuAuf - Miami ",
"Medi Deli - Louran",
"Centro Market - Saba Basha",
"Khan El Hussein Market - Kafr Abdo",
"Balbaa Pharmacy - Moharam Bek",
"Balbaa Pharmacy - Agamy",
"Mahfouz Pharmacy - Smouha",
"White Coats Pharmacy - Moharram Bek",
"Azar Pharmacy - Kafr Abdo",
"Pet Yard - Sidi Gaber",
"Ayman's Pets - Sporting",
"Pets Awy - Sporting",
"Zahran Market - El Alamain",
"Aswak El Karam - Kafr Abdo",
"Spinneys - Smouha",
"Needs Market - Pyramids Gardens",
"Bassem Market - Marbella Village",
"King Market - Janaklees",
"King Market - Miami",
"Zad Market - Ibrahimia",
"Beit ElGomla - Manshia",
"Hamada Market - Camp Cesar",
]
loginDashBoard(driver)
oosFilters(driver)  # this will click on all filters for checking OOS
flag = False
for client in clientList:
    chooseClientElement = elementWait(driver, timeOut=50, byWhat="css selector",
                                      selector="#clientSelect_chosen")  # waits for the search client textbox to appear for max 50 sec
    # asks for the client name to pass it the SelectClent.py
    #driver.find_element(By.CSS_SELECTOR, "#clientSelect_chosen > a").click()

    clientNameBox = driver.find_element(By.XPATH, 'id("clientSelect_chosen")/A[1]/SPAN[1]')
    clientNameBox.click()
    if flag:
        clientNameBox.click()
        flag = False
    clientNameTextBox =  driver.find_element(By.XPATH, 'id("clientSelect_chosen")/DIV[1]/DIV[1]/INPUT[1]')#id("clientSelect_chosen")/DIV[1]/DIV[1]/INPUT[1]
    clientNameTextBox.send_keys(client)
    try:
        WebDriverWait(driver, timeout=1).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "no-results"))
        )
        print("Wrong Client Name , please try again")
        clientNameTextBox.clear()
        driver.find_element(By.CSS_SELECTOR, "#clientSelect_chosen > a").click()
        continue
    except:
        clientNameTextBox.send_keys(Keys.RETURN)
    waitForLoading(driver)
    enabledProducts = driver.find_elements(By.CLASS_NAME, "proditem-mob")
    while len(enabledProducts)!=0:
        flag = True
        for product in enabledProducts:
            try:
                disableOrEnableButton=product.find_element(By.CLASS_NAME,"active")
                disableOrEnableButton.click()
            except:
                hi=""

        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(3)
        searchProducts = WebDriverWait(driver,1).until(
            EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div[9]/div[145]/div[6]/div[1]/div/div[2]/button"))
        )
        searchProducts.click()
        waitForLoading(driver)
        try:
            enabledProducts = driver.find_elements(By.CLASS_NAME, "proditem-mob")
        except:
            break
        #driver.find_element(By.CSS_SELECTOR,"#page-wrapper > div:nth-child(2) > div > button:nth-child(3)")




        continue


import time

from GettingReady import *

idsString=input("Enter the Ids from the sheet:\n")
idsList=idsString.split(",")
allPLUsList=[]
enabledOrDisabledList=[]
allBarcodes=[]
searchTextBox=returnProductsSearchTextBox(driver)
try:
    for id_ in idsList:
        searchTextBox.send_keys(id_)
        searchTextBox.send_keys(Keys.ENTER)
        waitForLoading(driver)
        waitForFakeLoading(driver)
        time.sleep(2)
        hasPLU = checkIfItemHasApprovedPlu(driver)
        returnBarcodeAndPLUBoxButton(driver).click()
        waitForFakeLoading(driver)
        WebDriverWait(driver,60).until(
            EC.visibility_of_element_located((By.XPATH,"/html/body/div[1]/div[9]/div[113]/div/div/div/div/div[2]"))
        )
        Barcodes = driver.find_elements(By.XPATH,'/html/body/div[1]/div[9]/div[113]/div/div/div/div/div[2]//input[@placeholder="barcode"]')
        PLUs = driver.find_elements(By.XPATH,'/html/body/div[1]/div[9]/div[113]/div/div/div/div/div[2]//input[@placeholder="Plu"]')
        innerPLUs = ""
        innerBarcodes = ""
        flag = True

        if not hasPLU:
            flag = False
            allPLUsList.append("No PLUs")

        if flag:

            for PLU in PLUs:

                innerPLUs += PLU.get_attribute("value")+" , "

            allPLUsList.append(innerPLUs[:-2])

        flag = True

        for barcode in Barcodes:
            if barcode.get_attribute("value") == "":
                allBarcodes.append("No Barcode")
                flag = False
                break
            innerBarcodes += barcode.get_attribute("value")+" , "
        if flag:
            allBarcodes.append(innerBarcodes[:-2])
        driver.find_element(By.XPATH,"/html/body/div[1]/div[9]/div[113]/div/div/div/div/div[4]/button[1]").click()
        WebDriverWait(driver,60).until(
            EC.invisibility_of_element_located((By.XPATH,"/html/body/div[1]/div[9]/div[113]/div/div/div/div/div[2]"))
        )


        time.sleep(1)
        if checkIfItemIsEnabled(driver):
            enabledOrDisabledList.append("Enabled")
        else:
            enabledOrDisabledList.append("Disabled")
        searchTextBox.clear()
        continue
        # exit from the plu and wait for loading please
except:
    print("crashed")
    print("last id ",idsList[len(allPLUsList)-1])
file_list = [idsList, allPLUsList,allBarcodes,enabledOrDisabledList]
exported = zip_longest(*file_list)
with open("C:\\Users\\Instashop\\Desktop\\"+clientName+" PLUs.csv", "w", encoding="utf-8", newline="") as myfile:
    wr = csv.writer(myfile)
    wr.writerow(["ID", "PLUs","Barcodes","Status"])
    wr.writerows(exported)
print(allPLUsList)






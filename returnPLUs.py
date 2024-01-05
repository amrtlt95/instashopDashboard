
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
        productsSearchButton(driver).click()
        waitForLoading(driver)
        waitForFakeLoading(driver)
        time.sleep(2)
        if checkIfItemHasApprovedPlu(driver):

            infoButton = returnElementInfoButton(driver)
            actions = ActionChains(driver)
            actions.move_to_element(infoButton)
            actions.click(infoButton)
            actions.perform()
            # try:
            #     returnElementInfoButton(driver).click()
            # except:
            #     productsSearchButton(driver).click()
            #     waitForLoading(driver)
            #     waitForFakeLoading(driver)
            #     returnElementInfoButton(driver).click()
            WebDriverWait(driver,10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR,".modal-body > div > .ng-not-empty > md-radio-button"))
            )
            returnPluFromInfoBulletButton(driver).click()
            time.sleep(1)
            returnNextButtonInInfo(driver).click()
            waitForFakeLoading(driver)
            waitForProgressBarInInfo(driver)
            time.sleep(1)
            PLUs = returnApprovedPLUOrBarCodes(driver)
            innerPLUs = ""
            for PLU in PLUs:

                innerPLUs+=PLU.text+" , "

            allPLUsList.append(innerPLUs[:-2])
            returnBackButtonInInfoMenu(driver).click()
            WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, ".modal-body > div > .ng-not-empty > md-radio-button"))
            )
            returnBarcodesFromInfoBulletButton(driver).click()
            time.sleep(1)
            returnNextButtonInInfo(driver).click()
            waitForFakeLoading(driver)
            waitForProgressBarInInfo(driver)
            time.sleep(1)
            Barcodes=returnApprovedPLUOrBarCodes(driver)
            innerBarcodes = ""
            if(not Barcodes):
                allBarcodes.append("Unable to obtain Barcodes")
            else:
                flag = True
                for Barcode in Barcodes:
                    if(Barcode.text == "All barcodes removed"):
                        allBarcodes.append("No Barcode")
                        flag = False

                    else:
                        innerBarcodes += Barcode.text + " , "
                if flag:
                    allBarcodes.append(innerBarcodes[:-2])





        else:
            allPLUsList.append("")
        returnCloseButtonInPluSectionInInfoMenu(driver).click()
        WebDriverWait(driver,10).until(
            EC.invisibility_of_element_located((By.XPATH,"/html/body/div[1]/div[9]/div[13]"))
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






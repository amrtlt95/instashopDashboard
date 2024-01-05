
from GettingReady import *


def getRefreshedPageSourceForBeautifulSoup(driver):
    page_source = driver.page_source
    return BeautifulSoup(page_source, 'lxml')

def clickEnglishTitlesElement(driver):

    driver.find_element(By.XPATH,"/html/body/div[1]/div[8]/div[145]/div[5]/div/div[1]/ul/li[1]/a").click()
    time.sleep(2)



def getAllEnglishTitles(driver,soapObject):
    return soapObject.findAll("h5",{"ng-if":"!selectedProductLanguage || selectedProductLanguage === 'en'"})



def getAllIDS(driver,soapObject):

    return soapObject.findAll("div",{"style":"margin-top:3px;","class":"no-view-only"})

def getAllTags(driver):
    global soapObject


    return soapObject.findAll("div",{"style":"min-height: 63px!important; height: 65px!important; overflow-y: scroll!important;"\
        ,"ng-class":"{'view-only': loggedInUser.extraPermissions.productsPageViewOnly === true}",\
                                     "class":"productTagContainer no-view-only"})
    #div_elements = [tag.div for tag in tag_elements]

    #return div_elements

def getAllQuantities(driver,soapObject):
    return soapObject.findAll("div",{"style":"display: inline-block;font-size:12px;","class":"packaging"})


def getAllTagsInATagBlock(CurrentTagBlock):



    allItemTagsWithStar="*"
    try:
        allTagsInAblock = CurrentTagBlock.findAll("div")
    except:
        allTagsInAblock = ""
        return allTagsInAblock

    for j in range(len(allTagsInAblock)):
        allItemTagsWithStar += allTagsInAblock[j].text+"*"
    clickEnglishTitlesElement(driver)
    return allItemTagsWithStar


xpathOfElementsToBeRemoved=[
    "/html/body/div[1]/div[8]",
    "/html/body/div[1]/div[9]/div[146]/div[3]",
    "/html/body/div[1]/div[9]/div[146]/div[3]/div[2]",
    "/html/body/div[1]/div[9]/div[146]/div[3]/div[3]",
    "/html/body/div[1]/div[9]/div[146]/div[4]/div[3]",
    "/html/body/div[1]/div[9]/div[146]/div[4]/div[4]",
    "/html/body/div[1]/div[9]/div[146]/div[4]/div[5]",
    "/html/body/div[1]/div[9]/div[146]/div[4]/div[6]",
    "/html/body/div[1]/div[9]/div[143]",
    "/html/body/div[1]/div[9]/div[146]/div[5]",
    "/html/body/div[1]/div[9]/div[146]/div[6]/div[1]/div/div[3]/div/div",
    "/html/body/div[1]/div[9]/div[146]/div[6]/div[1]/div/div[4]/button",
    "/html/body/div[1]/div[9]/div[146]/div[6]/div[3]/div/div",
    "/html/body/div[1]/div[9]/div[146]/div[7]/div[1]",
    "/html/body/div[1]/div[9]/div[146]/div[7]/div[2]/div[1]",
    "/html/body/div[1]/div[9]/div[146]/div[7]/div[2]/div[2]/ul/li[3]/a",
    "/html/body/div[1]/div[9]/div[146]/div[7]/div[2]/div[2]/ul/li[4]/a",
    "/html/body/div[1]/div[9]/div[146]/div[7]/div[2]/div[2]/ul/li[5]/a"
]

webDriverArray = []

ID=[]
eng_Title=[]
englishTags=[]
quantities=[]

# ID title local title  tagsWith* packagingString
#the english titles
eodFilter(driver)
hasWapClick(driver)
waitForLoading(driver)


for xpath in xpathOfElementsToBeRemoved:
    webDriverArray.append(driver.find_element(By.XPATH, xpath))

for singleElement in webDriverArray:
    try:
        # Find the element using XPath
        driver.execute_script("arguments[0].remove();", singleElement)


        print(f"Element removed: {singleElement}")
    except NoSuchElementException as e:
        print(f"Element not found: {singleElement}")
    except Exception as e:
        print(f"Error during removal: {e}")
time.sleep(20)
#looping
try:
    while(True):
    #Elements
        soapObject = getRefreshedPageSourceForBeautifulSoup(driver)
        all_IDS = getAllIDS(driver,soapObject)

        all_Eng_Titles= getAllEnglishTitles(driver,soapObject)

        all_En_Tags = getAllTags(driver)



        all_quantities = getAllQuantities(driver,soapObject)

        clickEnglishTitlesElement(driver)

        for i in range(len(all_IDS)):
            ID.append(all_IDS[i].text.replace("ID: ",""))

            eng_Title.append(all_Eng_Titles[i].text)


            englishTags.append(getAllTagsInATagBlock(all_En_Tags[i]))


            quantities.append(all_quantities[i].text.replace("multiplier x ",""))
        time.sleep(2)
        nextButton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[8]/div[145]/div[6]/div/button[2]"))
        )
        nextButton.click()
        waitForLoading(driver)
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)


except:
    print("Maximum pages reached")

    file_list=[ID,eng_Title,englishTags,quantities]
    exported = zip_longest(*file_list)
    with open("C:\\Users\\Instashop\\Desktop\\test.csv","w",encoding="utf-8",newline="") as myfile:
        wr = csv.writer(myfile)
        wr.writerow(["ID","Title","English Tags","Quantity"])
        wr.writerows(exported)


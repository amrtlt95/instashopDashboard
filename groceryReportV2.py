import time
from GettingReady import *

# check outer
#check searchOnly
#loop inside each catArray
#check scanned item
def deleteSearch(driver):
    productsSearchTextBox = returnProductsSearchTextBox(driver)


    actions = ActionChains(driver)

    actions.move_to_element(productsSearchTextBox)
    # Perform the action
    actions.perform()
    productsSearchTextBox.clear()

def searchProduct(driver,product):
    productsSearchTextBox = returnProductsSearchTextBox(driver)

    deleteSearch(driver)

    productsSearchTextBox.send_keys(product)
    productsSearchTextBox.send_keys(Keys.ENTER)
    waitForLoading(driver)


def chooseCorrectDate():
    global dateAnswer
    global formattedDate

    if dateAnswer == 'y' or dateAnswer == "":
        return formattedDate
    else:
        return dateAnswer

def dateDashboardStyleConverter(date):
    # Convert the input string to a datetime object
    if isinstance(date, list):
        return date

    date_object = datetime.strptime(date, "%d/%m/%Y")

    # Format the date as "Month Day, Year"
    correctFormattedDate = date_object.strftime("%b %d, %Y")
    return correctFormattedDate

def isScanned(driver):
    global alexPeople

    multiDays=False
    correctDate = dateDashboardStyleConverter(chooseCorrectDate())

    if isinstance(correctDate,list):
        firstDate =  dateDashboardStyleConverter(correctDate[0])
        firstDate = firstDate.replace(" 0"," ")
        firstDateConverted = date_object = datetime.strptime(firstDate, "%b %d, %Y")

        lastDate = dateDashboardStyleConverter(correctDate[1])
        lastDate = lastDate.replace(" 0"," ")
        lastDateConverted = date_object = datetime.strptime(lastDate, "%b %d, %Y")
        multiDays=True


        #createing lists of dates , values , and members
        allDashboardDates = driver.find_elements(By.CSS_SELECTOR,".table:nth-child(1) > tbody > tr .centered:nth-child(3) > span")
        allDashboardValues = driver.find_elements(By.CSS_SELECTOR,".table:nth-child(1) > tbody > tr strong")#start from fourth element
        allDashboardPeople = driver.find_elements(By.CSS_SELECTOR,".table:nth-child(1) > tbody > tr .centered > div")
        scannedValue="Enabled, In stock"

        #creating the for loop to check scanned or not
        for i in range(len(allDashboardDates)):

            dateCell = allDashboardDates[i].text
            dateCell = dateCell[:dateCell.find(" ",8)]#allDashboardDates[i].text.
            dateCellConverted = date_object = datetime.strptime(dateCell, "%b %d, %Y")

            stateCell = allDashboardValues[i+3].text
            personCell = allDashboardPeople[i].text
            if multiDays:
                if not allDashboardDates:
                    return False
                if firstDateConverted<=dateCellConverted <= lastDateConverted and\
                    stateCell == scannedValue and personCell in alexPeople:
                    return True
            else:
                if not allDashboardDates:
                    if dateCellConverted == correctDate and\
                        stateCell == scannedValue and \
                            personCell in alexPeople:
                        return True

        return False


def isOuter(productQuantity):
     if productQuantity.text.split(" ")[0].isdigit():
         return int(productQuantity.text.split(" ")[0]) >= 6
     return False

def loopProducts(driver,special=""):
    allProducts=driver.find_elements(By.CSS_SELECTOR,"div#allProducts > div div.admin-product")
    allMultiplierQuantities = driver.find_elements(By.CSS_SELECTOR,"div#allProducts > div .col-md-6 .editable:nth-child(1)")
    allInfoButton = driver.find_elements(By.CSS_SELECTOR,"div#allProducts > div div.solidonhover")
    allProductsTypes = driver.find_elements(By.CSS_SELECTOR,"div#allProducts > div .subcateg > span")

    #testing
    #print(len(allProducts) , "Enabled Products")
    for i in range(len(allInfoButton)):
        #print("Product number ",i)
        if (special=="Outers" and not isOuter(allMultiplierQuantities[i])) \
                or(special == "Normal Diapers" and not checkIfItemIsNormalBabyDiapers(allProductsTypes[i])) \
                or(special == "Golden" and not checkIfItemIsGoldenRice(allProductsTypes[i])):
                 # this checks if the current item is not outer , normal diapers or golden rice
            continue
        try:
            WebDriverWait(driver,3).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR,"div#allProducts > div div.solidonhover"))
            )
        except:
            return False

        action_chains = ActionChains(driver)

        action_chains.move_to_element(allInfoButton[i]).perform()
        time.sleep(0.5)

        action_chains.click(allInfoButton[i]).perform()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, ".modal-body > div > .ng-not-empty > md-radio-button"))
        )



        statusButton = driver.find_element(By.XPATH,"/html/body/div[1]/div[9]/div[13]/div/div/div/div/div[2]/div/md-radio-group/md-radio-button[15]")
        nextInfoButton = driver.find_element(By.XPATH,"/html/body/div[1]/div[9]/div[13]/div/div/div/div/div[3]/button[2]")

        statusButton.click()
        nextInfoButton.click()
        waitForLoading(driver)
        waitForFakeLoading(driver)
        waitForProgressBarInInfo(driver)
        closeButton = WebDriverWait(driver,60).until(
            EC.element_to_be_clickable((By.XPATH,"html/body/div[1]/div[9]/div[13]/div/div/div/div/div[3]/button[2]"))
        )
        waitForLoading(driver)
        waitForFakeLoading(driver)
        WebDriverWait(driver,3).until(
            EC.visibility_of_element_located((By.XPATH,"/html/body/div[1]/div[9]/div[13]/div/div/div/div/div[2]"))
        )
        if not isScanned(driver):


            closeButton.click()
            WebDriverWait(driver,120).until(
                EC.invisibility_of_element((By.XPATH,"/html/body/div[1]/div[9]/div[13]/div/div/div/div"))
            )
            continue

        else:
            closeButton.click()
            WebDriverWait(driver, 120).until(
                EC.invisibility_of_element((By.XPATH, "/html/body/div[1]/div[9]/div[13]/div/div/div/div"))
            )
            return True
    try:
        nextDashboardPageButton = WebDriverWait(driver,5).until(
            EC.element_to_be_clickable(By.XPATH,"/html/body/div[1]/div[9]/div[145]/div[8]/div/button[2]")
        )

        if nextDashboardPageButton:
            nextDashboardPageButton.click()
            waitForLoading(driver)
            loopProducts(driver,special)
    except Exception as e:
        return False

def isItemInSub(item):
    global  catAndSub
    for i in range(len(catAndSub)):
        if catAndSub[i].text == item:
            return True
    return False

def checkIfItemIsNormalBabyDiapers(productType):
    return productType.text == "normal diapers"

def checkIfItemIsGoldenRice(productType):
    return productType.text == "golden rice"






def checkLastCat(currentCat):
    if currentCat.text == "Water":
        return True


def catTotalCount(cat2dArray):
    count = 0
    for i in range(len(cat2dArray)):
        for j in range(len(cat2dArray[i])):
            if len(cat2dArray[i]) == 1 and i != 0 or  len(cat2dArray[i]) > 1 and j != 0:
                count += 1
    return count

def checkIfElementIsLastInSubCat(subCatArray,element):
    if subCatArray.index(element) == len(subCatArray)-1:
        return True
    return False
def handelReport(cat2dArray,currentItem,isScanned,currentSubCat,isSubCatIsTheOnlyElement=False):
    global catReportResult
    global healthyCounter
    global emptyCatCounter
    global didIusedTheyDoNotKeep
    global notKeepList
    global arrOfAll
    global arrOfAllCatCounter
    global i

    total = catTotalCount(cat2dArray)
    isThisTheLastIteminSub = checkIfElementIsLastInSubCat(arrOfAll[arrOfAllCatCounter][i],currentItem)



    if isScanned:
        healthyCounter += 1
    else:
        if not didIusedTheyDoNotKeep:
            catReportResult += "They do not keep the below items:\n"
        didIusedTheyDoNotKeep = True

        if isSubCatIsTheOnlyElement:
            catReportResult += f"{currentItem}\n"
        else:
            notKeepList.append(currentItem)


        emptyCatCounter += 1

    if isThisTheLastIteminSub and len(notKeepList) > 0:
        catReportResult += f"{currentSubCat} -> ("
        for element in notKeepList:
            catReportResult += f"{element}, "
        catReportResult = catReportResult[:-2]
        catReportResult += ")\n"
        notKeepList.clear()

    if healthyCounter == total:
        catReportResult = "Category Looks Healthy."
        return
    elif emptyCatCounter == total:
        catReportResult = "The shop does not support this category."
        return

    if healthyCounter + emptyCatCounter == total:
        catReportResult += "Because of not fast moving products"




eodFilter(driver) #The enabled filter
driver.minimize_window()
businessType = getBusniessType(driver)#store the bus type in a var and do the function body as it select the client from the dashboard also
driver.maximize_window()



today = datetime.today().date()
formattedDate = today.strftime("%d/%m/%Y")
dateAnswer = askingForToday(businessType)

waitForLoading(driver)
fullDashboardCategories = findCorrectVertical(driver,businessType)


categories = WebDriverWait(fullDashboardCategories,50).until(
    EC.visibility_of_all_elements_located((By.TAG_NAME,"li"))
)

#find_elements(By.TAG_NAME,"li") # this is a list of categories buttons
 # this is used in the next loops to confirm if the category cell is found , to not break the loop
  # ignore it now
  #initial variables


arrOfAll = [[  # auto
    ["Auto"],
    ["Interior Care"],
    ["Air Fresheners", "Car Air Freshener"],
    ["Accessories", "Usb Cable", "Aux Cable", "Booster Cable"],
    ["Exterior Care", "Car Cloth"],
    ["Others", "Engine Cleaner Spray"]
]
    ,  # baby Care
    [
        ["Baby Care"],
        ["Baby Food", "Cereals", "Puree"],
        ["Diapers", "Normal Diapers", "Pants Diapers", "Swimming Diapers"],
        ["Oral Care", "Toothbrush", "Toothpaste"],
        ["Milk Formula"],
        ["Skin Wipes"],
        ["Powders & Lotions", "Lotion", "Oil", "Powder", "Cologne"],
        ["Bath & Shower", "Shampoo", "Body Wash", "Hand Wash", "Conditioner"],
        ["Bottles, Pacifiers & Others"]
    ]
    ,



    [
        ["Bakery"],
        ["White Bread", "Flat", "Sliced Breads", "Rolls", "Buns"],
        ["Brown & Multigrain", "Flat","sliced Breads", "Multigrain Bread"],
        ["Croissants & Cakes", "Croissants", "Cakes", "Cake Rolls", "Muffins", "Cupcakes"],
        ["Buns & Sandwiches", "Buns", "Rolls"],
        ["Specialty Bread", "Bread Crumbs", "Rusks", "Soup Sticks", "Tortilla Wraps"],
        ["Freshly Baked","freshly baked","Arabic Sweets"],
        ["Specialty Sweets", "Cookies", "Barazek","Arabic Sweets"]#Specialty Sweets
    ]
    ,
    [
        ["Body Care"],
        ["Sun Care"],
        ["Perfumes & Fragrances"],
        ["Hand Wash & Care", "Soap Bar", "Liquid Hand Wash"],
        ["Lotions, Moisturizers & Oils", "Body Creams", "Body Lotions"],
        ["Powders"],
        ["Scrubs & Masks"],
        ["Bath & Shower", "Loofah", "Body Scrubs", "Shower Gels"]
    ]
    ,

    [
        ["Camping & BBQ Essentials"],
        ["Utensils & Accessories","Skewers"],
        ["Plates, Cups & Cutleries", "Plastic Plates", "Paper Cups", "Knives","Plastic Spoons","Plastic Knives","Foam Plates","Forks"],
        ["Lighters & Matches","Lighters", "Matches"],
        ["Charcoal & Wood"],
        ["Grills & Stoves", "Grills", "Grill Baskets", "Stoves"],
        ["Others"],
        ["Wraps & Foils", "Aluminium Foils","Sandwich Bags","Refrigerator Bags","Freezer Bags","Cling Film"]
    ]
    ,

    [
        ["Cans & Jars"],
        ["Sauces & Dressings", "Molasses", "Ketchup", "Mustard", "Mayo", "Soy Sauce", "Syrups", "Hot Sauce",
         "Bbq Sauce"],
        ["Oils & Vinegars", "Corn Oil", "Sunflower Oil", "Cooking Oils", "Apple Vinegar", "Olive Oil", "Vinegar"],
        ["Sweet Spreads & Dips", "Chocolate Spread", "Peanut Butter", "Jams"],
        ["Savory Spreads & Dips", "Morta", "Sauces", "Tahini"],
        ["Canned Meat", "Corned Beef", "Luncheon Meat"],
        ["Syrups & Honey", "Honey", "Syrups"],
        ["Pasta & Tomato Sauce", "Tomato Paste", "Pizza Sauce"],
        ["Desserts", "Halawa"],
        ["Soups & Beans"],
        ["Pickles & Olives", "Loose Pickles"],
        ["Tuna & Fish", "Tunas", "Mackerel"],
        ["Vegetables & Fruits", "Corn", "Peas", "Mushroom", "Vine Leaves"]
    ]
    ,
    [
        ["Cereals & Packets"],
        ["Oats & Muesli", "Oats", "Muesli", "Granola"],
        ["Dry Soups & Sauces", "Basak", "Knorr", "Maggi"],
        ["Cereals"],
        ["Cereal Bars","Outers"]
    ]
    ,

    [
        ["Chips & Snacks"],
        ["Croissants"],
        ["Protein & Energy Snacks"],
        ["Chips & Dips", "Chips", "Dips"],
        ["Healthy Snacks"],
        ["Biscuits & Cookies"],
        ["Crackers & Popcorn", "Microwave Popcorn", "Popcorn", "Bake Rolz", "Pretzo", "Tuc","Rice Cake"]
    ]
    ,

    [
        ["Chocolates & Candies"],
        ["Bars", "Bounty", "Cadbury", "Corona", "Galaxy", "Kit Kat", "Kinder", "Twix"],
        ["Slabs", "Milka", "Lindt"],
        ["Pouches & Boxes","Outers"],  # handle This Please
        ["Candies", "Bebeto", "Haribo", "Chupa Chups", "Skittles", "Mentos"],
        ["Gums & Mints", "Chiclets", "Trident", "Clorets", "Mentos"]
    ]
    ,

    [
        ["Coffee & Tea"],
        ["Flavored Teas"],
        ["Coffee Capsules"],
        ["Ground Coffee & Beans", "Dark", "Light"],
        ["Instant Coffee","Coffee Sachets", "Jars"],
        ["Green Tea", "Green Teas"],
        ["Black Tea","Black Teas"],
        ["Herbal & Infusion Tea", "Herbs"],
        ["Creamers & Sweeteners", "Creamers", "Low Calorie Sweeteners", "No Calorie Sweeteners"],
       # ["Pronto Fresh Coffee"],
        ["Fresh Coffee & Tea"],
        ["Chocolate", "Cocoa", "Drinking Chocolate Powder"],
        ["Others", "Coffee Filters"],
        ["Flavoured Drinks", "Sahlab Powder"]
    ]
    ,

    [
        ["Cosmetics"],

        ["Eyebrows & Lashes"],
        ["Nail Polish & More", "Nail Polish Remover", "Nail Clipper", "Nail Scissors"],
        ["Tools & Accessories","Face Shavers", "Nail File", "Tweezers", "Nail Brush", "Makeup Applicator",
         "Makeup Sponge"],
        ["Foundations & Concealers"],
        ["Cotton Swabs & Pads", "Cotton Pads", "Cotton Swabs", "Makeup Pads"],
        ["Makeup Removers"],
        ["Setting Sprays & Powders"],
        ["Blushes & Bronzers"],
        ["Highlight & Contour"],
        ["Bases & Primers"],
        ["Lipsticks & Liners"],
        ["Eyeliners & Eye Shadows"]

    ]
    ,

    [
        ["Dairy & Eggs"],
        ["Fresh Milk"],
        ["Eggs"],
        ["Spreads", "Loose","fresh", "Kiri", "La Vache Qui Rit", "Teama", "President", "Domty"],
        ["Cheese", "Loose", "Edam", "Rumy", "Baramily", "Cheddar", "Gouda", "Blue Cheese", "Feta", "Istanboli",
         "Triangles", "Mozzarella"],
        ["Butters & Creams", "Cooking Cream", "Whipping Cream", "Sour Cream", "Butter", "Ghee"],
        ["Yogurts & Laban", "Yogurts", "Fruit Yogurt", "Rayeb", "Greek Yogurt"],
        ["Shelf Milk", "Flavored Milk", "Half Cream", "Full Cream", "Skimmed", "Powder Milk"],
        ["Soya & Others", "Almond Drink", "Almond Milk", "Coconut Drink", "Coconut Milk", "Coconut Cream",
         "Coconut Drink With Soy"],
        ["Desserts", "Puddings"]
    ]
    ,
    [
        ["Electronics"],
        ["Home Appliances"],
        ["Personal Appliances"],
        ["Bulbs, Lamps & Lights"],
        ["Cables & Chargers"],
        ["Storage Devices"],
        ["Kitchen Appliances"],
        ["Others"],
        ["Batteries"],
        ["Earphones"],
        ["Plugs & Extensions"]
    ]
    ,

    [
        ["Facial Care"],
        ["Cleansers", "Facial Wash"],
        ["Scrubs & Masks", "Facial Scrubs", "Face Masks"],
        ["Cotton Swabs & Pads", "Cotton Swabs", "Cotton Pads"],
        ["Sun Care", "Sun Block"],
        ["Makeup Removers", "Makeup Remover", "Makeup Pads", "Cleansing Wipes"],
        ["Treatments", "Whitening Facial Cream", "Facial Cream"],
        ["Eye & Lip Care", "Lip Balm", "Eye Serum", "Eye Cream"],
        ["Moisturizers & Serums", "Moisturizing Cream"],
        ["Tissues & Wipes", "Tissues", "Wipes"],
        ["Toners & Facial Mists", "Toners", "Facial Sprays"],
        ["Powders", "Facial Powders"]
    ]
    ,

    [
        ["Flowers & Plants"],
        [ "Flowers"],
        ["Plants"]
    ]
    ,

    [
        ["Frozen"],

        ["Pizzas & Breads", "Tortilla", "Pizza"],
        ["Fruits", "Strawberry"],
        ["Meals", "Falafel", "Chicken Fillet", "Chicken Strips", "Chicken Tenders"],
        ["Pastries & Desserts", "Sambosa", "Goulash"],
        ["Vegetables & Potatoes", "French Fries", "Molokhia", "Peas", "Cauliflower", "Green Beans", "Spinach", "Okra"]
    ]
    ,

    [
        ["Fruits & Vegetables"],
        ["Fresh Herbs", "Parsley", "Coriander", "Gergeer", "Mint", "Rosemary"],
        ["Dried Vegetables"],
        ["Fruits", "Golden Apple", "Green Apple", "Red Apple", "Banana", "Lemon", "Orange", "Grape", "Guava", "Mango",
         "Peaches", "Tangerine"],
        ["Organic"],
        ["Veggies","Marrow", "Okra", "Potato", "Cabbage", "Capsicum", "Carrot", "Cucumber", "Chili", "Eggplant", "Garlic", "Lettuce", "Mushroom", "Onion" , "Tomato"]
    ]
    ,

    [
        ["General Health"],
        ["Antiseptics"],
        ["Others", "Mosquito Spray"],
        ["Herbal Remedies"],
        ["Wound Care", "Wound Plaster"],
        ["Common Symptoms", "Cough Relief Candies"],
        ["Face Masks"],
        ["Supplements", "Whey Protein", "Herbal Supplement Tea Bags"],
        ["Injury Support"]
    ]
    ,

    [
        ["Grab & Go"],
        ["Milkshakes & Slushies"],
        ["Fresh Coffee & Tea"],
        ["Fresh Spreads & Dips"],
        ["Meals & Salads"],
        ["Croissants & Pastries"],
        ["Fresh Juices & Smoothies"],
        ["Yogurt & Desserts"],
        ["Ready to Cook"],
        ["Wraps & Sandwiches"]
    ]
    ,

    [
        ["Healthy & Organic"],
        ["Pasta, Rice & Noodle"],
        ["Confectionery & Baking Goods"],
        [ "Dairy & Dairy Free"],
        [ "Soups, Sauces & Dressings"],
        [ "Vegan"],
        [ "Coffee & Tea"],
        [ "Gluten Free"],
        [ "Breads"],
        [ "Tomato & Pastes"],
        [ "Snacks & Spreads"],
        [ "Oils & Vinegars"],
        [ "Superfoods"],
        [ "Pulses, Grains & Seeds"],
        [ "Cereals, Oats & Muesli"]
    ]
    ,

    [
        ["Herbs & Spices"],

        ["Spices", "Coriander", "Cumin", "Chili", "Cinnamon", "Turmeric", "Cardamom", "Black Seed", "Cloves", "Paprika", "Nutmeg","Garlic Powder"],
        ["Herbs", "Thyme", "Mint", "Rosemary","Mastic","Bay Leaves"],
        ["Salt & Pepper", "Black Pepper", "White Pepper", "Table Salt"],
        ["Seasonings", "Garlic Powder", "Vegetar", "Onion Powder", "Meat Spices", "Hawawshi Mix", "Kabsa Mix",
         "Kofta Mix", "Chicken Stock", "Vegetable Stock", "Meat Stock", "Fries Seasonings", "Burger Mix", "Chicken Mix"]
    ]
    ,

    [
        ["Home Baking"],
        ["Accessories", "Baking Paper", "Food Paper", "Cupcake Cups","Egg Beater"],
        ["Baking Mixes", "Cake Mixes", "Ice Cream Mixes", "Om Ali", "Custard"],
        ["Baking Agents", "Baking Powder", "Yeast"],
        ["Flours", "All Purpose Flour", "Corn Starch", "Corn Flour", "Baking Powder"],
        ["Flavoring & Icing", "Vanilla Essence", "Cocoa Powder"],
        ["Confectionery", "White Sugar", "Brown Sugar", "Sugar Cubes", "Sticks"]

    ]
    ,

    [
        ["Household Care"],

        ["Mops & Brooms", "Mop", "Broom", "Dust Pan", "Wiper", "Mop Bucket"],
        ["Toilet Rolls", "Toilet Tissue Rolls"],
        ["Kitchen Rolls", "Kitchen Towel Rolls"],
        ["Bathroom Cleaning", "Toilet Brush","Plunger"],
        ["Powder Detergents"],
        ["Others", "Gloves", "Pegs"],
        ["Fabric Softeners"],
        ["Surface Cleaning"],
        ["Liquid Detergents"],
        ["Air Fresheners"],
        ["Dish Cleaning", "Steel Wool", "Washing Sponges", "Dishwashing Liquid"],
        ["Pest Control", "Insect Killer"],
        ["Garbage Bags"]
    ],

    [
        ["Hygiene & Personal Care"],
        ["Mouthwash, Floss & Others", "Mouthwash", "Toothpicks"],
        ["Toothbrushes"],
        ["Foot Care", "Foot Powder", "Shoe Spray", "Foot Cream", "Foot Mask"],
        ["Women Deo", "Spray", "Stick", "Roll"],
        ["Women Shaving", "Razors", "Paste", "Cream", "Strips"],
        ["Men Shaving", "Razors", "Gel", "Foam", "After Shave", "Cream"],
        ["Toothpastes"],
        ["Men Deo", "Spray", "Roll", "Stick"],
        ["Adult Pads & Diapers", "Adult Diapers"],
        ["Sanitizers", "Alcohol Solutions", "Antibacterial", "Hand Sanitizers", "Skin Wipes"],
        ["Fem Care", "Pantyliners", "Pads"]

    ]
    ,

    [
        ["Ice Creams"],
        ["Galaxy"],
        ["Cold Stone"],
        ["Mega"],
        ["Wonderville"],
        ["Carnavalita"],
        ["Sultana"],
        ["Cones"],
        ["Sorbet & Sticks"],
        ["Others"],
        ["Cups & Tubs"]
    ]
    ,

    [
        ["Kitchen & Pantry"],
        ["Pots & Pans","Coffee Pot"],
        ["Bottles & Shakers"],
        ["Cutlery","Plastic Spoons","Plastic Knives","Forks"],
        ["Plates & Cups","Paper Cups","Plastic Plates","Foam Plates"],
        ["Food Storage","Sandwich Bags","Refrigerator Bags","Aluminum Containers","Freezer Bags"],
        ["Serveware"],
        ["Accessories","Table Covers"],
        ["Plates & Cups",],
        ["Wraps & Foils","Aluminum Foil","Cling Film"],
        ["Utensils","straws","Grater", "Can Opener","Strainer","Egg Beater","Pizza Slicer","Knives"]
    ]
    ,

    [
        ["Meat & Fish"],
        ["Sausages & Burgers", "Burger", "Sausage", "Hotdogs", "Chicken Burger"],
        ["Cold Cuts", "Luncheon Beef", "Chicken Luncheon", "Salami", "Turkey Breasts", "Basterma", "Turkey Lobes"],
        ["Chicken & Turkey", "Chicken Strips", "Wings", "Pane", "Nuggets", "Shish", "Whole Chicken", "Chicken Breast",
         "Drumsticks", "Marinated", "Chicken Legs", "Chicken Thighs", "Duck", "Pigeon", "Rabbit",
         "Frozen Whole Chicken"],
        ["Lamb & Veal"],
        ["Beef"],
        ["Fresh Meat & Fish", "Kofta", "Burgers", "Cubes", "Escalope", "Steaks", "Liver", "Mince", "Neck", "Oxtail",
         "Sausage", "Shank", "Strips", "Chops", "Legs", "Shoulder"],
        ["Fish", "Fillet", "Mackerel", "Mullet", "Shrimps", "Squid", "Tilapia", "Caviar", "Herrings"],
        ["Others"],
        ["Pork"]

    ]
    ,

    [
        ["More"],
        ["Apparels", "Shirts", "Pants", "Dresses", "Scarves", "Belts", "Jewelries", "Sunglasses"],
        ["Charcoal","Shisha Charcoal"],
        ["Gardening"],
        ["Candles", "Birthday Candles", "Scented Candles", "Tea Lights", "Dinner Candles"],
        ["Others", "Shoe Polish"],
        ["Lighters & Matches","Lighters","Matches"],
        ["Bags", "Gift Bags"],
        ["Party Supplies", "Balloons", "Party Candles"]
    ]
    ,

    [
        ["Nuts & Seeds"],
        ["Salted & Roasted", "Almonds", "Cashews", "Pistachios", "Hazelnuts", "Peanuts"],
        ["Dried Fruits", "Dates", "Raisins"],

        ["Seeds", "Black Seeds", "Sunflower", "Pumpkin Seeds","White Pumpkin Seeds", "Sesame"],

        ["Raw Nuts", "Almonds", "Cashews", "Pistachios", "Hazelnuts", "Peanuts"]

    ]
    ,

    [
        ["Pasta, Rice & More"],
        ["Rice", "Egyptian", "Golden", "Basmati"],
        ["Gluten Free Pasta"],
        ["Pasta", "Big Rings", "Spaghetti", "Elbow", "Penne", "Risoni", "Small Rings", "Vermicelli", "Lasagne",
         "Fusilli", "Shells", "Linguine", "Fettuccine"],
        ["Noodles"],
        ["Pulses & Grains", "Fava Beans", "Black Eyed", "White Beans", "Yellow Lentils", "Brown Lentils", "Lupine",
         "Chickpeas"]
    ]
    ,

    [
        ["Pet Care"],
        ["Dog Food"],
        ["Cat Food"],
        ["Bird & Others"],
        ["Cat Care"],
        ["Dog Care"]

    ]
    ,

    [
        ["Prepaid Cards & Vouchers"],
        ["Vodafone"],
        ["We"],
        ["Orange"],
        ["Etisalat"]

    ]
    ,

    [
        ["Sensual Care"],
        ["Lubes"],
        ["Condoms"],
        ["Performance Enhancers"]

    ]
    ,

    [
        ["Shampoos & Hair Care"],
        ["Hair Treatments", "Hair Oil", "Conditioner", "Oil Replacement", "Hair Mask"],
        ["Hair Styling", "Hair Dyes"],
        ["Shampoos"],
        ["Conditioners"]
    ]
    ,

    [
        ["Soft Drinks & Juices"],
        ["Iced Coffee & Tea","Iced Coffee","Iced Tea"],
        ["Soft Drinks","Outers"], # handel this by not check outer and outer
        ["Fresh Juices & Smoothies"],
        ["Energy & Sports Drinks"],
        ["Malt Drinks"],
        ["Shelf Juices"]

    ]
    ,
    [  # back To School
        ["Stationery"],
         ["Tape"],
          ["Eraser"],
          ["Pencils"],
          ["Pens"],
          ["Markers"],
          ["notebooks"],
          ["Coloring Notebooks"],
         ["Sketches"],
          ["Sticky Notes"],
          ["Correction Pen"],
          ["Scissors"],
          ["Copy Papers"],
          ["School Bags"],
          ["Story Books"],
         ["Pencil Sharpener"]
    ]
    ,

    [
        ["Tobacco"],
        ["Rolling Paper & Filters","Rolling Paper", "Filters"],
        ["Regular"],
        ["Light"],
        ["Flavored"],
        ["Slims"],
        ["Heated Tobacco"],
        ["Cartons"],
        ["Vapes"],
        ["Lighters & Matches","Lighters","Matches"],
        ["Shisha & Cigars", "Flavors", "Cigars"]

    ]
    ,

    [
        ["Vegan & Vegetarian"],
        ["Drinks"],
        ["Desserts"],
        ["Tofu & Others"],
        ["Meat Alternatives"],
        ["Cheese, Spreads & Creams"],
        ["Yogurts"]

    ]
    ,

    [
        ["Water"],
        ["Gallons"],
        ["Single"],

        ["Packs"],

        ["Ice"],

        ["Still"],

        ["Sparkling"],

        ["Flavored", "Rose Water"]

    ]
]
alexPeople=["Amr Khalil",
            "Osama Mahmoud",
            "Mahmoud Eissa",
            "Abdelmaged Maged",
            "Maged Youssef",
            "Ahmed Mohamed",
            "Hossam ElAkad",
            "Ahmed Abdelazim"
            ]

arrOfAllCatCounter = 23
print()
notKeepList=[]




for element in categories:

    catNameInDashboard = element.text.split('\n')[0]
    try:
        catNameInArrOfAll = arrOfAll[arrOfAllCatCounter][0][0]
    except:
        break
    if catNameInDashboard == catNameInArrOfAll:
        categoryButton = WebDriverWait(element, 50).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "btn-link"))
        )
        deleteSearch(driver)
        print(categoryButton.text)
        #categoryButton.click()
        action_chains = ActionChains(driver)
        action_chains.move_to_element(categoryButton)
        action_chains.click(categoryButton)

        while categoryButton.get_attribute("class") != "btn btn-link menubtn-mob active":
            action_chains.perform()
            time.sleep(1)
        waitForLoading(driver)
        WebDriverWait(driver,10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR,'button[ng-repeat^="subc in subcategories"]'))
        )
        catAndSub = element.find_elements(By.CSS_SELECTOR, 'button[ng-repeat^="subc in subcategories"]')
        catReportResult = ""
        healthyCounter = 0
        emptyCatCounter = 0
        didIusedTheyDoNotKeep = False  # did we write they do not keep the below items ? , as we will not write it twice
        for i in range(1,len(arrOfAll[arrOfAllCatCounter])):



            for j in range(len(arrOfAll[arrOfAllCatCounter][i])):
                isCurrentItemScanned = False
                Handle = True
                #time.sleep(2)
                deleteSearch(driver)
                currentItem = arrOfAll[arrOfAllCatCounter][i][j]
                if isItemInSub(currentItem):#checks if the item is a subCat in the dashboard , see the return type of the funcion
                    for sub in catAndSub:
                        if sub.text == currentItem:
                            action_chains = ActionChains(driver)

                            # Move to the 'sub' element (optional, but useful if there are hover effects)
                            action_chains.move_to_element(sub)

                            # Click on the 'sub' element
                            action_chains.click(sub)
                            # Perform the actions

                            while sub.get_attribute("class") != "btn btn-link active":
                                action_chains.perform()
                            time.sleep(1)


                            try:
                                waitForLoading(driver)
                            except:
                                loopUntilProductsFound(driver)
                            if len(arrOfAll[arrOfAllCatCounter][i]) == 1:
                                if(loopProducts(driver)):
                                    isCurrentItemScanned = True
                            else:
                                Handle = False


                            break





                elif currentItem == "Outers" or currentItem == "Normal Diapers" or currentItem == "Golden":
                    if(loopProducts(driver,currentItem)):
                        isCurrentItemScanned = True
                else:
                    searchProduct(driver,currentItem)
                    time.sleep(1)
                    try:
                        waitForLoading(driver)
                    except:
                        loopUntilProductsFound(driver)




                    #check if any is scanned
                    if(loopProducts(driver)):
                        isCurrentItemScanned = True

                if Handle:
                    if len(arrOfAll[arrOfAllCatCounter][i]) == 1:
                        handelReport(arrOfAll[arrOfAllCatCounter], currentItem, isCurrentItemScanned,arrOfAll[arrOfAllCatCounter][i][0],True)
                    else:
                        handelReport(arrOfAll[arrOfAllCatCounter],currentItem,isCurrentItemScanned,arrOfAll[arrOfAllCatCounter][i][0])


        arrOfAllCatCounter += 1
        print(catReportResult)
        print()

#coffee and tea has some problems in not fast moving , kindly check green tea and back tea in the array compared to the dashboard
# cosmetics at the end of not fast moving it append another text
#category loogs healthy in cerials and packets has a problem

#just trying to see if git will be edited or not
#hello
#hello 2
#hello 2

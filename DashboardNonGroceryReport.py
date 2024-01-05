import time
from GettingReady import *

def handelCatOrSubReport(driver,excelSheet,catOrSub):
    global healthyCounter
    global emptyCatCounter
    global categoryStringInSheet
    global row_number
    global col_number

    try:  # remove driver wait and use time . wait instead as it not ret
        waitForLoading(driver)
        enabledProducts=driver.find_elements(By.CLASS_NAME,"proditem-mob")
        if len(enabledProducts)==0:
            emptyCatCounter+=1
            raise Exception
        elif len(enabledProducts) >= 4:
            healthyCounter += 1

        elif len(enabledProducts) == 3:
            categoryStringInSheet += (
                    "They keep three items only in " + catOrSub.text + "\n")
        elif len(enabledProducts) == 2:
            categoryStringInSheet += (
                    "They keep two items only in " + catOrSub.text + "\n")
        elif len(enabledProducts) == 1:
            categoryStringInSheet += (
                    "They keep one item only in " + catOrSub.text + "\n")

        merged_cells = finalExcelWorksheet.merged_cells.ranges
        for merged_range in merged_cells:
            if merged_range.min_row == row_number+1:
                if col_number in range(merged_range.min_col, merged_range.max_col + 1):
                    target_merged_cell = finalExcelWorksheet.cell(row=row_number+1, column=col_number)
                    target_merged_cell.value = categoryStringInSheet  # Update with your desired value
                    break

        # merged_cells = finalExcelWorksheet.merged_cells.ranges
        # for merged_range in merged_cells:
        #     if merged_range.min_row == row_number + 1:
        #         merged_range_col = merged_range.min_col
        #         firstCell = finalExcelWorksheet.cell(row=row_number + 1,
        #                                              column=merged_range_col)
        #         firstCell.value = categoryStringInSheet
        #         break

        # newCell.value=categoryStringInSheet
    except Exception as e:
        categoryStringInSheet+="They don't keep any items in " + catOrSub.text + "\n"


            # newCell.value += (
        merged_cells = finalExcelWorksheet.merged_cells.ranges
        for merged_range in merged_cells:
            if merged_range.min_row == row_number + 1:
                if col_number in range(merged_range.min_col, merged_range.max_col + 1):
                    target_merged_cell = finalExcelWorksheet.cell(row=row_number + 1, column=col_number)
                    target_merged_cell.value = categoryStringInSheet
                    break


eodFilter(driver)
driver.minimize_window()
businessType = getBusniessType(driver)#store the bus type in a var and do the function body as it select the client from the dashboard also
driver.maximize_window()
gc = setGoogleApi("googleSheetsCredintials.json") # set the google api credentials and get the gc var

sourceGoogleTemplate=openGoogleSheetsWorkbookByKey(gc,"1yHouDQE-Zj30xEa25leBEAC5X4vSo__U2FNb_AVpOIc") # open the google sheet that has all the templates
sourceGoogleTemplateWorksheet = selectGoogleTemplateSheet(driver,businessType,sourceGoogleTemplate)

sourceFormattingExcelWorkbook = load_workbook("All EOD Reports.xlsx") #open the excel workbook that will be used to copy all the formatting
sourceFormattingExcelWorksheet = selectExcelFormattingSheet(driver,businessType,sourceFormattingExcelWorkbook)

# Create our excel that will be used to fill in the report later on
finalExcelWorkbook = Workbook()
finalExcelWorksheet = finalExcelWorkbook.active #creating the report workshhet
finalExcelWorksheet.title = 'Report'
# all the next code will copy the cells from the google sheets template , and copy all the formatting from the ready excel file to our new file

copyAllGoogleSheetsToExcel(sourceGoogleTemplateWorksheet,finalExcelWorksheet)

copyCellFormating(sourceFormattingExcelWorksheet,finalExcelWorksheet)
removeSpacesInSheet(finalExcelWorksheet)
replaceCellValue(finalExcelWorksheet,"Cough, Cold and Flu","Cough, Cold & Flu")
replaceCellValue(finalExcelWorksheet,"Chocolate & Candies","Chocolates & Candies")
#Handel the upper cells of the report
teamLeader = getTeamLeader()
nonGroceryInfo(finalExcelWorksheet,1,2,8,8,teamLeader)
teamMembers = getTeamMembers()
nonGroceryInfo(finalExcelWorksheet,3,4,5,8,mergeTeamMembers(teamMembers))
today = datetime.today().date()
formattedDate = today.strftime("%d/%m/%Y")
dateAnswer = askingForToday(businessType)
if dateAnswer=='y':
    nonGroceryInfo(finalExcelWorksheet,startRow=2,endRow=2,startCol=2,endCol=3,value=" "+formattedDate)
else:
    nonGroceryInfo(finalExcelWorksheet, startRow=2, endRow=2, startCol=2, endCol=3, value=" " + dateAnswer)
shopName = clientName.split(" - ")[0]
location=clientName.split(" - ")[1]
nonGroceryInfo(finalExcelWorksheet,startRow=1,endRow=1,startCol=2,endCol=3,value=shopName)
nonGroceryInfo(finalExcelWorksheet,startRow=1,endRow=2,startCol=5,endCol=6,value=location)
if not teamMembers[0] == '':
    allMembers=teamMembers
    allMembers.append(teamLeader)
else:
    allMembers = [""]
    allMembers[0] = teamLeader
#.cell['H15']="Cough, Cold & Flu"
#getting the categories names in a list called categoriesList
categoriesList=getExcelCategories(businessType,finalExcelWorksheet)
#intializing variables
categoryNamesInExcel=[]
fullDashboardCategories = findCorrectVertical(driver,businessType)

'''fullDashboardCategories = WebDriverWait(driver,60).until(
    EC.visibility_of_element_located((By.CLASS_NAME,"vertical-categories-wrap"))
)'''
# driver.find_element(By.CLASS_NAME,"vertical-categories-wrap") # this is all categories elements
categories = WebDriverWait(fullDashboardCategories,50).until(
    EC.visibility_of_all_elements_located((By.TAG_NAME,"li"))
)
maxValue=len(allMembers)-1
#find_elements(By.TAG_NAME,"li") # this is a list of categories buttons
 # this is used in the next loops to confirm if the category cell is found , to not break the loop
  # ignore it now
for element in categories:  # for each category button
    if element.text.split('\n')[0] in categoriesList:  # checks if the category from the dashboard is in the template or not
        i = 0  # is used in the next loop , this variable is used to check if i'm in the first element , and the first element is the category again , so if we pressed it again , the category will disappear
        # we could use the webwaitelement to check for the sub categories , and if it fails it will press the category again , but we could implment it later
        healthyCounter = 0
        emptyCatCounter=0
        #category btn element
        category=WebDriverWait(element,50).until(
            EC.visibility_of_element_located((By.CLASS_NAME,"btn-link"))
        )
        category.click()
        time.sleep(2)
        #element.click()  # click the category button
        categoryButton = WebDriverWait(element, 50).until(
            EC.visibility_of_all_elements_located((By.CLASS_NAME,"btn-link"))
        )

        #element.find_elements(By.CLASS_NAME,"btn-link")
        flag = False# row found in sheet flag
        supportedCat = True #to indicate if the shop keeps any items in a category
        #element.find_elements(By.CLASS_NAME,
                     #                     "btn-link")  # after click the category , all sub will apear , and the fist element is the category again , as the name shows
        for row_index, row in enumerate(finalExcelWorksheet.iter_rows(min_row=5, values_only=True), start=5):
            checkEmptyCell = finalExcelWorksheet.cell(row=row_index, column=2)
            if not checkEmptyCell.value is None:
                for column_index, cell_value in enumerate(row[1:16], start=2):
                    if column_index < 15:  # 12 is the max column for any template
                        # Check if the current cell is part of a merged range
                        is_merged = False
                        for merged_range in finalExcelWorksheet.merged_cells.ranges:
                            if finalExcelWorksheet.cell(row=row_index, column=column_index).coordinate in merged_range:
                                is_merged = True
                                break

                        # Perform an exact word match
                        searched_word = element.text.split('\n')[0]
                        if not is_merged and cell_value and searched_word == cell_value:
                            flag=True
                            categoryStringInSheet=""
                            row_number = row_index
                            col_number = column_index
                            #column_letter = cell.column_letter

                            newCell = finalExcelWorksheet.cell(row=row_number+1,column=column_index)
                            for sub in categoryButton:  # for each category or sub category in the list as the list contains both
                                if i != 0:  # if i equals zero , that means we are at the category again , so we will not click it
                                    # Create an ActionChains object
                                    action_chains = ActionChains(driver)

                                    # Move to the 'sub' element (optional, but useful if there are hover effects)
                                    action_chains.move_to_element(sub)

                                    # Click on the 'sub' element
                                    action_chains.click(sub)

                                    # Perform the actions
                                    action_chains.perform()
                                if not (len(categoryButton) > 1 and i == 0):
                                    handelCatOrSubReport(driver,finalExcelWorksheet,sub)




                                i += 1


                                if len(categoryButton)>1 and (len(categoryButton) - 1 == healthyCounter or len(categoryButton) - 1 == emptyCatCounter):
                                    #newCell.value += (
                                    merged_cells = finalExcelWorksheet.merged_cells.ranges
                                    for merged_range in merged_cells:
                                        if merged_range.min_row == row_number + 1:
                                            if col_number in range(merged_range.min_col, merged_range.max_col + 1):
                                                target_merged_cell = finalExcelWorksheet.cell(row=row_number + 1,
                                                                                              column=col_number)
                                                if len(categoryButton)-1== healthyCounter:
                                                    target_merged_cell.value =  "Category looks healthy"
                                                elif len(categoryButton) - 1 == emptyCatCounter:
                                                    target_merged_cell.value = "The shop does not support this category"
                                                    supportedCat=False
                                                break
                                elif len(categoryButton)==1 and (len(categoryButton) == healthyCounter or len(categoryButton) == emptyCatCounter):

                                    merged_cells = finalExcelWorksheet.merged_cells.ranges
                                    for merged_range in merged_cells:
                                        if merged_range.min_row == row_number + 1:
                                            if col_number in range(merged_range.min_col, merged_range.max_col + 1):
                                                target_merged_cell = finalExcelWorksheet.cell(row=row_number + 1,
                                                                                              column=col_number)
                                                if len(categoryButton) == healthyCounter:
                                                    target_merged_cell.value = "Category looks healthy"
                                                elif len(categoryButton) == emptyCatCounter:
                                                    target_merged_cell.value = "The shop does not support this category"
                                                    supportedCat=False
                                                break


                            break
                if flag:
                    if supportedCat:
                        generateMemberInCell(maxValue,allMembers,finalExcelWorksheet,row_number,col_number+1)
                    break
if is_file_opened("C:\\Users\\Instashop\\Desktop\\"+clientName+" EOD"+".xlsx"):
    print("File is currently opened by another process. Please close it and run the program again.")
else:
    # Save the Excel file
    finalExcelWorkbook.save("C:\\Users\\Instashop\\Desktop\\"+clientName+" EOD"+".xlsx") #btn is the clickable
    print("Excel file saved successfully.")



#'Baby & Maternity'
# , 'Beauty & Cosmetics'
# , 'Body Care'
# , 'Clear Contact Lenses'
# , 'Color Contact Lenses',
# 'Common Symptoms'
# ,'Cough, Cold and Flu'
# , 'Equipment & Devices'
# , 'Eyes, Ears & Nose'
# ,'Eyewear Accessories',
# 'Facial Care'
# , 'First Aid'
# , 'Hair Care'
# , 'Headache & Fever'
# , 'Health & Fitness',
# 'Homeopathy & Aromatherapy'
# , 'Household Care'
# , 'Injury & Mobility Support'
# , 'Lens Solution',
# 'Medicines',
# 'Oral Care',
# 'Pain Relief',
# 'Pet Care (**for GREECE only**)'
# ,'Reading Glasses'
# ,'Sensual Care',
# 'Smoking Control'
# , 'Sun Care'
# ,'Supplements & Vitamins '
# , 'Women Care']



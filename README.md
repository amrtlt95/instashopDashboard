# Instashop Assortment Merchandiser Automation

This project automates various tasks related to the assortment merchandiser role in Instashop. Certain sensitive information has been excluded from the project to safeguard Instashop data.

## Files Included

1. **SetupProfile:**
   - Description: Sets up the Selenium web browser to open the dashboard.

2. **DashboardLogin:**
   - Description: Provides login credentials if required; otherwise, directs to the products page.

3. **GettingReady:**
   - Description: Asks for the client name and chooses it in the dashboard.

4. **ReturnPLUV2:**
   - Description: Used for the assortment coordinator task. Scrapes the dashboard for PLUs and Barcodes for specified IDs to simplify the task.

6. **freshItemsScraper:**
   - Description: Attempt to automate the enabling of fresh items. Note: Requires modification.

7. **OOS:**
   - Description: Automates the disabling of all out-of-stock (OOS) products for all clients in a list on a weekly basis.

8. **Methods:**
   - Description: Contains necessary methods, constants, and elements inside the dashboard.

9. **All EOD Reports.xlsx:**
   - Description: Used to copy the format into a new Excel file for final report formatting. (Main file in Google Sheets template does not copy formatting, only plain text).

10. **DashboardNonGroceryReport:**
    - Description: Automates EOD reports for non-grocery verticals. Grocery verticals may have additional validations and logic.

11. **groceryReport:**
    - Description: Automates grocery reports, checking for the date the item is scanned and whether someone in the team has enabled it.

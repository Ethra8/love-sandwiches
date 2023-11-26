import gspread #library first downloaded through terminal : pip3 install gspread google-auth
from google.oauth2.service_account import Credentials #imports just specific Credentials function from library, no need to import complete library
# from pprint import pprint --> must not be deployed. but very handy when coding and testing

#SCOPE in a constant, in Python, constant variables are written in CAPITALS
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

#CREDS is another constant variable, takes creds from file
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

"""
Code used to check Google sheets API is working

sales = SHEET.worksheet('sales') #to access 'sales' worksheet inside 'love-sandwiches' spreadsheet
data = sales.get_all_values() #gets all values from sales worksheet
print(data)
"""

def get_sales_data():
    """
    Get sales figures input from the user
    Run while loop to request valid data from the user via the terminal,
    which must be a string of 6 numbers separated by commas.
    The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:\n") #MUST \n with input, to deploy on Heroku --creates a simple string 1,2,3,4,5,6
        
    
        sales_data = data_str.split(",") #removes commas from string of sales data, and creates a list of strings ['1', '2', '3', '4', '5', '6']
    
        #check if validate_data() returns True
        if validate_data(sales_data):
            print("Data validated")
            break #breaks while loop
    
    return sales_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers
    Raises ValueError if string cannot be converted into int.
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values] #easy way to convert all strings values into integers
        if len(values) != 6:
            raise ValueError( #ValueError is renamed as e in except, and goes in the {e} in final message
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.")
        return False
    
    return True


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for every item type.

    The surplus is defined s the sales figures subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra sandwishes made when stock was solf out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    #pprint(stock) #pprint method makes data easier to read in the terminal - installed pprint on top of code from library
    stock_row = stock.pop() #last row in stock as list of strings
    #stock_row = stock[-1] --> also takes last row as index -1
    
    stock_row = [int(stock_item) for stock_item in stock_row] #converts strings of nums in integers [1, 22, 33, 4, 5, 66]
    #print(stock_row)

    surplus_data = []
    #zip() loops through various lists:
    for stock, sales in zip(stock_row, sales_row):
        surplus = stock - sales
        surplus_data.append(surplus) #includes sustraction of each item type to surplus_data empty string to contain totals of surplus
    
    return surplus_data

"""def update_sales_worksheet(data):
    print("Updating sales worksheet... \n") #informs user of process
    sales_worksheet = SHEET.worksheet('sales') #constant variable defined at begining of code
    sales_worksheet.append_row(data) # .appen_row adds row to our worksheet with data
    print("Sales worksheet updated successfully!\n")


def update_surplus_worksheet(data):
    print("Updating surplus worksheet...\n") #informs user of process
    
    surplus_worksheet.append_row(data) # .appen_row adds row to our worksheet with data
    print("Surplus worksheet updated successfully!\n")
"""

def update_worksheet(data, worksheet):
    """
    Refactor to update any worksheet, add new row with data provided.
    """
    print(f"Updating {worksheet}... \n") #informs user of process
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data) # .appen_row adds row to our worksheet with data
    print(f"{worksheet} updated successfully!\n")

def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet,
    collecting the last 5 entries for each sandwich,
    and returns the data ass a list of strings.
    """
    sales = SHEET.worksheet("sales")
    # column = sales.col_values(3) #retrieve values of 3rd column
    # print(column)
    
    columns = []
    for ind in range(1,7): #since columns in worksheet don't start at index 0 but index 1, we tell code to start at 1, and add 6 to retrieve all 6 columns
        column = sales.col_values(ind)
        columns.append(column[-5:]) #retrieves the range of the last 5 entries of each column, returning a list of lists.
    # pprint(columns)
    return columns

def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []
    
    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1 #adds 10% to average
        new_stock_data.append(round(stock_num)) #round() method rounds up decimal numbers (float nums) to int
    
    return new_stock_data


def main():
    """
    Run all program functions
    """
    data = get_sales_data() #still returns list of strings of nums ['1', '22', '33', '4', '5', '66']
    sales_data = [int(num) for num in data] #converts strings of nums in integers [1, 22, 33, 4, 5, 66]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    get_last_5_entries_sales()

    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")


print("Welcome to Love Sandwiches data automation")
main()

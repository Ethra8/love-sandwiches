import gspread #library first downloaded through terminal : pip3 install gspread google-auth
from google.oauth2.service_account import Credentials #imports just specific Credentials function from library, no need to import complete library

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

sales = SHEET.worksheet('sales') #to access 'sales' worksheet inside 'love-sandwishes' spreadsheet
data = sales.get_all_values() #gets all values from sales worksheet
print(data)
"""

def get_sales_data():
    """
    Get sales figures input from the user
    """
    print("Please enter sales data from the last market.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 10,20,30,40,50,60\n")

    data_str = input("Enter your data here: ") #creates a simple string
    # print(f"The data provided is {data_str}") -- 1,2,3,4,5,6
    
    sales_data = data_str.split(",") #removes commas from string of sales data, and creates a list of strings ['1', '2', '3', '4', '5', '6']
    validate_data(sales_data)


def validate_data(values):
    """
    Inside the try, converts all string values into integers
    Raises ValueError if string cannot be converted into int.
    or if there aren't exactly 6 values.
    """
    try:
        if len(values) != 6:
            raise ValueError( #ValueError is renamed as e in except, and goes in the {e} in final message
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.")


get_sales_data()
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials
# import pprint

# how to get the sheet using client_secret.json file
# scope = ['https://spreadsheets.google.com/feeds']
# creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
# client = gspread.authorize(creds)

# sheet = client.open('PFGOrders').sheet1

# a better way to print
# pp = pprint.PrettyPrinter()

# get all records
# records = sheet.get_all_records()
# pp.pprint(records)

# get a specific row
# row2 = sheet.row_values(2)
# pp.pprint(row2)

# get a specific column
# col2 = sheet.col_values(2)
# pp.pprint(col2)

# get a specific cell
# parameters are sheet.cell(row,col)
# cell2_2 = sheet.cell(3,2).value
# pp.pprint(cell2_2)

# update a cell
# sheet.update_cell(3,2,'=B2+B4')

# insert a row
# row = ['g6', 336, 6]
# index = 6
# sheet.insert_row(row, index)

# delete row
# sheet.delete_row(3)

# get row count
# print sheet.row_count
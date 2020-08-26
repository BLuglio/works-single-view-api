import csv

def write_dict_as_csv(name, _dict, dest):
    columns = _dict.keys()
    try:
        with open(dest + "/" + name + ".csv", 'w') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerow(_dict)
    except IOError:
        print("I/O error", flush=True)


# csv_columns = ['No','Name','Country']
# dict_data = [
# {'No': 1, 'Name': 'Alex', 'Country': 'India'},
# {'No': 2, 'Name': 'Ben', 'Country': 'USA'},
# {'No': 3, 'Name': 'Shri Ram', 'Country': 'India'},
# {'No': 4, 'Name': 'Smith', 'Country': 'USA'},
# {'No': 5, 'Name': 'Yuva Raj', 'Country': 'India'},
# ]
# csv_file = "Names.csv"
# try:
#     with open(csv_file, 'w') as csvfile:
#         writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
#         writer.writeheader()
#         for data in dict_data:
#             writer.writerow(data)
# except IOError:
#     print("I/O error")
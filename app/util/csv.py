import csv
import os

def write_dict_as_csv(name, _dict, dest):
    columns = _dict.keys()
    try:
        with open(dest + "/" + name, 'w') as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerow(_dict)
    except IOError:
        print("I/O error", flush=True)

def delete_csv(path):
    os.remove(path)
import os
import time
import sys
import csv


def to_csv(data, store_id=None, fieldnames=None):
    """Flexible function for CSV output"""
    today = time.strftime("%Y%m%d-%H%M%S") 
    appname = os.path.splitext(os.path.basename(sys.argv[0]))[0] 

    # Create a resonable filename with current datetime and appname
    if store_id:
        outfile_name = today + "_" + str(store_id) + "_" + appname + ".csv"
        data['site'] = store_id
    else:
        outfile_name = today + "_" + appname + ".csv"

    with open(outfile_name, 'w', newline='') as outfile:
        if not fieldnames:
            # Dict - If not provided, fieldnames are keys
            if isinstance(data, dict):
                fieldnames = data.keys()
                writer = csv.DictWriter(outfile, restval=0, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(data)
            # List of Dict - If not provided, fieldnames are keys from first record
            elif isinstance(data, list):
                try:
                    fieldnames = data[0].keys()
                    writer = csv.DictWriter(outfile, restval=0, fieldnames=fieldnames)
                    writer.writeheader()
                    for result in data:
                        writer.writerow(result)
                except:
                    raise
        else:
            # Use provided fieldnames
            writer = csv.DictWriter(outfile, restval=0, fieldnames=fieldnames)
            writer.writeheader()
            for result in data:
                writer.writerow(result)


def output_filename(extension='csv', store_id=None, appname=None):
    """Generate a name including current datetime for output file"""
    today = time.strftime("%Y%m%d-%H%M%S")

    if not appname: 
        appname = os.path.splitext(os.path.basename(sys.argv[0]))[0] 

    if store_id:
        return today + "_" + str(store_id) + "_" + appname + "." + extension
    else:
        return today + "_" + appname + "." + extension


def read_host_list(host_list='./host_list.csv'):
    """Parse host list and yield hosts"""
    with open(host_list) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['hostname', 'username', 'password'])

        for line in reader:
            yield line

if __name__ == "__main__":
    pass

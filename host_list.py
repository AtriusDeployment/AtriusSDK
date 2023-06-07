import csv
import pathlib


def iter(host_list='./host_list.csv'):
    """Parse host list and yield hosts"""
    with open(host_list) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['hostname', 'username', 'password'])

        for line in reader:
            yield line


def read(host_list='./host_list.csv'):
    """Return a list from hosts file"""
    # Return an empty list if the file does not exist yet. 
    if not pathlib.Path(host_list).is_file():
        return []

    # Return the contents of the file as a list
    with open(host_list) as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['hostname', 'username', 'password'])

        return [host for host in reader]


def write(hosts, host_list='./host_list.csv'):
    """Write hosts dictionary to the specified file"""
    with open(host_list, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['hostname', 'username', 'password'])

        writer.writerows(hosts)


def display(hosts):
    """Write the currently loaded host list dictionary to the display"""
    for host in hosts:
        print(host)


def add(hostname, username, password, host_list='./host_list.csv'):
    """Add a new host to the end of the dictionary and write the dict to the specified file"""
    # If the file already exists, read the current values into a dict
    if pathlib.Path(host_list).is_file():
        hosts = read(host_list)
    else:
        hosts = []

    # Add the new host to the dict
    hosts.append({'hostname': hostname, 'username': username, 'password': password})

    # Write the dict to the specified file
    write(hosts, host_list=host_list)


def delete(hostname, host_list='./host_list.csv'):
    """Delete all items by hostname from the dictionary and write the dict to the specified file"""
    # If the file already exists, read the current values into a dict
    if pathlib.Path(host_list).is_file():
        hosts = read(host_list)
    else:
        hosts = []

    # Find all instances by specified host name and remove from the dictionary
    for host in hosts:
        if hostname in host.values():
            hosts.remove(host)

    # Write the modified list to the specified file
    write(hosts, host_list=host_list)


if __name__ == '__main__':
    pass
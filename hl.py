import argparse
import host_list
import getpass


def main():

    # CLI and command line parameters
    parser = argparse.ArgumentParser(add_help=True, description="Manage host list")
    parser.add_argument('host_file', nargs='?', default='./host_list.csv', help='List of ECLYPSE controllers')

    args = parser.parse_args()

    # Initialize the loop variable
    command = None

    # Loop until the user enters quit as a command
    while command != 'quit':

        # Read and display the specified list
        hosts = host_list.read(host_list=args.host_file)
        host_list.display(hosts)
        print('\n')

        # Prompt for a command
        command = input('Command [add,delete,quit] >')

        # Loop if a command is not provided or quit
        if not command or command=='quit':
            continue

        # Split command 
        # This allows the user to enter all of the data for add/delete at once
        command_parsed = command.split(' ')

        # Get the hostname if provided or prompt for it
        if len(command_parsed) > 1:
            host = command_parsed[1]
        else:
            host = input('Hostname or IP address >')

        # Use the new match case introduced in Python 3.10
        # This defines the action for each command 
        match command_parsed[0]:
            case 'add':
                # Add case
                # Get username from command or prompt for it
                if len(command_parsed) > 2:
                    username = command_parsed[2]
                else: 
                    username = input('User Name >')

                # Get password from command or prompt for it
                if len(command_parsed) > 3:
                    password = command_parsed[3]
                else:
                    # We use getpass to hide the password input.
                    # If entered on the command line, the password is recorded in history
                    password = getpass.getpass("Password >")

                # Add the new host to the specified file
                host_list.add(host, username, password, host_list=args.host_file)
            case 'delete':
                # Delete case
                # The delete fucntion removes every record with the specified hostname
                host_list.delete(host, host_list=args.host_file)

if __name__ == "__main__":
    main()

#!/usr/bin/python3.5

# -------------------------------------------------
# iAM - The Simple and Speedy SSH Session Manager
# Designed and developed by Max Tuzzolino-Smith
# -------------------------------------------------

# __author__ = "Max Tuzzolino-Smith"

import sys
import os
import json
from tabulate import tabulate

# Global path variables
SESSION_PATH = os.path.dirname(os.path.realpath(__file__)) + "/sessions.json"
CONFIG_PATH = os.path.dirname(os.path.realpath(__file__)) + "/config.json"

# Headers
HEADERS = ["ID", "Alias", "Hostname"]

# Initial config
with open(CONFIG_PATH) as data:
    CONFIG = json.load(data)

try:
    DEF_USERNAME = CONFIG["username"]
except KeyError:
    # Initiate DEF_USERNAME
    DEF_USERNAME = ""

    if len(sys.argv) > 1:
        # Check if user is trying to change configuration
        if sys.argv[1] != "-c" and sys.argv[1] != "config":
            # Print error message
            print("ERROR: Default username not set, please set with `$ iam config user [username]`")

            # Exit program
            sys.exit()
try:
    DEF_TABLE_STYLE = CONFIG["table_style"]
except KeyError:
    if len(sys.argv) > 1:
        # Check if user is trying to change configuration
        if sys.argv[1] != "-c" and sys.argv[1] != "config":
            # Print error
            print("ERROR: A table_style was not defined, defaulting to `fancy_grid`"
                  "\n\t* To get rid of this error, set table style with `$ iam config table [style]`\n")

    # Set default table style
    DEF_TABLE_STYLE = "fancy_grid"


class IAM(object):
    # ---------------------------
    # Application Initiation
    #
    # ` argv[1] = command // - config
    # ` argv[2] = parameter 1 // - user/table
    # ` argv[3] = parameter 2 // - "username123"
    # ` argv[4] = ... etc.
    # ---------------------------

    def start(self):

        # Open session config
        with open(SESSION_PATH) as data:
            session_list = json.load(data)

        # If there are commands parsed
        if len(sys.argv) > 1:
            # Add session to list
            if sys.argv[1] == "-a" or sys.argv[1] == "add":
                if len(sys.argv) < 4:
                    print("Please include [hostname] [alias] and optional [group]")
                else:
                    try:
                        # Group is specified
                        group = sys.argv[4]
                    except IndexError:
                        # Group not specified
                        group = "unassigned"

                    # Add [hostname] [alias] [group] to session list
                    self.add(sys.argv[2], sys.argv[3], group, session_list)
            elif sys.argv[1] == "-l" or sys.argv[1] == "list":
                # List sessions
                self.list(session_list, sys.argv)
            elif sys.argv[1] == "-f" or sys.argv[1] == "format":
                # Format identifiers
                self.format(session_list)
            elif sys.argv[1] == "-c" or sys.argv[1] == "config":
                # Set configurations
                self.config(sys.argv)
            elif sys.argv[1] == "-r" or sys.argv[1] == "remove":
                # Remove session
                self.remove(session_list, sys.argv)
            elif sys.argv[1] == '-rg' or sys.argv[1] == "remove-group":
                self.removegroup(session_list, sys.argv)
            else:
                # Normal connect or search
                self.setup_session(sys.argv, session_list)
        else:
            # Nothing is defined - show help
            print("\t# -------------------------------------------------"
                  "\n\t# iAM - The Simple and Speedy SSH Session Manager"
                  "\n\t# Designed and developed by Max Tuzzolino-Smith"
                  "\n\t# ------------------------------------------------"
                  "\n\nCommands:"
                  "\n\t* Setting default username:\n\t\t`$ iam config user [username]`"
                  "\n\n\t* Setting table style:\n\t\t`$ iam config table [style]`"
                  "\n\n\t* Connecting to a session:\n\t\t`$ iam [id] or [alias]`"
                  "\n\n\t* List all sessions:\n\t\t`$ iam -l` or `$ iam list`"
                  "\n\n\t* List specific group:\n\t\t`$ iam -l [group]`"
                  "\n\n\t* Add to session list:\n\t\t`$ iam -a [hostname] [alias] [group](optional)`"
                  "\n\n\t* Remove specific session:\n\t\t`$ iam -r [id or alias]`"
                  "\n\n\t* Remove entire group (requires y/n prompt):\n\t\t`$ iam -rg [group-name]`"
                  "\n\n\t* Reformat identifiers:\n\t\t`$ iam -f` or `$ iam format`\n\t\t"
                  "Note: You should run this after manually editing the session file."
                  "\n\n\t* Copy SSH public key :\n\t\t`$iam [id or alias] -cid`")

    # Session setup
    def setup_session(self, argv, session_list):
        # Initiate session variable
        session = ""

        try:
            session_id = int(argv[1])

            for group, entry in session_list.items():
                for i in range(len(entry)):
                    if entry[i]["id"] == str(session_id):
                        session = entry[i]["hostname"]
        except ValueError:
            # Session based on ID not found, assuming name was parsed
            if not session:
                for group, entry in session_list.items():
                    for i in range(len(entry)):
                        if entry[i]["name"] == argv[1]:
                            session = entry[i]["hostname"]

        # If session is still empty, do a search for it. Unless it's an ID.
        if not session:
            self.search(argv[1], session_list)
        else:
            username = None
            protocol = None

            # If custom username or protocol (or both) specified
            if len(argv) > 2:
                if '-' not in argv[2]:
                    username = argv[2]
                else:
                    # ssh-copy-id script
                    if argv[2] == "-cid":
                        protocol = "ssh-copy-id"
                    else:
                        print("Protocol {} not recognized".format(argv[2]))
                        sys.exit()

                    # Protocol and username specified
                    if len(argv) > 3:
                        username = argv[3]

            # Connect to server based on ID.
            self.connect(session, username, protocol)

    # ---------------------------
    # Application Logic
    # ---------------------------

    # Connection initiation
    def connect(self, host, username, protocol):

        # If custom username is not specified then load from config
        if not username:
            username = DEF_USERNAME
        else:
            print("iAM connecting with username: {user}".format(user=username))

        # Protocol for connecting
        if not protocol:
            # Default protocol is SSH
            protocol = "ssh"
        else:
            print("iAM copying SSH public key")

        # Execute ssh session
        session = "{protocol} {username}@{host}".format(protocol=protocol, username=username, host=host)

        # Print session
        print("iAM now {host}".format(host=host))

        # Connect to session
        os.system(session)

    # Reusable output function used in search algorithm
    def output(self, results, hits):
        # Sort by name
        results = sorted(results, key=lambda entry: entry[1])

        print(tabulate(results, HEADERS, tablefmt=DEF_TABLE_STYLE))
        print("\t{hits} results found\n".format(hits=hits))

    # ---------------------------
    # Commands
    # ---------------------------

    # Add command
    def add(self, hostname, name, group_name, session_list):
        host_id = 0

        # First get latest ID and check if alias exits
        for group, entry in session_list.items():
            for i in range(len(entry)):
                host_id += 1

                # Check if alias exists
                if entry[i]["name"] == name:
                    # Print error
                    print(
                            "ERROR: Name '{name}' already exists in group '{group}', please try something different".format(
                                    name=name, group=group))

                    # Exit application
                    sys.exit()

        a_dict = None

        # Add to file
        for group, entry in session_list.items():
            # Group found
            if group == group_name:
                entry.append(
                        {
                            'id': str(host_id),
                            'name': name,
                            'hostname': hostname
                        }
                )

                a_dict = {group_name: entry}

                # Break out of loop
                break

        # No existing group - create a new one
        if a_dict is None:
            print("iAM creating a new group")

            a_dict = {
                group_name: [
                    {
                        'id': str(host_id),
                        'name': name,
                        'hostname': hostname
                    }]
            }

        session_list.update(a_dict)

        with open(SESSION_PATH, 'w') as f:
            json.dump(session_list, f, indent=4, sort_keys=True)

        print("Entry added:")
        print("ID: {id}, Name: {name}, Hostname: {host}, Group: {group}".format(id=host_id, name=name, host=hostname,
                                                                                group=group_name))

    # Remove command
    def remove(self, session_list, argv):
        hits = 0

        # Delete first entry of parsed id/alias
        if len(argv) > 2:
            for group, entry in session_list.items():
                for i in range(len(entry)):
                    if entry[i]["id"] == argv[2] or entry[i]["name"] == argv[2]:
                        # Increment hits
                        hits += 1
                        del entry[i]

                        # Break out of loop
                        break

            # No entries found
            if hits == 0:
                print("Could not find alias or identifier ' {item} '".format(item=argv[2]))
        else:
            print("Please include either an ID or an ALIAS as an argument")

        # Write + reformat identifiers after removing
        self.format(session_list)

    # Remove by group
    def removegroup(self, session_list, argv):
        hits = 0

        # Delete parsed group
        if len(argv) > 2:
            for group, entry in session_list.items():
                if group == argv[2]:
                    # Increment hits
                    hits += 1

                    # Prompt user for acceptance
                    prompt = input("Are you sure you wish to remove group ' {group} ' y/n? ".format(group=group))

                    if prompt == "y":
                        # Delete group
                        del session_list[group]

                        # Break out of loop
                        break
                    else:
                        # Do nothing
                        break

            # No entries found
            if hits == 0:
                print("Could not find group ' {group} '".format(group=argv[2]))
        else:
            print("Please include the name of the group you wish to remove")

        # Write + reformat identifiers after removing
        self.format(session_list)

    # Search command
    def search(self, item, session_list):
        print("Searching for ' {item} '".format(item=item))

        hits = 0
        results = []

        # Find results
        for group, entry in session_list.items():
            for i in range(len(entry)):
                if item in entry[i]["hostname"]:
                    # Increment hits
                    hits += 1

                    # Append results
                    results.append([entry[i]["id"], entry[i]["name"], entry[i]["hostname"]])

        # Output results
        self.output(results, hits)

        if hits == 0:
            print("Cannot find: ' {item} '".format(item=item))

    # List command
    def list(self, session_list, argv):

        hits = 0
        results = []

        # Search by group
        if len(argv) > 2:
            print("Listing group '{group}':".format(group=argv[2]))

            for group, entry in session_list.items():
                for i in range(len(entry)):
                    if group == argv[2]:
                        # Increment hits
                        hits += 1

                        # Append results
                        results.append([entry[i]["id"], entry[i]["name"], entry[i]["hostname"]])

            # Output results
            self.output(results, hits)
        else:
            # List everything
            for group, entry in session_list.items():
                for i in range(len(entry)):
                    # Increment hits
                    hits += 1

                    # Append results
                    results.append([entry[i]["id"], entry[i]["name"], entry[i]["hostname"]])

            # Output results
            self.output(results, hits)
        if hits == 0:
            print("No sessions. Add sessions to /opt/iam/sessions.json or with the 'iam add' command")

    # Format command (reindexes identifiers)
    def format(self, session_list):
        hits = 0

        # For every entry, increment and set id
        for group, entry in session_list.items():
            for i in range(len(entry)):
                # Set id
                entry[i]["id"] = str(hits)

                # Increment hits
                hits += 1

        with open(SESSION_PATH, 'w') as f:
            json.dump(session_list, f, indent=4, sort_keys=True)

    # Config command
    def config(self, args):
        # Set default properties
        username = DEF_USERNAME
        table = DEF_TABLE_STYLE

        if len(args) > 2:
            # Set username
            if args[2] == "user":
                if len(args) > 3:
                    username = args[3].strip("\"")
                else:
                    print("Please provide a username")

            # Set table style
            if args[2] == "table":
                if len(args) > 3:
                    table = args[3].strip("\"")
                else:
                    print("Please choose one of the following tables and run $ iam table [table_name]:\
                        \n\t* plain \
                        \n\t* simple\
                        \n\t* grid\
                        \n\t* fancy_grid\
                        \n\t* pipe\
                        \n\t* orgtbl\
                        \n\t* rst\
                        \n\t* mediawiki\
                        \n\t* html\
                        \n\t* latex\
                        \n\t* latex_booktabs")

            # Set configuration properties
            CONFIG["username"] = username
            CONFIG["table_style"] = table

            # Write to config
            with open(CONFIG_PATH, 'w') as f:
                json.dump(CONFIG, f, indent=4, sort_keys=True)


# ---------------------------
# Application Execution
# ---------------------------

if __name__ == '__main__':
    iam = IAM()
    iam.start()

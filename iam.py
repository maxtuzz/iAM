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
session_path = os.path.dirname(os.path.realpath(__file__)) + "/sessions.json"
config_path = os.path.dirname(os.path.realpath(__file__)) + "/config.json"

# Headers
headers = ["ID", "Alias", "Hostname"]

# Initial config
with open(config_path) as data:
    config = json.load(data)
    default_username = config["username"]
    default_table_style = config["table_style"]


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
        with open(session_path) as data:
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
            else:
                # Normal connect or search
                self.setup_session(sys.argv, session_list)
        else:
            # Nothing is defined - show help
            print(" -- iAM here to help --")

    # Session setup
    def setup_session(self, argv, session_list):

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

            # If custom username specified
            if len(argv) > 2:
                username = argv[2]

            # Connect to server based on ID.
            self.connect(session, username)

    # ---------------------------
    # Application Logic
    # ---------------------------

    # Connection initiation
    def connect(self, host, username):

        # If custom username is not specified then load from config
        if not username:
            username = default_username
        else:
            print("iAM connecting with username: {user}".format(user=username))

        # Execute ssh session
        session = "ssh {username}@{host}".format(username=username, host=host)

        # Print session
        print("iAM now {host}".format(host=host))

        # Connect to session
        os.system(session)

    # Reusable output function used in search algorithm
    def output(self, results, hits):
        # Sort by name
        results = sorted(results, key=lambda entry: entry[1])

        print(tabulate(results, headers, tablefmt=default_table_style))
        print("\t{hits} results found\n".format(hits=hits))

    # ---------------------------
    # Commands
    # ---------------------------

    # Add command
    def add(self, hostname, name, group_name, session_list):
        host_id = 0

        # First get latest ID
        for group, entry in session_list.items():
            for i in range(len(entry)):
                host_id += 1

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

        with open(session_path, 'w') as f:
            json.dump(session_list, f, indent=4, sort_keys=True)

        print("Entry added:")
        print("ID: {id}, Name: {name}, Hostname: {host}, Group: {group}".format(id=host_id, name=name, host=hostname,
                                                                                group=group_name))

    # Remove command
    def remove(self):
        print("Remove a session here")

    # Search command
    def search(self, item, session_list):
        print("Searching for ' {item} '".format(item=item))

        hits = 0
        results = []
        for group, entry in session_list.items():
            for i in range(len(entry)):
                if item in entry[i]["hostname"]:
                    # Increment hits
                    hits += 1

                    # Append results
                    results.append([entry[i]["id"], entry[i]["name"], entry[i]["hostname"]])

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
            self.output(results, hits)
        else:
            # List everything
            for group, entry in session_list.items():
                for i in range(len(entry)):
                    # Increment hits
                    hits += 1

                    # Append results
                    results.append([entry[i]["id"], entry[i]["name"], entry[i]["hostname"]])
            self.output(results, hits)
        if hits == 0:
            print("No sessions. Add sessions to /opt/iam/sessions.json or with the 'iam add' command")

    # Format command
    def format(self, session_list):
        hits = 0

        # For every entry, increment and set id
        for group, entry in session_list.items():
            for i in range(len(entry)):
                # Set id
                entry[i]["id"] = str(hits)

                # Increment hits
                hits += 1

        with open(session_path, 'w') as f:
            json.dump(session_list, f, indent=4, sort_keys=True)

    # Config command
    def config(self, args):
        # Set default properties
        username = default_username
        table = default_table_style

        if len(args) >2:
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
            config["username"] = username
            config["table_style"] = table

            # Write to config
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=4, sort_keys=True)

# ---------------------------
# Application Execution
# ---------------------------

if __name__ == '__main__':
    iam = IAM()
    iam.start()

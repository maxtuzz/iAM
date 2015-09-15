#!/usr/bin/python3
# Iam Dev Codebase

import sys
import subprocess
import json

# __author__ = "Max Tuzzolino-Smith"

# Global path variables
session_path = "/opt/iam/sessions.json"
config_path = "/opt/iam/config.json"

class IAM(object):
    # ---------------------------
    # Application Initiation
    # ---------------------------
    def start(self):

        # Open session config
        with open(session_path) as data:
            session_list = json.load(data)

        # If there are commands parsed
        if len(sys.argv) > 1:
            # Add session to list
            if sys.argv[1] == "-a" or sys.argv[1] == "add":
                if len(sys.argv) < 3:
                    print("Not enough arguments.")
                else:
                    try:
                        # Group is specified
                        group = sys.argv[4]
                    except IndexError:
                        # Group not specified
                        group = "unassigned"

                    self.add(sys.argv[2], sys.argv[3], group, session_list)
            elif sys.argv[1] == "-l" or sys.argv[1] == "list":
                # List sessions
                self.list(session_list, sys.argv)
            else:
                # Normal connect or search
                self.setup_session(sys.argv, session_list)
        else:
            # Nothing is defined - show help
            print("iAM Help")

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

    # Connection intiation
    def connect(self, host, username):
        if not username:
            with open(config_path) as data:
                config = json.load(data)
                username = config["username"]
        else:
            print("Connecting with username: " + username)

        # Execute ssh session
        session = "ssh {username}@{host}".format(username=username, host=host)

        # Print session
        print(session)

        # Connect to session
        subprocess.Popen(session.split())

    # Reusable output function used in search algorithm
    def output_find(self, hits, entry, i):
        # Output Search Results
        results = [
            "{hits}:".format(hits=str(hits)),
            "ID:[{id}]".format(id=entry[i]["id"]),
            "Name:{name}".format(name=entry[i]["name"]),
            "Hostname:{hostname}".format(hostname=entry[i]["hostname"])]

        # Format & print results
        print("{0:<0} {1:<10} {2:<20} {3:<10}".format(*results))

        # Connection initiation

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

                # Test print
                # print(json.dumps(entry, indent=4, sort_keys=True))
                a_dict = {group_name: entry}

                # Break out of loop
                break

        # No existing group - create a new one
        if a_dict is None:
            print("Creating new group")

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
        print("ID: {id}, Name: {name}, Hostname: {host}, Group: {group}".format(id=host_id, name=name, host=hostname, group=group_name))

    # Remove command
    def remove(self):
        print("Remove a session here")

    # Search command
    def search(self, item, session_list):
        print("Searching for ' {item} '".format(item=item))

        hits = 0
        for group, entry in session_list.items():
            for i in range(len(entry)):
                if item in entry[i]["hostname"]:
                    # Increment hits
                    hits += 1

                    # Output Search Results
                    self.output_find(hits, entry, i)
        if hits == 0:
            print("Cannot find: ' {item} '".format(item=item))

    # List command
    def list(self, session_list, argv):
        hits = 0

        # Search by group
        if len(argv) > 2:
            for group, entry in session_list.items():
                for i in range(len(entry)):
                    if group == argv[2]:
                        # Increment hits
                        hits += 1

                        # Output Search Results
                        self.output_find(hits, entry, i)
        else:
            # Search normal
            for group, entry in session_list.items():
                for i in range(len(entry)):
                    # Increment hits
                    hits += 1
                    self.output_find(hits, entry, i)

        if hits == 0:
            print("No sessions. Add sessions to /opt/iam/sessions.json or with the 'iam add' command")

    # Format example
    # tableData = [['apples', 'oranges', 'cherries', 'bananas'],
    # ['Alice', 'Bob', 'Carol', 'David',],
    # ['dogs', 'cats', 'moose', 'goose']]

    def print_table(table):
        columnwidth = [0] * len(table)

        for w in range(len(table[0])):
            for l in range(len(table)):
                if len(table[l][w]) > columnwidth[l]:
                    columnwidth[l] = len(table[l][w])
        print(columnwidth)

        for x in range(len(table[0])):
            for y in range(len(table)):
                print(table[y][x].rjust(columnwidth[y] + 1), end = '')
            print()
# ---------------------------
# Application Execution
# ---------------------------
iam = IAM()
iam.start()

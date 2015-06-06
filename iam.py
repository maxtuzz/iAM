#! /usr/bin/python3
# Iam Dev Codebase

import sys
import os
import json

# __author__ = "Max Tuzzolino-Smith"

class iAM(object):
    def start(self):
        # Open session config
        with open('sessions.json') as data:
            session_list = json.load(data)

        # If there are commands parsed
        if len(sys.argv) > 1:
            if sys.argv[1] == "-a" or sys.argv[1] == "add":
                # Test server
                self.add("testserver.auckland.ac.nz")
            elif sys.argv[1] == "-l" or sys.argv[1] == "list":
                self.list(session_list, sys.argv)
            else:
                self.setup_session(sys.argv, session_list)
        else:
            # Nothing is defined - show help
            print("iAM Help")

    # Helper functions
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

    # Commands
    def add(self, hostname):
        print("Create a session here")

    def remove(self):
        print("Remove a session here")

    def search(self, item, session_list):
        print("Searching for '", item, "'")

        hits = 0
        for group, entry in session_list.items():
            for i in range(len(entry)):
                if item in entry[i]["hostname"]:
                    # Increment hits
                    hits += 1

                    # Output Search Results
                    print(str(hits) + ": ID: [" + entry[i]["id"]
                          + "],\t Name: [" + entry[i]["name"]
                          + "],\t\t Hostname: [" + entry[i]["hostname"] + "]")
        if hits == 0:
            print("Cannot find: '", item, "'")

    def connect(self, host, username):
        if not username:
            with open('config.json') as data:
                config = json.load(data)
                username = config["username"]
        else:
            print("Connecting with username: " + username)
        # Execute ssh session
        os.system("ssh " + username + '@' + host)

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
                        print(str(hits) + ": ID: [" + entry[i]["id"]
                              + "],\t Name: [" + entry[i]["name"]
                              + "],\t\t Hostname: [" + entry[i]["hostname"] + "]")
        else:
            # Search normal
            for group, entry in session_list.items():
                for i in range(len(entry)):
                    # Increment hits
                    hits += 1

                    # Output Search Results
                    print(str(hits) + ": ID: [" + entry[i]["id"]
                          + "],\t Name: [" + entry[i]["name"]
                          + "],\t\t Hostname: [" + entry[i]["hostname"] + "]")
        if hits == 0:
            print("No sessions. Add sessions to /opt/iam/sessions.json or with the 'iam add' command")


iam = iAM()
iam.start()

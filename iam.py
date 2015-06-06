#! /usr/bin/python3
# Iam Dev Codebase

import sys
import os
import json

# __author__ = "Max Tuzzolino-Smith"

class iAM(object):

    def start(self):
        # If there are commands parsed
        if len(sys.argv) > 1:
            if sys.argv == "-a" or sys.argv == "add":
                # Test server
                self.add("testserver.auckland.ac.nz")
            else:
                self.setup_session(sys.argv)
        else:
            # Nothing is defined - show help
            print("iAM Help")

    # Helper functions
    def setup_session(self, argv):
        with open('sessions.json') as data:
                    session_list = json.load(data)

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
                        print("Searching for " + argv[1])
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

    def search(self, item, list):
        for group, entry in list.items():
            for i in range(len(entry)):
                if item in entry[i]["hostname"]:
                    # Output Search Results
                    print("ID: [" + entry[i]["id"]
                          + "],\t Name: [" + entry[i]["name"]
                          + "],\t Hostname: [" + entry[i]["hostname"] + "]")

    def connect(self, host, username):
        if not username:
            with open('config.json') as data:
                config = json.load(data)
                username = config["username"]
        print("Username = " + username)
        os.system("ssh " + username + '@' + host)


iam = iAM()
iam.start()

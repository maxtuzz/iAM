#! /usr/bin/python3
# Iam Dev Codebase

import sys
import os
import json

# __author__ = "Max Tuzzolino-Smith"

class iAM(object):

    def main(self):
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
                        print("Session not found, did you mean: ")
                        self.search(argv[1])
                    else:
                        # Connect to server based on ID.
                        self.connect(session)

    # Commands
    def add(self, hostname):
        print("Create a session here")

    def remove(self):
        print("Remove a session here")

    def search(self, item):
        print("Searching for ")

    def connect(self, host):
        os.system("ssh " + host)


iam = iAM()
iam.main()

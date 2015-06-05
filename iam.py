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
                with open('sessions.json') as data:
                    session_list = json.load(data)

                session = ""

                try:
                    # Load session based on ID parsed as argument
                    session = session_list["unassigned"][int(sys.argv[1])]["hostname"]
                except ValueError:
                    # Session based on ID not found, assuming name was parsed
                    if not session:

                        for group, entry in session_list.items():
                            i = 0
                            print(entry)

                            if entry[i]["name"] == sys.argv[1]:
                                print("hit!!")
                                session = entry[i]["hostname"]
                                break
                            else:
                                print("Incrementing i")
                                i += 1

                # Double check session
                print("Session: " + session)

                # Connect to server based on ID.
                # self.connect(session)
        else:
            # Nothing is defined - show help
            print("iAM Help")

        # Commands

    def add(self, hostname):
        print("Create a session here")

    def remove(self):
        print("Remove a session here")

    def search(self):
        print("Searching for ")

    def connect(self, host):
        os.system("ssh " + host)


iam = iAM()
iam.main()

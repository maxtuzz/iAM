#! /usr/bin/python3
# Iam Dev Codebase

import sys
import os

#__author__ = "Max Tuzzolino-Smith"

class iAM(object):
    def main(self):
        if len(sys.argv) > 1:
            if sys.argv == "-a" or sys.argv == "add":
                self.add("testserver.auckland.ac.nz")
            else:
                self.connect(sys.argv[1])
        else:
            print("iAM Help")

# Commands
    def add(self, hostname):
        print("Create a session here")

    def remove(self):
        print ("Remove a session here")

    def search(self):
        print("Searching for ")


    def connect(self, host):
        os.system("ssh " + host)

iam = iAM()
iam.main()

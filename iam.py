#! /usr/bin/env python3

# -------------------------------------------------
# iAM - The Simple and Speedy SSH Session Manager
# Developed by Max Tuzzolino-Smith
# -------------------------------------------------

# __author__ = "Max Tuzzolino"

import sys
import os
import json
from tabulate import tabulate

# Global path variables
SESSION_PATH = os.path.dirname(os.path.realpath(__file__)) + "/sessions.json"
CONFIG_PATH = os.path.dirname(os.path.realpath(__file__)) + "/config.json"

# Table headers
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

    # ---------------------------
    # Constructor
    # ---------------------------

    def __init__(self, session_list, argv):
        self.session_list = session_list
        self.argv = argv

    # Session setup
    def setup_session(self):
        # Initiate session variable
        session = self.get_host(self.argv[1])

        # If session is still empty, do a search for it. Unless it's an ID.
        if not session:
            self.search(self.argv[1])
        else:
            username = None
            protocol = None

            # If custom username or protocol (or both) specified
            if len(self.argv) > 2:
                if '-' not in self.argv[2]:
                    username = self.argv[2]
                else:
                    # ssh-copy-id script
                    if self.argv[2] == "-cid":
                        protocol = "ssh-copy-id"
                    else:
                        print("Protocol {} not recognized".format(self.argv[2]))
                        sys.exit()

                    # Protocol and username specified
                    if len(self.argv) > 3:
                        username = self.argv[3]

            # Connect to server based on ID.
            self.connect(session, username, protocol)

    def get_host(self, host):
        # Initiate session variable
        session = ""

        try:
            session_id = int(host)

            for group, entries in self.session_list.items():
                for entry in entries:
                    if entry["id"] == str(session_id):
                        session = entry["hostname"]
        except ValueError:
            # Session based on ID not found, assuming name was parsed
            if not session:
                for group, entries in self.session_list.items():
                    for entry in entries:
                        if entry["name"] == host:
                            session = entry["hostname"]
        return session

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
    def add(self, hostname, name, group_name):
        host_id = 0

        # First get latest ID and check if alias exits
        for group, entries in self.session_list.items():
            for entry in entries:
                host_id += 1

                # Check if alias exists
                if entry["name"] == name:
                    # Print error
                    print(
                        "ERROR: Name '{name}' already exists in group '{group}', please try something different".format(
                            name=name, group=group))

                    # Exit application
                    sys.exit()

        a_dict = None

        # Add to file
        for group, entries in self.session_list.items():
            # Group found
            if group == group_name:
                entries.append(
                    {
                        'id': str(host_id),
                        'name': name,
                        'hostname': hostname
                    }
                )

                a_dict = {group_name: entries}

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

        self.session_list.update(a_dict)

        with open(SESSION_PATH, 'w') as f:
            json.dump(self.session_list, f, indent=4, sort_keys=True)

        print("Entry added:")
        print("ID: {id}, Name: {name}, Hostname: {host}, Group: {group}".format(id=host_id, name=name, host=hostname,
                                                                                group=group_name))

    # Remove command
    def remove(self):
        hits = 0

        to_remove = self.argv[2]

        # Delete first entry of parsed id/alias
        if len(self.argv) > 2:
            for group, entries in self.session_list.items():
                for entry in entries:
                    if entry["id"] == to_remove or entry["name"] == to_remove:
                        # Increment hits
                        hits += 1
                        del entry

                        # Break out of loop
                        break

            # No entries found
            if hits == 0:
                print("Could not find alias or identifier ' {item} '".format(item=self.argv[2]))
        else:
            print("Please include either an ID or an ALIAS as an argument")

        # Write + reformat identifiers after removing
        self.format()

    # Remove by group
    def remove_group(self):
        hits = 0

        # Delete parsed group
        if len(self.argv) > 2:
            for group, entries in self.session_list.items():
                if group == self.argv[2]:
                    # Increment hits
                    hits += 1

                    # Prompt user for acceptance
                    prompt = input("Are you sure you wish to remove group ' {group} ' y/n? ".format(group=group))

                    if prompt == "y":
                        # Delete group
                        del self.session_list[group]

                        # Break out of loop
                        break
                    else:
                        # Do nothing
                        break

            # No entries found
            if hits == 0:
                print("Could not find group ' {group} '".format(group=self.argv[2]))
        else:
            print("Please include the name of the group you wish to remove")

        # Write + reformat identifiers after removing
        self.format()

    # Search command
    def search(self, item):
        print("Searching for ' {item} '".format(item=item))

        hits = 0
        results = []

        # Find results
        for group, entries in self.session_list.items():
            for entry in entries:
                if item in entry["hostname"]:
                    # Increment hits
                    hits += 1

                    # Append results
                    results.append([entry["id"], entry["name"], entry["hostname"]])

        # Output results
        self.output(results, hits)

        if hits == 0:
            print("Cannot find: ' {item} '".format(item=item))

    # List command
    def list(self):

        hits = 0
        results = []

        # Search by group
        if len(self.argv) > 2:
            print("Listing group '{group}':".format(group=self.argv[2]))

            for group, entries in self.session_list.items():
                for entry in entries:
                    if group == self.argv[2]:
                        # Increment hits
                        hits += 1

                        # Append results
                        results.append([entry["id"], entry["name"], entry["hostname"]])

            # Output results
            self.output(results, hits)
        else:
            # List everything
            for group, entries in self.session_list.items():
                for entry in entries:
                    # Increment hits
                    hits += 1

                    # Append results
                    results.append([entry["id"], entry["name"], entry["hostname"]])

            # Output results
            self.output(results, hits)
        if hits == 0:
            print("No sessions. Add sessions to /opt/iam/sessions.json or with the 'iam add' command")

    # Format command (re-indexes identifiers)
    def format(self):
        hits = 0

        # For every entry, increment and set id
        for group, entries in self.session_list.items():
            for entry in entries:
                # Set id
                entry["id"] = str(hits)

                # Increment hits
                hits += 1

        with open(SESSION_PATH, 'w') as f:
            json.dump(self.session_list, f, indent=4, sort_keys=True)

    # Config command
    def config(self):
        # Set default properties
        username = DEF_USERNAME
        table = DEF_TABLE_STYLE

        if len(self.argv) > 2:
            # Set username
            if self.argv[2] == "user":
                if len(self.argv) > 3:
                    username = self.argv[3].strip("\"")
                else:
                    print("Please provide a username")

            # Set table style
            if self.argv[2] == "table":
                if len(self.argv) > 3:
                    table = self.argv[3].strip("\"")
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

    # Copy command (scp implementation)
    def copy(self):
        if len(self.argv) > 2:
            username = DEF_USERNAME

            if '!' in self.argv[2]:
                connection = self.argv[2].split(':')
                host = connection[0][1:]
                path = connection[1]
                session = self.get_host(host)

                if not session:
                    print("Host {} could not be found".format(host))
                    sys.exit()

                print("iAM copying from {} to {}".format(session, self.argv[3]))

                # Copy file
                os.system(
                    "scp {user}@{hostname}:{path} {local}".format(user=username, hostname=session, path=path,
                                                                  local=self.argv[3]))

            elif '!' in self.argv[3]:
                connection = self.argv[3].split(':')
                host = connection[0][1:]
                path = connection[1]
                session = self.get_host(host)

                if not session:
                    print("Host {} could not be found".format(host))
                    sys.exit()

                print("iAM copying from {} to {}".format(self.argv[2], session))

                # Copy file
                os.system("scp {local} {user}@{hostname}:{path}".format(user=username, hostname=session, path=path,
                                                                        local=self.argv[2]))
            else:
                print("Please reference an alias or id. Example: !alias, or /41.")
        else:
            print("Please provide a source and destination: `$ iam cp !alias:/home/user/file.txt ~/`")


# ---------------------------
# Application Execution
# ---------------------------

if __name__ == '__main__':

    # Open session config
    with open(SESSION_PATH) as data:
        hosts = json.load(data)

    # Create new iam object with session list and arguments parsed
    iam = IAM(hosts, sys.argv)

    # Commands parsed as arguments
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
                iam.add(sys.argv[2], sys.argv[3], group)
        elif sys.argv[1] == "-l" or sys.argv[1] == "list":
            # List sessions
            iam.list()
        elif sys.argv[1] == "-f" or sys.argv[1] == "format":
            # Format identifiers
            iam.format()
        elif sys.argv[1] == "-c" or sys.argv[1] == "config":
            # Set configurations
            iam.config()
        elif sys.argv[1] == "-r" or sys.argv[1] == "remove":
            # Remove session
            iam.remove()
        elif sys.argv[1] == '-rg' or sys.argv[1] == "remove-group":
            iam.remove_group()
        elif sys.argv[1] == 'cp' or sys.argv[1] == "copy":
            iam.copy()
        else:
            # Normal connect or search
            iam.setup_session()
    else:
        # Nothing is defined - show help
        print("\t# -------------------------------------------------"
              "\n\t# iAM - The Simple and Speedy SSH Session Manager"
              "\n\t# Developed by Max Tuzzolino-Smith"
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
              "\n\n\t* Copy SSH public key:\n\t\t`$ iam [id or alias] -cid`"
              "\n\n\t* Copy file:\n\t\t`$ iam cp ![id or alias]:/path/to/file /path/to/destination` or reversed")

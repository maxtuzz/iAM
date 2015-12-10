# iAM
A simple, lightweight, SSH session manager tool

#### For now, only dependency is tabulate:
`sudo pip install tabulate`

You may need to specify which Python3.x version you want to run with depending on your version of Pip. 
For instance, pip3 defaults to Python3.5 - so this may need to be specified in source header at least until some VirtualEnv stuff is set up.

#### Status:
Development progressing as things that I think can be improved are added.

What needs to be done: 
* More customization - full path to `ssh` and `ssh-copy-id` need to be configurable in properties in case these protocols aren't included within a users path correctly
* Config needs to be formatted in standard ini-style using configparser instead of current json format for readability
* Remove by session command
* Remove by group command
* Testing and bugfixes


## Abstract 
The goal of this application is to first and formost provide more efficient methodologies of managing SSH sessions.

For those working in administration, a lot of time spent is remotely connecting to specific hosts and administrating endless applications across an Enterprise.There are some solutions at play that others utilize: 1. Look up servers on company wiki and remind yourself all the time. 2. Use a bulky GUI like RemoteNG which works great, but is hard to customize and setup for preferred use. You also have to manually search down a list before your eye catches on the service you are looking for. 3. Compile a list of hosts and search through list for keywords you remember about the host name or 4. Ctrl + R and search previous sessions from terminal history. 

iAM seeks to remedy this through providing a easy-to-use, terminal-based solution, designed for speed and a low gulf-of-execution. 

## Quick start from clone

##### Linux/MacOS:
1. Clone environment
    * `$ git clone .../iam.git`
2. Move environment to /opt/
    * `$ sudo cp -r iAM /opt`
4. Make yourself the owner of files
    * `$ sudo chown $USER:$USER /opt/iAM/*`
5. Symlink over to /usr/local/bin
    * `$ sudo ln -s /opt/iAM/iam.py /usr/local/bin`
6. Run anywhere from a terminal

##### Windows 
1. Install iAM to Program Files or anywhere convenient
2. Add iam directory to your PATH

## Features
* Application invocation through easy ‘iam’ command.
* Maintainable SSH lists
* Easy addition/removal of SSH sessions.
* SSH session groups. i.e. group by DEV, TEST, or PRODUCTION servers. 
* Easy SSH list search. 
* Session initiation through ‘iam [id]’ or 'iam [alias]'.
* Share external session lists between team members.
* High flexibility in how sessions lists are formatted.
* Customizable table output
* Easily copy ssh public keys to hosts

#### Soon to come ...
* 'Remove' commands for groups and specific sessions in list. 

## Table formats

Configured in config.json

Supported table formats are:

* “plain”
* “simple”
* “grid”
* “fancy_grid” <-- Default
* “pipe”
* “orgtbl”
* “rst”
* “mediawiki”
* “html”
* “latex”
* “latex_booktabs”

## Simple Use-Case

I am given a task to do a simple application upgrade of ‘graduate search’ app on astwebrttst01.its.auckland.ac.nz. I have never utilized this server before, as such I will have to add it to my host list.
```
$ iam -a astwebrttst01.its.auckland.ac.nz asttest1 AST
```
This command follows the following format … 
[Host address] [Host short name (alias)] [Host Group]

So essentially we are asking the iam application to add an SSH host, with a specified name and a specified group we want to add it to. In this case we are adding it to the “AST” group - where all AST based servers will be listed. 

Crap! We forgot the server name already (exactly the problem iAM tries to fix ;-) ). 
```
$ iam ast

Searching for ‘ast’ .. 
[30], asttest1, astwebrttst01.its.auckland.ac.nz

$ iam 30
```
(or of course, $ iam asttest1)
SSH connecting to astwebrttst01.its.auckland.ac.nz... 

You can use $ iam 30 [USERNAME] to connect under a different user other than what is specified in config.json
```
[ SSH SESSION INITIATED ]
```
This is but a simple use case. First we search for our server keyword that we know of, and iAM spits out results in the form of: identifier, host name, host address. 

We can then invoke iam [ID] to start a session with the address linked to that identifer! Easy as pie! And all with less characters than typing out the actual server address, not to mention searching to find out what it is.

From here on out, all I have to do is memorize the ID, or name of server to connect directly to it. Of course this isn’t ideal, so we can just do our fast search whenever we want.

### Configuring iAM

To set your default username:

```
$ iam config user [username]
```

To set table style:

```
$ iam config table [style]
```

### General Commands

```
$ iam [id] or [alias]
```
Connect to session

```
$ iam -l 
```
Lists all sessions. 
```
$ iam -l [group-name] 
```
Lists all sessions related to group. 
```
$ iam -r [alias] or [id]
```
Remove session

```
$ iam -rg [group_name]
```
Remove group 

Note: Removing has not yet been implemented and will need to be handled manually. 

```
iam format
``` 
This will iterate through session list and reformat identifiers so that there are no inconsistencies. Once 'remove' command
is implemented, this will run automatically to reindex identifiers. 

```
$ iam [id/alias] -cid
```
Invokes ssh-copy-id script on specified host to copy public key across for each access. This is only recommended for dev/test servers.

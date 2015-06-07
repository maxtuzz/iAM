# iAM
A simple, lightweight, SSH session manager tool

#### Status:
Undergoing heavy development. Most of the features work. Use in production environment at your own risk. 

## Abstract 
The goal of this application is to first and formost provide more efficient methodologies of managing SSH sessions.


For those working in administration, a lot of time spent is remotely connecting to specific hosts and administrating endless applications across an Enterprise.There are some solutions at play that others utilize: 1. Look up servers on company wiki and remind yourself all the time. 2. Use a bulky GUI like RemoteNG which works great, but is hard to customize and setup for preferred use. You also have to manually search down a list before your eye catches on the service you are looking for. 3. Compile a list of hosts and search through list for keywords you remember about the host name or 4. Ctrl + R and search previous sessions from terminal history. 

iAM seeks to remedy this through providing a easy-to-use, terminal-based solution, designed for speed and a low gulf-of-execution. 

## Features
* Application invocation through easy ‘iam’ command.
* Maintainable SSH lists
* Easy addition/removal of SSH sessions.
* SSH session groups. i.e. group by DEV, TEST, or PRODUCTION servers. 
* Easy SSH list search. 
* Session initiation through ‘iam SSH_ID’ or 'iam SSH_NAME'.
* Share external session lists between team members.
* High flexibility in how sessions lists are formatted. 

#### Soon to come ...
* Add default user (at the moment you can specify this in config.json). 
* 'Remove' commands for groups and specific sessions in list. 
* 'Format' command to relieve identification inconsistencies in manually generated session lists. 

## Simple Use-Case

I am given a task to do a simple application upgrade of ‘graduate search’ app on astwebrttst01.its.auckland.ac.nz. I have never utilized this server before, as such I will have to add it to my SSH list.
```
$ iam -a astwebrttst01.its.auckland.ac.nz asttest1 AST
```
This command follows the following format … 
[Host address] [Host short name] [Host Group]

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


### Other Commands... 
Other commands:
```
$ iam -l 
```
Lists all sessions. 
```
$ iam -l ‘group-name’ 
```
Lists all sessions related to group. 
```
$ iam -r 'session_name'
```
Remove session

```
$ iam -rg 'group_name'
```
Remove group 

Note: Removing has not yet been implemented and will need to be handled manually. 

```
iam format
``` 
This will iterate through session list and reformat identifiers so that there are no inconsistencies.

Note: format feature not yet implemented.  

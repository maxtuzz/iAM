# iAM
A simple, lightweight, SSH session manager tool

The goal of this project is first and foremost to provide efficient methodologies in the maintenance and management of SSH sessions. This application was developed to mitigate and reduce the time spent in remotely connecting to specific hosts through various automated approaches. iAM provides an elegant, and simple solution to group, connect, tunnel and manage ssh-keys between hosts.
This tool is used hundreds of times daily and has become a central part of members of the Application Engineering team, and other ITS team’s daily workflows.

#### For now, only dependency is tabulate:
`sudo pip install tabulate`

You may need to specify which Python3.x version you want to run with depending on your version of Pip. 
For instance, pip3 defaults to Python3.5 - so this may need to be specified in source header at least until some VirtualEnv stuff is set up.

#### Status:
Used in production daily. 
Development progressing.

Roadmap: 
* More customization - full path to `ssh` and `ssh-copy-id` need to be configurable in properties in case these protocols aren't included within a users path correctly - or a user prefers to use a custom SSH implementation. 
* Config needs to be formatted in standard ini-style using configparser instead of current json format for readability and for the sake of sticking to standards.
* Testing and bugfixes.

## Why iAM is useful:
For those working in distributed environments, a lot of time spent is remotely connecting to specific hosts. There are some solutions at play that can be utilized: 
1. Look up servers in company documentation to remind yourself (or memorize hostnames). 
2. Use a GUI like RemoteNG or Putty which works great, but is hard to customize and setup for preferred use. You also have to manually search down a list before your eye catches on the service you are looking for which is time consuming. 
3. Compile a list of hosts and search through list for keywords you remember about the host name .
4. Use your command history to search for previous sessions connected to. 

iAM seeks to remedy this through providing a easy-to-use, terminal-based solution, designed for speed and a low gulf-of-execution. 

## Quick start from clone

##### Linux/MacOS:
1. Clone environment
    * `$ git clone .../iam.git`
2. Move environment to /opt/
    * `$ sudo cp -r iAM /opt`
4. Make yourself the owner of files
    * `$ sudo chown -R $USER:$USER /opt/iAM/*`
5. Make sure iam is executable
   * `$ chmod +x /opt/iAM/iam.py`
5. Symlink over to /usr/local/bin
    * `$ sudo ln -s /opt/iAM/iam.py /usr/local/bin/iam`
6. Run anywhere from a terminal with `$ iam [arg1] [arg2]`

Or:
1. Clone to `$HOME/bin` and rename iam.py to iam and make it executable

##### Windows 
1. Install iAM to Program Files or anywhere convenient
2. Add iam directory to your PATH

## Features
* Application invocation through easy ‘iam’ command.
* Maintainable SSH lists.
* Easy addition/removal of SSH sessions.
* SSH session groups. i.e. group by DEV, TEST, or PRODUCTION servers. 
* Easy SSH list search. 
* Session initiation through ‘iam [id]’ or 'iam [alias]'.
* Share external session lists between team members.
* High flexibility in how sessions lists are formatted.
* Customizable table output.
* Easily copy ssh public keys to hosts.

#### Soon to come ...
* More customization.
* Easier distribution and obtainability of iam application.

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
$ iam -a astwebrttst01.its.auckland.ac.nz asttst1 AST
```
This command follows the following format … 
[Host address] [Host short name (alias)] [Host Group]

So essentially we are asking the iam application to add an SSH host, with a specified name and a specified group we want to add it to. In this case we are adding it to the “AST” group - where all AST based servers will be listed. 

But we've forgotten this long hostname already. 

```
$ iam ast

Searching for ‘ast’ .. 
[30], asttst1, astwebrttst01.its.auckland.ac.nz

$ iam 30
```

(or of course, `$ iam asttest1`)
`iAM now astwebrttst01.its.auckland.ac.nz...`

NOTE: You can use `$ iam 30 [USERNAME]` to connect under a different user other than what is specified in config.json

This is but a simple use case. First we search for our server keyword that we know of, and iAM spits out results in the form of: identifier, host name, host address. 

We can then invoke `$ iam [ID]` to start a session with the address linked to that identifer! Very easy and all with less characters than typing out the actual server address, not to mention searching to find out what it is.

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
Remove host

```
$ iam -rg [group_name]
```
Remove group 

```
iam format
``` 
This will iterate through session list and reformat identifiers so that there are no inconsistencies. Once 'remove' command
is implemented, this will run automatically to reindex identifiers. 

```
$ iam [id/alias] -cid
```
Invokes ssh-copy-id script on specified host to copy public key across for easy access.

#### License
Copyright 2015 Max Tuzzolino-Smith

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

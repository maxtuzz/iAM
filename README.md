# iAM
A simple, lightweight, SSH host management tool

The goal of this project is to provide efficient methodologies in the maintenance and management of SSH hosts. This small CLI was developed to mitigate and reduce the time spent in remotely connecting to specific hosts through various automated approaches. iAM provides an elegant, and simple solution to group, connect, tunnel and manage ssh-keys between hosts.

#### Status:
Used in production daily.

Roadmap:
* More customization - full path to `ssh` and `ssh-copy-id` need to be configurable in properties in case these protocols aren't included within a users path correctly - or a user prefers to use a custom SSH implementation.
* Testing and bugfixes.
* Fully implemented ssh functionality for better cross-system compatibility (possibly).

## Quick start from release
##### Linux/MacOS:
1. Head to the [releases page](https://github.com/maxtuzz/iAM/releases)
2. Download 'iam.tar.gz'
3. Extract with your favorite tool or through command line with `$ tar zxvf iam.tar.gz`
4. Run iam and create your default user `$ ./iam config user [username]`
5. Symlink to /usr/bin/local so that it is accessible anywhere `$ sudo ln -s {path_to_iam} /usr/local/bin/iam`

## Quick start from clone

##### For now, only dependency is tabulate:
`$ sudo pip install tabulate`
or `$ sudo pip install requirements.txt`

You may need to specify which Python3.x version you want to run with depending on your version of Pip.

Find out which version of pip you are using with `pip --version`.
If this says you are running Python 2.x you may need to use `pip3`.

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

```
$ iam -a appserver.test.mydomain.com apptst host_group
```
This command follows the following format …
[Host address] [Host short name (alias)] [Host Group]

So essentially we are asking the iam application to add an SSH host, with a specified name and a specified group we want to add it to. In this case we are adding it to the “host_group” group - where all 'host_group' based servers will be listed.

But we've forgotten this long hostname already.

```
$ iam app

Searching for ‘app’ ..
[30], apptst, appserver.test.mydomain.com

$ iam 30
```

(or of course, `$ iam apptst`)
`iAM now appserver.test.mydomain.com...`

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
$ iam [id or alias] -cid
```
Invokes ssh-copy-id script on specified host to copy public key across for easy access.

```
$ iam cp ![id or alias]:/path/to/file /path/to/destination
or
$ iam cp /path/to/file ![id or alias]:/path/to/destination 
```
Invokes 'scp' command to securely copy files between your local and host using iam aliases. 

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

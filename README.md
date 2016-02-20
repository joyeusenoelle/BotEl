# BotEl
BotEl is a Python bot for interacting with a TinyMUX chat server. It offers limited access to information outside the MUX world, and implements several useful or fun features that are difficult to implement in MUX softcode.

## Requirements

BotEl requires Python 3.5. It also needs the following modules:
* telnetlib
* ftplib
* urllib
* importlib
* time
* re
* random
* datetime

All of these should be part of the base Python 3 installation, but you may want to verify that they're installed.

## Installation

1. Copy `default_config.txt` to `config.txt`.
2. Fill in the configuration values in `config.txt`. These will vary depending on the settings of the MUSH you're connecting to.
3. That's it! You're done.

## Usage

Once `config.txt` is filled out, you can run BotEl from the command line:

    python BotEl.py

(If you have separate installations of Python 2 and Python 3, remember to use the correct command to invoke Python 3.)

BotEl will automatically connect and begin listening for input.

## Notes

BotEl expects a particular form of directed speech, which takes this form:

    Speaker [to Recipient]: message

You can implement this by placing this command on an object in the MUSH's master room or in the room where BotEl will exist:

    $^'([^' ]+) (.+)$:@switch [orflags(*%1,pP)]=1, {@switch [name(%#)]=[name(*%1)], @pemit %#=You shouldn't talk to yourself., {@switch [loc(*%1)]=[loc(%#)], {@switch [left(%2,1)]=:, {@pemit/contents [loc(%#)]=[u(oocflag)][name(%#)] <to [name(*%1)]> [right(%2,[sub([strlen(%2)], 1)])]}, \;, {@pemit/contents [loc(%#)]=[u(oocflag)][name(%#)][right(first(%2),[sub([strlen(first(%2))], 1)])] <to [name(*%1)]> [rest(%2)]}, {@pemit/contents [loc(%#)]=[u(oocflag)][name(%#)] \[to [name(*%1)]\]: %2}}, @pemit %#=That player is not here.}}, @pemit %#=No such player. (Make sure you're not addressing an object!)

Make sure to set the [R] flag on the command so it can correctly match text.

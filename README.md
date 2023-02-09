# Discord Course Config

Bot for setting up discord channels via commands. Designed for Massey CSIT server, which has lots of similar categories, one for each course.

## Setup

* Install discord.py (https://discordpy.readthedocs.io/en/latest/intro.html)
* Create a bot account and invite it to your server (https://discordpy.readthedocs.io/en/latest/discord.html)
  - Required Privileged Gateway Intents (Bot): Message Content Intent
  - Required Permissions (OAuth2): Manage Roles, Manage Channels, View Channels, Send Messages
  - Ensure its role is listed before any course roles (Server Settings > Roles)
* Copy the token (under Bot on https://discord.com/developers/applications/...) and save as token.txt
* Run the bot locally (python3 discord-config.py)

## Commands

The following commands are available (any server channel the bot can see will work, author must have admin permission):
* `!ccadd <course_names>`

Will add roles & channels for the listed courses. Course names must start with a 6-digit number, and are separated by a newline character. Example:
```
!ccadd
159271 Computational Thinking
158247 Database Design
```

*Note: This must be entered as a single command. Copy & paste or use `<shift-enter>`.*

* `!ccdelete <course_numbers>`

Will delete matching roles & channels using regular expression. Examples:
```
!ccdelete 159271|158247
!ccdelete 159.*
!ccdelete .*
```

*Note: Matching will be done via role names. Only 6-digit role names are considered, so non-course channels will never be deleted.*

**Watch out for active courses running in summer semester!**

* `!ccmatch <course_numbers>`

Like `!ccdelete` except that it only lists matching courses without deleting them.

## Other

For role auto-assignment, YAGPDB bot can be used:
* Setup of role auto-assign must be done manually on https://yagpdb.xyz/manage/ under Tools & Utilities > Role Commands
* Once set up, create new role menu (https://docs.yagpdb.xyz/tools-and-utilities/self-assignable-roles#role-menu)

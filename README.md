# Discord Config

Bot for setting up discord channels via commands. Designed for Massey CSIT server, which has lots of similar categories, one for each course.

# Setup

* Install discord.py (https://discordpy.readthedocs.io/en/latest/intro.html)
* Create a bot account and invite it to your server (https://discordpy.readthedocs.io/en/latest/discord.html)
  - requires Administrator permission
* Copy the token (under Bot on https://discord.com/developers/applications/...) and save as token.txt
* Run the bot locally (python3 discord-config.py)

# Commands

The following commands are available (any server channel will work, requires Administrator permission):
* !addcourse <course_names>

Will add roles & channels for the listed courses. Course names must start with a 6-digit number, and are separated by a newline character. Example:
```
!addcourse
159271 Computational Thinking
158247 Database Design
```

*Note: This must be entered as a single command. Copy & paste or use `<shift-enter>`.*

* !delcourse <course_numbers>

Will delete matching roles & channels. Course numbers must either be a single 6-digit number, or a 0-5 digit number followed by `*`. Examples:
```
!delcourse 159271
!delcourse 159*
!delcourse *
```

*Note: Matching will be done via role names. Only 6-digit role names are considered, so non-course channels will never be deleted.*

# Other

For role auto-assignment, YAGPDB bot can be used:
* Setup of role auto-assign must be done manually on https://yagpdb.xyz/manage/ under rolecommands
* Once set up, create new role menu (https://docs.yagpdb.xyz/tools-and-utilities/self-assignable-roles#role-menu)

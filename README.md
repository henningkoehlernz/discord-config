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
* !addcourse <course_nr>
* !delcourse <course_nr>

# Other

For role auto-assignment, YAGPDB bot can be used:
* Setup of role auto-assign must be done manually on https://yagpdb.xyz/manage/ under rolecommands
* Once set up, create new role menu (https://docs.yagpdb.xyz/tools-and-utilities/self-assignable-roles#role-menu)

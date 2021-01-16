# bot for setting up Massey CSIT discord server
import discord
from discord.ext import commands
import re

# only check guild messages, private messages don't contain a guild
intents = discord.Intents.none()
intents.guilds = True
intents.guild_messages = True
bot = commands.Bot(command_prefix='!', intents=intents)
# default channels that every course gets
course_channels = ["general", "assignments"]

def is_course_nr(course: str):
    return re.fullmatch("[0-9]{6}", course) != None

def get_course_nr(course: str):
    return course[:6]

def is_course_name(course: str):
    return is_course_nr(get_course_nr(course))

async def check_course(ctx, course: str):
    # courses are 6-digit numbers
    if not is_course_name(course):
        await ctx.send("'{}' is not a valid course name. Must start with a 6-digit number.".format(course))
        return False
    return True

async def filter_courses(ctx, pattern: str):
    # allows single course of list of courses with common prefix
    if re.fullmatch("[0-9]{6}|[0-9]{0,5}\*", pattern) == None:
        await ctx.send("'{}' is not a valid course pattern. Use a 6-digit number or a prefix followed by *.".format(pattern))
        return None
    # only consider 6-digit roles
    candidates = [ role.name for role in ctx.guild.roles if is_course_name(role.name) ]
    # convert pattern into regular expression
    reg_pattern = pattern.replace("*", ".*")
    return [ c for c in candidates if re.fullmatch(reg_pattern, c) != None ]

@bot.event
async def on_ready():
    print('Logged in as {} ID {}'.format(bot.user.name, bot.user.id))

@bot.command()
@commands.has_permissions(administrator=True)
async def addcourse(ctx, *, courses: str):
    for course in courses.split("\n"):
        if await check_course(ctx, course):
            # create role & category
            role = await ctx.guild.create_role(name=get_course_nr(course))
            category = await ctx.guild.create_category(name=course)
            # configure permissions
            await category.set_permissions(role, view_channel=True)
            await category.set_permissions(ctx.guild.default_role, view_channel=False)
            # create default channels
            for channel in course_channels:
                await category.create_text_channel(name=channel)
            await ctx.send("Created role & channels for {}".format(course))

@bot.command()
@commands.has_permissions(administrator=True)
async def delcourse(ctx, course_pattern: str):
    courses = await filter_courses(ctx, course_pattern)
    if courses == None:
        return
    categories = [ c for c in ctx.guild.categories if get_course_nr(c.name) in courses ]
    for c in categories:
        for ch in c.channels:
            await ch.delete()
        await c.delete()
    roles = [ r for r in ctx.guild.roles if r.name in courses ]
    for r in roles:
        await r.delete()
    # list full channel names for easy recreation
    deleted = [ c.name for c in categories ]
    await ctx.send("Deleted roles & channels for\n{}".format("\n".join(deleted)))

# run the bot - token is stored in separate file to avoid accidental check-in
with open('token.txt') as f:
    token = f.read();
bot.run(token)

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

async def check_course_name(ctx, course: str):
    if not is_course_name(course):
        await ctx.send("'{}' is not a valid course name. Must start with a 6-digit number.".format(course))
        return False
    return True

async def match_roles(ctx, pattern: str):
    # only consider roles that are valid course numbers
    course_roles = [ role for role in ctx.guild.roles if is_course_name(role.name) ]
    try:
        matched = [ role for role in course_roles if re.fullmatch(pattern, role.name) != None ]
        return matched
    except re.error as e:
        await ctx.send("RegExp error: {}".format(e))
    return None

@bot.event
async def on_ready():
    print('Logged in as {} ID {}'.format(bot.user.name, bot.user.id))

@bot.command()
@commands.has_permissions(administrator=True)
async def ccadd(ctx, *, courses: str):
    for course_name in courses.split("\n"):
        if await check_course_name(ctx, course_name):
            course_nr = get_course_nr(course_name)
            # check if role already exists
            existing = [ role for role in ctx.guild.roles if role.name == course_nr ]
            if existing:
                await ctx.send("Role {} already exists.".format(course_nr))
                continue
            # create role & category
            role = await ctx.guild.create_role(name=course_nr)
            category = await ctx.guild.create_category(name=course_name)
            # configure permissions
            await category.set_permissions(role, view_channel=True)
            await category.set_permissions(ctx.guild.default_role, view_channel=False)
            # create default channels
            for channel in course_channels:
                await category.create_text_channel(name=channel)
            await ctx.send("Created role & channels for {}".format(course_name))

@bot.command()
@commands.has_permissions(administrator=True)
async def ccdelete(ctx, pattern: str):
    roles = await match_roles(ctx, pattern)
    if roles == None:
        return
    for role in roles:
        categories = [ c for c in ctx.guild.categories if get_course_nr(c.name) == role.name ]
        for category in categories:
            try:
                # grant role to self so we can see the category to delete it
                await ctx.guild.me.add_roles(role)
                for channel in category.channels:
                    await channel.delete()
                await category.delete()
                await ctx.send("Deleted {}".format(category.name))
            except discord.Forbidden:
                await ctx.send("Failed to delete category {}. Check role order?".format(category.name))
                continue
        try:
            await role.delete()
        except discord.Forbidden:
            await ctx.send("Failed to delete role {}. Check role order?".format(role.name))

@bot.command()
@commands.has_permissions(administrator=True)
async def ccmatch(ctx, pattern: str):
    roles = await match_roles(ctx, pattern)
    if roles == None:
        return
    course_nrs = [ r.name for r in roles ]
    categories = [ c.name for c in ctx.guild.categories if get_course_nr(c.name) in course_nrs ]
    await ctx.send("{} matches the following:\n{}".format(pattern, "\n".join(categories)))

# run the bot - token is stored in separate file to avoid accidental check-in
with open('token.txt') as f:
    token = f.read();
bot.run(token)

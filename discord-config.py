# bot for setting up Massey CSIT discord server
import discord
from discord.ext import commands
import re

# only check guild messages, private messages don't contain a guild
intents = discord.Intents.none()
intents.guilds = True
intents.guild_messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)
# default channels that every course gets
course_channels = ["general", "assignments"]

def is_course_nr(course: str):
    return re.fullmatch("[0-9]{6}", course) != None

def get_course_nr(course: str):
    return course[:6]

def is_course_name(course: str):
    return is_course_nr(get_course_nr(course))

def role_usage(ctx, role):
    return " & ".join([ c.name for c in ctx.guild.categories if not c.overwrites_for(role).is_empty() ])

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
            # create role or use existing one
            existing = [ role for role in ctx.guild.roles if role.name == course_nr ]
            if existing:
                role = existing[0]
                #await ctx.send("Using existing role for {}.".format(course_nr))
            else:
                role = await ctx.guild.create_role(name=course_nr)
            #create category
            category = await ctx.guild.create_category(name=course_name)
            # configure permissions
            await category.set_permissions(role, view_channel=True)
            await category.set_permissions(ctx.guild.default_role, view_channel=False)
            # create default channels
            for channel in course_channels:
                await category.create_text_channel(name=channel)
            if existing:
                await ctx.send("Created channels for {}".format(course_name))
            else:
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

@bot.command()
@commands.has_permissions(administrator=True)
async def ccmatch(ctx, pattern: str):
    roles = await match_roles(ctx, pattern)
    if roles == None:
        return
    course_nrs = [ r.name for r in roles ]
    categories = [ c.name for c in ctx.guild.categories if get_course_nr(c.name) in course_nrs ]
    await ctx.send("{} matches the following:\n{}".format(pattern, "\n".join(categories)))

@bot.command()
@commands.has_permissions(administrator=True)
async def rcdelete(ctx, pattern: str):
    roles = await match_roles(ctx, pattern)
    if roles == None:
        return
    for role in roles:
        used_by = role_usage(ctx, role)
        if used_by:
            await ctx.send("Role {} still used by {}".format(role.name, used_by))
            continue
        try:
            await role.delete()
            await ctx.send("Deleted {}".format(role.name))
        except discord.Forbidden:
            await ctx.send("Failed to delete role {}. Check role order?".format(role.name))

@bot.command()
@commands.has_permissions(administrator=True)
async def rcmatch(ctx, pattern: str):
    roles = await match_roles(ctx, pattern)
    if roles == None:
        return
    roles_with_usage = [ "{} used by {}".format(r.name, role_usage(ctx, r)) for r in roles ]
    await ctx.send("{} matches the following:\n{}".format(pattern, "\n".join(roles_with_usage)))

# run the bot - token is stored in separate file to avoid accidental check-in
with open('token.txt') as f:
    token = f.read();
bot.run(token)

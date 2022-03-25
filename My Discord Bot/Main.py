#TOKEN : OTQxMzUxMTg1NTk4Nzg3NTk3.YgUrnA.k6GaiThfCVmXf-SVycSjBcctM98
#Client ID : 941351185598787597
#Client Secret : R0FnnQG4QwLzC3A8AKcjYjnOyfz-FPgq
#!/usr/bin/python
# coding: utf-8
# Doc String:
"""

load
*unload
*reload
level
*setprefix
setup
*setwelcom
info
*warn
wanrs
*rmwarn
getprefix
*clear
*kick
*ban
*unban
tas
say
helpme
userinfo
server


"""


import discord
from discord.ext import commands
import os
import time
import random
import json
# First Assigments
intents = discord.Intents.default()
intents.members = True
# client = discord.Client(intents=intents)
client = commands.Bot(command_prefix = '$', intents=intents)
# Removed Commands
client.remove_command('help')

# Main Functions
def auto_role(client, message):
    with open('roleid.json', 'r') as f:
        role_id = json.load(f)
    return role_id[str(message.guild.id)]

def set_up(client, message):
    with open('setup.json', 'r') as f:
        c_id = json.load(f)
    return c_id[str(message.guild.id)]
def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]


def save_warn(ctx, member: discord.Member):
    with open('warns.json', 'r') as f:
        warns = json.load(f)

        warns[str(member.id)] +1

    with open('warns.json', 'w') as f:
        json.dump(warns, f)

def remove_warn(ctx, member: discord.Member, amount: int):
    with open('warns.json', 'r') as f:
        warns = json.load(f)

        warns[str(member.id)] -= amount

    with open('warns.json', 'w') as f:
         json.dump(warns, f)
    
def warns_check(member: discord.Member):
    with open('warns.json', 'r') as f:
        warns = json.load(f)

        warns[str(member.id)]
    return warns
# Events
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Task Force 1.4.1'))
    print('-------< Bot Is Ready >-------')
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('درخواست شما **کامل نیست**.دوباره امتحان کنید:x:')
@client.event
async def on_guild_join(guild):
    # with open('prefixes.txt', 'r') as f:
    #     temp = json.load(f)
    
    # g_id = str(guild.id)
    name = str(guild.name)
    b = await guild.templates()
    if b == []:
        a = await guild.create_template(name = name, description="This is a simple template :)")
        # temp[str(guild.name)] = a
        with open('templates.txt', 'a') as f:
            f.write(str(a) + "\n")
            f.close()
    else:
        # temp[str(guild.name)] = b
        with open('templates.txt', 'a') as f:
            f.write(str(b) + "\n")
            f.close()
    

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(guild.id)] = "$"
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f)

@client.event
async def on_member_join(member):

    with open('setup.json', 'r') as f:
        c_id = json.load(f)
    welc = c_id[str(member.guild.id)]
    channel = client.get_channel(int(welc))
    embed = discord.Embed(title=f"Welcome {member.name}", description=f"Thanks for joining {member.guild.name}!", color=discord.Color.blue()) # F-Strings!
    embed.set_thumbnail(url=member.avatar_url) # Set the embed's thumbnail to the member's avatar image!
    await channel.send(embed=embed)

    icon = str(member.guild.icon_url)
    dm = await client.fetch_user(member.id)
    embed2 = discord.Embed(title="🥳 Welcome:", description=f"Welcome To {member.guild.name}! 🤩🥰", color=discord.Color.purple())
    embed2.set_thumbnail(url=icon)
    embed2.add_field(name="📜 Rules:", value="❗ Be Respectful of EVERYONE in Server. \n❗ Don't Post any Harmful and +18 Content! \n❗ Don't Advertise. \n❗ Don't Spam.", inline=False)
    embed2.set_footer(text="Don't Break The Rules And Have Fun.", icon_url=icon)
    embed2.set_author(name=member.guild.name, icon_url=icon)
    await dm.send(embed=embed2)

    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

    with open('warns.json', 'r') as f:
        warns = json.load(f)

    warns[str(member.guild.id)] = 0

    with open('warns.json', 'w') as f:
        json.dump(warns, f)

@client.event
async def on_message(message):
    if message.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)
        await update_data(users, message.author)
        await add_experience(users, message.author, 5)
        await level_up(users, message.author, message)

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
    await client.process_commands(message)

async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1
async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp


async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1 / 4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has leveled up to level {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end


# Commands

@client.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    client.load_extension(f'cog.{extension}')
    await ctx.send(f"{extension} Loaded")
@client.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    client.unload_extension(f'cog.{extension}')
    await ctx.send(f"{extension} Unloaded")
@client.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    client.unload_extension(f'cog.{extension}')
    client.load_extension(f'cog.{extension}')
    await ctx.send(f"{extension} Reloaded")

@client.command()
async def level(ctx, member: discord.Member = None):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'You are at level {lvl}!')
    else:
        id = member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'{member} is at level {lvl}!')

@client.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f)
    await ctx.send(f"The Prefix Was Changed to {prefix}")

@client.command()
async def setup(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefix = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title="Help : Setup Command", description="with this command you can Set up your welcome channel", color=ctx.author.color)
    embed.add_field(name=f"`{prefix}setwelcom` : ", value=f"Exm : {prefix}setwelcom [ Channel ID ]", inline=False)
    # embed.add_field(name=f"`{prefix}setrole` : ", value=f"Exm : {prefix}setrole [ Role ID ]", inline=False)
    # embed.add_field(name=f"`{prefix}rolereact` : ", value=f"Exm : {prefix}rolereact [ Message ] [ @Role ]", inline=False)
    
    embed.add_field(name="For More Infomation You Can Join the Support Server: ", value="Support server URL",inline=False)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(administrator=True)
async def setwelcom(ctx, channelid):
    with open('setup.json', 'r') as f:
        c_id = json.load(f)
    c_id[str(ctx.guild.id)] = channelid
    with open('setup.json', 'w') as f:
        json.dump(c_id, f)
    await ctx.send(f"Your Welcom Channel is <#{channelid}>")

@client.command()
async def info(ctx):
    embed = discord.Embed(title="Information :", description="Information About Bot", color=discord.Color.dark_gold())
    embed.add_field(name="Creator: ", value="Ali Nabati", inline=True)
    embed.add_field(name="Version: ", value="2.1", inline=True)
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason):
    with open('warns.json', 'r') as f:
        warns = json.load(f)
    if warns[str(member.id)] < 0:
        warns = 0
        ctx.send("An Error Raised Please Try Again this Command")
    else:
        warns[str(member.id)] + 1
    with open('warns.json', 'w') as f:
        json.dump(warns, f)
    # save_warn(ctx, member)
    dm = await client.fetch_user(member.id)
    em = discord.Embed(title="Warning", description=f"Server: {ctx.guild.name}\nReason: {reason}")
    embed = discord.Embed(title="Warning", description=f"{member.mention} You Have been Warned \n {member.guild.name}", color=discord.Color.red())
    await dm.send(embed=em)
    await ctx.send(embed=embed)
@client.command()
async def warns(ctx, user: discord.Member=None):
    if user is None:
        user = ctx.author
    with open('warns.json', 'r') as f:
        users = json.load(f)
    warns = users[str(user.id)]
    if warns < 0:
        # warns = 0
        await ctx.send(f'{user} dont have any warnings.')
    else:
        await ctx.send(f'{user} has {warns} warnings')

@client.command()
@commands.has_permissions(kick_members=True)
async def rmwarn(ctx, member: discord.Member, amount: int):
    with open('warns.json', 'r') as f:
        warns = json.load(f)

        warns[str(member.id)] -= amount

    with open('warns.json', 'w') as f:
        json.dump(warns, f)
    await ctx.send(f"Removed {amount} warnings from {member.name}!")

@client.command()
async def getprefix(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefix = prefixes[str(ctx.guild.id)]
    await ctx.reply(f"Your Server Prefix Is : {prefix}")


@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount : int):
    am = amount+1
    await ctx.channel.purge(limit=am)


@client.command(aliases=['siktir', 'dokme'])
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason=None):
    if reason is None:
        await ctx.send('چطور جرعت میکنی بدون دلیل کیک کنی؟؟؟')
        return
    await member.kick(reason=reason)
    await ctx.send(f'Successful :white_check_mark:\n*Kicked* **{member}** *Reason:* **{reason}**')
@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason=None):
    if reason is None:
        await ctx.send('چطور جرعت میکنی بدون دلیل بن کنی ممبر مردمو؟؟')
        return
    await member.ban(reason=reason)
    await ctx.send(f'Successful :white_check_mark:\n*Banned* **{member.mention}** *Reason:* **{reason}**')
@client.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Successful :white_check_mark:\n*Unbanned* **{user.mention}**')
            return

@client.command(aliases=['dice'])
async def tas(ctx):
    deice_num = ['1', '2', '3', '4', '5', '6', '7']
    embed1 = discord.Embed(title='درحال انداختن تاس', description='5 Sec', color=ctx.author.color)
    await ctx.send(embed=embed1)
    time.sleep(5)
    rand_answ = random.choice(deice_num)
    embed2 = discord.Embed(title='عدد تاس :', description=f'{rand_answ}', color=ctx.author.color)
    await ctx.send(embed=embed2)
    if rand_answ == '7':
        await ctx.send('**WTF** !! Mage 7 Darim??? *Ye Bar Dg Bendaz* :|')
        return

@client.command(aliases=['bego', 'speak'])
async def say(ctx, *, msg):
    await ctx.message.delete()
    await ctx.send(f'{msg}')


@client.command()
async def helpme(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefix = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title="Help Command", description="You Can Use These Commands:", color=ctx.author.color)
    # embed.add_field(name=f":white_check_mark: `{prefix}tictactoe [ @player ]` : ", value="New Discord Game: Tic Tac Toe", inline=False)
    embed.add_field(name=f":white_check_mark: `{prefix}getprefix` : ", value="Shows Your Server Prefix", inline=False)
    embed.add_field(name=f":white_check_mark: `{prefix}level` : ", value="Shows Your Level at Server", inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}tas / dice`', value='Dice', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}serverinfo`', value='Shows Server Information', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}admhelp`', value='Administrator Commands', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}setup` : ', value="it's help you to setup your welcome channel and more", inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}userinfo / stat / user / amar`', value="Shows User Information ( data joined to server, permissions, ... )", inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}info` : ', value="Give Some Information Aboute Bot", inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}say [ Text ]`', value='Say Something', inline=False)
    # embed.add_field(name=f':white_check_mark: `{prefix}donate`', value='Ways to Support Me', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}warns`', value='Warning of User', inline=False)
    embed.set_footer(text='Bot Create & Develped By Ali Nabati')
    await ctx.send(embed=embed)


@client.command()
async def admhelp(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefix = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title='Admin Help', description='Bot In Version: 1.7.0', color=ctx.author.color)
    embed.add_field(name=f':white_check_mark: `{prefix}setprefix [ new prefix ]` : ', value='Set a New Prefix For This Server', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}ban [ @member ]` : ', value='Ban Members From Server', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}unban [ Member#Tag ]` : ', value='Unban Members', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}kick [ @Member ]` : ', value='Kick Members From Server', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}warn [ @member ] [ Reason ]` : ', value='Warn To Members', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}rmwarn [ @member ] [ Amount : int ]` : ', value='Remove Members Warn', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}setup` : ', value="it's help you to setup your welcome channel and more", inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}Mute [ @member ] [ Reason ]` : ', value='Ban Members From Server', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}unmute [ @member ] [ Reason ]` : ', value='Ban Members From Server', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}clear [ amount ]` : ', value='Ban Members From Server', inline=False)
    # embed.add_field(name=f':white_check_mark: `{prefix}ban [ @member ]` : ', value='Ban Members From Server', inline=False)

    embed.set_footer(text='Bot Create & Develped By Ali Nabati')
    embed.set_author(name='By Ali Nabati')
    embed_react = await ctx.send(embed=embed)
    await embed_react.add_reaction('✅')    

# New Commands

@client.command(aliases=['stat', 'user', 'amar'])
async def userinfo(ctx, *, user: discord.Member = None): # b'\xfc'
    if user is None:
        user = ctx.author
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=user.color, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join position", value=str(members.index(user)+1))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    # embed.add_field(name="Member Status: ", value=user.status, inline=True)
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='User ID: ' + str(user.id))
    return await ctx.send(embed=embed)

@client.command()
async def server(ctx):
    date_format = "%a, %d %b %Y %I:%M %p"
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)
    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)
    # channels = str(ctx.guild.channels)
    created_at = str(ctx.guild.created_at.strftime(date_format))
    embed = discord.Embed(
        title=name + "'s Server Information",
        description=description,
        color=discord.Color.red()
    )
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name="Owner: ", value=owner, inline=True)
    embed.add_field(name="Server ID: ", value=id, inline=True)
    embed.add_field(name="Region: ", value=region, inline=True)
    embed.add_field(name="Member Count: ", value=memberCount, inline=True)
    embed.add_field(name="Server Created At: ", value=created_at, inline=True)
    await ctx.send(embed=embed)

for filename in os.listdir('./cog'):
    if filename.endswith('.py'):
        client.load_extension(f"cog.{filename[:-3]}")

client.run("YOUR TOKEN HERE")
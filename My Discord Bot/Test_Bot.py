import discord
from discord.ext import commands
import json

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



intents = discord.Intents().all()
client = commands.Bot(get_prefix, intents=intents)

client.remove_command('help')
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Task Force 1.4.1'))
    print('-------< Bot Is Ready >-------')
# @client.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send('درخواست شما **کامل نیست**.دوباره امتحان کنید:x:')


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
async def getprefix(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefix = prefixes[str(ctx.guild.id)]
    await ctx.reply(f"Your Server Prefix Is : {prefix}")

@client.command()
async def setup(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefix = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title="Help : Setup Command", description="with this command you can Set up your welcome channel", color=ctx.author.color)
    embed.add_field(name=f"`{prefix}setwelcom` : ", value=f"Exm : {prefix}setwelcom [ Channel ID ]", inline=False)
    # embed.add_field(name=f"`{prefix}setrole` : ", value=f"Exm : {prefix}setrole [ Role ID ]", inline=False)
    embed.add_field(name=f"`{prefix}rolereact` : ", value=f"Exm : {prefix}rolereact [ Message ] [ @Role ]", inline=False)
    
    embed.add_field(name="For More Infomation You Can Join the Support Server: ", value="Support server URL",inline=False)
    await ctx.send(embed=embed)


# @client.command()
# @commands.has_permissions(administrator=True)
# async def setrole(ctx, role: discord.Role):
#     with open('roleid.json', 'r') as f:
#         roleid = json.load(f)
        
#     roleid[str(ctx.guild.id)] = role.name
#     with open('roleid.json', 'w') as f:
#         json.dump(roleid, f)
#     await ctx.send(f"Role Were Set to `<@{role.name}>`")

# @client.command()
# async def giverol(ctx, member: discord.Member, role: discord.Role):
#     if role == None:
#         with open('roleid.json', 'r') as f:
#             roleid = json.load(f)
        
#         role1 = roleid[str(ctx.guild.id)] = role

#         a = discord.utils.get(ctx.guild.roles, name=role1)
#         await member.add_roles(a)
#     else:
#         b = discord.utils.get(ctx.guild.roles, name=role.name)
#         if b == None:
#             await ctx.send("In Role Vojood Nadarad!")
#         else:
#             await member.add_roles(b)


@client.command()
@commands.has_permissions(administrator=True)
async def setwelcom(ctx, channelid):
    with open('setup.json', 'r') as f:
        c_id = json.load(f)
    c_id[str(ctx.guild.id)] = channelid
    with open('setup.json', 'w') as f:
        json.dump(c_id, f)
    await ctx.send(f"Your Welcom Channel is <#{channelid}>")

# @client.command()
# @commands.has_permissions(manage_messages=True)
# async def mute(ctx, member: discord.Member, *, reason=None):
#     guild = ctx.guild
#     mutedrole = discord.utils.get(guild.roles, name="Mute")
#     if mutedrole == None:
#         mutedrole = guild.create_role(name="Mute")
#         for channel in guild.channels:
#             await channel.set_permissions(mutedrole, speak=False, send_messages=False, read_message_history=True)#, read_messages=False)
#     await member.add_roles(mutedrole)#, reason=reason)
#     if reason == None:
#         await ctx.send(f"{member.mention} Were *Muted*!")
#         await member.send(f"You were Muted in the Server *{guild.name}*")
#     else:
#         await ctx.send(f"{member.mention} Muted For *{reason}*")
#         await member.send(f"You were Muted in the Server *{guild.name}* For *{reason}*\nContact the server owner to Unmute")


# @client.command()
# @commands.has_permissions(manage_messages=True)
# async def unmute(ctx, member: discord.Member):
#     mutedrole = discord.utils.get(ctx.guild.roles, name="Mute")
#     await member.remove_roles(mutedrole)
#     await ctx.send(f"{member.mention} Unmuted!")
#     await member.send(f"You were Unmuted in the Server *{ctx.guild.name}*")



@client.command()
async def info(ctx):
    embed = discord.Embed(title="Information :", description="Information About Bot", color=discord.Color.dark_gold())
    embed.add_field(name="Creator: ", value="Ali Nabati", inline=True)
    embed.add_field(name="Version: ", value="2.1", inline=True)
    await ctx.send(embed=embed)
    # embed.add_field(name="", value="", inline=False)

# @client.command()
# async def rolereact(ctx, msg: str, role: discord.Role, channel: discord.channel):
#     with open('roleid.json', 'r') as f:
#         roleid = json.load(f)
#     roleid[str(ctx.guild.id)] = role.name
#     with open('roleid.json', 'r') as f:
#         json.dump(roleid, f)
#     channel_id = channel
#     embed = discord.Embed(title="Reaction Role", description=f"{msg}", color=discord.Color.green())

# @client.command()
# async def setmute(ctx, role: discord.Role):
#     embed = discord.Embed()




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

    # try:
    #     with open('warns.json', 'r') as f:
    #         users = json.load(f)

    #     warns = users[str(user.id)]

    #     await ctx.send(f'{user} has {warns} warnings')
    # except:
    #     await ctx.send(f'{user} dont have any warnings.')


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
async def helpme(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefix = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(title="Help Command", description="You Can Use These Commands:", color=ctx.author.color)
    embed.add_field(name=f":white_check_mark: `{prefix}getprefix` : ", value="Shows Your Server Prefix", inline=False)
    embed.add_field(name=f":white_check_mark: `{prefix}level` : ", value="Shows Your Level at Server", inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}tas / dice`', value='Dice', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}serverinfo`', value='Shows Server Information', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}admhelp`', value='Administrator Commands', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}userinfo / stat / user / amar`', value="Shows User Information ( data joined to server, permissions, ... )", inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}say`', value='Say Something', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}donate`', value='Ways to Support Me', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}warns`', value='Warning of User', inline=False)
    embed.set_footer(text='Bot Create & Develped By Ali Nabati')
    # embed.add_field(name=f"`{prefix}setprefix` : ", value="Change The Prefix ( Administrator Required! )", inline=False)
    await ctx.send(embed=embed)

@client.command()
# @commands.has_permissions(administrator=True)
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
    embed.add_field(name=f':white_check_mark: `{prefix}rwarn [ @member ] [ Amount : int ]` : ', value='Remove Members Warn', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}setup` : ', value="it's help you to setup your welcome channel and more", inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}Mute [ @member ] [ Reason ]` : ', value='Ban Members From Server', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}unmute [ @member ] [ Reason ]` : ', value='Ban Members From Server', inline=False)
    embed.add_field(name=f':white_check_mark: `{prefix}clear [ amount ]` : ', value='Ban Members From Server', inline=False)
    # embed.add_field(name=f':white_check_mark: `{prefix}ban [ @member ]` : ', value='Ban Members From Server', inline=False)

    embed.set_footer(text='Bot Create & Develped By Ali Nabati')
    embed.set_author(name='By Ali Nabati')
    embed_react = await ctx.send(embed=embed)
    await embed_react.add_reaction('✅')    



client.run('TOKEN')
from importlib import reload  
import lexicore.configReader as configReader
import discord
from discord.ext import commands, tasks
import redis
import os
import datetime
import time
import random
import lexicore.variding as variding
import secrets
import lexicore.numerals as numerals
import asyncio
import lexicore.compress as compressionAlgo
import math
import requests
from io import StringIO   
import colorsys
import io
from concurrent.futures import ThreadPoolExecutor, as_completed
import randomcolor
from PIL import Image, ImageDraw, ImageColor, ImageSequence
from urllib.request import urlopen
from lexicore.sorting import bubble as bubbleSort
from lexicore.sorting import cocktail as cocktailSort
from lexicore.sorting import bogo as bogoSort

#this just makes no errors happen
lexiRole, lexiId, token, prefixes = (None, None, None, [])

#this updates globals with anything in the config
globals().update(configReader.loadConfig())

try: 
    db = redis.from_url(os.environ.get("REDIS_URL"), decode_responses=True)
except:
    db = redis.from_url("redis://:p14a587f3bc40c7f85a691224d118543cef4c58d742d6d04f4d7be6290053880a@ec2-34-238-101-201.compute-1.amazonaws.com:19209", decode_responses=True)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=prefixes[0], intents=intents)

def getUserColor(ctx):
    for i in ctx.guild.get_member(bot.user.id).roles[::-1]:
        if i.color != discord.Color.from_rgb(0, 0, 0) and i.color != None:
            return i.color
    return discord.Color.from_rgb(0, 0, 0)

def getUserColorGuild(guild):
    for i in guild.get_member(bot.user.id).roles[::-1]:
        if i.color != discord.Color.from_rgb(0, 0, 0) and i.color != None:
            return i.color
    return discord.Color.from_rgb(0, 0, 0)

def getUserName(ctx):
    if ctx.guild.get_member(bot.user.id).nick == None:
        return ctx.guild.get_member(bot.user.id).name
    else:
        return ctx.guild.get_member(bot.user.id).nick

def getUserNameAuthor(author):
    if author.nick == None:
        return author.name
    else:
        return author.nick

#
#commands
#
def isWinter():
    async def predicate(ctx):
        return ctx.author.id == 681531347583631444
    return commands.check(predicate)

@bot.event
async def on_ready():
    print('Logged in as')
    print("Name:", bot.user.name + "#" + bot.user.discriminator)
    print("ID:", bot.user.id)
    # Status Stuff
    activity = discord.Activity(type=discord.ActivityType.unknown, name="For commands run L!help")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    #await bot.get_channel(log).send("Aravae Online")

@bot.event
async def on_raw_reaction_add(payload):
    #messageid = payload.message_id
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    user = bot.get_user(payload.user_id)

    if str(payload.emoji.name) == '❌' and (message.author.id == bot.user.id or user.id == 681531347583631444):
        await message.delete()
    else:
        pass

@bot.command()
async def addrole(ctx, *, arg):
    if ctx.author.id == 681531347583631444:
        try:
            await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name=arg), reason="I was told to")
        except:
            await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, id=int(arg)), reason="I was told to")

@bot.command()
async def userinfo(ctx, *args):
    userId = int(args[0].replace("<", "").replace("@", "").replace(">", "").replace("!", ""))
    user = ctx.guild.get_member(userId)
    lastMessage = None
    
    e = discord.Embed(colour=user.color)
    e.title = f"{user.name}#{user.discriminator}"
    e.description = ""
    e.description += f"`Name:` {user.name}"
    e.description += f"\n`Nickname:` {user.nick}"
    e.description += f"\n`Ping:` {user.mention}"
    e.description += f"\n`Roles:` {' '.join([f'<@&{i.id}>' for i in user.roles[1:]])}"
    e.description += f"\n`ID:` {user.id}"
    e.description += f"\n`Activities:` {', '.join([i.name for i in user.activities])}"
    e.description += f"\n`Perms:` {', '.join([f'{str.title(i[0].replace(chr(95), chr(32))) if i[1] else str()}' for i in user.guild_permissions])}".replace(" ,", "")
    e.description += f"\n`Flags:` {', '.join([f'{str.title(i[0].replace(chr(95), chr(32)))}' for i in user.public_flags.all()])}".replace(" ,", "")
    e.description += f"\n`Bot:` {user.bot}"
    e.description += f"\n`Representative:` {user.system}"
    e.description += f"\n`Created at:` {user.created_at} (UTC)"
    e.description += f"\n`Joined at:` {user.joined_at} (UTC)"
    e.description += f"\n`On mobile:` {user.is_on_mobile()}"
    e.description += f"\n`Verified:` {not user.pending}"
    e.description += f"\n`Status:`\n - `Current`: {user.status}\n - `Web`: {user.web_status}\n - `Mobile`: {user.mobile_status}\n - `Desktop`: {user.desktop_status}"
    e.set_thumbnail(url=user.avatar_url)
    message = await ctx.send(embed=e)


@bot.command()
async def bubble(ctx, *args):
    sort = bubbleSort.sort(int(args[0]))

    async with ctx.typing():
        image = Image.new("P", sort.widHig)
        image.save("bubble.gif", 'GIF', save_all=True, append_images=sort.images)
        await ctx.send(file=discord.File(fp="bubble.gif"))

@bot.command()
async def cocktail(ctx, *args):
    sort = cocktailSort.sort(int(args[0]))

    async with ctx.typing():
        image = Image.new("P", sort.widHig)
        image.save("cocktail.gif", 'GIF', save_all=True, append_images=sort.images)
        await ctx.send(file=discord.File(fp="cocktail.gif"))

@bot.command()
async def bogo(ctx, *args):
    sort = bogoSort.sort(int(args[0]))
    
    async with ctx.typing():
        image = Image.new("P", sort.widHig)
        image.save("bogo.gif", 'GIF', save_all=True, append_images=sort.images)
        await ctx.send(file=discord.File(fp="bogo.gif"))

def getAiImg(text, images):
    r = requests.post(
            "https://api.deepai.org/api/text2img",
            data={
                'text': text,
            },
            headers={'api-key': 'e1b08947-ff17-4c62-941b-bb5bb174aa81'}
        )
    images.append(discord.File(io.BytesIO(requests.get(r.json()["output_url"]).content), filename=f"aiImage{images.__len__()}.jpg"))

@bot.command()
async def aimg(ctx, *, arg):
    try:
        images = []
        futures = []
        executor = ThreadPoolExecutor(max_workers=10)
        imageCount = min(10, max(0, int(arg.split()[0])))
        imagesDone = 0

        e = discord.Embed(colour=getUserColor(ctx))
        e.title = f"Collecting images"
        e.description = f"{imagesDone}/{imageCount}"
        e.set_footer(text="Credits for ai go to Scott Ellison Reed at https://deepai.org/machine-learning-model/text2img")
        message = await ctx.send(embed=e)

        for _ in range(imageCount):
            futures.append(executor.submit(getAiImg, " ".join(arg.split()[1:]).replace("\\n", "\n"), images))

        for future in as_completed(futures):
            print(future.result())
            imagesDone += 1
            e.description = f"{imagesDone}/{imageCount}"
            await message.edit(embed=e)

        e.description = f"Requested by {getUserNameAuthor(ctx.author)}"
        e.title = " ".join(arg.split()[1:]).replace("\\n", "\n")
        e.set_footer(text="Credits for ai go to Scott Ellison Reed at https://deepai.org/machine-learning-model/text2img")
        #for i in images:
            #await ctx.send(file=i)
        await ctx.send(embed=e, files=images)
        await message.delete()
    except BaseException as exception:
        print(exception)

        e = discord.Embed(colour=getUserColor(ctx))
        e.title = f"Could not get image"
        e.description = ""
        await ctx.send(embed=e)

@bot.command()
async def capt(ctx):
    attachment = ctx.message.attachments[0]

    r = requests.post(
        "https://api.deepai.org/api/neuraltalk",
        data={
            'image': attachment.url,
        },
        headers={'api-key': 'e1b08947-ff17-4c62-941b-bb5bb174aa81'}
    )
    e = discord.Embed(colour=getUserColor(ctx))
    e.title = r.json()["output"]
    e.description = f"Description for {attachment.filename} made by an ai! Requested by {getUserNameAuthor(ctx.author)}"
    e.set_footer(text="Credits for ai go to Andrej Karpathy at https://deepai.org/machine-learning-model/neuraltalk")
    f = await attachment.to_file()
    await ctx.send(embed=e, file=f)

@bot.command()
async def faces(ctx):
    attachment = ctx.message.attachments[0]

    r = requests.post(
        "https://api.deepai.org/api/facial-recognition",
        data={
            'image': attachment.url,
        },
        headers={'api-key': 'e1b08947-ff17-4c62-941b-bb5bb174aa81'}
    )

    fd = urlopen(attachment.url)
    image_file = io.BytesIO(fd.read())
    im = Image.open(image_file).convert("RGBA")
    dr = ImageDraw.Draw(im)
    print(r.json())
    randc = randomcolor.RandomColor()

    for i in r.json()["output"]["faces"]:
        dr.rectangle([i["bounding_box"][0], i["bounding_box"][1], i["bounding_box"][0]+i["bounding_box"][2], i["bounding_box"][1]+i["bounding_box"][3]], outline=randc.generate(format_="rgb")[0], width=2)

    output = io.BytesIO()
    im.save(output, format="PNG")
    output.seek(0)
    f = discord.File(output)
    
    e = discord.Embed(colour=getUserColor(ctx))
    e.title = f"Located {len(r.json()['output']['faces'])} faces"
    e.description = f"Faces found by an ai! Requested by {getUserNameAuthor(ctx.author)}"
    e.set_footer(text="Credits for ai go to [UNKNOWN] at https://deepai.org/machine-learning-model/facial-recognition")
    await ctx.send(embed=e, file=f)

@bot.command()
async def sendanon(ctx, *, arg):
    if ctx.author.id == lexiId:
        args = arg.split()
        if (x := bot.get_guild(int(args[0]))) != None:
            try: 
                if (y:=discord.utils.get(x.channels, name=args[1])) != None:
                    e = discord.Embed(colour=getUserColorGuild(x))
                    e.description = " ".join(args[2:]).replace("\\n", "\n")
                    await y.send(embed=e)
                elif (y:=discord.utils.get(x.channels, id=int(args[1]))) != None:
                    e = discord.Embed(colour=getUserColorGuild(x))
                    e.description = " ".join(args[2:]).replace("\\n", "\n")
                    await y.send(embed=e)
            except: 
                e = discord.Embed(colour=getUserColor(ctx))
                e.description = f"Channel name/id \"{args[0]}\" not found in this guild"
                e.title = "Channel not found"
                await ctx.send(embed=e)
        else:
            e = discord.Embed(colour=getUserColor(ctx))
            e.description = f"Guild of id \"{args[0]}\" not found"
            e.title = "Guild not found"
            await ctx.send(embed=e)

@bot.command()
async def rename(ctx, *args):
    if ctx.author.id == lexiId:
        user = ctx.guild.get_member(int(args[0]))
        await user.edit(nick=" ".join(args[1:])[:31])

@bot.command()
async def ping(ctx, *args):
    e = discord.Embed(colour=getUserColor(ctx))
    e.description = f"Pong! {bot.latency*1000}ms"
    e.title = getUserName(ctx) + " PingPong"
    await ctx.send(embed=e)

@bot.command()
async def romnum(ctx, *args):
    e = discord.Embed(colour=getUserColor(ctx))
    e.description = str(int(args[0])) + " -> " + str(numerals.toNumerals(int(args[0])))
    e.title = getUserName(ctx) + " Number to Numerals"
    await ctx.send(embed=e)

@bot.command()
async def roll(ctx, *args):
    e = discord.Embed(colour=getUserColor(ctx))
    e.title = getUserName(ctx) + " Die Roller"

    dieSets = []

    for i in range(len(args)):
        if i >= 4:
            break
        dieSet = args[i].lower().split("d")
        dieSet.append(0)
        dieString = ""
        for i in range(max(min(int(dieSet[0]), 100), 1)):
            num = min(secrets.randbelow(max(int(dieSet[1]), 1) - 1) + 1, max(int(dieSet[1]), 1))
            dieSet[2] += num
            dieString += str(num) + ", "
            
        setattr(e, "_fields", getattr(e, "_fields", []) + [{
                    'inline': False,
                    'name': "d".join(dieSet[:2]),
                    'value': str(dieString[:-2])
                }])

        dieSets.append(dieSet)

    e.description = f"Total: " + str(sum([i[2] for i in dieSets]))
    await ctx.send(embed=e)

@bot.command()
async def send(ctx, *, arg):
    args = arg.split()
    
    try:
        if (x:=discord.utils.get(ctx.guild.channels, name=args[0])) != None:
            e = discord.Embed(colour=getUserColor(ctx))
            e.description = " ".join(args[1:]).replace("\\n", "\n")
            e.set_footer(text=f"Sent by @{getUserNameAuthor(ctx.author)} in #{ctx.channel.name} from {ctx.guild.name}")
            await x.send(embed=e)
        elif (x:=discord.utils.get(ctx.guild.channels, id=int(args[0]))) != None:
            e = discord.Embed(colour=getUserColor(ctx))
            e.description = " ".join(args[1:]).replace("\\n", "\n")
            e.set_footer(text=f"Sent by @{getUserNameAuthor(ctx.author)} in #{ctx.channel.name} from {ctx.guild.name}")
            await x.send(embed=e)
    except:
        e = discord.Embed(colour=getUserColor(ctx))
        e.description = f"Channel name/id \"{args[0]}\" not found in this guild"
        e.title = "Channel not found"
        await ctx.send(embed=e)

@bot.command()
async def sendext(ctx, *, arg):
    args = arg.split()

    if (x := bot.get_guild(int(args[0]))) != None:
        try: 
            if (y:=discord.utils.get(x.channels, name=args[1])) != None:
                e = discord.Embed(colour=getUserColorGuild(x))
                e.description = " ".join(args[2:]).replace("\\n", "\n")
                e.set_footer(text=f"Sent by @{getUserNameAuthor(ctx.author)} in #{ctx.channel.name} from {ctx.guild.name}")
                await y.send(embed=e)
            elif (y:=discord.utils.get(x.channels, id=int(args[1]))) != None:
                e = discord.Embed(colour=getUserColorGuild(x))
                e.description = " ".join(args[2:]).replace("\\n", "\n")
                e.set_footer(text=f"Sent by @{getUserNameAuthor(ctx.author)} in #{ctx.channel.name} from {ctx.guild.name}")
                await y.send(embed=e)
        except: 
            e = discord.Embed(colour=getUserColor(ctx))
            e.description = f"Channel name/id \"{args[0]}\" not found in this guild"
            e.title = "Channel not found"
            await ctx.send(embed=e)
    else:
        e = discord.Embed(colour=getUserColor(ctx))
        e.description = f"Guild of id \"{args[0]}\" not found"
        e.title = "Guild not found"
        await ctx.send(embed=e)

@bot.command()
async def senddm(ctx, *, arg):
    args = arg.split()

    try:
        if (x:=bot.get_user(int(args[0]))) != None:
            e = discord.Embed(colour=discord.Color(0))
            e.description = " ".join(args[1:]).replace("\\n", "\n")
            e.set_footer(text=f"Sent by @{getUserNameAuthor(ctx.author)} in #{ctx.channel.name} from {ctx.guild.name}\nReply within 5 minutes to reply to the sender if they have dms enabled.")
            y = await x.create_dm()
            await y.send(embed=e)

            await ctx.message.delete()

            z = await ctx.author.create_dm()
            zz = ctx.author

            def check1(message):
                return message.author == x and message.channel == y
            def check2(message):
                return message.author == zz and message.channel == z

            message1, message2 = (None, None)
            exitLoop = False
            while(not exitLoop):
                try:
                    message1 = await bot.wait_for('message', timeout=60*5, check=check1)
                except asyncio.TimeoutError:
                    exitLoop = True
                    pass
                else:
                    try:
                        r = message1.content
                    except:
                        r = ' '.join(args[1:]).replace('\\n', '\n')

                    if r.lower() == "eot":
                        exitLoop = True
                    else:
                        e.description = message1.content
                        e.set_footer(text=f"Sent by @{ctx.guild.get_member(int(message1.author.id)).name}#{ctx.guild.get_member(int(message1.author.id)).discriminator} in response to you saying \"{r}\"\nSend \"eot\" to end the chat.")

                        await z.send(embed=e)

                try:
                    message2 = await bot.wait_for('message', timeout=60*5, check=check2)
                except asyncio.TimeoutError:
                    exitLoop = True
                    pass
                else:
                    if message2.content.lower() == "eot":
                        exitLoop = True
                    else:
                        e.description = message2.content
                        e.set_footer(text=f"Sent by @{ctx.guild.get_member(int(message2.author.id)).name}#{ctx.guild.get_member(int(message2.author.id)).discriminator} in response to you saying \"{message1.content}\"\nSend \"eot\" to end the chat.")

                        await y.send(embed=e)
        else:
            raise BaseException
    except:
        e = discord.Embed(colour=getUserColor(ctx))
        e.description = f"User of id \"{args[0]}\" not found or had dms disabled"
        e.title = "User not found"
        await ctx.send(embed=e)

def chunkstring(string, length):
    return (string[0+i:length+i] for i in range(0, len(string), length))

@bot.command()
async def compress(ctx, *, arg, file=False, filename=""):
    global variding
    encoded = compressionAlgo.compress(arg)
    encoded = encoded[0] + "􀐏" + "􀐍".join("􀐎".join(i) for i in encoded[2])
    e = discord.Embed(colour=getUserColor(ctx))
    if not file:
        encoded = list(chunkstring("Compressed to " + str(len(encoded)/len(arg)*100) + "% of the size\n\n" + encoded, 1018))
        for i in encoded:
            e.description = "```" + i + "```"
            e.title = "Text Compressor"
            await ctx.send(embed=e)
    else:
        e.description = "Compressed to " + str(len(encoded)/len(arg)*100) + "% of the size\n\n"
        e.title = "File Compressor"
        file = StringIO(encoded)
        await ctx.send(embed=e, file=discord.File(file, filename + ".comp"))
 
@bot.command()
async def compressf(ctx):
    attachmentUrl = ctx.message.attachments[0].url
    fileRequest = requests.get(attachmentUrl)
    await compress(ctx, arg=fileRequest.text, file=True, filename=ctx.message.attachments[0].filename)

@bot.command()
async def decompressf(ctx):
    attachmentUrl = ctx.message.attachments[0].url
    fileRequest = requests.get(attachmentUrl)
    decoded = fileRequest.text.split("􀐏")
    decoded = compressionAlgo.decompress(decoded[0], [i.split("􀐎") for i in decoded[1].split("􀐍")])
    e = discord.Embed(colour=getUserColor(ctx))
    e.title = "File Decompressor"
    e.description = ""
    file = StringIO(decoded)
    await ctx.send(embed=e)
    await ctx.send(file=discord.File(file, ctx.message.attachments[0].filename[:-5]))

@bot.command()
async def decompress(ctx, *, arg):
    global variding
    decoded = arg.split("􀐏")
    decoded = compressionAlgo.decompress(decoded[0], [i.split("􀐎") for i in decoded[1].split("􀐍")])
    decoded = list(chunkstring(decoded, 1018))
    e = discord.Embed(colour=getUserColor(ctx))
    for i in decoded:
        e.description = "```" + i + "```"
        e.title = "Text Decompressor"
        await ctx.send(embed=e)

@bot.command()
async def encode(ctx, *args):
    global variding
    encoded = variding.encoder(" ".join(args), n=1)
    e = discord.Embed(colour=getUserColor(ctx))
    if encoded == "error":
        e.description = "Message too long for current settings"
        e.title = "Variding Encoder"
        await ctx.send(embed=e)
        return
    
    e.description = encoded
    e.title = "Variding Encoder"
    await ctx.send(embed=e)
    variding = reload(variding)

@bot.command()
async def decode(ctx, *args):
    global variding
    decoded = variding.decoder(" ".join(args))[0]
    print(" ".join(args), "---", decoded)
    e = discord.Embed(colour=getUserColor(ctx))
    e.description = decoded
    e.title = "Variding Decoder"
    await ctx.send(embed=e)
    variding = reload(variding)


bot.remove_command("help")
@bot.command()
async def help(ctx, *args):
    await ctx.message.delete()

    e = discord.Embed(colour=getUserColor(ctx))

    helpmessage = " - ``encode <text to encode>`` Encodes something in variding as long as result isnt over 2000 chars\n"
    helpmessage = helpmessage + " - ``decode <text to decode>`` Decodes an encoded text, may have to run it twice to decode correctly\n"
    helpmessage = helpmessage + " - ``roll <die count>d<die sides>`` Rolls specified dice specified times, accepts multiple die sets to roll, max 100 dice to roll per set and 4 sets\n"
    helpmessage = helpmessage + " - ``romnum <number>`` Converts a number to roman numerals\n"
    helpmessage = helpmessage + " - ``compress <text>`` Compresses text using up to 1000 iterations\n"
    helpmessage = helpmessage + " - ``decompress <text>`` Decompresses text\n"
    helpmessage = helpmessage + " - ``send <channel name/id> <message>`` Sends a message in another channel\n"
    helpmessage = helpmessage + " - ``senddm <user id> <message>`` Sends a dm to specified user\n"
    helpmessage = helpmessage + " - ``sendext <server id> <channel name/id> <message>`` Sends a message in another channel from another server (if the bot is in it)\n"
    helpmessage = helpmessage + " - ``sendanon <server id> <channel name/id> <message>`` Sends a message in another channel from another server (if the bot is in it) as noone, admin only\n"
    helpmessage = helpmessage + " - ``rename <user id> <name>`` Rename user by id, admin only\n"
    helpmessage = helpmessage + " - ``aimg <count> <image description>`` Gets an ai generated image given a description\n"
    helpmessage = helpmessage + " - ~~``faces <image file>`` Puts a box around all faces in an image recognized by an ai~~ broken\n"
    helpmessage = helpmessage + " - ``capt <image file>`` Gets an ai descriprion given an image \n"
    helpmessage = helpmessage + " - ``bogo <bars>`` Bogo sorts a randomized array, valid bars counts are 2-4 \n"
    helpmessage = helpmessage + " - ``bubble <bars>`` Bubble sorts a randomized array, valid bars counts are 2-16 \n"
    helpmessage = helpmessage + " - ``cocktail <bars>`` Cocktail sorts a randomized array, valid bars counts are 2-16 \n"
    helpmessage = helpmessage + " - ``userinfo <ping/id>`` Returns info about the user \n"
    helpmessage = helpmessage + " - ``ping`` Shows bot latency\n"
    helpmessage = helpmessage + " - ``help`` Shows this menu\n"
    helpmessage = helpmessage + "React to any message sent by the bot with ❌ to delete it\n"

    e.description = helpmessage
    e.title = getUserName(ctx) + " Help"
    await ctx.send(embed=e)

@bot.command()
@isWinter()
async def banname(ctx, *, arg):
    names = db.get("bannedNames")
    if names != None: db.set("bannedNames", db.get("bannedNames") + ";" + arg.lower())
    else: db.set("bannedNames", arg.lower())

@bot.command()
@isWinter()
async def unbanname(ctx, *, arg):
    names = db.get("bannedNames")
    if names != None: db.set("bannedNames", db.get("bannedNames").replace(arg, "").replace(";;", ";"))
    else: db.set("bannedNames", "")

@bot.command()
@isWinter()
async def bannednames(ctx):
    names = db.get("bannedNames")
    await ctx.send("\n".join(names.split(";")))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    try:
        if message.author.display_name.lower() in db.get("bannedNames").split(";") and message.author.bot:
            await message.delete()
            return
    except: pass

    for i in prefixes:
        if message.content.lower().startswith(i):
            if message.author.bot:
                await message.delete()
                return
            message.content = (prefixes[0] + message.content[len(i):]).replace("\n", "\\n")
            await bot.process_commands(message)
            await message.delete()

@bot.event
async def on_raw_message_edit(payload):
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    await on_message(message)


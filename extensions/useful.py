import discord
from discord.ext import commands
import json
import sys
import os
import aiohttp
import random
import asyncio
import re
from time import *
import __main__ as main
from subprocess import check_output
try:
    from pyshorteners import Shortener as shortener
    error = False
except:
    print("You don't have pyshorteners installed, installing it now...")
    try:
        check_output("pip3 install pyshorteners", shell=True)
        import pyshorteners
        error = False
        print("Pyshorteners succesfully installed.")
    except:
        print("Pyshorteners didn't succesfully install, useful extension not loaded...")
        error = True
try:
    import ffmpy
    error = False
except:
    print("You don't have FFMpy installed, installing it now...")
    try:
        check_output("pip3 install ffmpy", shell=True)
        import ffmpy
        error = False
        print("FFMpy succesfully installed.")
    except:
        print("FFMpy didn't succesfully install, exiting...")
        error = True
        
class useful:
    
    def __init__(self, bot):
        self.bot = bot
        main.cmds['useful'] = {'discrim': {'help': 'Searched through all members the bot can see to see if they have the given discriminator (the number after your name (example: YourName#4157))', 'usage': 'discrim <discrim'},
                                'emoteurl': {'help': 'Gives the url for the given emote.', 'usage': 'emoteurl <emote_name>'},
                                'genbotoauth': {'help': 'Generates an oauth url of the given bot.', 'usage': 'genbotoauth <bot_name>'},
                                'genoauth': {'help': 'Generates an oauth url for the given client id.', 'usage': 'genoauth <client_id>'},
                                'calc': {'help': 'Calculates a math problem so you don\'t have to.', 'usage': 'calc <problem>'},
                                'avatar': {'help': 'Shows the avatar of the given user.', 'usage': 'avatar <user>'},
                                'qrcode': {'help': 'Creates a qrcode of the given url.', 'usage': 'qrcode <url>'},
                                'ping': {'help': 'Pong!', 'usage': 'ping'},
                                'shorten': {'help': 'Shortens a link.', 'usage': 'shorten <url>'},
                                'convert': {'help': 'Converts a file to something like mp4 mp3 png gif all that stuff.', 'usage': 'convert <file_url>'}}
        
    async def on_message(self, message):
        msgchan = message.channel
        if await main.command(message, "discrim ", True):
            discriminator = message.content[len(main.prefix + "discrim "):].replace("#", "")
            if not discriminator.isdigit():
                await main.say(msgchan, "A Discriminator can only have digits and a #\nExamples\n`#4157`, `4157`")
                return
            members = [str(s) for s in list(self.bot.get_all_members()) if s.discriminator == discriminator]
            members = ", ".join(list(set(members)))
            if not members:
                await main.say(msgchan, "I could not find any users in any of the servers I'm in with a discriminator of `{}`".format(discriminator))
                return
            else:
                embed = discord.Embed(colour=0X00B6FF)
                embed.add_field(name="Discriminator #{}".format(discriminator), value=str(members), inline=False)
                try:
                    await main.say(msgchan, embed=embed)
                except:
                    await main.say(msgchan, "An unknown error occured while embedding.")
                
        elif await main.command(message, "emoteurl ", True):
            emote = message.content[len(main.prefix + "emoteulr "):]
            emote = discord.utils.find(lambda e: e.name == emote, message.server.emojis)
            await main.say(msgchan, emote.url)
            
        elif await main.command(message, "genbotoauth ", True):
            oauth_bot = message.content[len(main.prefix + "genbotoauth "):]
            oauth_bot = discord.utils.find(lambda m: m.name == oauth_bot, message.server.members)
            url = discord.utils.oauth_url(oauth_bot.id)
            await main.say(msgchan, "What perms should the invite have? \nFor help you can goto https://discordapi.com/permissions.html. Or just put 'all', 'admin' or 'None'.\nDoesn't always work")
            await asyncio.sleep(0.2)
            perms = await self.bot.wait_for_message(timeout=15, author=message.author)
            if not oauth_bot.bot:
                await main.say(msgchan, "User is not a bot.")
                return
            if perms.content.lower() == "all":
                await main.say(msgchan, ""
                "{}, here you go:\n"
                "{}&permissions=-1".format(message.author.mention, url))
            elif perms.content.lower() == "admin":
                await main.say(msgchan, ""
                "{}, here you go:\n"
                "{}&permissions=8".format(message.author.mention, url))
            elif perms.content.lower() == "none":
                await main.say(msgchan, ""
                "{}, here you go:\n"
                "{}".format(message.author.mention, url))
            elif perms.content:
                await main.say(msgchan, ""
                "{}, here you go:\n"
                "{}&permissions={}".format(message.author.mention, url, perms.content))
                
        elif await main.command(message, "genoauth ", True):
            oauth_bot = message.content[len(main.prefix + "genoauth "):]
            url = discord.utils.oauth_url(oauth_bot)
            await main.say(msgchan, "What perms should the invite have? \nFor help you can goto https://discordapi.com/permissions.html. Or just put 'all', 'admin' or 'None'.\nDoesn't always work")
            await asyncio.sleep(0.2)
            perms = await self.bot.wait_for_message(timeout=15, author=message.author)
            if perms.content.lower() == "all":
                await main.say(msgchan, ""
                "{}, here you go:\n"
                "{}&permissions=-1".format(message.author.mention, url))
            elif perms.content.lower() == "admin":
                await main.say(msgchan, ""
                "{}, here you go:\n"
                "{}&permissions=8".format(message.author.mention, url))
            elif perms.content.lower() == "none":
                await main.say(msgchan, ""
                "{}, here you go:\n"
                "{}".format(message.author.mention, url))
            elif perms.content:
                await main.say(msgchan, ""
                "{}, here you go:\n"
                "{}&permissions={}".format(message.author.mention, url, perms.content))
                
        elif await main.command(message, "calc ", True):
            prob = re.sub("[^0-9+-/* ]", "", message.content[len(main.prefix + "calc "):])
            try:
                answer = str(eval(prob))
                await main.say(msgchan, "`{}` = `{}`".format(prob, answer))
            except:
                await main.say(msgchan, "I couldn't solve that problem, it's too hard")
            
        elif await main.command(message, "avatar ", True):
            user = message.content[len(main.prefix + "avatar "):]
            user = discord.utils.get(message.server.members, name=user)
            if user.avatar_url:
                avatar = user.avatar_url
            else:
                avatar = user.default_avatar_url
            em = discord.Embed(color=discord.Color.red())
            em.add_field(name=user.mention + "'s avatar", value=avatar)
            em.set_image(url=avatar)
            await main.say(msgchan, embed=em)
            
        elif await main.command(message, "qrcode ", True):
            link = message.content[len(main.prefix + "qrcode "):]
            if link == "":
                await main.say(msgchan, "I can't make a qrcode of an empty string can I?")
                return
            else:
                shorten = shortener('Bitly', bitly_token='dd800abec74d5b12906b754c630cdf1451aea9e0')
                short_link = shorten.short(link)
            if not os.path.exists("data/qrcodes"):
                os.makedirs("data/qrcodes")
            async with aiohttp.get(shorten.qrcode(width=128, height=128)) as r:
                file = await r.content.read()
            number = random.randint(1000, 9999)
            fileloc = "data/qrcodes/qrcode{}.png".format(number)
            with open(fileloc, 'wb') as f:
                f.write(file)
                file = None
                f = None
            await self.bot.send_file(msgchan, fp="data/qrcodes/qrcode{}.png".format(number), filename="qrcode{}.png".format(number))
            os.remove("data/qrcodes/qrcode{}.png".format(number))
            
        elif await main.command(message, "convert ", True):
            file_url = message.content[len(main.prefix + "convert "):]
            await main.say(msgchan, "What is the output format?")
            await asyncio.sleep(0.5)
            output_format = await self.bot.wait_for_message(timeout=15, author=message.author)
            if output_format is None:
                await main.say(msgchan, "K then not.")
                return
            convertmsg = await main.say(msgchan, "Setting up...")
            # The copy of rickrolled part.
            if file_url == "rickrolled":
                file_url = "https://raw.githubusercontent.com/PlanetTeamSpeakk/PTSCogs-attributes/master/rickrolled.ogg"
                meme = True
                number = 'rickrolled_' + ''.join([random.choice('0123456789') for x in range(6)])
                if output_format == "rick astley":
                    input_format = "ogg"
                    output_format = "mp3"
            # The copy of We are number one part.
            elif file_url == "lazytown":
                meme = True
                file_url = "https://raw.githubusercontent.com/PlanetTeamSpeakk/PTSCogs-attributes/master/numberone.ogg"
                number = 'numberone_' + ''.join([random.choice('0123456789') for x in range(6)])
                if output_format == "number one":
                    input_format = "ogg"
                    output_format = "mp3"
            else:
                meme = False
                number = ''.join([random.choice('0123456789') for x in range(6)])
            if meme is False:
                form_found = False
                for i in range(6):
                    if file_url[len(file_url) - i:].startswith("."):
                        input_format = file_url[len(file_url) - i:]
                        form_found = True
                    else:
                        if form_found is not True:
                            form_found = False
                if form_found is not True:
                    convertmsg = await main.say(msgchan, "Your link is corrupt, it should end with something like .mp3, .mp4, .png, etc.")
                    print(form_found)
                    return
            if not os.path.exists("data/converter"):
                os.makedirs("data/converter")
            input = "data/converter/{}.{}".format(number, input_format)
            output = "data/converter/{}.{}".format(number, output_format.content)
            outputname = "{}.{}".format(number, output_format.content)
            convertmsg = await main.say(msgchan, "Downloading...")
            try:
                async with aiohttp.get(file_url) as r:
                    file = await r.content.read()
                with open(input, 'wb') as f:
                    f.write(file)
            except:
                convertmsg = await main.say(msgchan, "Could not download the file.")
                try:
                    os.remove(input)
                except:
                    pass
                return
            try:
                converter = ffmpy.FFmpeg(inputs={input: "-y"}, outputs={output: "-y"})
                convertmsg = await main.say(msgchan, "Converting...")
                converter.run()
            except:
                convertmsg = await main.say(msgchan, "Could not convert your file, an error occured.")
                try:
                    os.remove(input)
                    os.remove(output)
                except:
                    pass
                return
            await self.bot.send_file(message.channel, content="Convertion done!", fp=output, filename=outputname)
            os.remove(input)
            os.remove(output)
            
        elif await main.command(message, "print ", True):
            to_print = message.content[len(main.prefix + "print "):]
            print(to_print)
            
        elif await main.command(message, "ping", True):
            t1 = perf_counter()
            await self.bot.send_typing(msgchan)
            t2 = perf_counter()
            await main.say(msgchan, "Pong! Response time was **{}** seconds.".format(float(t2 - t1)))
            
        elif await main.command(message, "shorten ", True):
            url = message.content[len(main.prefix + "shorten "):]
            shorten = shortener('Bitly', bitly_token='dd800abec74d5b12906b754c630cdf1451aea9e0')
            if not url == "":
                await main.say(msgchan, "{}, here you go <{}>.".format(message.author.mention, shorten.short(url)))
            else:
                await main.say(msgchan, "You think I can shorten an empty string for you? That's not gonna work.")
                
        elif await main.command(message, "ctof ", True):
            celsius = message.content[len(main.prefix + "ctof "):]
            if (celsius == "") or not (self.is_digit(celsius)):
                await main.say(msgchan, "I can't convert an empty string to fahrenheit. Neither can I convert words.")
            else:
                celsius = float(celsius)
                await main.say(msgchan, "{}°C = {}°F ({}°K)".format(celsius, celsius * float(1.8) + 32, celsius - 273))

        elif await main.command(message, "ftoc ", True):
            fahrenheit = message.content[len(main.prefix + "ftoc "):]
            if (fahrenheit == "") or not (self.is_digit(fahrenheit)):
                await main.say(msgchan, "I can't convert an empty string to celsius. Neither can I convert words.")
            else:
                fahrenheit = float(fahrenheit)
                await main.say(msgchan, "{}°F = {}°C ({}°K)".format(fahrenheit, (fahrenheit - 32) / float(1.8), ((fahrenheit - 32) / float(1.8)) - 273))
        
    def is_digit(self, digit):
        check = re.compile('\d+(\.\d+)?')
        check2 = re.compile('\d+(\d+)?')
        if (check.match(digit)) or (check2.match(digit)):
            return True
        else:
            return False
        
def setup(bot):
    if error:
        raise RuntimeError("A library was not installed, could not load extension.")
    bot.add_cog(useful(bot))
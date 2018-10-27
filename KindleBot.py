import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
import asyncio
import json
import os
import youtube_dl
import urbandict
import datetime
import requests
import wikipedia
import urllib
import pathlib
import os
import zipfile
import io
import random
import csv
import pyjokes
#from PyLyrics import *

Client = discord.Client()
prefix = '!'
bot = commands.Bot(command_prefix=prefix)
extensions = ["Music"]
bot.remove_command("help")

champ_ids = []
champ_keys = []
champ_names = []
champ_titles = []

with open('champion.csv', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        champ_ids.append(row[0])
        champ_keys.append(row[1])
        champ_names.append(row[2])
        champ_titles.append(row[3])

summs_ids = []
summs_names = []
summs_descriptions = []
summs_levels = []
summs_keys = []

with open('summs.csv', 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        summs_ids.append(row[0])
        summs_names.append(row[1])
        summs_descriptions.append(row[2])
        summs_levels.append(row[3])
        summs_keys.append(row[4])

#pokemon stats
species_ids = []
species_name = []
species_height = []
species_weight = []
species_baseexp = []

with open('pokemon.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        species_ids.append(row[0])
        species_name.append(row[1])
        species_height.append(row[3])
        species_weight.append(row[4])
        species_baseexp.append(row[5])

species_ids_typecsv = []
species_type_id = []

with open('pokemon_types.csv', 'r') as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        species_ids_typecsv.append(row[0])
        species_type_id.append(row[1])

type_ids = []
type_name = []

with open('types.csv', 'r') as f:
    reader= csv.reader(f, delimiter=",")
    for row in reader:
        type_ids.append(row[0])
        type_name.append(row[1])

#1 = hp, 2 = attack, 3 = defense, 4 = special attack, 5 = special defense, 6 = speed
pokemon_base_ids = []
pokemon_stat_ids = []
pokemon_base_stats = []

with open('pokemon_stats.csv', 'r') as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        pokemon_base_ids.append(row[0])
        pokemon_stat_ids.append(row[1])
        pokemon_base_stats.append(row[2])

color_ids = []
colors = []

with open('pokemon_colors.csv', 'r') as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        color_ids.append(row[0])
        colors.append(row[1])

habitat_ids = []
habitats = []

with open('pokemon_habitats.csv', 'r') as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        habitat_ids.append(row[0])
        habitats.append(row[1])

shape_ids = []
shapes = []

with open('pokemon_shapes.csv', 'r') as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        shape_ids.append(row[0])
        shapes.append(row[1])

pokemon_species_ids = []
pokemon_species_identifier = []
pokemon_species_generation = []
pokemon_species_evolved = []
pokemon_species_color = []
pokemon_species_shape = []
pokemon_species_habitat = []
pokemon_species_catch = []
pokemon_species_happiness = []

with open('pokemon_species.csv', 'r') as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        pokemon_species_ids.append(row[0])
        pokemon_species_identifier.append(row[1])
        pokemon_species_generation.append(row[2])
        pokemon_species_evolved.append(row[3])
        pokemon_species_color.append(row[5])
        pokemon_species_shape.append(row[6])
        pokemon_species_habitat.append(row[7])
        pokemon_species_catch.append(row[9])
        pokemon_species_happiness.append(row[10])

#for henle
henle_composers = []
henle_piecegroups = []
henle_ordernums = []
with open('works.csv', 'r') as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        henle_composers.append(row[0])
        henle_piecegroups.append(row[1])
        henle_ordernums.append(row[2])

#for imslp
imslp_composers = []
imslp_piecegroups = []
with open('imslp.csv', 'r') as f:
    reader = csv.reader(f, delimiter=",")
    for row in reader:
        imslp_composers.append(row[0])
        imslp_piecegroups.append(row[1])

#connect the bot online
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name='Good Music'))

class Main_Commands():
    def __init__(self, bot):
        self.bot = bot

#custom help command
@bot.command(pass_context = True)
async def help(ctx):
    """Commands for the bot"""
    embed = discord.Embed(title=":robot: UrbanBot Commands", description="Prefix is '!' by default, but is subject to change", color=0xffffff)
    embed.add_field(name=":question: Help Command Menu", value="""1. Music Commands
                                                                        \n2. Need for Madness Commands
                                                                        \n3. Search/Utility Commands
                                                                        \n4. Server Commands
                                                                        \n5. Picture and Meme
                                                                        \n6. League of Legends Commands
                                                                        \n7. Classical Piano Commands
                                                                        \n8. NSFW Commands
                                                                        \n9. Joke/Quote Commands
                                                                        \n10. Mod/Admin Commands""")
    embed.set_footer(text="Discord", icon_url="https://www.shareicon.net/data/512x512/2017/06/21/887435_logo_512x512.png")
    await bot.say(embed=embed)
    await bot.say("Select an option from the menu above")
    msg = await bot.wait_for_message(author = ctx.message.author)
    reply = msg.content

    embed2 = discord.Embed(title=":robot: UrbanBot Commands", description="Prefix is '!' by default, but is subject to change", color=0xffffff)

    if reply == "1":
        embed2.add_field(name=":notes: Music Commands", value="""***join*** - bot joins the voice channel the user is summoning it from
                                                            \n***play <Search Query/YouTube Link>*** - search through youtube and play the first video found or play your youtube link
                                                            \n***pause*** - pauses the song
                                                            \n***resume*** - resumes playing the song
                                                            \n***stop*** - clears queue and stops all music
                                                            \n***playing*** - gives information about current song playing
                                                            \n***dc*** - disconnects the bot from the voice channel
                                                            \n***lyrics*** - get the lyrics of a song""")
    elif reply == "2":
        embed2.add_field(name=":race_car: Need For Madness Commands", value="""***nfmplayer <playerName>*** - profile information about a player
                                                                            \n***nfmclan <clanName>*** - information about a clan
                                                                            \n***nfmstage <stageName>*** - information about a specific stage
                                                                            \n***nfmcar <carName>*** - information about a specific car
                                                                            \n***nfmlinks*** - important links related to NFM
                                                                            \n***nfmstats*** - reference to what java variables in the NFM source code represent""")
    elif reply == "3":
        embed2.add_field(name=":mag: Search/Utility Commands", value="""***dict <word>*** - look up a word in the Oxford dictionary
                                                                        \n***urbandict <word>*** - look up a word in Urban Dictionary
                                                                        \n***wiki <entry>*** - look up an article in Wikipedia
                                                                        \n***weather <city>(,2-Letter-State-Abbrev)(,2-Letter-Country-Abbrev*** - look up the weather in a certain city""")
    elif reply == "4":
        embed2.add_field(name=":earth_americas: Server/Help Commands", value="""***user <name>*** - get information about a user in the server (Case Sensitive!)
                                                                        \n***server*** - get information about the server you're in right now
                                                                        \n***help*** - shows this message
                                                                        \n***info*** - shows information about this bot""")
    elif reply == "5":
        embed2.add_field(name=":frame_photo: Picture and Meme Commands", value="""***dog*** - random picture of a dog
                                                                            \n***fox*** - random picture of a fox
                                                                            \n***cat*** - random picture of a cat
                                                                            \n***bird*** - random picture of a bird
                                                                            \n***flower*** - random picture of a tree
                                                                            \n***tree*** - random picture of a tree
                                                                            \n***findpic*** - find a picture of something on Pixabay
                                                                            \n***randpic*** - get a random picture from Pixabay
                                                                            \n***makeameme*** - make a meme using the bot's instructions""")
    elif reply == "6":
        embed2.add_field(name=":crossed_swords: League of Legends Commands", value="""\n***lol <region> <summoner name>*** - information about a player in League of Legends
                                                                    \n***lolmatch <region> <summoner name>*** - current match a player is in
                                                                    \n***lolchamp <champion*** - returns detailed information about a specific champion""")
    elif reply == "7":
        embed2.add_field(name="<:Piano:404389994497703947> Classical Piano Commands", value="""***henle <composer>*** - look up pieces by various composers and view the Henle difficulties for each piece. You can also pass the argument "composers" to see all the composers available.
                                                                                            \n***imslp <composer>*** - look up sheet music by various composers by entering the composer's name and then picking the piece group. You can also pass the argument "composers" to see all the composers available.
                                                                                            """)
    elif reply == "8":
        embed2.add_field(name=":smirk: NSFW Commands", value="""***boobs*** - random picture of boobs
                                                        \n***ass*** - random picture of ass
                                                        \n***hentai <tag>*** - random hentai gif. Tags are:
                                                        \n\t1. Pussy
                                                        \n\t2. Boobs
                                                        \n\t3. Anal
                                                        \n\t4. Lesbian
                                                        \n\t5. BJ
                                                        \n\t6. Cum""")
    elif reply == "9":
        embed2.add_field(name=":speech_balloon: Joke Commands", value="""***yomama*** - random yomama joke
                                                                        \n***chuck*** - random Chuck Norris joke
                                                                        \n***insult*** - random insult
                                                                        \n***trump <user>*** - random trump insult
                                                                        \n***dadjoke*** - random dad joke
                                                                        \n***yesorno*** - it returns...well yes or no
                                                                        \n***crappyjoke*** - gives you a random crappy programming joke
                                                                        \n***leet <mode> <sentence>*** - translate a sentence between English and 1337 5|>34|<, modes can either be 'english' or 'leet'""")
        embed2.add_field(name=":thought_balloon: Quote Commands", value="""\n***trumpquote*** - random trump quote
                                                                          \n***randquote*** - random quote
                                                                          \n***findquote <filter> <value/name>*** - find a quote through filter; the following are the 3 possible filters:
                                                                          \n\t1. author - find a quote by a specific author
                                                                          \n\t2. contains - find a quote containing a certain word/words
                                                                          \n\t3. tag - find a quote with a specific tag""")
    elif reply == "10":
        embed2.add_field(name=":crown: Mod/Admin Commands", value="""***clearmessages <# of messages>*** - clears a certain number of messages in a specific channel (if the bot has rights to do so)
                                                                \n***prefix <new prefix>*** - change the bot's prefix (Warning: it's a universal change across ALL servers""")

    else:
        embed2.add_field(name=":x: Error", value="Not a valid entry")
    
    embed2.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed2.set_thumbnail(url='https://s3.amazonaws.com/files.enjin.com/292623/Web_Dev/images/discord-icon-7.png')
    embed2.set_footer(text="Discord", icon_url='https://www.shareicon.net/data/512x512/2017/06/21/887435_logo_512x512.png')

    await bot.say(embed=embed2)

@bot.command()
async def info():
    """Return bot info"""
    appinfo = await bot.application_info()

    membercount = 0
    for server in bot.servers:
        for member in server.members:
            membercount += 1
    
    embed = discord.Embed(title=":robot: UrbanBot Info", description="A private general purpose discord bot.", color=0x000000)
    embed.add_field(name=":tools: Made By", value=appinfo.owner.mention)
    embed.add_field(name=":calendar_spiral: Made On", value=bot.user.created_at)
    embed.add_field(name=":busts_in_silhouette: Number of Servers", value=str(len(bot.servers)))
    embed.add_field(name=":handshake: Number of Members", value=str(membercount))
    embed.add_field(name=":desktop: Made With", value="[Discord.py Async](https://github.com/Rapptz/discord.py)")
    embed.add_field(name=":link: Other Links", value="[General Server](https://discord.gg/sSqnYJb)"
                                                        + "\n[Discord.py Help Server](https://discord.gg/r3sSKJJ)")
    embed.set_thumbnail(url=appinfo.icon_url)
    embed.set_footer(text="Discord", icon_url='https://www.shareicon.net/data/512x512/2017/06/21/887435_logo_512x512.png')

    await bot.say(embed=embed)

#test commands for development purposes
@bot.command()
async def hello():
    """Test Command"""
    embed = discord.Embed(title="World", description="Embed test", colour=0xf44242)
    await bot.say(embed=embed)

@bot.command()
async def ping():
    """Test Command 2"""
    await bot.say("Pong!")

@bot.command()
async def rules():
    """Read the rules of the server"""
    await bot.say("Check the rules channel (if there isn't, use common sense!)")

#change the prefix, for certain users only
@bot.command()
@commands.has_permissions(manage_server = True)
async def prefix(pref):
    """Change the bot's prefix"""
    bot.command_prefix=pref
    pref_string = "Prefix changed to: " + pref
    await bot.say(pref_string)

@bot.event
async def on_member_join(member):
    #for aim
    if member.server.id == '326099786413506563':
        channel = member.server.get_channel("352540159121686551")
    #for personal server
    elif member.server.id == '247587233358544897':    
        channel = member.server.get_channel("382974608829054978")
    #for piano server
    elif member.server.id == '397500118846144524':    
        channel = member.server.get_channel("397514525911547916")
        
    fmt = 'Welcome to the {1.name} Discord server, {0.mention}, please read the rules and enjoy your stay.'
    await bot.send_message(channel, fmt.format(member, member.server))

@bot.event
async def on_member_remove(member):
    #for aim
    if member.server.id == '326099786413506563':
        channel = member.server.get_channel("352540159121686551")
    #for personal server
    elif member.server.id == '247587233358544897':    
        channel = member.server.get_channel("382974608829054978")
    #for piano server
    elif member.server.id == '397500118846144524':    
        channel = member.server.get_channel("397514525911547916")
    fmt = '{0.mention} has left the server.'
    await bot.send_message(channel, fmt.format(member, member.server))

#bot clears certain number of latest messages in text channel
@bot.command(pass_context=True)
@commands.has_permissions(administrator = True)
async def clearmessages(ctx, number):
    """Clears messages(admins only)"""
    messages = []
    number = int(number)#int cast
    async for x in bot.logs_from(ctx.message.channel, limit = number):
        messages.append(x)
    await bot.delete_messages(messages)

@bot.command()
async def urban(*, word: str):
    """Browse Urban Dictionary."""
    defi = urbandict.define(word)

    definition = defi[0]['def'] #definition of the word
    example = defi[0]['example'] #example of usage (if available)

    #make an embedded message colored blue
    embed = discord.Embed(title=":mag:" + word, description=definition, color=0x0062f4)
    embed.add_field(name = ":bulb: Example", value = example, inline = False)
    embed.set_footer(text="Urban Dictionary API", icon_url='https://vignette.wikia.nocookie.net/logopedia/images/a/a7/UDAppIcon.jpg/revision/latest?cb=20170422211150')
    embed.set_thumbnail(url='https://s3.amazonaws.com/pushbullet-uploads/ujxPklLhvyK-RGDsDKNxGPDh29VWVd5iJOh8hkiBTRyC/urban_dictionary.jpg?w=188&h=188&fit=crop')
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    await bot.say(embed=embed)

#weather command
@bot.command()
async def weather(*, area):
    """Get the weather in a certain city. If your city is in a different country, just do 'CityName,CountryAbbrev'"""
    url = "http://api.openweathermap.org/data/2.5/weather?appid=7431c5a61cb80d9ad48cd390f3e1e409&q=" + area

    json_data = requests.get(url).json()
    city = json_data['name'] + ", " + json_data['sys']['country']
    celcius = int(round(json_data['main']['temp']-273))
    farenheight = int(round(9.0/5.0*celcius+32))
    c_min = int(json_data['main']['temp_min']-273.0)
    c_max = int(json_data['main']['temp_max']-273.0)
    f_min = int(9.0/5.0*c_min+32)
    f_max = int(9.0/5.0*c_max+32)
    
    embed = discord.Embed(title="Weather in " + city + ":cityscape:", description=json_data['weather'][0]['description'], color=0x00ff00)
    embed.add_field(name=":thermometer: Temperature (C)", value=celcius)
    embed.add_field(name=":thermometer: Temperature (F)", value=farenheight)
    embed.add_field(name=":scales: Range (C)", value=str(c_min)+" - "+str(c_max))
    embed.add_field(name=":scales: Range (F)", value=str(f_min)+" - "+str(f_max))
    embed.add_field(name=":droplet: Humidity", value=str(json_data['main']['humidity'])+"%")
    embed.add_field(name=":wind_blowing_face: Wind Speed", value=str(json_data['wind']['speed']) + " km/h")
    embed.set_footer(text="Open Weather Map", icon_url="https://lh3.googleusercontent.com/7cQ8YkOKxsDHOT3fXap_dOLvbvKrfn0mMuSFdqNTM267wA3MAV9D4rvHRdc-y3H89A=w300")
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    if json_data['weather'][0]['main'] == 'Clouds':
        embed.set_thumbnail(url="https://openclipart.org/image/800px/svg_to_png/235807/Storm-Clouds-Icon.png")
    elif json_data['weather'][0]['main'] == 'Smoke':
        embed.set_thumbnail(url="https://d30y9cdsu7xlg0.cloudfront.net/png/123807-200.png")
    elif json_data['weather'][0]['main'] == 'Snow':
        embed.set_thumbnail(url="http://www.free-icons-download.net/images/blue-snow-icon-38706.png")
    elif json_data['weather'][0]['main'] == 'Rain':
        embed.set_thumbnail(url="https://cdn3.iconfinder.com/data/icons/picons-weather/57/15_heavy_rain-512.png")
    elif json_data['weather'][0]['main'] == 'Thumderstorm':
        embed.set_thumbnail(url="https://cdn0.iconfinder.com/data/icons/weather-3/512/rain_with_sun1-512.png")
    elif json_data['weather'][0]['main'] == 'Drizzle':
        embed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/weather-118/48/Drizzle-128.png")
    elif json_data['weather'][0]['main'] == 'Mist':
        embed.set_thumbnail(url='http://icons.iconarchive.com/icons/icons-land/weather/128/Fog-icon.png')
    elif json_data['weather'][0]['main'] == 'Fog' or json_data['weather'][0]['main'] == 'Haze':
        embed.set_thumbnail(url="https://cdn0.iconfinder.com/data/icons/large-weather-icons/512/Heavy_fog.png")
    elif json_data['weather'][0]['main'] == 'Clear':
        embed.set_thumbnail(url="https://s3.amazonaws.com/user-media.venngage.com/935086-5110f175564395a54dbdf0437452cd26.jpg")
    await bot.say(embed=embed)

#user information
@bot.command()
async def user(*, discorduser: discord.Member):
    """Get information about a specific user (Case Sensitive!)"""
    roles = discorduser.roles
    role_string = str(roles[0].name)
    for x in range (1, len(roles)):
        role_string = str(roles[x].name) + ", " + role_string

    print(role_string)
    embed = discord.Embed(title=":dark_sunglasses: User Info For: " + discorduser.display_name, description="ID: " + discorduser.id, color=0xcc1818)
    embed.add_field(name=":two_men_holding_hands: Server", value=discorduser.server)
    embed.add_field(name=":clipboard: Roles", value=role_string)
    embed.add_field(name=":vertical_traffic_light: Status", value=discorduser.status)
    embed.add_field(name=":video_game: Currently Playing", value=discorduser.game)
    embed.add_field(name=":calendar_spiral: Discord Join Date", value=discorduser.created_at.strftime("%m/%d/%y"))
    embed.add_field(name=":calendar_spiral: Server Join Date", value=discorduser.joined_at.strftime("%m/%d/%y"))
    embed.add_field(name=":robot: Bot", value=discorduser.bot)
    if discorduser.avatar_url=="":
        embed.set_thumbnail(url=discorduser.default_avatar_url)
    else:
        embed.set_thumbnail(url=discorduser.avatar_url)
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="Discord", icon_url='https://www.shareicon.net/data/512x512/2017/06/21/887435_logo_512x512.png')
    await bot.say(embed=embed)

#╲⎝⧹╲⎝⧹╲⎝⧹╲⎝⧹Cool⧸⎠╱⧸⎠╱⧸⎠╱⧸⎠╱#
@bot.command(pass_context=True)
async def server(ctx):
    """Get information about the server you're in right now"""
    server = ctx.message.server

    roles = list(reversed(server.role_hierarchy))
    role_string = str(roles[0].name)
    for x in range (1, len(roles)):
        role_string = str(roles[x].name) + ", " + role_string

    """channels = list(server.channels)
    channel_string = ""
    print(channels[0].name)
    for x in range (0, len(channels)):
        channel_string = channel_string + channels[x].name + "\n"""

    emojis = list(server.emojis)
    emoji_string = str(emojis[0].name)
    for x in range (1, len(emojis)):
        emoji_string = emojis[x].name + ", " + emoji_string 

    print(emoji_string)

    embed = discord.Embed(title="Server Info", color=0xc44805)
    embed.add_field(name=":newspaper2: Server Name", value=server.name)
    embed.add_field(name=":heavy_plus_sign: Server ID", value=server.id)
    embed.add_field(name=":two_men_holding_hands: Number of Members", value=server.member_count)
    embed.add_field(name=":calendar_spiral: Server Creation Date", value=server.created_at.strftime("%m/%d/%y"))
    embed.add_field(name=":clipboard: Roles", value=role_string)
    #embed.add_field(name=":speech_balloon: Channels", value=channel_string)
    embed.add_field(name=":map: Region", value=server.region)
    embed.add_field(name=":crown: Owner", value=server.owner)
    embed.add_field(name=":radio: Default Channel", value=server.default_channel)
    embed.add_field(name=":zzz: AFK Timeout", value=str(server.afk_timeout) + "s")
    try:
        embed.add_field(name=":orange_book: Custom Emojis", value=emoji_string)
    except:
        embed.add_field(name=":orange_book: Custom Emojis", value="None")
    embed.set_thumbnail(url=server.icon_url)
    embed.set_author(name="UrbanBot")
    embed.set_footer(text="Discord", icon_url='https://www.shareicon.net/data/512x512/2017/06/21/887435_logo_512x512.png')
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    await bot.say(embed=embed)

#search wikipedia
@bot.command()
async def wiki(*, article):
    """Search for wikipedia articles (English Wikipedia Only)"""
    wiki = wikipedia.page(wikipedia.search(article, results=1))
    
    embed = discord.Embed(title=":mag_right: " + wiki.title, description=wiki.url, color=0xFFFF00)
    embed.add_field(name=":blue_book: Description", value=wikipedia.summary(article, sentences=3))
    embed.set_thumbnail(url=wiki.images[0])
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="Wikipedia", icon_url='https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1200px-Wikipedia-logo-v2.svg.png')
    await bot.say(embed=embed)

#look up a word in the dictionary
@bot.command()
async def dict(*, word):
    """Look up a word and get the definition, synonyms, and antonyms"""
    app_id = '458b10ed'
    app_key = 'd69f8eb1fecab1cad9fec24ee13a86c1'

    url1 = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/' + word.lower()
    json_dict = requests.get(url1, headers = {'app_id': app_id, 'app_key': app_key}).json()

    url2 = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/en/' + word.lower() + '/synonyms;antonyms'
    r = requests.get(url2, headers = {'app_id': app_id, 'app_key': app_key})

    definition = json_dict['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0] + '.'
    
    embed = discord.Embed(title=":closed_book: Oxford Dictionary", description="Word: " + word, color=0x551a8b)
    embed.add_field(name=":paperclip: Definition", value=definition)
    try:
        example = json_dict['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['examples'][0]['text'] + '.'
        embed.add_field(name=":pencil2: Example", value=example)
    except:
        embed.add_field(name=":pencil2: Example", value='N/A')
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_thumbnail(url='http://www.krbe.com/wp-content/uploads/sites/115/2017/02/d19c1a2a07fa63bd2a86bca70dfa6d56_41788864.oxford.png')
    embed.set_footer(text="Oxford Dictionaries API", icon_url='https://pbs.twimg.com/profile_images/875679902216970241/NAw23Gdg_400x400.jpg')
    await bot.say(embed=embed)

#league of legends user information
@bot.command()
async def lol(region, *, user):
    """Get league of legends information"""
    if region.lower() == 'na':
        region = 'NA1'
    elif region.lower() == 'euw':
        region = 'EUW1'
    elif region.lower() == 'eun':
        region = 'EUN1'
    elif region.lower() == 'oce':
        region = 'OC1'
    api_key = 'RGAPI-a7ff64ee-756e-458f-b089-5a1e7c4ff14d'
    url_basic = 'https://' + region + '.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + user + '?api_key=' + str(api_key)
    print(url_basic)
    """
        embed = discord.Embed(title=":x: Error", description="Summoner " + summoner + " does not exist.", color=0x16a9bc)
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="Riot Games API", icon_url='https://orig00.deviantart.net/6fba/f/2016/311/4/5/lolalpha_launcher_by_giorgsavv-danohsj.png')
        embed.set_thumbnail(url="http://2.bp.blogspot.com/-HqSOKIIV59A/U8WP4WFW28I/AAAAAAAAT5U/qTSiV9UgvUY/s1600/icon.png")

        await bot.say(embed=embed)
        return
    """
    
    json1 = requests.get(url_basic).json()
    print(json1)

    try:
        status = json1['status']['message']

        embed = discord.Embed(title=":x: Error", description="Summoner " + user + " does not exist.", color=0x16a9bc)
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="Riot Games API", icon_url='https://orig00.deviantart.net/6fba/f/2016/311/4/5/lolalpha_launcher_by_giorgsavv-danohsj.png')
        embed.set_thumbnail(url="http://2.bp.blogspot.com/-HqSOKIIV59A/U8WP4WFW28I/AAAAAAAAT5U/qTSiV9UgvUY/s1600/icon.png")

        await bot.say(embed=embed)
        return
    except:
        print("Success! Getting data")
    
    user_id = json1['id']
    account_id = json1['accountId']
    level = json1['summonerLevel']

    embed = discord.Embed(title=":video_game: Summoner: " + json1['name'], description="Summoner ID: " + str(user_id), color=0x16a9bc)
    embed.add_field(name=":crown: Level", value=str(level))
    embed.add_field(name=":level_slider: Account ID", value=str(account_id))
    embed.add_field(name=":earth_americas: Region", value=region)

    url_rank = 'https://' + region + '.api.riotgames.com/lol/league/v3/positions/by-summoner/' + str(user_id) + '?api_key=' + str(api_key)
    json2 = requests.get(url_rank).json()
    solo_rank = 'N/A'
    flex_rank = 'N/A'
    tree_rank = 'N/A'
    
    for x in range(0, len(json2)):
        if json2[x]['queueType'] == 'RANKED_SOLO_5x5':
            solo_rank = json2[x]['tier'] + " " + json2[x]['rank'] + ", " + str(json2[x]['leaguePoints']) + "LP"
            if json2[x]['tier'] == 'BRONZE':
                embed.set_thumbnail(url='https://www.lol-smurfs.com/blog/wp-content/uploads/2017/01/bronzei.png')
            elif json2[x]['tier'] == 'SILVER':
                embed.set_thumbnail(url='https://vignette.wikia.nocookie.net/leagueoflegends/images/3/3f/SilverBadgeSeason2.png/revision/latest?cb=20130928162033')
            elif json2[x]['tier'] == 'GOLD':
                embed.set_thumbnail(url='https://vignette.wikia.nocookie.net/leagueoflegends/images/7/77/GoldBadgeSeason2.png/revision/latest?cb=20130928162204')
            elif json2[x]['tier'] == 'PLATINUM':
                embed.set_thumbnail(url='https://pro-rankedboost.netdna-ssl.com/wp-content/uploads/2014/09/platinum-rewards-lol.png')
            elif json2[x]['tier'] == 'DIAMOND':
                embed.set_thumbnail(url='https://www.lol-smurfs.com/blog/wp-content/uploads/2017/01/diamondi.png')
            elif json2[x]['tier'] == 'MASTER':
                embed.set_thumbnail(url='https://pro-rankedboost.netdna-ssl.com/wp-content/uploads/2014/09/master-rewards-lol.png')
            elif json2[x]['tier'] == 'CHALLENGER':
                embed.set_thumbnail(url='https://pro-rankedboost.netdna-ssl.com/wp-content/uploads/2014/09/challenger-rewards-lol.png')
        elif json2[x]['queueType'] == 'RANKED_FLEX_SR':
            flex_rank = json2[x]['tier'] + " " + json2[x]['rank'] + ", " + str(json2[x]['leaguePoints']) + "LP"
    
    embed.add_field(name=":large_blue_diamond: Solo Queue Rank", value=solo_rank)
    embed.add_field(name=":large_orange_diamond: Flex Queue Rank", value=flex_rank)
    embed.add_field(name=":palm_tree: Twisted Treeline Rank", value=tree_rank)
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="Riot Games API", icon_url='https://orig00.deviantart.net/6fba/f/2016/311/4/5/lolalpha_launcher_by_giorgsavv-danohsj.png')
    #embed.set_image(url='https://avatar.leagueoflegends.com/' + region + '/' + json1['name'] + '.png')
    #print('https://avatar.leagueoflegends.com/' + region + '/' + json1['name'] + '.png')
    await bot.say(embed=embed)

#random yomama joke
@bot.command()
async def yomama():
    """Random Yo Mama Joke"""
    json_data = requests.get('http://api.yomomma.info/').json()
    embed = discord.Embed(title=":large_orange_diamond: Yo Mama Joke", description=json_data['joke'], color=0x228B22)
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="yomomma.info", icon_url='https://i.ytimg.com/vi/wvw1NWMtYTk/maxresdefault.jpg')

    await bot.say(embed=embed)

#print out the NFM stat variables
@bot.command()
async def nfmstats():
    """Statistics and their respective java variable"""
    embed = discord.Embed(title=":hotsprings: NFM Java Statistics", description="Which statistic corresponds to which variable", color=0xff69b4)
    embed.set_thumbnail(url="https://media.giphy.com/media/11YVnpLvl58K2s/200w.gif")
    embed.add_field(name="Top Speed", value="int swits[][]\nEach element is as such: {gear 1, gear 2, gear3}")
    embed.add_field(name="Acceleration", value="float acelf[][]\nEach element is as such: {how fast car can move from rest position, accel1, accel2}")
    embed.add_field(name="Hand Break", value="int handb[]")
    embed.add_field(name="Turn Sensitivity", value="int turn[]")
    embed.add_field(name="Grip", value="float grip[]")
    embed.add_field(name="Handling Statbar", value="float dishandle[]")
    embed.add_field(name="Lifts Other Cars", value="int lift[]")
    embed.add_field(name="Gets Lifted", value="int revlift[]")
    embed.add_field(name="Bounciness", value="float bounce[]")
    embed.add_field(name="Aerial Rotation/Spin Speed", value="float airs[]")
    embed.add_field(name="Aerial Control", value="int airc[]")
    embed.add_field(name="Strength", value="float moment[]")
    embed.add_field(name="Strength Statbar", value="float outdam[]")
    embed.add_field(name="External Car Tolerance", value="float comprad[]")
    embed.add_field(name="Track Tolerance", value="float simag[]")
    embed.add_field(name="Pushing", value="int push[]")
    embed.add_field(name="Gets Pushed", value="int revpush[]")
    embed.add_field(name="Roof Breakage", value="int msquash[]")
    embed.add_field(name="Damage Multiplier", value="float dammult[]")
    embed.add_field(name="Collision Radius", value="int clrad[]")
    embed.add_field(name="Health", value="int[] maxmag")
    embed.add_field(name="Car Name", value="String[] names")
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="All Data Provided by Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")
    
    await bot.say(embed=embed)

#all the links you'll need for need for madness
@bot.command()
async def nfmlinks():
    """Important NFM links that may prove to be useful"""
    embed = discord.Embed(title=":link: Need for Madness Links", description="All the useful NFM related links", color=0xed10c4)
    embed.set_thumbnail(url="https://media.giphy.com/media/11YVnpLvl58K2s/200w.gif")
    embed.add_field(name=":race_car: General NFM Stuff", value="""[Official NFM Site](http://multiplayer.needformadness.com)
                                                                    \n[NFM Wiki](http://http://needformadness.wikia.com/wiki/Need_For_Madness_Wiki)
                                                                    \n[AIM Forums](http://http://aimgames.forummotion.com/)""")
    embed.add_field(name=":video_game: Addons", value="""[DS Addons](http://dscore.webcindario.com/software/addons.php)
                                                        \n[Phy Addons](http://aimgames.forummotion.com/t4203-nfmm-phy-addons-and-other-cool-stuff)
                                                        \n[Phy Addons(alternative link if you don't have an AIM account)](https://www.facebook.com/NeedForMadness/posts/990653057638811)""")
    embed.add_field(name=":bookmark_tabs: Fixed Source Code Downloads", value="""[NFM 1 Source Code](http://mediafire.com?nc7jp3t6k5u50ty)
                                                                                \n[NFM 2 Source Code](https://github.com/HulaSamsquanch/unfm2jg/releases)
                                                                                \n[NFM Multiplayer Source Code](https://goo.gl/iFqNRG)""")
    embed.add_field(name=":tools: Java Editing Stuff", value="""[Java](https://java.com/en/download/)
                                                                \n[Java SDK](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)
                                                                \n[Eclipse Neon](https://www.eclipse.org/downloads/packages/release/neon/3)
                                                                \n[BlueJ 3.04 (If you're working with older code)](http://www.bluej.org/download/files/bluejsetup-304.exe)
                                                                \n[JDK Project](http://jd.benow.ca/)
                                                                \n[Online Decompiler](http://www.javadecompilers.com/)""")
    embed.add_field(name=":mag: Misc", value="""[OpenMPT (listening to .mod and .xm files)](https://openmpt.org/)
                                                        \n[Blender (other software for making your car model)](https://www.blender.org/)""")
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="All Data Provided by Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")

    await bot.say(embed=embed)

@bot.command()
async def nfmplayer(*, player):
    """General profile information of a certain player"""
    player_o = player
    
    player = player.replace(" ", "_")
    
    url_car = "http://multiplayer.needformadness.com/cars/lists/" + player + ".txt?reqlo=500"
    url_stage = "http://multiplayer.needformadness.com/tracks/lists/" + player + ".txt?reqlo=823"
    url_info = "http://multiplayer.needformadness.com/profiles/" + player + "/info.txt?req=412"
    url_friends = "http://multiplayer.needformadness.com/profiles/" + player + "/friends.txt?req=253"

    cartext = requests.get(url_car)
    cars = cartext.text
    cars = cars[7:len(cars)-3]
    cars = cars.replace(",", "\n")
    car_list = cars.splitlines()

    stagetext = requests.get(url_stage)
    stages = stagetext.text
    stages = stages[9:len(stages)-3]
    stages = stages.replace(",", "\n")
    stage_list = stages.splitlines()

    infotext = requests.get(url_info)
    userinfo = infotext.text
    userinfo = userinfo.replace("|", "\n")
    info_list = userinfo.splitlines()
    bio = "N/A"
    clan = "N/A"
    theme_song = "N/A"
    race = "N/A"
    waste = "N/A"
    total = "N/A"

    friendtext = requests.get(url_friends)
    friends = friendtext.text
    friends = friends.replace("|", "\n")
    friends_list = friends.splitlines()

    newmod = info_list[0].replace(" ", "_")
    if info_list[0] != "" and info_list[0] != '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">':
        theme_song = "[" + info_list[0] + "](http://multiplayer.needformadness.com/tracks/music/" + newmod.replace(")", "\)") + ".zip)"
    if info_list[2] != "" and info_list[0] != '<head>':
        race = info_list[2]
    if info_list[3] != "" and info_list[3] != '<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>':
        waste = info_list[3]
    if info_list[4] != "" and info_list[4] != '<title>404 - File or directory not found.</title>':
        clan = info_list[4]
    if info_list[8] != "" and info_list[8] != "fieldset{padding:0 15px 10px 15px;} ":
        bio = info_list[8]

    if race == "<head>":
        race = "N/A"
    if waste == '<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1"/>':
        waste = "N/A"

    try:
        total = str(int(race) + int(waste))
    except:
        print("Couldn't add the total")
    
    temp_friends_string = "N/A"

    if len(friends_list) > 0:
        if '<!DOCTYPE html' not in friends_list[0] and friends_list[0] != "\n":
            temp_friends_string = ""
            if (friends.count('\n') + 1 > 10):
                for x in range(0, 10):
                    temp_friends_string = temp_friends_string + friends_list[x] + "\n"

                temp_friends_string = temp_friends_string + "\n...and " + str(friends.count('\n') - 9) + " more"
            else:
               for x in range (0, len(friends_list) - 1):
                   temp_friends_string = temp_friends_string + friends_list[x] + "\n"

    cars_list = cars.splitlines()
    stages_list = stages.splitlines()
    temp_car_string = "N/A"
    temp_stage_string = "N/A"

    try:
        if car_list[0] == 'PE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">':
            temp_car_string = "N/A"
        else:
            temp_car_string = ""
            if (cars.count('\n') + 1 > 10):
                for x in range (0, 10):
                    temp_car_string = temp_car_string + car_list[x] + "\n"
                temp_car_string = temp_car_string + "\n...and " + str(cars.count('\n') - 9) + " more"
            else:
                for x in range (0, len(car_list)):
                    temp_car_string = temp_car_string + car_list[x] + "\n"
    except:
        temp_car_string = "N/A"

    try:
        if stage_list[0] == ' html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">':
            temp_stage_string = "N/A"
        else:
            temp_stage_string = ""
            if (stages.count('\n') + 1 > 10):
                for x in range (0, 10):
                    temp_stage_string = temp_stage_string + stage_list[x] + "\n"
                temp_stage_string = temp_stage_string + "\n...and " + str(stages.count('\n') - 9) + " more"
            else:
                for x in range (0, len(stage_list) - 1):
                    temp_stage_string = temp_stage_string + stage_list[x] + "\n"
    except:
        temp_car_string = "N/A"

    if bio == "N/A" and clan == "N/A" and theme_song == "N/A" and race == "N/A" and waste == "N/A" and temp_friends_string == "N/A" and temp_car_string == "N/A" and temp_stage_string == "N/A":
        print("Error: Clan doesn't exist")
        embed = discord.Embed(title=":x: Error", description="Player " + player_o + " doesn't exist", color=0xdb18c1)
        embed.set_thumbnail(url="https://media.giphy.com/media/11YVnpLvl58K2s/200w.gif")
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="All Data Provided By Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")

        await bot.say(embed=embed)
        return

    embed = discord.Embed(title=":crown: Player: " + player, description="Player Profile Information", color=0xdb18c1)
    embed.add_field(name=":green_book: Bio", value=bio)
    embed.add_field(name=":checkered_flag: Racing Wins", value=race)
    embed.add_field(name=":boom: Wasting Wins", value=waste)
    embed.add_field(name=":medal: Total Wins", value=total)
    embed.add_field(name=":notes: Theme Song", value=theme_song)
    embed.add_field(name=":busts_in_silhouette: Clan", value=clan)
    embed.add_field(name=":two_men_holding_hands: Friends", value=temp_friends_string)
    embed.add_field(name=":race_car: Cars", value=temp_car_string)
    embed.add_field(name=":map: Stages", value=temp_stage_string)
    
    try:
        embed.set_thumbnail(url="http://multiplayer.needformadness.com/profiles/" + player + "/avatar.png?req=912")
    except:
        print("No PFP Found")

    try:
        embed.set_image(url="http://multiplayer.needformadness.com/profiles/" + player + "/logo.png")
    except:
        print("No Logo Found")
        
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="All Data Provided By Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")

    await bot.say(embed=embed)

@bot.command()
async def nfmclan(*, clan):
    """General clan profile information"""
    clan_o = clan
    
    clan = clan.replace(' ', '_')
    url_members = "http://multiplayer.needformadness.com/clans/" + clan + "/members.txt?req=416"
    url_cars = "http://multiplayer.needformadness.com/clans/" + clan + "/cars.txt?req=416"
    url_stages = "http://multiplayer.needformadness.com/clans/" + clan + "/stages.txt"
    url_link = "http://multiplayer.needformadness.com/clans/" + clan + "/link.txt?req=135"

    print(url_members)
    print(url_cars)
    print(url_stages)
    print(url_link)

    try:
        memberstext = requests.get(url_members)
        members = memberstext.text
        members_list = members.splitlines()
        if members_list[0] == '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">':
            print("Error: Clan doesn't exist")
            embed = discord.Embed(title=":x: Error", description="Clan " + clan_o + " doesn't exist", color=0xdb18c1)
            embed.set_thumbnail(url="https://media.giphy.com/media/11YVnpLvl58K2s/200w.gif")
            embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
            embed.set_footer(text="All Data Provided By Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")

            await bot.say(embed=embed)
            return
    except:
        print("Error: Clan doesn't exist")
        embed = discord.Embed(title=":x: Error", value="Clan " + clan_o + " doesn't exist", color=0xdb18c1)
        embed.set_thumbnail(url="https://media.giphy.com/media/11YVnpLvl58K2s/200w.gif")
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="All Data Provided By Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")

        await bot.say(embed=embed)
        return

    carstext = requests.get(url_cars)
    cars = carstext.text
    cars_list = cars.splitlines()

    temp_cars_string = "N/A"
    try:
        if cars_list[0] == '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">' or cars_list[0] == "":
            temp_cars_string = "N/A"
        else:
            temp_cars_string = ""
            if len(cars_list) > 10:
                for x in range (0, 10):
                    temp_cars_string = temp_cars_string + cars_list[x] + "\n"
                temp_cars_string = temp_cars_string + "\n...and " + str(len(cars_list) - 10) + " more"
            else:
                for x in range (0, len(cars_list)):
                    temp_cars_string = temp_cars_string + cars_list[x] + "\n"
    except:
        print("Error: Nothing on cars page")
        temp_cars_string = "N/A"

    stagestext = requests.get(url_stages)
    stages = stagestext.text
    stages_list = stages.splitlines()
    
    temp_stages_string = "N/A"
    try:
        if stages_list[0] == '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">' or stages_list[0] == "":
            temp_stages_string = "N/A"
        else:
            temp_stages_string = ""
            if len(stages_list) > 10:
                for x in range (0, 10):
                    temp_stages_string = temp_stages_string + stages_list[x] + "\n"
                temp_stages_string = temp_stages_string + "\n...and " + str(len(stages_list) - 10) + " more"
            else:
                for x in range (0, len(cars_list)):
                    temp_stages_string = temp_stages_string + stages_list[x] + "\n"
    except:
        print("Error: Nothing on stages page")
        temp_stages_string = "N/A"

    linktext = requests.get(url_link)
    link = linktext.text
    link_list = link.splitlines()
    if link_list[0] == '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">':
         clan_link = "N/A"
    else:
        clan_link = "[Click here](" + link_list[2] + ")"

    members = members.replace("|", " - ")
    """print(members)
    print("----------")
    print(cars_list)
    print("----------")
    print(stages_list)
    print("----------")
    print(clan_link)"""

    embed = discord.Embed(title=":shield: Clan: " + clan_o, description="Clan Information", color=0xe226d0)
    embed.add_field(name=":busts_in_silhouette: Clan Members", value=members)
    embed.add_field(name=":race_car: Clan Cars", value=temp_cars_string)
    embed.add_field(name=":map: Clan Stages", value=temp_stages_string)
    embed.add_field(name=":link: Clan Website", value=clan_link)
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="All Data Provided By Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")

    try:
        print("http://multiplayer.needformadness.com/clans/" + clan + "/bg.jpg?req=912")
        embed.set_thumbnail(url="http://multiplayer.needformadness.com/clans/" + clan + "/bg.jpg?req=912")
    except:
        print("No Background Image Found")

    try:
        print("http://multiplayer.needformadness.com/clans/" + clan + "/logo.png")
        embed.set_image(url="http://multiplayer.needformadness.com/clans/" + clan + "/logo.png")
    except:
        print("No Logo Found")

    await bot.say(embed=embed)

#get info about a specific stage
#0 = private
#1 = public
#2 = super public
@bot.command()
async def nfmstage(*, stagename):
    """Get information about a specific stage"""
    stagename_o = stagename

    url_stageinfo = "http://multiplayer.needformadness.com/tracks/" + stagename.replace(" ", "_") + ".txt?reqlo=823"

    stageinfo = requests.get(url_stageinfo)
    stagetext = stageinfo.text
    stagetext = stagetext[8:len(stagetext) - 3]
    stagetext = stagetext.replace(",", "\n")
    stage_list = stagetext.splitlines()

    print(stage_list[0])

    if stage_list[0] == 'E html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">' or stage_list[0] == 'E HTML PUBLIC "-//W3C//DTD HTML 4.01//EN""http://www.w3.org/TR/html4/strict.dtd">':
        print("Error: Stage doesn't exist")
        embed = discord.Embed(title=":x: Error", description="Stage " + stagename_o + " doesn't exist", color=0xdb18c1)
        embed.set_thumbnail(url="https://media.giphy.com/media/11YVnpLvl58K2s/200w.gif")
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="All Data Provided By Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")
        
        await bot.say(embed=embed)
        return

    temp_stage_string = ""
    if(len(stage_list) > 14):
        for x in range(2, 12):
            temp_stage_string = temp_stage_string + stage_list[x] + "\n"
        temp_stage_string = temp_stage_string + "\n...and " + str(len(stage_list)-8) + " more"
    else:
        for x in range(2, len(stage_list)):
            temp_stage_string = temp_stage_string + stage_list[x] + "\n"

    stage_access = ""
    if stage_list[1] == '0':
        stage_access = "Private"
    elif stage_list[1] == '1':
        stage_access = "Public"
    elif stage_list[1] == '2':
        stage_access = "Super Public"
    

    embed = discord.Embed(title=":map: Stage: " + stagename_o, description=":small_red_triangle_down: Download(.radq): [Click Here](http://multiplayer.needformadness.com/tracks/" + stagename.replace(" ", "_") + ".radq)", color=0xaf0a8e)
    embed.add_field(name=":tools: Made By", value=stage_list[0])
    embed.add_field(name=":red_circle: Accessibility", value=stage_access)
    embed.add_field(name=":busts_in_silhouette: Added By", value=temp_stage_string)
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="All Data Provided By Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")
    embed.set_thumbnail(url="https://media.giphy.com/media/11YVnpLvl58K2s/200w.gif")

    await bot.say(embed=embed)

#get info about a specific car
#0 = Class C
#1 = Class B/C
#2 = Class B
#3 = Class A/B
#4 = Class A
@bot.command()
async def nfmcar(*, carname):
    """Get information about a certain car"""
    carname_o = carname
    print("http://multiplayer.needformadness.com/cars/" + carname.replace(" ", "_") + ".radq?reqlo=644")

    carname = carname.replace(' ', '_')
    url_carinfo = "http://multiplayer.needformadness.com/cars/" + carname + ".txt?reqlo=325"
    print(url_carinfo)
    carinfo = requests.get(url_carinfo)
    carinfotext = carinfo.text
    carinfotext = carinfotext[8:len(carinfotext)-3]
    carinfotext = carinfotext.replace(",","\n")
    carinfo_list = carinfotext.splitlines()

    if carinfo_list[0] == 'E html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">' or carinfo_list[0] == 'E HTML PUBLIC "-//W3C//DTD HTML 4.01//EN""http://www.w3.org/TR/html4/strict.dtd">':
        print("Error: Car doesn't exist")
        embed = discord.Embed(title=":x: Error", description="Car " + carname_o + " doesn't exist", color=0xdb18c1)
        embed.set_thumbnail(url="https://media.giphy.com/media/11YVnpLvl58K2s/200w.gif")
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="All Data Provided By Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")
        
        await bot.say(embed=embed)
        return

    car_access = ""
    if carinfo_list[1] == '0':
        car_access = "Private"
    if carinfo_list[1] == '1':
        car_access = "Public"
    if carinfo_list[1] == '2':
        car_access = "Super Public"

    car_class = ""
    if carinfo_list[2] == '0':
        car_class = 'C'
    elif carinfo_list[2] == '1':
        car_class = 'B/C'
    elif carinfo_list[2] == '2':
        car_class = 'B'
    elif carinfo_list[2] == '3':
        car_class = 'A/B'
    elif carinfo_list[2] == '4':
        car_class = 'A'

    temp_car_string = "N/A"
    if len(carinfo_list) > 13:
        temp_car_string = ""
        for x in range(3, 13):
            temp_car_string = temp_car_string + carinfo_list[x] + "\n"
        temp_car_string = temp_car_string + "\n...and " + str(len(carinfo_list)-7) + " more"
    else:
        temp_car_string = ""
        for x in range(3, len(carinfo_list)):
            temp_car_string = temp_car_string + carinfo_list[x] + "\n"
    
    print(carinfo_list[0])
    print(carinfo_list[1])
    print(carinfo_list[2])
    print(car_class)
    print(car_access)
    print(temp_car_string)
    embed = discord.Embed(title=":race_car: Car: " + carname_o, description="Download(.radq): [Click Here](http://multiplayer.needformadness.com/cars/" + carname.replace(" ", "_") + ".radq?reqlo=644)", color=0xc11bc4)
    embed.add_field(name=":tools: Made By", value=carinfo_list[0])
    embed.add_field(name=":large_blue_diamond: Class", value=car_class)
    embed.add_field(name=":diamonds: Accessibility", value=car_access)
    embed.add_field(name=":busts_in_silhouette: Added By", value=temp_car_string)
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="All Data Provided By Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")
    embed.set_thumbnail(url="https://media.giphy.com/media/11YVnpLvl58K2s/200w.gif")

    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def nfmdl(ctx, car_stage, *, name):
    bin_file_name = name + ".radq"

    rolelist = ctx.message.author.roles
    role_list = []
    for x in range(0, len(rolelist)):
        role_list.append(rolelist[x].name)
    print(role_list)
    if "hidden block" not in role_list:
        embed2 = discord.Embed(title=":small_red_triangle_down: Download Failed!", description = "Permission requirements not met.", color=0xffc0cb)
        embed2.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed2.set_footer(text="All Data Provided By Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")
        embed2.set_thumbnail(url="https://media.giphy.com/media/11YVnpLvl58K2s/200w.gif")

        await bot.say(embed = embed2)
        return
    
    if car_stage.lower() == "car" or car_stage.lower() == "stage":
        name_o = name
        name = name.replace(' ', '_')
        
        try:
            testfile = urllib.request.FancyURLopener()
            if car_stage.lower() == "car":
                testfile.retrieve("http://multiplayer.needformadness.com/cars/" + name + ".radq?reqlo=644", bin_file_name)
            elif car_stage.lower() == "stage":
                testfile.retrieve("http://multiplayer.needformadness.com/tracks/" + name + ".radq?reqlo=644", bin_file_name)
        except:
            if car_stage.lower() == "car":
                embed2 = discord.Embed(title=":small_red_triangle_down: Download Failed!", description = "Car does not exist. Please check your car spelling and try again.", color=0xffc0cb)
            if car_stage.lower() == "stage":
                embed2 = discord.Embed(title=":small_red_triangle_down: Download Failed!", description = "Stage does not exist. Please check your car spelling and try again.", color=0xffc0cb)
            embed2.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
            embed2.set_footer(text="All Data Provided By Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")
            embed2.set_thumbnail(url="https://media.giphy.com/media/11YVnpLvl58K2s/200w.gif")

            await bot.say(embed = embed2)
            return
            
        with open(bin_file_name, 'rb') as f:
            data = f.read()

        car_data_array = bytearray(data)
        length_in_bytes = len(car_data_array)
        if car_data_array[0] == 80 and car_data_array[1] == 75 and car_data_array[2] == 3:
            print("Passed file type validation..")
            car_zip_file = zipfile.ZipFile(io.BytesIO(bytes(car_data_array)), "r")
        else:
            j1 = 0
            new_byte_array = ['' for x in range(0, length_in_bytes - 40)]
            while j1 < length_in_bytes - 40:
                byte0 = 20
                if j1 >= 500:
                     byte0 = 40
                new_byte_array[j1] = car_data_array[(j1 + byte0)]
                j1 += 1

            car_zip_file = zipfile.ZipFile(io.BytesIO(bytes(new_byte_array)), "r")

        info_list = str(car_zip_file.infolist())
        print(info_list)
        x = 20
        file_name = ""
        while info_list[x] != "'":
            file_name = file_name + info_list[x]
            x += 1

        zipentry = car_zip_file.extract(file_name)
        print(zipentry)
        os.rename(zipentry, name + ".rad")

        #post processing messages and file cleanup

        if car_stage.lower() == "car":
            embed2 = discord.Embed(title=":race_car: Car Download Complete!", description = "Attachment has been sent :thumbsup: ", color=0xffc0cb)
        elif car_stage.lower() == "stage":
            embed2 = discord.Embed(title=":map: Stage Download Complete!", description = "Attachment has been sent :thumbsup: ", color=0xffc0cb)
        embed2.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed2.set_footer(text="All Data Provided By Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")
        embed2.set_thumbnail(url="https://media.giphy.com/media/11YVnpLvl58K2s/200w.gif")

        await bot.say(embed=embed2)
        await bot.send_file(ctx.message.author, name + ".rad")

        if car_stage.lower() == "stage":
            with open(name + ".rad", 'r') as content_file:
                content = content_file.read()

            content_list = content.splitlines()
            for x in range(0, len(content_list)):
                soundtrack = content_list[x]
                if "soundtrack" in soundtrack:
                    mod_chars = list(soundtrack)
                    mod = ""
                    x = 11
                    while mod_chars[x] != ",":
                        mod = mod + mod_chars[x]
                        x += 1

                    print(mod)
                    mod = mod.replace(' ', '_')
                    mod_zip_name = mod + ".zip"
                            
                    try:
                        testfile = urllib.request.FancyURLopener()
                        testfile.retrieve("http://multiplayer.needformadness.com/tracks/music/" + mod + ".zip", mod_zip_name)
                    except:
                        embed2 = discord.Embed(title=":small_red_triangle_down: Download Failed!", description = "Please check your mod spelling and try again.", color=0xffc0cb)
                        embed2.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
                        embed2.set_footer(text="All Data Provided By Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")
                        embed2.set_thumbnail(url="https://media.giphy.com/media/11YVnpLvl58K2s/200w.gif")

                        await bot.say(embed = embed2)
                        return

                    embed2 = discord.Embed(title=":notes: Mod Download Complete!", description = "Attachment has been sent :thumbsup: ", color=0xffc0cb)
                    embed2.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
                    embed2.set_footer(text="All Data Provided By Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")
                    embed2.set_thumbnail(url="https://media.giphy.com/media/11YVnpLvl58K2s/200w.gif")

                    await bot.say(embed=embed2)
                    await bot.send_file(ctx.message.author, mod_zip_name)

                    try:
                        os.remove(mod_zip_name)
                    except:
                        await bot.say(".mod file isn't there :thinking:")

        try:
            os.remove(name + ".rad")
        except:
            await bot.say(".rad file isn't there :thinking:")

        try:
            os.remove(name_o + ".radq")
        except:
            await bot.say(".radq file isn't there :thinking:")
            
        return
    elif car_stage.lower() == "mod":
        name = name.replace(' ', '_')
        mod_zip_name = name + ".zip"
                               
        try:
           pathlib.Path('C:/NFMMods').mkdir(parents=True, exist_ok=True)
        except:
            print("Directory already exists")
            
        try:
            testfile = urllib.request.FancyURLopener()
            testfile.retrieve("http://multiplayer.needformadness.com/tracks/music/" + name + ".zip", mod_zip_name)
        except:
            embed2 = discord.Embed(title=":small_red_triangle_down: Download Failed!", description = "Please check your mod spelling and try again.", color=0xffc0cb)
            embed2.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
            embed2.set_footer(text="All Data Provided By Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")
            embed2.set_thumbnail(url="https://media.giphy.com/media/11YVnpLvl58K2s/200w.gif")

            await bot.say(embed = embed2)
            return

        embed2 = discord.Embed(title=":notes: Mod Download Complete!", description = "Attachment has been sent :thumbsup: ", color=0xffc0cb)
        embed2.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed2.set_footer(text="All Data Provided By Omar Waly and Radical Play Games", icon_url="http://www.radicalplay.com/logo.png")
        embed2.set_thumbnail(url="https://media.giphy.com/media/11YVnpLvl58K2s/200w.gif")

        await bot.say(embed=embed2)
        await bot.send_file(ctx.message.author, mod_zip_name)

        try:
            os.remove(mod_zip_name)
        except:
            await bot.say(".mod file isn't there :thinking:")
        return

@bot.command()
async def dog():
    """Return random picture of a dog"""
    json_data = requests.get("https://dog.ceo/api/breeds/image/random").json()
    embed = discord.Embed(title=":dog: Random Dog", description=json_data['message'], color=0x8B4513)
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="dog.ceo", icon_url="https://www.programmableweb.com/sites/default/files/styles/article_profile_150x150/public/Dog%20CEO%20Dog.png?itok=wFzt5rrs")
    embed.set_image(url=json_data['message'])

    await bot.say(embed=embed)

@bot.command()
async def chuck():
    """Random Chuck Norris Joke"""
    json_data = requests.get("https://api.chucknorris.io/jokes/random").json()
    embed = discord.Embed(title=":fist: Random Chuck Norris Joke", description=json_data['value'], color=0x261212)
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="api.chucknorris.io", icon_url=json_data['icon_url'])
    embed.set_thumbnail(url='https://orig00.deviantart.net/7a56/f/2011/249/8/d/chuck_norris_by_normantweeter-d493apq.png')

    await bot.say(embed = embed)

@bot.command()
async def fox():
    """Return random picture of a fox"""
    json_data = requests.get("https://randomfox.ca/floof/").json()
    embed = discord.Embed(title=":fox: Random Fox", description=json_data['link'], color=0xff3705)
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="randomfox.ca", icon_url='https://d30y9cdsu7xlg0.cloudfront.net/png/367421-200.png')
    embed.set_image(url=json_data['image'])

    await bot.say(embed=embed)

@bot.command()
async def cat():
    """Return random picture of a cat"""
    json_data = requests.get("http://shibe.online/api/cats?count=[1-100]&urls=[true/false]&httpsUrls=[true/false]").json()
    embed = discord.Embed(title=":cat: Random Cat", description=json_data[0], color=0x9b9696)
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="shibe.online", icon_url='https://cdn.dribbble.com/users/375546/screenshots/1724494/shibe_1x.png')
    embed.set_image(url=json_data[0])

    await bot.say(embed=embed)

@bot.command()
async def bird():
    """Return random picture of a bird"""
    json_data = requests.get("http://shibe.online/api/birds?count=[1-100]&urls=[true/false]&httpsUrls=[true/false]").json()
    embed = discord.Embed(title=":bird: Random Bird", description=json_data[0], color=0x9b9696)
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="shibe.online", icon_url='https://cdn.dribbble.com/users/375546/screenshots/1724494/shibe_1x.png')
    embed.set_image(url=json_data[0])

    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def boobs(ctx):
    """Return random image of boobs"""
    if "nsfw" not in ctx.message.channel.name.lower():
        embed = discord.Embed(title="Don't be naughty in a clean channel :stuck_out_tongue_winking_eye:", color=0x71a9f2)
        embed.set_footer(text="media.oboobs.ru", icon_url="https://cdn.iconscout.com/public/images/icon/premium/png-512/boobs-breast-33bfee18f33b3f52-512x512.png")
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        await bot.say(embed=embed)

        return
    
    number = random.randint(5000, 12500)
    url = ""
    if number < 10000:
        url = "http://media.oboobs.ru/boobs_preview/0" + str(number) + ".jpg"
    else:
        url = "http://media.oboobs.ru/boobs_preview/" + str(number) + ".jpg"

    embed = discord.Embed(title=":chestnut: Random Boobs", color=0x71a9f2)
    embed.set_image(url=url)
    embed.set_footer(text="media.oboobs.ru", icon_url="https://cdn.iconscout.com/public/images/icon/premium/png-512/boobs-breast-33bfee18f33b3f52-512x512.png")
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')

    await bot.say(embed=embed)

@bot.command(pass_context=True)
async def ass(ctx):
    """Return random image of ass"""
    if "nsfw" not in ctx.message.channel.name.lower():
        embed = discord.Embed(title="Don't be naughty in a clean channel :stuck_out_tongue_winking_eye:", color=0xffb238)
        embed.set_footer(text="media.oboobs.ru", icon_url="https://cdn.iconscout.com/public/images/icon/premium/png-512/boobs-breast-33bfee18f33b3f52-512x512.png")
        await bot.say(embed=embed)

        return
    
    number = random.randint(7, 5565)
    url = ""
    if number < 10:
        url = "http://media.obutts.ru/butts_preview/0000" + str(number) + ".jpg"
    if number < 100:
        url = "http://media.obutts.ru/butts_preview/000" + str(number) + ".jpg"
    if number < 1000:
        url = "http://media.obutts.ru/butts_preview/00" + str(number) + ".jpg"
    else:
        url = "http://media.obutts.ru/butts_preview/0" + str(number) + ".jpg"

    embed = discord.Embed(title=":peach: Random Ass", color=0xffb238)
    embed.set_image(url=url)
    embed.set_footer(text="media.obutts.ru", icon_url="https://d30y9cdsu7xlg0.cloudfront.net/png/462430-200.png")
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')

    await bot.say(embed=embed)

@bot.command()
async def insult():
    """Return a random insult"""
    insult = requests.get("https://insult.mattbas.org/api/insult")
    insulttext = insult.text

    embed = discord.Embed(title=":fire: Random Insult", description=insulttext, color=0xe25822)
    embed.set_thumbnail(url="http://aniode.com/blog/wp-content/uploads/2015/02/fire1.gif")
    embed.set_footer(text="https://insult.mattbas.org/api/", icon_url="https://d30y9cdsu7xlg0.cloudfront.net/png/691640-200.png")
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')

    await bot.say(embed=embed)

@bot.command()
async def trump(user: discord.Member):
    """Return random trump insult"""
    insult_json = requests.get("https://api.whatdoestrumpthink.com/api/v1/quotes/personalized?q=" + str(user)).json()
    embed = discord.Embed(title=":speaking_head: Random Trump Insult", description=insult_json['message'], color=0xd68113)
    embed.set_thumbnail(url="https://www.motherjones.com/wp-content/uploads/2017/08/trumpbomb.jpg?w=1200&h=630&crop=1")
    embed.set_footer(text="whatdoestrumpthink.com", icon_url="https://whatdoestrumpthink.com/api-docs/images/logo.png")
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')

    await bot.say(embed=embed)

@bot.command()
async def trumpquote():
    """Random Trump Quote"""
    quote_json = requests.get("https://api.whatdoestrumpthink.com/api/v1/quotes/random").json()
    embed = discord.Embed(title=":speaking_head: Random Trump Quote", description=quote_json['message'], color=0xd68113)
    embed.set_thumbnail(url="https://static01.nyt.com/images/2016/04/14/us/politics/00NYC-candidates-slide-HFSW/00NYC-candidates-slide-HFSW-blog427.png")
    embed.set_footer(text="whatdoestrumpthink.com", icon_url="https://whatdoestrumpthink.com/api-docs/images/logo.png")
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')

    await bot.say(embed=embed)

@bot.command()
async def dadjoke():
    """Random dad joke"""
    joke_json = requests.get("https://icanhazdadjoke.com/slack").json()
    embed = discord.Embed(title=":rolling_eyes: Random Dad Joke", description=joke_json['attachments'][0]['fallback'], color=0x29d199)
    embed.set_thumbnail(url="https://www.imore.com/sites/imore.com/files/styles/xlarge/public/field/image/2017/07/emoji_update_2017_1.png?itok=YeSOfgLc")
    embed.set_footer(text="icanhazdadjoke.com", icon_url="https://cdn.shopify.com/s/files/1/1061/1924/products/Expressionless_Face_Emoji_large.png?v=1480481052")
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')

    await bot.say(embed=embed)

@bot.command()
async def flower():
    """Random flower picture"""
    flower_json = requests.get("https://pixabay.com/api/?key=8273523-1d94a6763e24dfdb8f0197a3d&image_type=photo&q=flower&per_page=200&page=" + str(random.randint(1, 3))).json()
    random_int = random.randint(0, 200)
    
    embed = discord.Embed(title=":sunflower: Random Flower Picture", description="Tags: " + flower_json['hits'][random_int]['tags'] + "\nAuthor: " + flower_json['hits'][random_int]['user'])
    embed.set_image(url=flower_json['hits'][random_int]['previewURL'])
    embed.set_footer(text="pixabay.com", icon_url="https://pixabay.com/static/img/logo_square.png")
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')

    await bot.say(embed=embed)

@bot.command()
async def tree():
    """Random tree picture"""
    tree_json = requests.get("https://pixabay.com/api/?key=8273523-1d94a6763e24dfdb8f0197a3d&image_type=photo&q=tree&per_page=200&page=" + str(random.randint(1, 3))).json()
    random_int = random.randint(0, 200)
    
    embed = discord.Embed(title=":evergreen_tree: Random Tree Picture", description="Tags: " + tree_json['hits'][random_int]['tags'] + "\nAuthor: " + tree_json['hits'][random_int]['user'])
    embed.set_image(url=tree_json['hits'][random_int]['previewURL'])
    embed.set_footer(text="pixabay.com", icon_url="https://pixabay.com/static/img/logo_square.png")
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')

    await bot.say(embed=embed)

@bot.command()
async def findpic(*, name):
    """Random picture of anything of your choice"""
    name = name.replace(" ", "+")
    pic_json = requests.get("https://pixabay.com/api/?key=8273523-1d94a6763e24dfdb8f0197a3d&image_type=photo&q=" + name + "&per_page=200&page=" + str(random.randint(1, 3))).json()
    random_int = random.randint(0, len(pic_json['hits']))
    
    embed = discord.Embed(title=":camera: Random Picture", description="Tags: " + pic_json['hits'][random_int]['tags'] + "\nAuthor: " + pic_json['hits'][random_int]['user'])
    embed.set_image(url=pic_json['hits'][random_int]['previewURL'])
    embed.set_footer(text="pixabay.com", icon_url="https://pixabay.com/static/img/logo_square.png")
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')

    await bot.say(embed=embed)

@bot.command()
async def randpic():
    """Just get a random picture"""
    pic_json = requests.get("https://pixabay.com/api/?key=8273523-1d94a6763e24dfdb8f0197a3d&image_type=photo&per_page=200&page=" + str(random.randint(1, 3))).json()
    random_int = random.randint(0, len(pic_json['hits']))

    embed = discord.Embed(title=":camera_with_flash: Random Picture", description="Tags: " + pic_json['hits'][random_int]['tags'] + "\nAuthor: " + pic_json['hits'][random_int]['user'])
    embed.set_image(url=pic_json['hits'][random_int]['previewURL'])
    embed.set_footer(text="pixabay.com", icon_url="https://pixabay.com/static/img/logo_square.png")
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')

    await bot.say(embed=embed)

@bot.command()
async def randquote():
    """Get a random quote"""
    quote_json = requests.get("https://favqs.com/api/quotes", headers={'Content-Type': 'application/json', 'Authorization': 'Token token="6d274a73cd9072d5de3ea041db31799a"'}).json()

    embed = discord.Embed(title=":speech_balloon: Random Quote", description="[Link to quote](" + quote_json['quotes'][1]['url'] + ")", color=0x701693)
    embed.add_field(name=":speech_left: Quote", value=quote_json['quotes'][1]['body'])
    embed.add_field(name=":writing_hand: Author", value=quote_json['quotes'][1]['author'])
    embed.add_field(name=":arrow_up_small: Upvotes", value=str(quote_json['quotes'][1]['upvotes_count']))
    embed.add_field(name=":arrow_down_small: Downvotes", value=str(quote_json['quotes'][1]['downvotes_count']))
    embed.add_field(name=":star: Favorites", value=str(quote_json['quotes'][1]['favorites_count']))
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="favqs.com", icon_url="https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2016-09-13/79096605889_ac5cb03e541289f17b6d_512.png")
    embed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/education-89/512/education-09-512.png")

    await bot.say(embed=embed)

@bot.command()
async def findquote(filt, *, val):
    """Find a quote by filter"""
    if filt.lower() == "author":
        try:
            quote_json = requests.get("https://favqs.com/api/quotes?filter=" + val.lower().replace(" ", "+") + "&type=author", headers={'Content-Type': 'application/json', 'Authorization': 'Token token="6d274a73cd9072d5de3ea041db31799a"'}).json()
            randint = random.randint(0, len(quote_json['quotes']))
            embed = discord.Embed(title=":speech_balloon: Quote By Author: " + val, description="[Link to quote](" + quote_json['quotes'][1]['url'] + ")", color=0x701693)
            embed.add_field(name=":speech_left: Quote", value=quote_json['quotes'][randint]['body'])
            embed.add_field(name=":writing_hand: Author", value=quote_json['quotes'][randint]['author'])
            embed.add_field(name=":arrow_up_small: Upvotes", value=str(quote_json['quotes'][randint]['upvotes_count']))
            embed.add_field(name=":arrow_down_small: Downvotes", value=str(quote_json['quotes'][randint]['downvotes_count']))
            embed.add_field(name=":star: Favorites", value=str(quote_json['quotes'][randint]['favorites_count']))
        except:
            embed = discord.Embed(title=":x: Error", description='Author "' + val + '" not found.', color=0x701693)
    elif filt.lower() == "contains":
        try:
            quote_json = requests.get("https://favqs.com/api/quotes?filter=" + val.lower().replace(" ", "+"), headers={'Content-Type': 'application/json', 'Authorization': 'Token token="6d274a73cd9072d5de3ea041db31799a"'}).json()
            randint = random.randint(0, len(quote_json['quotes']))
            embed = discord.Embed(title=":speech_balloon: Quote Containing: " + val, description="[Link to quote](" + quote_json['quotes'][1]['url'] + ")", color=0x701693)
            embed.add_field(name=":speech_left: Quote", value=quote_json['quotes'][randint]['body'])
            embed.add_field(name=":writing_hand: Author", value=quote_json['quotes'][randint]['author'])
            embed.add_field(name=":arrow_up_small: Upvotes", value=str(quote_json['quotes'][randint]['upvotes_count']))
            embed.add_field(name=":arrow_down_small: Downvotes", value=str(quote_json['quotes'][randint]['downvotes_count']))
            embed.add_field(name=":star: Favorites", value=str(quote_json['quotes'][randint]['favorites_count']))
        except:
            embed = discord.Embed(title=":x: Error", description='Could not find quote containing "' + val + '".', color=0x701693)
    elif filt.lower() == "tag":
        try:
            quote_json = requests.get("https://favqs.com/api/quotes?filter=" + val.lower().replace(" ", "+") + "&type=tag", headers={'Content-Type': 'application/json', 'Authorization': 'Token token="6d274a73cd9072d5de3ea041db31799a"'}).json()
            randint = random.randint(0, len(quote_json['quotes']))
            embed = discord.Embed(title=":speech_balloon: Quote With Tag: " + val, description="[Link to quote](" + quote_json['quotes'][1]['url'] + ")", color=0x701693)
            embed.add_field(name=":speech_left: Quote", value=quote_json['quotes'][randint]['body'])
            embed.add_field(name=":writing_hand: Author", value=quote_json['quotes'][randint]['author'])
            embed.add_field(name=":arrow_up_small: Upvotes", value=str(quote_json['quotes'][randint]['upvotes_count']))
            embed.add_field(name=":arrow_down_small: Downvotes", value=str(quote_json['quotes'][randint]['downvotes_count']))
            embed.add_field(name=":star: Favorites", value=str(quote_json['quotes'][randint]['favorites_count']))
        except:
            embed = discord.Embed(title=":x: Error", description='Could not find quote with tag "' + val + '".', color=0x701693)
    else:
        embed = discord.Embed(title=":x: Error", description='Filter "' + filt + '" does not exist.', color=0x701693)

    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="favqs.com", icon_url="https://slack-files2.s3-us-west-2.amazonaws.com/avatars/2016-09-13/79096605889_ac5cb03e541289f17b6d_512.png")
    embed.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/education-89/512/education-09-512.png")
    
    await bot.say(embed=embed)

@bot.command()
async def yesorno():
    """Says yes or no"""
    json = requests.get("https://yesno.wtf/api/").json()

    if json['answer'] == "yes":
        emoji = ":white_check_mark: "
    else:
        emoji = ":x: "
    embed = discord.Embed(title=emoji + json['answer'])
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="yesno.wtf", icon_url="http://www.pvhc.net/img165/lotaonzrtznehrehmoff.png")
    embed.set_image(url=json['image'])
    
    await bot.say(embed=embed)

@bot.command()
async def lolmatch(region, *, summoner):
    """Returns match information for a certain user"""
    if region.lower() == 'na':
        region = 'NA1'
    elif region.lower() == 'euw':
        region = 'EUW1'
    elif region.lower() == 'eun':
        region = 'EUN1'
    elif region.lower() == 'oce':
        region = 'OC1'
    api_key = 'RGAPI-a7ff64ee-756e-458f-b089-5a1e7c4ff14d'
    
    try:
        url = 'https://' + region + '.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + summoner + '?api_key=' + str(api_key)
        summoner_json = requests.get(url).json()
        user_id = summoner_json['id']
    except:
        embed = discord.Embed(title=":x: Error", description="Summoner " + summoner + " does not exist.", color=0x16a9bc)
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="Riot Games API", icon_url='https://orig00.deviantart.net/6fba/f/2016/311/4/5/lolalpha_launcher_by_giorgsavv-danohsj.png')
        embed.set_thumbnail(url="http://2.bp.blogspot.com/-HqSOKIIV59A/U8WP4WFW28I/AAAAAAAAT5U/qTSiV9UgvUY/s1600/icon.png")

        await bot.say(embed=embed)
        return

    url2 = "https://" + region + ".api.riotgames.com/lol/spectator/v3/active-games/by-summoner/" + str(user_id) + "?api_key=" + api_key
    match_json = requests.get(url2).json()
    print(url2)

    try:
        status = match_json['status']['message']
        
        embed = discord.Embed(title=":x: Error", description="Summoner " + summoner + " not in a game at the moment.", color=0x16a9bc)
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="Riot Games API", icon_url='https://orig00.deviantart.net/6fba/f/2016/311/4/5/lolalpha_launcher_by_giorgsavv-danohsj.png')
        embed.set_thumbnail(url="http://2.bp.blogspot.com/-HqSOKIIV59A/U8WP4WFW28I/AAAAAAAAT5U/qTSiV9UgvUY/s1600/icon.png")

        await bot.say(embed=embed)
        return
    except:
        print("Success! Getting match data")
        await bot.say("Success! Getting match data (may take a little bit...)")

    embed = discord.Embed(title=":crossed_swords: League Current Match", description="Game Type: " + match_json["gameType"] + " - " + match_json["gameMode"], color=0x16a9bc)
    
    for x in range(0, len(match_json['participants'])):
        player = match_json['participants'][x]['summonerName']
        team = ""
        if (match_json['participants'][x]['teamId'] == 100):
            team = ":large_blue_circle: "
        else:
            team = ":red_circle: "
        try:
            url_rank = 'https://' + region + '.api.riotgames.com/lol/league/v3/positions/by-summoner/' + str(match_json['participants'][x]['summonerId']) + '?api_key=' + str(api_key)
            json2 = requests.get(url_rank).json()

            rank = json2[0]['tier'] + " " + json2[0]['rank'] + ", " + str(json2[0]['leaguePoints'])
        except:
            rank = "Unranked"

        champ_id = match_json['participants'][x]['championId']
        champion = ""
        summ1_id = match_json['participants'][x]['spell1Id']
        summ2_id = match_json['participants'][x]['spell2Id']
        summ1 = ""
        summ2 = ""
        
        for x in range(0, len(champ_ids)):
            if str(champ_id) == champ_ids[x]:
                champion = champ_names[x]
                break

        for x in range(0, len(summs_ids)):
            if str(summ1_id) == summs_ids[x]:
                summ1 = summs_names[x]
                break
        for x in range(0, len(summs_ids)):
            if str(summ2_id) == summs_ids[x]:
                summ2 = summs_names[x]
                break
        
        #bot = match_json['participants'][x]['bot']
        
        embed.add_field(name=team + player + " - " + champion, value="Rank: " + rank + "\nSummoner Spells: " + summ1 + ", " + summ2)

    map_id = match_json['mapId']
    thumbnail_url = "http://ddragon.leagueoflegends.com/cdn/8.5.2/img/map/map" + str(map_id) + ".png"

    embed.set_thumbnail(url=thumbnail_url)
    
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="Riot Games API", icon_url='https://orig00.deviantart.net/6fba/f/2016/311/4/5/lolalpha_launcher_by_giorgsavv-danohsj.png')

    await bot.say(embed=embed)

@bot.command()
async def lolchamp(*, name):
    """Returns information about a specific champion"""
    name = name.lower()

    champion = ""
    key = ""
    description = ""
    Id = ""
    for x in range(0, len(champ_names)):
        if name == champ_names[x].lower():
            champion = champ_names[x]
            key = champ_keys[x]
            description = champ_titles[x]
            Id = champ_ids[x]
            break

    if champion == "":
        embed = discord.Embed(title=":x: Error", description="Champion not found", color=0x00f2ff)
        embed.set_thumbnail(url="https://vignette.wikia.nocookie.net/leagueoflegends/images/1/12/League_of_Legends_Icon.png/revision/latest?cb=20150402234343")
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="Riot Games API", icon_url='https://orig00.deviantart.net/6fba/f/2016/311/4/5/lolalpha_launcher_by_giorgsavv-danohsj.png')

        await bot.say(embed=embed)
        return

    if name.lower() == "fiddlesticks":
        key = "FiddleSticks"
        
    url_champ = "http://ddragon.leagueoflegends.com/cdn/8.5.2/data/en_US/champion/" + key + ".json"
    champ_json = requests.get(url_champ).json()

    basic_info = "Attack: " + str(champ_json['data'][key]['info']['attack']) \
                            + "\nDefense: " + str(champ_json['data'][key]['info']['defense']) \
                            + "\nMagic: " + str(champ_json['data'][key]['info']['magic']) + "\nDifficulty: " \
                            + str(champ_json['data'][key]['info']['difficulty'])
    tags = ""
    if len(champ_json['data'][key]['tags']) == 1:
        tags = champ_json['data'][key]['tags'][0]
    else:
        tags = champ_json['data'][key]['tags'][0] + "\n" + champ_json['data'][key]['tags'][1]

    lore = champ_json['data'][key]['lore']

    allytips = ""
    for x in range(0, len(champ_json['data'][key]['allytips'])):
        allytips = allytips + "-" + champ_json['data'][key]['allytips'][x] + "\n"

    enemytips = ""
    for x in range(0, len(champ_json['data'][key]['enemytips'])):
        enemytips = enemytips + "-" + champ_json['data'][key]['enemytips'][x] + "\n"

    embed = discord.Embed(title=champion, description=description, color=0x16a9bc)

    secondary = champ_json['data'][key]['partype']
    embed.add_field(name=":fleur_de_lis: Secondary Bar", value=secondary)
    
    embed.add_field(name=":pencil: Basic Information", value=basic_info)

    base_stats = "Health: " + str(champ_json['data'][key]['stats']['hp'])

    if secondary.lower() != "none":
        base_stats = base_stats + "\n" + secondary + ": " + str(champ_json['data'][key]['stats']['mp'])
        
    base_stats = base_stats + "\nMovement Speed: " + str(champ_json['data'][key]['stats']['movespeed']) + \
                 "\nArmor: " + str(champ_json['data'][key]['stats']['armor']) + \
                 "\nMagic Resistance: " + str(champ_json['data'][key]['stats']['spellblock']) + \
                 "\nHealth Regeneration: " + str(champ_json['data'][key]['stats']['hpregen'])

    if secondary.lower() != "none":
        base_stats = base_stats + "\n" + secondary + " Regeneration: " + str(champ_json['data'][key]['stats']['mpregen'])

    base_stats = base_stats + "\nAttack Damage: " + str(champ_json['data'][key]['stats']['attackdamage']) + \
                             "\nAttack Speed: " + str(0.625/(1 + champ_json['data'][key]['stats']['attackspeedoffset'])) + \
                             "\nAbility Power: 0" + \
                             "\nCritical Strike Chance: " + str(champ_json['data'][key]['stats']['crit'])

    stats_per_level = "Health Per Level: " + str(champ_json['data'][key]['stats']['hpperlevel'])
    if secondary.lower() != "none":
        stats_per_level = stats_per_level + "\n" + secondary + " Per Level: " + str(champ_json['data'][key]['stats']['mpperlevel'])

    stats_per_level = stats_per_level + "\nArmor Per Level: " + str(champ_json['data'][key]['stats']['armorperlevel']) + \
                      "\nMagic Resistance Per Level: " + str(champ_json['data'][key]['stats']['spellblockperlevel']) + \
                      "\nHP Regeneration Per Level: " + str(champ_json['data'][key]['stats']['hpregenperlevel'])

    if secondary.lower() != "none":
        stats_per_level = stats_per_level + "\n" + secondary + " Regeneration Per Level: " + str(champ_json['data'][key]['stats']['mpregenperlevel'])

    stats_per_level = stats_per_level + "\nAttack Damage Per Level: " + str(champ_json['data'][key]['stats']['attackdamageperlevel']) + \
                    "\nAttack Speed Per Level: " + str(champ_json['data'][key]['stats']['attackspeedperlevel']) + \
                    "\nAbility Power Per Level: 0" + \
                    "\nCritical Strike Chance Per Level: " + str(champ_json['data'][key]['stats']['critperlevel'])

    embed.add_field(name=":label: Tags", value=tags)
    embed.add_field(name=":dagger: Base Stats", value=base_stats)
    embed.add_field(name=":knife: Stats Per Level", value=stats_per_level)
    embed.add_field(name=":blue_book: Lore", value=lore)

    embed.add_field(name=":small_orange_diamond: Passive - " + champ_json['data'][key]['passive']['name'],
                    value=champ_json['data'][key]['passive']['description'])
    spell_list = [':small_blue_diamond: Q', ':small_blue_diamond: W', ':small_blue_diamond: E', ':diamond_shape_with_a_dot_inside: R']
    for x in range(0, 4):
        cost = ""
        if champ_json['data'][key]['spells'][x]['costType'].lower() == "no cost" or champ_json['data'][key]['spells'][x]['costType'].lower() == " no cost":
            cost = champ_json['data'][key]['spells'][x]['costType']

        else:
            cost = champ_json['data'][key]['spells'][x]['costBurn'] + " " + champ_json['data'][key]['spells'][x]['costType']
        
        embed.add_field(name=spell_list[x] + " - " + champ_json['data'][key]['spells'][x]['name'],
                        value="Description: " + champ_json['data'][key]['spells'][x]['description']
                        + "\nMax Rank: " + str(champ_json['data'][key]['spells'][x]['maxrank']) \
                        + "\nCooldown: " + champ_json['data'][key]['spells'][x]['cooldownBurn']
                        + "\nCost: " + cost)
    
    embed.add_field(name=":crossed_swords: Ally Tips", value = allytips)
    embed.add_field(name=":skull_crossbones: Enemy Tips", value=enemytips)
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="Riot Games API", icon_url='https://orig00.deviantart.net/6fba/f/2016/311/4/5/lolalpha_launcher_by_giorgsavv-danohsj.png')
    embed.set_thumbnail(url="http://ddragon.leagueoflegends.com/cdn/6.24.1/img/champion/" + key + ".png")
    if name.lower() == "fiddlesticks":
        key = "Fiddlesticks"
    #embed.set_image(url="http://ddragon.leagueoflegends.com/cdn/img/champion/splash/" + key + "_0.jpg")

    await bot.say(embed=embed)

@bot.command()
async def lolsumm(*, spell):
    """Returns information about a summoner spell"""
    spell_key = ""
    
    for x in range(0, len(summs_names)):
        if spell.lower() == summs_names[x].lower():
            spell_key = summs_keys[x]
            break

    url = "http://ddragon.leagueoflegends.com/cdn/8.5.2/data/en_US/summoner.json"
    spell_json = requests.get(url).json()

    embed = discord.Embed(title="Summoner Spell: " + spell_json['data'][spell_key]['name'],
                          description="Spell ID: " + spell_json['data'][spell_key]['id'], color=0x16a9bc)

    stages = ""
    for x in range(0, len(spell_json['data'][spell_key]['modes'])):
        stage = spell_json['data'][spell_key]['modes'][x].lower()
        stages = stages + stage.title() + "\n"
    
    embed.add_field(name=":green_book: Description", value=spell_json['data'][spell_key]['description'])
    embed.add_field(name=":timer: Cooldown", value=str(spell_json['data'][spell_key]['cooldownBurn']) + " seconds")
    embed.add_field(name=":o: Range", value=str(spell_json['data'][spell_key]['cooldownBurn']))
    embed.add_field(name=":crown: Available At", value="Level " + str(spell_json['data'][spell_key]['summonerLevel']))
    embed.add_field(name=":map: Stages Usable On", value=stages)
    embed.add_field(name=":large_blue_circle: Cost", value="No Cost")

    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="Riot Games API", icon_url='https://orig00.deviantart.net/6fba/f/2016/311/4/5/lolalpha_launcher_by_giorgsavv-danohsj.png')
    embed.set_thumbnail(url="http://ddragon.leagueoflegends.com/cdn/6.24.1/img/spell/" + spell_key + ".png")

    await bot.say(embed=embed)

@bot.command()
async def pokemon(*, pokemon):
    """returns information about a pokemon"""
    pokemonid = 29384234723
    for x in range(0, len(species_ids)):
        if species_name[x] == pokemon.lower():
            pokemonid = species_ids[x]
            height = species_height[x]
            weight = species_weight[x]
            baseexp = species_baseexp[x]
            break
    
    #random initialized values
    type1id = 523
    type2id = 523
    count = 1
    for x in range(0, len(species_ids_typecsv)):
        if pokemonid == species_ids_typecsv[x]:
            if count == 1:
                type1id = species_type_id[x]
                count += 1
            elif count == 2:
                type2id = species_type_id[x]
                break

    type1 = ""
    type2 = "N/A"
    for x in range(0, len(type_ids)):
        if type1id == type_ids[x]:
            type1 = type_name[x]
        elif type2id == type_ids[x]:
            type2 = type_name[x]

    hp = 0
    attack = 0
    defense = 0
    sattack = 0
    sdefense = 0
    speed = 0

    for x in range(0, len(pokemon_base_ids)):
        #print(pokemon_stat_ids[x])
        if pokemon_base_ids[x] == pokemonid:
            if pokemon_stat_ids[x] == '1':
                hp = pokemon_base_stats[x]
            elif pokemon_stat_ids[x] == '2':
                attack = pokemon_base_stats[x]
            elif pokemon_stat_ids[x] == '3':
                defense = pokemon_base_stats[x]
            elif pokemon_stat_ids[x] == '4':
                sattack = pokemon_base_stats[x]
            elif pokemon_stat_ids[x] == '5':
                sdefense = pokemon_base_stats[x]
            elif pokemon_stat_ids[x] == '6':
                speed = pokemon_base_stats[x]
                break

    evolved_from = ""
    color_id = '0'
    shape_id = '0'
    habitat_id = '0'
    catch_rate = '0'
    base_happiness = '0'
    generation = '1'

    for x in range(0, len(pokemon_species_ids)):
        if pokemon_species_ids[x] == pokemonid:
            try:
                evolved_from = pokemon_species_identifier[int(pokemon_species_evolved[x])].title()
            except:
                evolved_from = "N/A"
            color_id = pokemon_species_color[x]
            shape_id = pokemon_species_shape[x]
            habitat_id = pokemon_species_habitat[x]
            catch_rate = pokemon_species_catch[x]
            base_happiness = pokemon_species_happiness[x]
            generation = pokemon_species_generation[x]
            break

    color = "N/A"
    shape = "N/A"
    habitat = "N/A"

    for x in range(0, len(color_ids)):
        if color_id == color_ids[x]:
            color = colors[x]
            break

    for x in range(0, len(habitat_ids)):
        if habitat_id == habitat_ids[x]:
            habitat = habitats[x]
            break

    for x in range(0, len(shape_ids)):
        if shape_id == shape_ids[x]:
            shape = shapes[x]
            break

    try:
        embed = discord.Embed(title="Pokemon Information: " + pokemon, description="Primary Type: " + type1.title() + "\nSecondary Type: " + type2.title(), color=0x0f4c15)
        embed.add_field(name=":1234: National Dex Number", value=str(pokemonid))
        embed.add_field(name=":straight_ruler: Height", value=str(height))
        embed.add_field(name=":scales: Weight", value=str(weight))
        embed.add_field(name=":red_circle: Color", value=color)
        embed.add_field(name=":record_button: Shape", value=shape)
        embed.add_field(name=":evergreen_tree: Habitat", value=habitat)
        embed.add_field(name=":boom: Evolves From", value=evolved_from)
        embed.add_field(name=":busts_in_silhouette: Generation", value=generation)
        embed.add_field(name=":dagger: Base Combat Stats", value="HP: " + hp
                                                            + "\nAttack: " + attack
                                                            + "\nDefense: " + defense
                                                            + "\nSpecial Attack: " + sattack
                                                            + "\nSpecial Defense: " + sdefense
                                                            + "\nSpeed: " + speed
                                                            + "\nTotal: " + str(int(hp) + int(attack) + int(defense) + int(sattack) + int(sdefense) + int(speed)))
        embed.add_field(name=":cyclone: Other Base Stats", value="\nBase Experience: " + str(baseexp)
                                                                    + "\nCatch Rate: " + catch_rate
                                                                    + "\nBase Happiness: " + base_happiness)

        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="All Rights to Pokemon Owned By Nintendo", icon_url='https://static-cdn.jtvnw.net/jtv_user_pictures/nintendo-profile_image-849418bb6ce6264a-300x300.png')
        try:
            embed.set_thumbnail(url='https://img.pokemondb.net/sprites/black-white/anim/back-normal/' + pokemon.lower() + '.gif')
            embed.set_image(url='https://img.pokemondb.net/sprites/black-white/anim/normal/' + pokemon.lower() + '.gif')
        except:
            embed.set_thumbnail(url='https://img.pokemondb.net/sprites/x-y/normal/' + pokemon.lower() + '.png')

        await bot.say(embed=embed)
    except:
        embed = discord.Embed(title=":x: Error", description="Pokemon " + pokemon + " not found.", color=0x0f4c15)
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="All Rights to Pokemon Owned By Nintendo", icon_url='https://static-cdn.jtvnw.net/jtv_user_pictures/nintendo-profile_image-849418bb6ce6264a-300x300.png')
        embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR5g81Pawn7hrF8K8PABYrdl-IHp3VxBZgY7sy62DE2BJhEg_Uk')

        await bot.say(embed=embed)

@bot.command(pass_context=True)
async def henle(ctx, *, composer):
    """returns henle difficulties"""
    if ctx.message.author.id == "225264828304850944" or ctx.message.author.id == "100238213167206400":
        return
    
    composers = []
    
    for x in range(0, len(henle_composers)):
        if x == 0:
            composers.append(henle_composers[x])
        elif henle_composers[x] == henle_composers[x-1]:
            continue
        else:
            composers.append(henle_composers[x])

    if composer.lower() == "composers":
        composer_string = ""
        for x in range(0, len(composers)):
            composer_string = composer_string + str(x+1) + ". " + composers[x] + "\n"
        embed1 = discord.Embed(title="<:piano:504104327606960128> Available Composers", description=composer_string, color=0x551a8b)
        embed1.set_thumbnail(url="https://is4-ssl.mzstatic.com/image/thumb/Purple118/v4/f3/b2/ca/f3b2ca8e-7c88-cc75-99b0-18a0895c4b10/AppIcon-1x_U007emarketing-85-220-0-4.png/246x0w.jpg")
        embed1.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed1.set_footer(text="All Data Obtained From And Owned By G. Henle Verlag Publication", icon_url="https://www.amphio.co/img/henle/icon-scoreproducer.png")

        await bot.say(embed=embed1)
        return

    if composer.title() not in composers:
        embed1 = discord.Embed(title=":x: Error", description="Composer " + composer + " not found in database", color=0x551a8b)
        embed1.set_thumbnail(url="https://is4-ssl.mzstatic.com/image/thumb/Purple118/v4/f3/b2/ca/f3b2ca8e-7c88-cc75-99b0-18a0895c4b10/AppIcon-1x_U007emarketing-85-220-0-4.png/246x0w.jpg")
        embed1.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed1.set_footer(text="All Data Obtained From And Owned By G. Henle Verlag Publication", icon_url="https://www.amphio.co/img/henle/icon-scoreproducer.png")

        await bot.say(embed=embed1)
        return
    
    piecegroups = []
    ordernums = []
    piece_string = ""
    count = 1
    for x in range(0, len(henle_composers)):
        if henle_composers[x].lower() == composer.lower():
            piecegroups.append(henle_piecegroups[x])
            ordernums.append(henle_ordernums[x])
            piece_string = piece_string + str(count) + ". " + henle_piecegroups[x] + "\n"
            count += 1
    
    embed1 = discord.Embed(title="<:piano:504104327606960128> Select the pieces using the respective number", description=piece_string, color=0x551a8b)
    embed1.set_thumbnail(url="https://is4-ssl.mzstatic.com/image/thumb/Purple118/v4/f3/b2/ca/f3b2ca8e-7c88-cc75-99b0-18a0895c4b10/AppIcon-1x_U007emarketing-85-220-0-4.png/246x0w.jpg")
    embed1.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed1.set_footer(text="All Data Provided and Owned By G. Henle Verlag Publication", icon_url="https://www.amphio.co/img/henle/icon-scoreproducer.png")

    await bot.say(embed=embed1)

    msg = await bot.wait_for_message(author = ctx.message.author)
    reply = msg.content

    try:
        piece = piecegroups[int(reply) - 1]
        ordernum = ordernums[int(reply) - 1]
    except:
        embed1 = discord.Embed(title=":x: Error", description="Invalid Input", color=0x551a8b)
        embed1.set_thumbnail(url="https://is4-ssl.mzstatic.com/image/thumb/Purple118/v4/f3/b2/ca/f3b2ca8e-7c88-cc75-99b0-18a0895c4b10/AppIcon-1x_U007emarketing-85-220-0-4.png/246x0w.jpg")
        embed1.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed1.set_footer(text="All Data Obtained From And Owned By G. Henle Verlag Publication", icon_url="https://www.amphio.co/img/henle/icon-scoreproducer.png")

        await bot.say(embed=embed1)
        return

    await bot.say("Success, fetching data(may take a little bit...)")
    csvfile = composer.lower() + "-" + piece.lower() + ".csv"

    difficulty_string = ""
    orderstring = ""
    if int(ordernum) > 999:
        orderstring = ordernum
    elif int(ordernum) > 99:
        orderstring = "0" + ordernum
    elif int(ordernum) > 9:
        orderstring = "00" + ordernum
    else:
        orderstring = "000" + ordernum

    difficulty_string = ""

    with open(csvfile, 'r') as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            difficulty_string = difficulty_string + "**" + row[0] + "** - " + row[1] + "\n"

    embed2 = discord.Embed(title="<:piano:504104327606960128> " + composer.title() + ": " + piece, description=difficulty_string, color=0x551a8b)
    embed2.set_thumbnail(url="https://is4-ssl.mzstatic.com/image/thumb/Purple118/v4/f3/b2/ca/f3b2ca8e-7c88-cc75-99b0-18a0895c4b10/AppIcon-1x_U007emarketing-85-220-0-4.png/246x0w.jpg")
    embed2.add_field(name=":musical_note: More Info", value="[Click here for more info on these pieces](https://www.henle.de/en/detail/?Title=" + ordernum + ")")
    #embed2.set_image(url="http://www.henleusa.com/cover/small/HN-" + orderstring + ".gif")
    embed2.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed2.set_footer(text="All Data Provided and Owned By G. Henle Verlag Publication", icon_url="https://www.amphio.co/img/henle/icon-scoreproducer.png")

    await bot.say(embed=embed2)

@bot.command(pass_context=True)
async def hentai(ctx, tag):
    """returns a random hentai image or gif"""
    if "nsfw" not in ctx.message.channel.name.lower():
        embed = discord.Embed(title="Don't be naughty in a clean channel :stuck_out_tongue_winking_eye:", color=0xF08080)
        embed.set_footer(text="All Images Owned by the Creators of NekoBot", icon_url="https://images.discordapp.net/avatars/310039170792030211/b14caa57a169fdd3595c8560f7e31a3f.png?size=512")
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        await bot.say(embed=embed)

        return

    if tag.lower() == "boobs":
        number = random.randint(0, 304)

        num_string = ""
        if number < 10:
            num_string = "00" + str(number)
        elif number < 100:
            num_string = "0" + str(number)
        else:
            num_string = str(number)

        embed = discord.Embed(title=":chestnut: Random Hentai Boobs", color=0xF08080)
        embed.set_image(url="https://cdn.nekos.life/boobs/boobs" + num_string + ".gif")
        embed.set_footer(text="All Images Owned by the Creators of NekoBot", icon_url="https://images.discordapp.net/avatars/310039170792030211/b14caa57a169fdd3595c8560f7e31a3f.png?size=512")
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        await bot.say(embed=embed)

        return

    elif tag.lower() == "pussy":
        tempembed = discord.Embed(title="Select an option", description="\n1. Pussy Eating \n2. Other Pussy Gifs", color=0xF08080)
        tempembed.set_footer(text="All Images Owned by the Creators of NekoBot", icon_url="https://images.discordapp.net/avatars/310039170792030211/b14caa57a169fdd3595c8560f7e31a3f.png?size=512")
        tempembed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        await bot.say(embed=tempembed)

        msg = await bot.wait_for_message(author = ctx.message.author)
        choice = msg.content

        if choice == "2":
            number = random.randint(1, 127)

            num_string = ""
            if number < 10:
                num_string = "00" + str(number)
            elif number < 100:
                num_string = "0" + str(number)
            else:
                num_string = str(number)

            embed = discord.Embed(title=":peach: Random Hentai Pussy", color=0xF08080)
            embed.set_image(url="https://cdn.nekos.life/pussy/pwank" + num_string + ".gif")
            embed.set_footer(text="All Images Owned by the Creators of NekoBot", icon_url="https://images.discordapp.net/avatars/310039170792030211/b14caa57a169fdd3595c8560f7e31a3f.png?size=512")
            embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
            await bot.say(embed=embed)

            return
        else:
            number = random.randint(1, 32)

            num_string = ""
            if number < 10:
                num_string = "0" + str(number)
            else:
                num_string = str(number)

            embed = discord.Embed(title=":peach: Random Hentai Pussy", color=0xF08080)
            embed.set_image(url="https://cdn.nekos.life/kuni/kuni" + num_string + ".gif")
            embed.set_footer(text="All Images Owned by the Creators of NekoBot", icon_url="https://images.discordapp.net/avatars/310039170792030211/b14caa57a169fdd3595c8560f7e31a3f.png?size=512")
            embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
            await bot.say(embed=embed)

            return

    elif tag.lower() == "anal":
        number = random.randint(1, 42)

        num_string = ""
        if number < 10:
            num_string = "0" + str(number)
        else:
            num_string = str(number)

        embed = discord.Embed(title=":peach: Random Hentai Anal", color=0xF08080)
        embed.set_image(url="https://cdn.nekos.life/anal/anal" + num_string + ".gif")
        embed.set_footer(text="All Images Owned by the Creators of NekoBot", icon_url="https://images.discordapp.net/avatars/310039170792030211/b14caa57a169fdd3595c8560f7e31a3f.png?size=512")
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        await bot.say(embed=embed)

        return

    elif tag.lower() == "lesbian":
        number = random.randint(1, 197)

        num_string = ""
        if number < 10:
            num_string = "00" + str(number)
        elif number < 100:
            num_string = "0" + str(number)
        else:
            num_string = str(number)

        embed = discord.Embed(title=":two_women_holding_hands: Random Hentai Lesbian", color=0xF08080)
        embed.set_image(url="https://cdn.nekos.life/les/OnlyG" + num_string + ".gif")
        embed.set_footer(text="All Images Owned by the Creators of NekoBot", icon_url="https://images.discordapp.net/avatars/310039170792030211/b14caa57a169fdd3595c8560f7e31a3f.png?size=512")
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        await bot.say(embed=embed)

        return

    elif tag.lower() == "bj":
        number = random.randint(1, 207)

        num_string = ""
        if number < 10:
            num_string = "00" + str(number)
        elif number < 100:
            num_string = "0" + str(number)
        else:
            num_string = str(number)

        embed = discord.Embed(title=":eggplant: Random Hentai Blowjob", color=0xF08080)
        embed.set_image(url="https://cdn.nekos.life/bj/bjl" + num_string + ".gif")
        embed.set_footer(text="All Images Owned by the Creators of NekoBot", icon_url="https://images.discordapp.net/avatars/310039170792030211/b14caa57a169fdd3595c8560f7e31a3f.png?size=512")
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        await bot.say(embed=embed)

        return

    elif tag.lower() == "cum":
        number = random.randint(1, 64)

        num_string = ""
        if number < 10:
            num_string = "0" + str(number)
        else:
            num_string = str(number)

        print("https://cdn.nekos.life/cum/cum" + num_string + ".gif")

        embed = discord.Embed(title=":sweat_drops: Random Hentai Cum", color=0xF08080)
        embed.set_image(url="https://cdn.nekos.life/cum/cum" + num_string + ".gif")
        embed.set_footer(text="All Images Owned by the Creators of NekoBot", icon_url="https://images.discordapp.net/avatars/310039170792030211/b14caa57a169fdd3595c8560f7e31a3f.png?size=512")
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        await bot.say(embed=embed)

        return

    else:
        embed = discord.Embed(title=":x: Error", description="Invalid tag. In the meantime, fap to this :wink:", color=0xF08080)
        embed.set_image(url="http://www.hentaibus.com/images/big_images/2015/09/30/hentai-girls-nude-and-sexy-holy-shit-that-u0026-s-hot-1122.png")
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="All Images Owned by the Creators of NekoBot", icon_url="https://images.discordapp.net/avatars/310039170792030211/b14caa57a169fdd3595c8560f7e31a3f.png?size=512")

        await bot.say(embed=embed)

        return

@bot.command(pass_context=True)
async def imslp(ctx, *, composer):
    """get direct links to sheets on imslp"""
    if ctx.message.author.id == "225264828304850944" or ctx.message.author.id == "100238213167206400":
        return
    
    composers = []
    
    for x in range(0, len(imslp_composers)):
        if x == 0:
            composers.append(imslp_composers[x])
        elif imslp_composers[x] == imslp_composers[x-1]:
            continue
        else:
            composers.append(imslp_composers[x])

    if composer.lower() == "composers":
        composer_string = ""
        for x in range(0, len(composers)):
            composer_string = composer_string + str(x+1) + ". " + composers[x] + "\n"
        embed1 = discord.Embed(title="<:piano:504104327606960128> Available Composers", description=composer_string, color=0x0d98ba)
        embed1.set_thumbnail(url="https://cdn.dribbble.com/users/807834/screenshots/2819480/imslp_1x.png")
        embed1.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed1.set_footer(text="All Data Obtained From And Owned By IMSLP", icon_url="https://wendyhellerbaroquemusic.files.wordpress.com/2015/04/imslp-2.png?w=551")

        await bot.say(embed=embed1)
        return

    if composer.title() not in composers:
        embed1 = discord.Embed(title=":x: Error", description="Composer " + composer + " not found in database", color=0x0d98ba)
        embed1.set_thumbnail(url="https://cdn.dribbble.com/users/807834/screenshots/2819480/imslp_1x.png")
        embed1.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed1.set_footer(text="All Data Obtained From And Owned By IMSLP", icon_url="https://wendyhellerbaroquemusic.files.wordpress.com/2015/04/imslp-2.png?w=551")

        await bot.say(embed=embed1)
        return

    piecegroups = []
    piece_string = ""
    count = 1
    for x in range(0, len(imslp_composers)):
        if imslp_composers[x].lower() == composer.lower():
            piecegroups.append(imslp_piecegroups[x])
            piece_string = piece_string + str(count) + ". " + imslp_piecegroups[x] + "\n"
            count += 1

    embed1 = discord.Embed(title="<:piano:504104327606960128> Select the pieces using the respective number", description=piece_string, color=0x0d98ba)
    embed1.set_thumbnail(url="https://cdn.dribbble.com/users/807834/screenshots/2819480/imslp_1x.png")
    embed1.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed1.set_footer(text="All Data Obtained From And Owned By IMSLP", icon_url="https://wendyhellerbaroquemusic.files.wordpress.com/2015/04/imslp-2.png?w=551")

    await bot.say(embed=embed1)

    msg = await bot.wait_for_message(author = ctx.message.author)
    reply = msg.content

    try:
        piece = piecegroups[int(reply) - 1]
    except:
        embed2 = discord.Embed(title=":x: Error", description="Invalid Input", color=0x0d98ba)
        embed2.set_thumbnail(url="https://cdn.dribbble.com/users/807834/screenshots/2819480/imslp_1x.png")
        embed2.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed2.set_footer(text="All Data Obtained From And Owned By IMSLP", icon_url="https://wendyhellerbaroquemusic.files.wordpress.com/2015/04/imslp-2.png?w=551")

        await bot.say(embed=embed1)
        return

    await bot.say("Success, fetching data(may take a little bit...)")
    csvfile = "imslp-" + composer.lower() + "-" + piece.lower() + ".csv"

    piece_link_string = ""

    with open(csvfile, 'r') as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            piece_link_string = piece_link_string + "[" + row[0] + "](" + row[1].replace('(', '%28').replace(')', '%29') + ")\n"

    embed2 = discord.Embed(title="<:piano:504104327606960128> " + composer.title() + ": " + piece, description=piece_link_string, color=0x0d98ba)
    embed2.set_thumbnail(url="https://cdn.dribbble.com/users/807834/screenshots/2819480/imslp_1x.png")
    embed2.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed2.set_footer(text="All Data Obtained From And Owned By IMSLP", icon_url="https://wendyhellerbaroquemusic.files.wordpress.com/2015/04/imslp-2.png?w=551")

    await bot.say(embed=embed2)

@bot.command(pass_context=True)
async def makeameme(ctx):
    """testing"""
    embed1 = discord.Embed(title=":pushpin: Select an option from the menu below", description="""\n1. Aliens
                                                                                                    \n2. Two Buttons
                                                                                                    \n3. One Does Not Simply
                                                                                                    \n4. Futurama
                                                                                                    \n5. Yo Dawg Heard You
                                                                                                    \n6. I Don't Always
                                                                                                    \n7. Blank Nut Button
                                                                                                    \n8. Batman Slapping Robin
                                                                                                    \n9. Highway Exit
                                                                                                    \n10. The Rock Driving
                                                                                                    \n11. That Would be Great
                                                                                                    \n12. Scroll of Truth
                                                                                                    \n13. First World Problems
                                                                                                    \n14. Laughing Men in Suits""", color=0xb499cd)
    embed1.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed1.set_footer(text="ImgFlip API", icon_url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")
    await bot.say(embed=embed1)

    msg = await bot.wait_for_message(author = ctx.message.author)
    reply = msg.content

    if reply == "1":
        await bot.say("Enter top text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text0 = ' '
        else:
            text0 = reply

        await bot.say("Enter bottom text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text1 = ' '
        else:
            text1 = reply
        
        params = {'template_id': '101470', 'username': 'ThispersonIscool', 'password': 'gameboy98', 'text0': text0, 'text1': text1}

        r = requests.post('https://api.imgflip.com/caption_image', data=params)

        json_stuff = r.json()

        embed = discord.Embed(title="URL For Phone Users: " + json_stuff['data']['url'], color=0xb499cd)
        embed.set_image(url=json_stuff['data']['url'])
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="ImgFlip API", icon_url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")

        await bot.say(embed=embed)
        
        return
    elif reply == "2":
        await bot.say("Enter left text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text0 = ' '
        else:
            text0 = reply

        await bot.say("Enter right text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text1 = ' '
        else:
            text1 = reply
        
        params = {'template_id': '87743020', 'username': 'ThispersonIscool', 'password': 'gameboy98', 'text0': text0, 'text1': text1}

        r = requests.post('https://api.imgflip.com/caption_image', data=params)

        json_stuff = r.json()

        embed = discord.Embed(title="URL For Phone Users: " + json_stuff['data']['url'], color=0xb499cd)
        embed.set_image(url=json_stuff['data']['url'])
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="ImgFlip API", icon_url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")

        await bot.say(embed=embed)
    elif reply == "3":
        await bot.say("Enter text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text1 = ' '
        else:
            text1 = reply
        
        params = {'template_id': '61579', 'username': 'ThispersonIscool', 'password': 'gameboy98', 'text0': "One does not simply", 'text1': text1}

        r = requests.post('https://api.imgflip.com/caption_image', data=params)

        json_stuff = r.json()

        embed = discord.Embed(title="URL For Phone Users: " + json_stuff['data']['url'], color=0xb499cd)
        embed.set_image(url=json_stuff['data']['url'])
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="ImgFlip API", icon_url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")

        await bot.say(embed=embed)

        return
    elif reply == "4":
        await bot.say("Enter top text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text0 = ' '
        else:
            text0 = reply

        await bot.say("Enter bottom text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text1 = ' '
        else:
            text1 = reply
        
        params = {'template_id': '61520', 'username': 'ThispersonIscool', 'password': 'gameboy98', 'text0': text0, 'text1': text1}

        r = requests.post('https://api.imgflip.com/caption_image', data=params)

        json_stuff = r.json()

        embed = discord.Embed(title="URL For Phone Users: " + json_stuff['data']['url'], color=0xb499cd)
        embed.set_image(url=json_stuff['data']['url'])
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="ImgFlip API", icon_url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")

        await bot.say(embed=embed)

        return
    elif reply == "5":
        await bot.say("Enter top text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text0 = ' '
        else:
            text0 = reply

        await bot.say("Enter bottom text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text1 = ' '
        else:
            text1 = reply
        
        params = {'template_id': '101716', 'username': 'ThispersonIscool', 'password': 'gameboy98', 'text0': text0, 'text1': text1}

        r = requests.post('https://api.imgflip.com/caption_image', data=params)

        json_stuff = r.json()

        embed = discord.Embed(title="URL For Phone Users: " + json_stuff['data']['url'], color=0xb499cd)
        embed.set_image(url=json_stuff['data']['url'])
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="ImgFlip API", icon_url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")

        await bot.say(embed=embed)

        return
    elif reply == "6":
        await bot.say("Enter top text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text0 = ' '
        else:
            text0 = reply

        await bot.say("Enter bottom text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text1 = ' '
        else:
            text1 = reply
        
        params = {'template_id': '61532', 'username': 'ThispersonIscool', 'password': 'gameboy98', 'text0': text0, 'text1': text1}

        r = requests.post('https://api.imgflip.com/caption_image', data=params)

        json_stuff = r.json()

        embed = discord.Embed(title="URL For Phone Users: " + json_stuff['data']['url'], color=0xb499cd)
        embed.set_image(url=json_stuff['data']['url'])
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="ImgFlip API", icon_url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")

        await bot.say(embed=embed)

        return
    elif reply == "7":
        await bot.say("Enter hand text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text0 = ' '
        else:
            text0 = reply

        await bot.say("Enter button text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text1 = ' '
        else:
            text1 = reply
        
        params = {'template_id': '119139145', 'username': 'ThispersonIscool', 'password': 'gameboy98', 'text0': text0, 'text1': text1}

        r = requests.post('https://api.imgflip.com/caption_image', data=params)

        json_stuff = r.json()

        embed = discord.Embed(title="URL For Phone Users: " + json_stuff['data']['url'], color=0xb499cd)
        embed.set_image(url=json_stuff['data']['url'])
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="ImgFlip API", icon_url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")

        await bot.say(embed=embed)
        
        return
    elif reply == "8":
        await bot.say("Enter left text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text0 = ' '
        else:
            text0 = reply

        await bot.say("Enter right text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text1 = ' '
        else:
            text1 = reply
        
        params = {'template_id': '438680', 'username': 'ThispersonIscool', 'password': 'gameboy98', 'text0': text0, 'text1': text1}

        r = requests.post('https://api.imgflip.com/caption_image', data=params)

        json_stuff = r.json()

        embed = discord.Embed(title="URL For Phone Users: " + json_stuff['data']['url'], color=0xb499cd)
        embed.set_image(url=json_stuff['data']['url'])
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="ImgFlip API", icon_url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")

        await bot.say(embed=embed)
        
        return
    elif reply == "9":
        await bot.say("Enter left text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text0 = ' '
        else:
            text0 = reply

        await bot.say("Enter right text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text1 = ' '
        else:
            text1 = reply
        
        params = {'template_id': '124822590', 'username': 'ThispersonIscool', 'password': 'gameboy98', 'text0': text0, 'text1': text1}

        r = requests.post('https://api.imgflip.com/caption_image', data=params)

        json_stuff = r.json()

        embed = discord.Embed(title="URL For Phone Users: " + json_stuff['data']['url'], color=0xb499cd)
        embed.set_image(url=json_stuff['data']['url'])
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="ImgFlip API", icon_url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")

        await bot.say(embed=embed)
        
        return
    elif reply == "10":
        await bot.say("Enter top text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text0 = ' '
        else:
            text0 = reply

        await bot.say("Enter bottom text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text1 = ' '
        else:
            text1 = reply
        
        params = {'template_id': '21735', 'username': 'ThispersonIscool', 'password': 'gameboy98', 'text0': text0, 'text1': text1}

        r = requests.post('https://api.imgflip.com/caption_image', data=params)

        json_stuff = r.json()

        embed = discord.Embed(title="URL For Phone Users: " + json_stuff['data']['url'], color=0xb499cd)
        embed.set_image(url=json_stuff['data']['url'])
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="ImgFlip API", icon_url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")

        await bot.say(embed=embed)
        
        return
    elif reply == "11":
        await bot.say("Enter top text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text0 = ' '
        else:
            text0 = reply

        await bot.say("Enter bottom text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text1 = ' '
        else:
            text1 = reply
        
        params = {'template_id': '563423', 'username': 'ThispersonIscool', 'password': 'gameboy98', 'text0': text0, 'text1': text1}

        r = requests.post('https://api.imgflip.com/caption_image', data=params)

        json_stuff = r.json()

        embed = discord.Embed(title="URL For Phone Users: " + json_stuff['data']['url'], color=0xb499cd)
        embed.set_image(url=json_stuff['data']['url'])
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="ImgFlip API", icon_url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")

        await bot.say(embed=embed)
        
        return
    elif reply == "12":
        await bot.say("Enter text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text0 = ' '
        else:
            text0 = reply
        
        params = {'template_id': '123999232', 'username': 'ThispersonIscool', 'password': 'gameboy98', 'text0': text0, 'text1': ' '}

        r = requests.post('https://api.imgflip.com/caption_image', data=params)

        json_stuff = r.json()

        embed = discord.Embed(title="URL For Phone Users: " + json_stuff['data']['url'], color=0xb499cd)
        embed.set_image(url=json_stuff['data']['url'])
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="ImgFlip API", icon_url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")

        await bot.say(embed=embed)
        
        return
    elif reply == "13":
        await bot.say("Enter top text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text0 = ' '
        else:
            text0 = reply

        await bot.say("Enter bottom text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text1 = ' '
        else:
            text1 = reply
        
        params = {'template_id': '61539', 'username': 'ThispersonIscool', 'password': 'gameboy98', 'text0': text0, 'text1': text1}

        r = requests.post('https://api.imgflip.com/caption_image', data=params)

        json_stuff = r.json()

        embed = discord.Embed(title="URL For Phone Users: " + json_stuff['data']['url'], color=0xb499cd)
        embed.set_image(url=json_stuff['data']['url'])
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="ImgFlip API", icon_url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")

        await bot.say(embed=embed)
        
        return
    elif reply == "14":
        await bot.say("Enter top text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text0 = ' '
        else:
            text0 = reply

        await bot.say("Enter bottom text (type none to skip this text)")
        msg = await bot.wait_for_message(author = ctx.message.author)
        reply = msg.content

        if reply.lower() == 'none':
            text1 = ' '
        else:
            text1 = reply
        
        params = {'template_id': '922147', 'username': 'ThispersonIscool', 'password': 'gameboy98', 'text0': text0, 'text1': text1}

        r = requests.post('https://api.imgflip.com/caption_image', data=params)

        json_stuff = r.json()

        embed = discord.Embed(title="URL For Phone Users: " + json_stuff['data']['url'], color=0xb499cd)
        embed.set_image(url=json_stuff['data']['url'])
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="ImgFlip API", icon_url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")

        await bot.say(embed=embed)
        
        return
    else:
        embed = discord.Embed(title=":x: Error: Invalid Entry", color=0xb499cd)
        embed.set_thumbnail(url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_footer(text="ImgFlip API", icon_url="https://d1ge76rambtuys.cloudfront.net/icons/com.imgflip.png")

        await bot.say(embed=embed)
        return

@bot.command(pass_context=True)
async def crappyjoke(ctx):
    """gets a random crappy programming joke"""
    random_joke = pyjokes.get_joke(language='en', category="all")

    embed1 = discord.Embed(title=":speech_left: Random crappy joke", description=random_joke, color=0x9ACD32)
    embed1.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed1.set_thumbnail(url="https://emojipedia-us.s3.amazonaws.com/thumbs/120/apple/129/face-palm_1f926.png")
    embed1.set_footer(text="Pyjokes Library", icon_url="http://pyjok.es/images/pyjokes.png")
    await bot.say(embed=embed1)

@bot.command()
async def leet(mode, *, sentence):
    original_sentence = sentence
    
    sentence.lower()

    if mode.lower() == 'leet':
        sentence = sentence.replace('a', '4')
        sentence = sentence.replace('b', '8')
        sentence = sentence.replace('c', '[')
        sentence = sentence.replace('d', 'o|')
        sentence = sentence.replace('e', '3')
        sentence = sentence.replace('f', '|=')
        sentence = sentence.replace('g', '6')
        sentence = sentence.replace('h', '|-|')
        sentence = sentence.replace('i', '!')
        #sentence = sentence.replace('j', '_|')
        sentence = sentence.replace('k', '|<')
        sentence = sentence.replace('l', '1')
        sentence = sentence.replace('m', '|\ /|')
        sentence = sentence.replace('n', '|\ |')
        sentence = sentence.replace('o', '0')
        sentence = sentence.replace('p', '|>')
        sentence = sentence.replace('q', '9')
        sentence = sentence.replace('r', '|Z')
        sentence = sentence.replace('s', '5')
        sentence = sentence.replace('t', '7')
        sentence = sentence.replace('u', '|_|')
        sentence = sentence.replace('v', '\ /')
        sentence = sentence.replace('w', 'vv')
        sentence = sentence.replace('x', '><')
        sentence = sentence.replace('y', '¥')
        sentence = sentence.replace('z', '2')
    elif mode.lower() == 'english':
        sentence = sentence.replace('4', 'a')
        sentence = sentence.replace('8', 'b')
        sentence = sentence.replace('[', 'c')
        sentence = sentence.replace('{', 'c')
        sentence = sentence.replace('{', 'c')
        sentence = sentence.replace('o|', 'd')
        sentence = sentence.replace('0|', 'd')
        sentence = sentence.replace('|)', 'd')
        sentence = sentence.replace('|]', 'd')
        sentence = sentence.replace('|}', 'd')
        sentence = sentence.replace('3', 'e')
        sentence = sentence.replace('|=', 'f')
        sentence = sentence.replace('6', 'g')
        sentence = sentence.replace('|-|', 'h')
        sentence = sentence.replace('!', 'i')
        sentence = sentence.replace('_|', 'j')
        sentence = sentence.replace('|<', 'k')
        sentence = sentence.replace('1', 'l')
        sentence = sentence.replace('|\ /|', 'm')
        sentence = sentence.replace('|\ |', 'n')
        sentence = sentence.replace('0', 'o')
        sentence = sentence.replace('|>', 'p')
        sentence = sentence.replace('9', 'q')
        sentence = sentence.replace('|Z', 'r')
        sentence = sentence.replace('5', 's')
        sentence = sentence.replace('7', 't')
        sentence = sentence.replace('vv', 'w')
        sentence = sentence.replace('v', 'u')
        sentence = sentence.replace('|_|', 'u')
        sentence = sentence.replace('\ /', 'v')
        sentence = sentence.replace('><', 'x')
        sentence = sentence.replace('¥', 'y')
        sentence = sentence.replace('2', 'z')
    else:
        embed = discord.Embed(title=":x: Error: Not a valid mode", description="Please pick a mode between english and leet", color=0x003366)
        embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
        embed.set_thumbnail(url="https://image.winudf.com/v2/image/Y29tLktpbGxlckJMUy5sZWV0X2ljb25fMF8zMzE5Mzc5Mw/icon.png?w=170&fakeurl=1&type=.png")
        embed.set_footer(text="Discord", icon_url='https://www.shareicon.net/data/512x512/2017/06/21/887435_logo_512x512.png')

        await bot.say(embed=embed)

        return

    embed = discord.Embed(title="1337 translator", description="Original Sentence: " + original_sentence, color=0x003366)
    embed.add_field(name="Translated Sentence:", value=sentence)
    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_thumbnail(url="https://image.winudf.com/v2/image/Y29tLktpbGxlckJMUy5sZWV0X2ljb25fMF8zMzE5Mzc5Mw/icon.png?w=170&fakeurl=1&type=.png")
    embed.set_footer(text="Discord", icon_url='https://www.shareicon.net/data/512x512/2017/06/21/887435_logo_512x512.png')

    await bot.say(embed=embed)

"""
@bot.command(pass_context=True)
async def lyrics(ctx):
    returns the lyrics of a specific song
    await bot.say("Please enter song name")
    msg = await bot.wait_for_message(author = ctx.message.author)
    song = msg.content

    await bot.say("Please enter artist name")
    msg2 = await bot.wait_for_message(author = ctx.message.author)
    artist = msg2.content

   
    line = PyLyrics.getLyrics(artist,song)
    stanzas = [line[i:i+1000] for i in range(0, len(line), 1000)]

    embed = discord.Embed(title=":headphones: " + song, description=artist, color=0x75d1af)
    for x in range(0, len(stanzas)):
        embed.add_field(name="\u200b", value=stanzas[x])

    embed.set_author(name="UrbanBot", icon_url='https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/hostedimages/1393787701i/8763384.jpg')
    embed.set_footer(text="PyLyrics Library and lyrics.wikia.com", icon_url='https://vignette.wikia.nocookie.net/lyricwiki/images/8/89/Wiki-wordmark.png/revision/latest?cb=20171025141541')

    await bot.say(embed=embed)
"""
#error catcher
@bot.async_event
async def on_command_error(error, ctx):
    if isinstance(error, commands.MissingRequiredArgument):
        await bot.send_message(ctx.message.channel, "Error: Missing command arguments")
    elif isinstance(error, commands.BadArgument):
        await bot.send_message(ctx.message.channel, "Error: Bad command argument")
    elif isinstance(error, commands.TooManyArguments):
        await bot.send_message(ctx.message.channel, "Error: Too many arguments")
    elif isinstance(error, commands.CommandNotFound):
        print("Error: Command not found")
    else:
        await bot.send_message(ctx.message.channel, str(error))

#to initialize the main class and extend the music.py file
if __name__ == "__main__":
    for extension in extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print("main Error: ", e)

bot.run('Insert Token Here')

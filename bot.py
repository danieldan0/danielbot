import discord
import asyncio
import urllib.request
import json
from math import *
from random import *

client = discord.Client()
allstar1 = """BODY  once told me the world is gonna roll me
I ain't the sharpest tool in the shed
She was looking kind of dumb with her finger and her thumb
In the shape of an "L" on her forehead
Well the years start coming and they don't stop coming
Fed to the rules and I hit the ground running
Didn't make sense not to live for fun
Your brain gets smart but your head gets dumb
So much to do, so much to see
So what's wrong with taking the back streets?
You'll never know if you don't go
You'll never shine if you don't glow
Hey now, you're an all-star, get your game on, go play
Hey now, you're a rock star, get the show on, get paid
And all that glitters is gold
Only shooting stars break the mold
It's a cool place and they say it gets colder
You're bundled up now, wait till you get older
But the meteor men beg to differ
Judging by the hole in the satellite picture
The ice we skate is getting pretty thin
The water's getting warm so you might as well swim
My world's on fire, how about yours?
That's the way I like it and I never get bored
Hey now, you're an all-star, get your game on, go play
Hey now, you're a rock star, get the show on, get paid
All that glitters is gold
Only shooting stars break the mold
Hey now, you're an all-star, get your game on, go play
Hey now, you're a rock star, get the show, on get paid
And all that glitters is gold
Only shooting stars
Somebody once asked could I spare some change for gas?
I need to get myself away from this place
I said yep what a concept
I could use a little fuel myself
And we could all use a little change
Well, the years start coming and they don't stop coming
Fed to the rules and I hit the ground running
Didn't make sense not to live for fun
Your brain gets smart but your head gets dumb
So much to do, so much to see
So what's wrong with taking the back streets?
You'll never know if you don't go (go!)
You'll never shine if you don't glow
Hey now, you're an all-star, get your game on, go play"""
allstar2 = """Hey now, you're a rock star, get the show on, get paid
And all that glitters is gold
Only shooting stars break the mold
And all that glitters is gold
Only shooting stars break the mold"""

tpt_general_id = "311697121914912768"

tpt_snapshots = """**TPT snapshots**:
 
*Windows 32-bit*: http://starcatcher.us/TPT/Download/Snapshot.zip
*Linux 64-bit*: http://starcatcher.us/TPT/Download/Snapshot%20linux64.zip
*Linux 32-bit*: http://starcatcher.us/TPT/Download/Snapshot%20linux32.zip
*MacOS*: http://starcatcher.us/TPT/Download/Snapshot.dmg"""

async def teval(channel, x, t):
    await asyncio.sleep(t)
    await client.send_message(channel, eval(x))

async def motd_task():
    await client.wait_until_ready()
    channel = discord.Object(id=tpt_general_id)
    motd = ""
    while not client.is_closed:
        await asyncio.sleep(10) # task runs every 10 seconds

async def get_save(save):
    await client.wait_until_ready()
    return "http://tpt.io/~" + str(save["ID"]) + " "

async def get_fp(channel, data):
    message = ""
    for save in data["Saves"]:
        message += await get_save(save)
    await client.send_message(channel, message)

async def get_user(channel, username):
    await client.wait_until_ready()
    data = json.load(urllib.request.urlopen("http://powdertoy.co.uk/User.json?Name=" + username))
    data = data["User"]
    message = ""
    message += "Username: " + data["Username"] + "\n"
    if data["Biography"] :
        message += "Biography: " + str(data["Biography"]) + "\n"
    if data["Avatar"].startswith("/Avatars"):
        message += " http://powdertoy.co.uk" + data["Avatar"] + " \n"
    else:
        message += " " + data["Avatar"] + " \n"
    if data["Age"]:
        message += "Age: " + str(data["Age"]) + "\n"
    if data["Website"]:
        message += "Website: " + data["Website"] + " \n"
    message += "Saves:\n"
    message += "Count:" + str(data["Saves"]["Count"]) + " Avg. Score: " + str(data["Saves"]["AverageScore"]) + " Highest Score: " + str(data["Saves"]["HighestScore"])
    await client.send_message(channel, message)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='The Powder Toy'))

@client.event
async def on_message(message):
    if (message.content.lower().startswith('some') and len(message.content) < 5) or message.content.lower().startswith('someBODY'):
        await client.send_message(message.channel, allstar1)
        await client.send_message(message.channel, allstar2)
    elif message.content.startswith('~') and not message.content.startswith('~~'):
        await client.send_message(message.channel, 'http://tpt.io/' + message.content.split(" ")[0])
        await client.send_message(message.channel, 'http://static.powdertoy.co.uk/' + message.content.split(" ")[0][1:] + '.png')
    elif message.content.lower().startswith('id:'):
        await client.send_message(message.channel, 'http://tpt.io/~' + message.content.split(" ")[0].split(":")[1])
        await client.send_message(message.channel, 'http://static.powdertoy.co.uk/' + message.content.split(" ")[0].split(":")[1] + '.png')
    elif message.content.startswith(r'<@!374150521365463040>'):
        if (''.join(message.content.split(" ")[1:3])).lower().startswith("goodbot"):
            await client.send_message(message.channel, "good human")
        elif (''.join(message.content.split(" ")[1:3])).lower().startswith("badbot"):
            await client.send_message(message.channel, "bad human")
        elif message.author.id == "330502591731597313":
            await client.send_message(message.channel, input())
    elif message.content.lower().startswith('download'):
        await client.send_message(message.channel, tpt_snapshots)
    elif message.content.lower().startswith('fp'):
        await get_fp(message.channel, json.load(urllib.request.urlopen("http://powdertoy.co.uk/Browse.json")))
    elif message.content.lower().startswith('recent saves'):
        await get_fp(message.channel, json.load(urllib.request.urlopen("http://powdertoy.co.uk/Browse.json?Search_Query=sort%3Adate")))
    elif message.content.lower().startswith('user '):
        await get_user(message.channel, message.content.split(" ")[1])
    elif message.content.lower().startswith('search '):
        await get_fp(message.channel, json.load(urllib.request.urlopen("http://powdertoy.co.uk/Browse.json?Search_Query=" + "+".join(message.content.split(" ")[1:]))))
    elif message.content.lower().startswith('eval '):
        await client.send_message(message.channel, str(eval(" ".join(message.content.split(" ")[1:]))))
    elif message.content.lower().startswith('teval '):
        await teval(message.channel, ' '.join(message.content.split(" ")[2:]), float(message.content.split(" ")[1]))
    elif message.content.lower().startswith('lovecalc '):
        await client.send_message(message.channel, str(random() * 100) + "%")
    elif message.content.lower().startswith('hi bot'):
        await client.send_message(message.channel, "omae wa mou shindeiru")
    elif message.content.lower().startswith('omae wa mou shindeiru') and message.author.id != "374150521365463040":
        await client.send_message(message.channel, "***N-NANI?!***")
        

client.loop.create_task(motd_task())
client.run(open("token.txt", "r").read())

#bot.py
from email import message
import os
from re import L
import model
import fumo as fumoModule
from math import ceil

import discord
from discord.ext import commands
from dotenv import load_dotenv

STORE_DICT = {
    'auction': "Yahoo! JAPAN Auction",
    'shopping': "Yahoo! JAPAN Shopping",
    'mercari': "Mercari",
    'rakuten': "Rakuten",
    'rakuma': 'Rakuma'
}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.members = True

# client = discord.Client(intents=intents)


bot = commands.Bot(command_prefix='f!', intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for guild in bot.guilds:
        break

    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name} (id: {guild.id})'
    )

@bot.command(name='help')
async def _help(ctx, command=''):
    embed = discord.Embed(title="FumoBot Help",
        color=discord.Color.blue())

    embed.set_author(name='FumoBot',
                    icon_url=bot.user.avatar_url)

    embed.add_field(name='f!search', value='Displays a list of the given fumos on sale.\n__Example:__ **f!search koishi**', inline=False)
    embed.add_field(name='f!saved', value='Gets the link to see your saved fumos.', inline=False)
    embed.add_field(name='f!vote', value='Make a vote for your favorite fumo.\n__Example:__ **f!vote reimu**', inline=False)
    embed.add_field(name='f!seeVotes', value='Check the current fumo vote tally.', inline=False)
    embed.add_field(name='f!gif', value='Get a random fumo GIF!\n__Example:__ **f!gif tewi** (can also leave blank)\n', inline=False)

    await ctx.send(embed=embed)

    # members = '\n - '.join([member.name for member in guild.members])
    # print(f'Guild members:\n - {members}')

@bot.command()
async def saved(ctx):
    personalURL = f'http://fumo-search.herokuapp.com/saved/?userName={ctx.author.name}'
    await ctx.author.send(f"Your saved fumos can be viewed at:\n{personalURL}")


@bot.command()
async def vote(ctx, fumo=''):
    if fumo == '':
        await ctx.send('Please enter a fumo to vote for!', delete_after=5)
        return
    
    fumo = fumoModule.getFumoKey(fumo)
    if fumo == '':
        await ctx.send('Invalid fumo entered.', delete_after=5)
        return
    
    model.voteForFumo(str(ctx.author), fumo)
    await ctx.send(f'{ctx.author.name} voted for {fumo}!', delete_after=5)

@bot.command()
async def seeVotes(ctx):
    votes = model.getVotes()

    embedText = ''
    
    for fumo, voteNum in votes:
        embedText += f'**{fumo}**: {voteNum} votes\n'

    embed = discord.Embed(title="Fumo Popularity",
        color=discord.Color.blue())

    embed.add_field(name="Votes", value=embedText)

    embed.set_footer(text='Make a vote with *f!vote* !')

    await ctx.send(embed=embed)

@bot.command()
async def gif(ctx, fumo=''):
    if fumo != '':
        fumo = fumoModule.getFumoKey(fumo)
        if fumo == '':
            await ctx.send('Invalid fumo entered.', delete_after=5)
            return

    url = model.getFumoGIF(fumo)
    if url == '':
        await ctx.send('No GIF found of that fumo. <:sanaeEat:966579048010616832>')
        return

    await ctx.send(url)

# @bot.command()
# async def reply(ctx, *, text):
#     await ctx.send(text)

# @bot.command()
# async def add(ctx, n1: int, n2: int):
#     await ctx.send(n1 + n2)

@bot.command()
async def whoami(ctx):
    await ctx.send(str(ctx.author))

FUMO_MESSAGES = list()
CACHED_FUMO_DATA = list()
CUR_PAGE = 0
LAST_PAGE = 0

def getEmbedFumos(fumoData):
    embedArr = []

    for i, fumo in enumerate(fumoData):
        embed = discord.Embed(title=fumo["title"],
                          url=fumo['buyLink'],
                          color=0xFF5733)
        embed.set_image(url=fumo['imgLink']+'?w=150&h=150')
        embed.add_field(name="Store", value=STORE_DICT[fumo['shop']])
    
        if fumo['isAuction']:
            embed.add_field(name="Current Price", value=f'{fumo["price"]} yen', inline=True)
            if fumo['buyoutPrice'] != 0:
                embed.add_field(name="Buyout Price", value=f'{fumo["buyoutPrice"]} yen', inline=True)
        else:
            embed.add_field(name="Price", value=f'{fumo["price"]} yen')

        if i == len(fumoData)-1:
            embed.set_footer(text='http://fumo-search.herokuapp.com/ for more info and filtering options!')

        # embed.add_field(name="Info", value=f'{fumo["buyLink"]}\nPrice: {fumo["price"]} yen')
        embedArr.append(embed)
    
    return embedArr

async def sendEmbedFumos(embedArr, channel):
    global FUMO_MESSAGES

    for oldMsg in FUMO_MESSAGES:
        await oldMsg.delete()

    FUMO_MESSAGES = list()
    
    for embed in embedArr:
        message = await channel.send(embed=embed)
        await message.add_reaction('❤️')
        FUMO_MESSAGES.append(message)

    lastMessage = FUMO_MESSAGES[-1]
    if CUR_PAGE > 1:
        await lastMessage.add_reaction('⬅️')  
    if CUR_PAGE < LAST_PAGE:
        await lastMessage.add_reaction('➡️')

@bot.command()
async def search(ctx, fumoName=''):
    global CACHED_FUMO_DATA
    global CUR_PAGE
    global LAST_PAGE

    if fumoName == '':
        message = await ctx.send("Please enter a fumo to search for!", delete_after=5)
        return

    fumoKey = fumoModule.getFumoKey(fumoName)
    if fumoKey == '':
        message = await ctx.send("Could not find that fumo!", delete_after=5)
        return

    fumoData = model.getFumos(fumoKey)
    CACHED_FUMO_DATA = fumoData
    CUR_PAGE = 1
    LAST_PAGE = ceil(len(fumoData) / 5)

    embedArr = getEmbedFumos(fumoData[:5])              # Get up to 5 fumos initially
    await sendEmbedFumos(embedArr, ctx.channel)


async def editFumoList(emoji, channel):
    global CUR_PAGE

    if emoji == '⬅️' and CUR_PAGE > 1:
        CUR_PAGE -= 1
        startIndex = (CUR_PAGE-1) * 5
        embedArr = getEmbedFumos(CACHED_FUMO_DATA[startIndex:startIndex+5])
        await sendEmbedFumos(embedArr, channel)
    elif emoji == '➡️' and CUR_PAGE < LAST_PAGE:
        CUR_PAGE += 1
        startIndex = (CUR_PAGE-1) * 5
        embedArr = getEmbedFumos(CACHED_FUMO_DATA[startIndex:startIndex+5])
        await sendEmbedFumos(embedArr, channel)



@bot.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel

    if user.id == bot.user.id:                          # Don't do anything for reactions the bot added itself
        return

    if reaction.message.id not in set(msg.id for msg in FUMO_MESSAGES):        # Don't do anything for reactions that weren't on the message the bot sent
        return

    if reaction.emoji == '➡️' or reaction.emoji == '⬅️':
        await editFumoList(reaction.emoji, channel)

    if reaction.emoji == '❤️':
        buyLink = reaction.message.embeds[0].url
        userName = user.name
        
        addedNew = model.toggleSaveFumo(userName, buyLink, add=True)

        await channel.send(content=f'Fumo added to saved!\nHead to https://fumo-search.herokuapp.com/saved/?userName={user.name} to see your saved fumos.', delete_after=6)
        print("Fumo successfully added!")

    
    # if reaction.emoji == '➡️':
    #     await reaction.message.channel.send('Right clicked')
    # elif reaction.emoji == '⬅️':
    #     await reaction.message.channel.send('Left clicked')

@bot.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel

    if user.id == bot.user.id:                          # Don't do anything for reactions the bot removed itself
        return

    if reaction.message.id not in set(msg.id for msg in FUMO_MESSAGES):        # Don't do anything for reactions that weren't on the message the bot sent
        return

    if reaction.emoji == '❤️':
        buyLink = reaction.message.embeds[0].url
        userName = user.name
        
        addedNew = model.toggleSaveFumo(userName, buyLink, add=False)

        await channel.send(content=f'Fumo removed from saved!\nHead to https://fumo-search.herokuapp.com/saved/?userName={user.name} to see your saved fumos.', delete_after=6)


    


bot.run(TOKEN)

# @client.event
# async def on_message(message):
#     if message.author == client.user:
#         return

#     if message.content.startswith('f!hello'):
#         await message.channel.send('Hello yourself!')
    
    # print(f'Message from {message.author}: {message.content}')

    


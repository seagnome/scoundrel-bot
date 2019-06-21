import discord
import os
import json
import random
from discord.ext import commands
from discord.ext.commands import Bot 

bot = commands.Bot(command_prefix='$')

with open('config.json') as f:
    config = json.load(f)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def hd(ctx, a: int=1, b: int=6): #highest dice, for Blades
    highest = -1
    storage = []
    cc = 0
    for i in range(0, a):
        storage.append(random.randrange(1,b+1))
        if storage[i] > highest:
            highest = storage[i]
        if storage[i] == 6:
            cc+=1
    await ctx.send(storage)
    if cc<2:
        await ctx.send("Highest Result:{}".format(highest))
    else:
        await ctx.send("Highest Result: CRIT")

@bot.command()
async def ld(ctx, a: int=1, b: int=6): #lowest dice, for Blades vice/obligation/0d
    lowest = b+1
    storage = []
    for i in range(0, a):
        storage.append(random.randrange(1,b+1))
        if storage[i] < lowest:
            lowest = storage[i]
    await ctx.send(storage)
    await ctx.send("Lowest Result:{}".format(lowest))

@bot.command()
async def sd(ctx, a: int=1, b: int=20, c:int=0): #sums #a dice with #b sides each, then adds c
    summation = 0
    for i in range(0, a):
        summation+=random.randrange(1,b+1)
    await ctx.send(summation+c)

@bot.command()
async def rd(ctx, a: int=1, b:int=6):
    highest = -1
    lowest = b+1
    storage = []
    cc = 0
    if a<1:
        for i in range(0,2):
            storage.append(random.randrange(1,b+1))
            if storage[i] < lowest:
                lowest = storage[i]
    else:
        for i in range(0, a):
            storage.append(random.randrange(1,b+1))
            if storage[i] > highest:
                highest = storage[i]
            if storage[i] == 6:
                cc+=1
    await ctx.send(storage)
    if a<1:
        await ctx.send("Stress Taken:{}".format(6-lowest))
    elif cc<2:
        await ctx.send("Stress Taken:{}".format(6-highest))
    else:
        await ctx.send("Highest Result: CRIT")

@bot.command()
async def vamp(ctx, a: int=1, t: int=6):
    storage = []
    sc = 0
    oc = 0
    for i in range(0, a):
        storage.append(random.randrange(1,11))
        if storage[i] >=t or storage[i]==10:
            sc+=1
        elif storage[i] ==1:
            oc +=1
    await ctx.send(storage)
    await ctx.send("Net Successes: {}".format(sc-oc))
    await ctx.send("Rolls over {}:{}".format(t, sc))
    await ctx.send("Ones:{}".format(oc))

@bot.command()
async def mage(ctx, a: int=1):
    storage = []
    sc = 0
    tc = 0
    for i in range(0, a):
        storage.append(random.randrange(1,11))
        if storage[i] >=8:
            sc+=1
            if storage[i]==10:
                tc+=1
    await ctx.send(storage)
    if sc>=5:
        await ctx.send("Exceptional! Successes: {}".format(sc))
    else:
        await ctx.send("Successes: {}".format(sc))
    await ctx.send("Tens:{}".format(tc))

@bot.command()
async def ex(ctx, a: int,  auto: str='0', dif:int=7, double: int=10):
    storage = [] #recursive function needed for rerolling (like open rolls in BW)
    sc = 0          # default difficulty is >=7
    auto = int(auto)
    for i in range(0, a): #default auto is 0
        storage.append(random.randrange(1,11)) #default doubling is 10s
        if storage[i] >=dif:
            sc+=1
            if storage[i]>=double:
                sc+=1
    await ctx.send(storage)
    await ctx.send("Automatic Successes: {}".format(auto))
    await ctx.send("Total Successes: {}".format(sc+auto))
    
@bot.command()
async def choose(ctx, a: int,  b: int):
    factorial = {0:1,1:1, 2:2, 3:6}
    #(a!)/(b!*(b-a)!)
    ch = fact(a)/(fact(b)*fact(a-b))
    await ctx.send(ch)

@bot.command(pass_context=True)
async def addrole(ctx, role: discord.Role, member: discord.Member=None):
    member = member or ctx.message.author
    await client.add_roles(member, role)
    await ctx.send("{} Role Added to User".format(role))

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Scoundrel Bot", description="A bot for rolling Dice, particularly for Blades in the Dark/Forged in the Dark, Exalted, and WOD", color=0xeee657)
    
    # give info about you here
    embed.add_field(name="Author", value="SeaGnome")
    
    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Invite link](<I'm not ready to share this yet>)")

    await ctx.send(embed=embed)

bot.remove_command('help')

@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Scoundrel Bot", description="List of commands:", color=0xeee657)

    embed.add_field(name="$hd X Y", value="Gives the highest value of **X** number of die rolled, with each die having **Y** sides", inline=False)
    embed.add_field(name="$ld X Y", value="Gives the lowest value of **X** number of die rolled, with each die having **Y** sides", inline=False)
    embed.add_field(name="$sd X Y", value="Gives the summed value of **X** number of die rolled, with each die having **Y** sides", inline=False)
    embed.add_field(name="$vamp X Y", value="Gives the number of successes of **X** d10s rolled with a result greater than or equal to **Y**", inline=False)
    embed.add_field(name="$mage X", value="Gives the number of successes of **X** d10s rolled with a result greater than or equal to 8", inline=False)
    embed.add_field(name="$ex X", value="Counts exalted successes", inline=False)
    embed.add_field(name="$info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="$help", value="Gives this message", inline=False)

    await ctx.send(embed=embed)

def fact(a):
    if a in factorial.keys():
        return factorial[a]
    else:
        factorial[a]= a*fact(a-1)
        return factorial[a]
    
    
   
#bot.run(config.get('token'))
bot.run(os.environ['SCOUNDRELTOKEN'])

import aiohttp, json, requests
import asyncio
from getpass import getpass
import discord
import random
import asyncio
from discord.ext import commands
import api as m
import league_client.exceptions
import datetime
import a

def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return r,g,b

def wjson(ssid,nick,filename='db.json'):
    with open(filename,'r+',encoding='UTF-8') as f:
        file_data = json.load(f)
        txt = a.encrypt(ssid.encode(),a.keygener(),nick)
        data = {
            # f"{nick}":{
            #     f"{id}":txt.decode(),
            #     f"{nick}":f"{id}",
            # }
            f"{nick}" : f"{txt.decode()}"
        }
        file_data.update(data)
        f.seek(0)
        json.dump(file_data,f,indent=4)

def getpass(nick):
    with open('db.json','r',encoding='UTF-8') as f:
        data = json.load(f)
        try:
            txt = data[nick]
            p = a.decrypt(txt,nick).decode()
        except:
            p = None
        return p

def logger(log):
    time = datetime.datetime.now()
    rt =str(time)[0:10]
    with open(f'{rt}.log.txt','a',encoding='utf-8') as f:
        f.write(f"[{time}]{log}\n")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
time = datetime.datetime.now()

logger(f"--------------------------------------------------\n[{time}]Bot Started\n[{time}]--------------------------------------------------")
# with open(f'{rt}.log.txt', 'a',encoding='UTF-8') as f:
#     f.write(f"[{time}]--------------------------------------------------\n[{time}]Bot Started\n[{time}]--------------------------------------------------\n")

global login
login = dict()

badwords=[]
words = []
    
bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="발로란트 상점"))

def rint(min:int, max:int):
    max+=1
    return random.sample(range(min,max),1)

@bot.command(aliases=["valshp","vs","valoshop","valorantshop","vlshop","ㅍ미놰ㅔ","valahop","ㅍㄴ"])
async def valshop(ctx,nick=None,c=None):
    global login
    if nick == None or c == None or getpass(nick) == None:
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author.mention} 사용법 : !valshop [NickName] [Your Region: na - North America, latam - Latin America, br -	Brazil, eu - Europe, ap - Asia Pacific, kr - Korea]")
    else:
        await ctx.message.delete()
        if(c in ["kr","br","na","eu","latam","ap"]):
            # try:
            ssid = getpass(nick)
            if ssid != None:
                try:
                    auth,bulid = await asyncio.create_task(m.Auths(ssid))
                    storers = await asyncio.create_task(m.store(auth,bulid,c))
                    plcurl = await asyncio.create_task(m.playercard(auth,bulid,c))
                    nametag = await asyncio.create_task(m.nametag(auth))
                    name = ctx.message.author.name
                    name = name.title()
                    embed1 = discord.Embed(timestamp=ctx.message.created_at, color=storers[0][2],description="",title=f"{nametag}'s\nValorant Shop 1st Offer")
                    embed1.set_image(url=storers[5][0])
                    embed1.set_thumbnail(url=plcurl[0])
                    embed1.add_field(name=storers[0][0],value=f"Price : {storers[0][1]}vp", inline=False) #inline이 False라면 다음줄로 넘깁니다.

                    embed2 = discord.Embed(timestamp=ctx.message.created_at, color=storers[1][2],description="",title=f"{nametag}'s\nValorant Shop 2nd Offer")
                    embed2.set_image(url=storers[5][1])
                    embed2.set_thumbnail(url=plcurl[0])
                    embed2.add_field(name=storers[1][0],value=f"Price : {storers[1][1]}vp", inline=False) #inline이 False라면 다음줄로 넘깁니다.

                    embed3 = discord.Embed(timestamp=ctx.message.created_at, color=storers[2][2],description="",title=f"{nametag}'s\nValorant Shop 3rd Offer")
                    embed3.set_image(url=storers[5][2])
                    embed3.set_thumbnail(url=plcurl[0])
                    embed3.add_field(name=storers[2][0],value=f"Price : {storers[2][1]}vp", inline=False) #inline이 False라면 다음줄로 넘깁니다.

                    embed4 = discord.Embed(timestamp=ctx.message.created_at, color=storers[3][2],description="",title=f"{nametag}'s\nValorant Shop 4th Offer")
                    embed4.set_image(url=storers[5][3])
                    embed4.set_thumbnail(url=plcurl[0])
                    embed4.add_field(name=storers[3][0],value=f"Price : {storers[3][1]}vp", inline=False) #inline이 False라면 다음줄로 넘깁니다.
                    await ctx.send(f"""{ctx.message.author.mention}""")
                    await ctx.send(embeds = [embed1,embed2,embed3,embed4])
                    logger(f"{ctx.message.author} logged in Riot with 'Id : {nick}', 'Region : {c}' and checked Valorant Shop Offers. Used Server : {ctx.message.guild}. Issued Server ID : {ctx.message.guild.id}")
                except league_client.exceptions.AuthFailureError:
                    await ctx.send("Login Failed.")
                    logger(f"{ctx.message.author} logged in Riot with 'ID : {nick}', but Failed.")
                # except:
                #     await ctx.send(f"{ctx.message.author.mention}\nYou did something wrong.\nCheck your ID or Password or Region.\nThen retry again")
                #     rt =str(time)[0:10]
                #     with open(f'{rt}.log.txt', 'a',encoding='UTF-8') as f:
                #         f.write(f"[{time}] {ctx.message.author} issued problem : {m.re()}. Issued Server : {ctx.message.guild}. Issued Server ID : {ctx.message.guild.id}\n")
            else:
                await ctx.send(f"{ctx.message.author.mention}\n현재 이 닉네임으로 등록된 계정이 없습니다.")
                logger(f"{ctx.message.author} There wasn't {nametag}'s account.")
        else:
            await ctx.send(f"{ctx.message.author.mention}\nRegion ERROR")
            sdfs="Region ERROR"
            logger(f"{ctx.message.author} issued problem : {sdfs}. Issued Server : {ctx.message.guild}. Issued Server ID : {ctx.message.guild.id}")
        
@bot.command(aliases=["mn","ㅜㅡ","암"])
async def nm(ctx,nick=None,c=None):
    if nick ==None or c == None:
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author.mention} 사용법 : !nm [Riot ID] [Password] [Your Region: na - North America, latam - Latin America, br -	Brazil, eu - Europe, ap - Asia Pacific, kr - Korea]")
    else:
        await ctx.message.delete()
        ssid = getpass(nick)
        if ssid != None:
            try:
                auth,bulid = await asyncio.create_task(m.Auths(ssid))
                storers = await asyncio.create_task(m.store(auth,bulid,c))
                plcurl = await asyncio.create_task(m.playercard(auth,bulid,c))
                nametag = await asyncio.create_task(m.nametag(auth))
                name = ctx.message.author.name
                name = name.title()
                embed1 = discord.Embed(timestamp=ctx.message.created_at, color=storers[4][0][0][4],description="",title=f"{nametag}'s\nValorant Night Market 1st Offer")
                embed1.set_image(url=storers[4][1][0])
                embed1.set_thumbnail(url=plcurl[0])
                embed1.add_field(name=storers[4][0][0][0],value=f"Price : {storers[4][0][0][1]}vp\nBasic Price : {storers[4][0][0][2]}\nDiscount : {storers[4][0][0][3]}%", inline=False) #inline이 False라면 다음줄로 넘깁니다.

                embed2 = discord.Embed(timestamp=ctx.message.created_at, color=storers[4][0][1][4],description="",title=f"{nametag}'s\nValorant Night Market 2nd Offer")
                embed2.set_image(url=storers[4][1][1])
                embed2.set_thumbnail(url=plcurl[0])
                embed2.add_field(name=storers[4][0][1][0],value=f"Price : {storers[4][0][1][1]}vp\nBasic Price : {storers[4][0][1][2]}\nDiscount : {storers[4][0][1][3]}%", inline=False) #inline이 False라면 다음줄로 넘깁니다.

                embed3 = discord.Embed(timestamp=ctx.message.created_at, color=storers[4][0][2][4],description="",title=f"{nametag}'s\nValorant Night Market 3rd Offer")
                embed3.set_image(url=storers[4][1][2])
                embed3.set_thumbnail(url=plcurl[0])
                embed3.add_field(name=storers[4][0][2][0],value=f"Price : {storers[4][0][2][1]}vp\nBasic Price : {storers[4][0][2][2]}\nDiscount : {storers[4][0][2][3]}%", inline=False) #inline이 False라면 다음줄로 넘깁니다.

                embed4 = discord.Embed(timestamp=ctx.message.created_at, color=storers[4][0][3][4],description="",title=f"{nametag}'s\nValorant Night Market 4th Offer")
                embed4.set_image(url=storers[4][1][3])
                embed4.set_thumbnail(url=plcurl[0])
                embed4.add_field(name=storers[4][0][3][0],value=f"Price : {storers[4][0][3][1]}vp\nBasic Price : {storers[4][0][3][2]}\nDiscount : {storers[4][0][3][3]}%", inline=False) #inline이 False라면 다음줄로 넘깁니다.

                embed5 = discord.Embed(timestamp=ctx.message.created_at, color=storers[4][0][4][4],description="",title=f"{nametag}'s\nValorant Night Market 5th Offer")
                embed5.set_image(url=storers[4][1][4])
                embed5.set_thumbnail(url=plcurl[0])
                embed5.add_field(name=storers[4][0][4][0],value=f"Price : {storers[4][0][4][1]}vp\nBasic Price : {storers[4][0][4][2]}\nDiscount : {storers[4][0][4][3]}%", inline=False) #inline이 False라면 다음줄로 넘깁니다.

                embed6 = discord.Embed(timestamp=ctx.message.created_at, color=storers[4][0][5][4],description="",title=f"{nametag}'s\nValorant Night Market 6th Offer")
                embed6.set_image(url=storers[4][1][5])
                embed6.set_thumbnail(url=plcurl[0])
                embed6.add_field(name=storers[4][0][5][0],value=f"Price : {storers[4][0][5][1]}vp\nBasic Price : {storers[4][0][5][2]}\nDiscount : {storers[4][0][5][3]}%", inline=False) #inline이 False라면 다음줄로 넘깁니다.
                await ctx.send(f"""{ctx.message.author.mention}""")
                await ctx.send(embeds = [embed1,embed2,embed3,embed4,embed5,embed6])
                logger(f"{ctx.message.author} logged in Riot with 'Id : {nick}', 'Region : {c}' and checked night market Offers. Used Server : {ctx.message.guild}. Issued Server ID : {ctx.message.guild.id}")
            except league_client.exceptions.AuthFailureError:
                    await ctx.send("Login Failed.")
                    logger(f"{ctx.message.author} logged in Riot with 'ID : {nick}', but Failed.")
        else:
            await ctx.send(f"{ctx.message.author.mention}\n현재 이 닉네임으로 등록된 계정이 없습니다.")
            logger(f"[{ctx.message.author}] There wasn't {nametag}'s account.")


@bot.command()
async def set(ctx,ID=None,Password=None,nickname=None):
    if (ID==None or Password == None or nickname==None):
        await ctx.send("!set [ID] [Password] [NickName]")
    else:
        if ctx.guild:
            return
        else:
            if(getpass(nickname) == None):
                try:
                    auth,bulid = await asyncio.create_task(m.Auth(ID,Password))
                    ssid = auth.ssid
                    wjson(ssid,nickname)
                    await ctx.send(f"Your Account registered.\nYou can login with '{nickname}' from now on.")
                    logger(f"{ctx.message.author} registered Riot Account with 'Id : {ID}', 'NickName : {nickname}")
                except league_client.exceptions.AuthFailureError:
                    await ctx.send("Login Failed.")
                    logger(f"{ctx.message.author} registered Riot Account with 'ID : {ID}', but Failed.")
            else:
                await ctx.send(f"{nickname} is already registerd by someone.\nRetry with other nickname.")
                logger(f"{ctx.message.author} failed register account with {nickname} nickname.")

@bot.command(aliases=["Balances","balances","Bl","bl","bc","rp"])
async def vp(ctx,nick=None,c=None):
    if nick ==None or c == None:
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author.mention} 사용법 : !vp [NickName] [Your Region: na - North America, latam - Latin America, br -	Brazil, eu - Europe, ap - Asia Pacific, kr - Korea]")
    else:
        await ctx.message.delete()
        ssid = getpass(nick)
        if ssid != None:
            try:
                auth,bulid = await asyncio.create_task(m.Auths(ssid))
                plcurl = await asyncio.create_task(m.playercard(auth,bulid,c))
                nametag = await asyncio.create_task(m.nametag(auth))
                bc = await asyncio.create_task(m.balance(auth,bulid,c))
                name = ctx.message.author.name
                name = name.title()
                embed1 = discord.Embed(timestamp=ctx.message.created_at, color=discord.Color(0xFFFFFF),description="",title=f"{nametag}'s\nValorant Points")
                embed1.set_image(url=plcurl[1])
                embed1.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/9/9d/Valorant_Points.png/revision/latest?cb=20200408014952")
                embed1.add_field(name=str(bc[0]) + "VP",value="", inline=False) #inline이 False라면 다음줄로 넘깁니다.

                embed2 = discord.Embed(timestamp=ctx.message.created_at, color=discord.Color(0xFFFFFF),description="",title=f"{nametag}'s\nKingdom Credits")
                embed2.set_image(url=plcurl[1])
                embed2.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/9/9f/Kingdom_Credits.png/revision/latest?cb=20230608160711")
                embed2.add_field(name=str(bc[1]) + "KC",value=f"", inline=False) #inline이 False라면 다음줄로 넘깁니다.

                embed3 = discord.Embed(timestamp=ctx.message.created_at, color=discord.Color(0xFFFFFF),description="",title=f"{nametag}'s\nRadianite Points")
                embed3.set_image(url=plcurl[1])
                embed3.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/4/47/Radianite_Points.png/revision/latest?cb=20200408015457")
                embed3.add_field(name=str(bc[2]) + "RP",value=f"", inline=False)
                await ctx.send(f"""{ctx.message.author.mention}""")
                await ctx.send(embeds = [embed1,embed2,embed3])
                logger(f"{ctx.message.author} checked {nametag}'s balances")
            except league_client.exceptions.AuthFailureError:
                    await ctx.send("Login Failed.")
                    logger(f"{ctx.message.author} logged in Riot with 'ID : {nick}', but Failed.")
        else:
            await ctx.send(f"{ctx.message.author.mention}\n현재 이 닉네임으로 등록된 계정이 없습니다.")
            
            logger(f"[{ctx.message.author}] There wasn't {nametag}'s account.")

@bot.command()
async def info(ctx,nick=None,c=None):
    if nick ==None or c == None:
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author.mention} 사용법 : !info [NickName] [Your Region: na - North America, latam - Latin America, br -	Brazil, eu - Europe, ap - Asia Pacific, kr - Korea]")
    else:
        await ctx.message.delete()
        ssid = getpass(nick)
        if ssid != None:
            try:
                auth,bulid = await asyncio.create_task(m.Auths(ssid))
                plcurl = await asyncio.create_task(m.playercard(auth,bulid,c))
                nametag = await asyncio.create_task(m.nametag(auth))
                lvl = await asyncio.create_task(m.lvl(auth,bulid,c))
                name = ctx.message.author.name
                name = name.title()
                embed1 = discord.Embed(timestamp=ctx.message.created_at, color=discord.Color(0xFFFFFF),description="",title=f"{nametag}'s\nInformation")
                embed1.set_image(url=plcurl[1])
                embed1.set_thumbnail(url=plcurl[0])
                embed1.add_field(name=f"Level",value=f"{lvl}", inline=False)
                await ctx.send(f"""{ctx.message.author.mention}""")
                await ctx.send(embeds = [embed1])
                logger(f"{ctx.message.author} checked {nametag}'s account info.")
            except league_client.exceptions.AuthFailureError:
                    await ctx.send("Login Failed.")
                    logger(f"{ctx.message.author} logged in Riot with 'ID : {nick}', but Failed.")
        else:
            await ctx.send(f"{ctx.message.author.mention}\n현재 이 닉네임으로 등록된 계정이 없습니다.")
            logger(f"[{ctx.message.author}] There wasn't {nametag}'s account.")
@bot.command()
async def 평균티어(ctx,nick=None,c=None):
    if nick ==None or c == None:
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author.mention} 사용법 : !평균티어 [NickName] [Your Region: na - North America, latam - Latin America, br -	Brazil, eu - Europe, ap - Asia Pacific, kr - Korea]")
    else:
        await ctx.message.delete()
        ssid = getpass(nick)
        if ssid != None:
            try:
                auth,bulid = await asyncio.create_task(m.Auths(ssid))
                tier = await asyncio.create_task(m.avgtier(auth,bulid,c))
                plcurl = await asyncio.create_task(m.playercard(auth,bulid,c))
                nametag = await asyncio.create_task(m.nametag(auth))
                name = ctx.message.author.name
                name = name.title()
                embed1 = discord.Embed(timestamp=ctx.message.created_at, color=discord.Color(0xFFFFFF),description="",title=f"{nametag}의 현재게임의 평균티어")
                embed1.set_image(url=plcurl[1])
                embed1.set_thumbnail(url=tier[1])
                embed1.add_field(name=f"평균티어",value=f"{tier[0]}", inline=False)
                await ctx.send(f"""{ctx.message.author.mention}""")
                await ctx.send(embeds = [embed1])
                logger(f"{ctx.message.author} checked current games's average tier.")
            except league_client.exceptions.AuthFailureError:
                    await ctx.send("Login Failed.")
                    logger(f"{ctx.message.author} logged in Riot with 'ID : {nick}', but Failed.")
        else:
            await ctx.send(f"{ctx.message.author.mention}\n현재 이 닉네임으로 등록된 계정이 없습니다.")
            logger(f"[{ctx.message.author}] There wasn't {nametag}'s account.")

@bot.command()
async def delpl(ctx,nick=None,c=None):
    if nick ==None or c == None:
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author.mention} 사용법 : !delpl [NickName] [Your Region: na - North America, latam - Latin America, br -	Brazil, eu - Europe, ap - Asia Pacific, kr - Korea]")
    else:
        await ctx.message.delete()
        ssid = getpass(nick)
        if ssid != None:
            try:
                auth,bulid = await asyncio.create_task(m.Auths(ssid))
                nametag = await asyncio.create_task(m.nametag(auth))
                await asyncio.create_task(m.delplay(auth,bulid,c))
                await ctx.send(f"{nametag} was deleted in current party.")
                logger(f"{ctx.message.author} deleted {nick} from {nick}'s party")
            except league_client.exceptions.AuthFailureError:
                    await ctx.send("Login Failed.")
                    logger(f"{ctx.message.author} logged in Riot with 'ID : {nick}', but Failed.")
        else:
            await ctx.send(f"{ctx.message.author.mention}\n현재 이 닉네임으로 등록된 계정이 없습니다.")
            logger(f"[{ctx.message.author}] There wasn't {nametag}'s account.")

@bot.command(aliases=["as"])
async def AccessoryStore(ctx,nick=None,c=None):
    if nick ==None or c == None:
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author.mention} 사용법 : !AccessoryStore [NickName] [Your Region: na - North America, latam - Latin America, br -	Brazil, eu - Europe, ap - Asia Pacific, kr - Korea]")
    else:
        await ctx.message.delete()
        ssid = getpass(nick)
        if ssid != None:
            try:
                auth,bulid = await asyncio.create_task(m.Auths(ssid))
                accs = await asyncio.create_task(m.accst(auth,bulid,c))
                plcurl = await asyncio.create_task(m.playercard(auth,bulid,c))
                nametag = await asyncio.create_task(m.nametag(auth))
                c1,c2,c3 = random_color()
                embed1 = discord.Embed(timestamp=ctx.message.created_at,description=f"Time remaining until next : \n{accs[5]}",color = discord.Color.from_rgb(c1,c2,c3),title=f"{nametag}'s\nAccessary Store 1st Offer")
                embed1.set_image(url=accs[4][0])
                embed1.set_thumbnail(url=plcurl[0])
                embed1.add_field(name=accs[0][0],value=f"Price : {accs[0][1]} KC", inline=False)

                embed2 = discord.Embed(timestamp=ctx.message.created_at,description=f"Time remaining until next : \n{accs[5]}",color = discord.Color.from_rgb(c1,c2,c3),title=f"{nametag}'s\nAccessary Store 2st Offer")
                embed2.set_image(url=accs[4][1])
                embed2.set_thumbnail(url=plcurl[0])
                embed2.add_field(name=accs[1][0],value=f"Price : {accs[1][1]} KC", inline=False)

                embed3 = discord.Embed(timestamp=ctx.message.created_at,description=f"Time remaining until next : \n{accs[5]}",color = discord.Color.from_rgb(c1,c2,c3),title=f"{nametag}'s\nAccessary Store 3st Offer")
                embed3.set_image(url=accs[4][2])
                embed3.set_thumbnail(url=plcurl[0])
                embed3.add_field(name=accs[2][0],value=f"Price : {accs[2][1]} KC", inline=False)

                embed4 = discord.Embed(timestamp=ctx.message.created_at,description=f"Time remaining until next : \n{accs[5]}",color = discord.Color.from_rgb(c1,c2,c3),title=f"{nametag}'s\nAccessary Store 4st Offer")
                embed4.set_image(url=accs[4][3])
                embed4.set_thumbnail(url=plcurl[0])
                embed4.add_field(name=accs[3][0],value=f"Price : {accs[3][1]} KC", inline=False)
                await ctx.send(f"""{ctx.message.author.mention}""")
                await ctx.send(embeds = [embed1,embed2,embed3,embed4])
                logger(f"{ctx.message.author} logged in Riot with 'Id : {nick}', 'Region : {c}' and checked Valorant Accessory Shop Offers. Used Server : {ctx.message.guild}. Issued Server ID : {ctx.message.guild.id}")
            except league_client.exceptions.AuthFailureError:
                    await ctx.send("Login Failed.")
                    logger(f"{ctx.message.author} logged in Riot with 'ID : {nick}', but Failed.")
        else:
            await ctx.send(f"{ctx.message.author.mention}\n현재 이 닉네임으로 등록된 계정이 없습니다.")
            logger(f"[{ctx.message.author}] There wasn't {nametag}'s account.") 

@bot.event
async def on_message(msg):
    # if msg.content == "/Set":
    #         if msg.author.dm_channel:
    #             await msg.author.dm_channel.send(msg.content)
    #         elif msg.author.dm_channel is None:
    #             channel = await msg.author.create_dm()
    #             await channel.send(msg)
    await bot.process_commands(msg)

bot.run("")

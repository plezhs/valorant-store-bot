import aiohttp, json, requests
import os, sys
import asyncio
from riot_auth import RiotAuth, auth_exceptions
from getpass import getpass
import discord
import random
import asyncio
import os
from discord.ext import commands
from discord.utils import get
from hashlib import new
from requests import session as sesh, get
from requests.adapters import HTTPAdapter
from ssl import PROTOCOL_TLSv1_2
from urllib3 import PoolManager
from collections import OrderedDict
from re import compile
import os
import api as m
import datetime
import a



def wjson(id,password,nick,filename='db.json'):
    with open(filename,'r+',encoding='UTF-8') as f:
        file_data = json.load(f)
        txt = a.encrypt(password.encode(),a.keygener(),nick)
        data = {
            f"{nick}":{
                f"{id}":txt.decode(),
                f"{nick}":f"{id}",
            }
        }
        file_data.update(data)
        f.seek(0)
        json.dump(file_data,f,indent=4)

def getpass(nick):
    with open('db.json','r',encoding='UTF-8') as f:
        data = json.load(f)
        try:
            id = data[f'{nick}'][f'{nick}']
            txt = data[nick][id]
            p = a.decrypt(txt,nick).decode()
        except:
            id = None
            p = None
        return id,p

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
time = datetime.datetime.now()

rt =str(time)[0:10]
with open(f'{rt}.log.txt', 'a',encoding='UTF-8') as f:
    f.write(f"[{time}]--------------------------------------------------\n[{time}]Bot Started\n[{time}]--------------------------------------------------\n")

global login
login = dict()

badwords=[]
words = []

# path = "./bads"
# file_lst = os.listdir(path)

# for file in file_lst:
#     filepath = path + '/' + file
#     with open(filepath,'r', encoding='UTF8') as bad:
#         badwords=bad.read().splitlines()
#         for i in badwords:
#             words.append(i)
    
bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="발로란트 상점"))

def rint(min:int, max:int):
    max+=1
    return random.sample(range(min,max),1)

@bot.command(aliases=["valshp","vs","valoshop","valorantshop","vlshop","ㅍ미놰ㅔ","valahop"])
async def valshop(ctx,nick=None,c=None):
    global login
    if nick == None or c == None or getpass(nick) == (None,None):
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author.mention} 사용법 : !valshop [NickName] [Your Region: na - North America, latam - Latin America, br -	Brazil, eu - Europe, ap - Asia Pacific, kr - Korea]")
    else:
        await ctx.message.delete()
        if(c in ["kr","br","na","eu","latam","ap"]):
            # try:
            iii,ppp = getpass(nick)
            if iii != None and ppp != None:
                await asyncio.create_task(m.store(iii,ppp,c))
                name = ctx.message.author.name
                name = name.title()
                embed1 = discord.Embed(timestamp=ctx.message.created_at, color=m.re()[0][2],description="",title=f"{m.re()[5]}'s\nValorant Shop 1st Offer")
                embed1.set_image(url=m.url1)
                embed1.set_thumbnail(url=m.re()[4])
                embed1.add_field(name=m.re()[0][0],value=f"Price : {m.re()[0][1]}vp", inline=False) #inline이 False라면 다음줄로 넘깁니다.

                embed2 = discord.Embed(timestamp=ctx.message.created_at, color=m.re()[1][2],description="",title=f"{m.re()[5]}'s\nValorant Shop 2nd Offer")
                embed2.set_image(url=m.url2)
                embed2.set_thumbnail(url=m.re()[4])
                embed2.add_field(name=m.re()[1][0],value=f"Price : {m.re()[1][1]}vp", inline=False) #inline이 False라면 다음줄로 넘깁니다.

                embed3 = discord.Embed(timestamp=ctx.message.created_at,color= m.re()[2][2],description="",title=f"{m.re()[5]}'s\nValorant Shop 3rd Offer")
                embed3.set_image(url=m.url3)
                embed3.set_thumbnail(url=m.re()[4])
                embed3.add_field(name=m.re()[2][0],value=f"Price : {m.re()[2][1]}vp", inline=False) #inline이 False라면 다음줄로 넘깁니다.

                embed4 = discord.Embed(timestamp=ctx.message.created_at, color=m.re()[3][2],description="",title=f"{m.re()[5]}'s\nValorant Shop 4th Offer")
                embed4.set_image(url=m.url4)
                embed4.set_thumbnail(url=m.re()[4])
                embed4.add_field(name=m.re()[3][0],value=f"Price : {m.re()[3][1]}vp", inline=False) #inline이 False라면 다음줄로 넘깁니다.
                await ctx.send(f"""{ctx.message.author.mention}""")
                await ctx.send(embeds = [embed1,embed2,embed3,embed4])
                rt =str(time)[0:10]
                with open(f'{rt}.log.txt', 'a',encoding='UTF-8') as f:
                    f.write(f"[{time}] {ctx.message.author} logged in Riot with 'Id : {iii}', 'Region : {c}' and checked Valorant Shop Offers. Used Server : {ctx.message.guild}. Issued Server ID : {ctx.message.guild.id}\n")
                # except:
                #     await ctx.send(f"{ctx.message.author.mention}\nYou did something wrong.\nCheck your ID or Password or Region.\nThen retry again")
                #     rt =str(time)[0:10]
                #     with open(f'{rt}.log.txt', 'a',encoding='UTF-8') as f:
                #         f.write(f"[{time}] {ctx.message.author} issued problem : {m.re()}. Issued Server : {ctx.message.guild}. Issued Server ID : {ctx.message.guild.id}\n")
            else:
                await ctx.send(f"{ctx.message.author.mention}\n현재 이 닉네임으로 등록된 계정이 없습니다.")
        else:
            await ctx.send(f"{ctx.message.author.mention}\nRegion ERROR")
            sdfs="Region ERROR"
            rt =str(time)[0:10]
            with open(f'{rt}.log.txt', 'a',encoding='UTF-8') as f:
                f.write(f"[{time}] {ctx.message.author} issued problem : {sdfs}. Issued Server : {ctx.message.guild}. Issued Server ID : {ctx.message.guild.id}\n")
        
@bot.command(aliases=["mn","ㅜㅡ"])
async def nm(ctx,nick=None,c=None):
    if nick ==None or c == None:
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author.mention} 사용법 : !nm [Riot ID] [Password] [Your Region: na - North America, latam - Latin America, br -	Brazil, eu - Europe, ap - Asia Pacific, kr - Korea]")
    else:
        await ctx.message.delete()
        iii,ppp = getpass(nick)
        if iii != None and ppp != None:
            await asyncio.create_task(m.store(iii,ppp,c))
            name = ctx.message.author.name
            name = name.title()
            embed1 = discord.Embed(timestamp=ctx.message.created_at, color=m.re()[6][0][0][4],description="",title=f"{m.re()[5]}'s\nValorant Night Market 1st Offer")
            embed1.set_image(url=m.re()[6][1][0])
            embed1.set_thumbnail(url=m.re()[4])
            embed1.add_field(name=m.re()[6][0][0][0],value=f"Price : {m.re()[6][0][0][1]}vp\nBasic Price : {m.re()[6][0][0][2]}\nDiscount : {m.re()[6][0][0][3]}%", inline=False) #inline이 False라면 다음줄로 넘깁니다.

            embed2 = discord.Embed(timestamp=ctx.message.created_at, color=m.re()[6][0][1][4],description="",title=f"{m.re()[5]}'s\nValorant Night Market 2nd Offer")
            embed2.set_image(url=m.re()[6][1][1])
            embed2.set_thumbnail(url=m.re()[4])
            embed2.add_field(name=m.re()[6][0][1][0],value=f"Price : {m.re()[6][0][1][1]}vp\nBasic Price : {m.re()[6][0][1][2]}\nDiscount : {m.re()[6][0][1][3]}%", inline=False) #inline이 False라면 다음줄로 넘깁니다.

            embed3 = discord.Embed(timestamp=ctx.message.created_at, color=m.re()[6][0][2][4],description="",title=f"{m.re()[5]}'s\nValorant Night Market 3rd Offer")
            embed3.set_image(url=m.re()[6][1][2])
            embed3.set_thumbnail(url=m.re()[4])
            embed3.add_field(name=m.re()[6][0][2][0],value=f"Price : {m.re()[6][0][2][1]}vp\nBasic Price : {m.re()[6][0][2][2]}\nDiscount : {m.re()[6][0][2][3]}%", inline=False) #inline이 False라면 다음줄로 넘깁니다.

            embed4 = discord.Embed(timestamp=ctx.message.created_at, color=m.re()[6][0][3][4],description="",title=f"{m.re()[5]}'s\nValorant Night Market 4th Offer")
            embed4.set_image(url=m.re()[6][1][3])
            embed4.set_thumbnail(url=m.re()[4])
            embed4.add_field(name=m.re()[6][0][3][0],value=f"Price : {m.re()[6][0][3][1]}vp\nBasic Price : {m.re()[6][0][3][2]}\nDiscount : {m.re()[6][0][3][3]}%", inline=False) #inline이 False라면 다음줄로 넘깁니다.

            embed5 = discord.Embed(timestamp=ctx.message.created_at, color=m.re()[6][0][4][4],description="",title=f"{m.re()[5]}'s\nValorant Night Market 5th Offer")
            embed5.set_image(url=m.re()[6][1][4])
            embed5.set_thumbnail(url=m.re()[4])
            embed5.add_field(name=m.re()[6][0][4][0],value=f"Price : {m.re()[6][0][4][1]}vp\nBasic Price : {m.re()[6][0][4][2]}\nDiscount : {m.re()[6][0][4][3]}%", inline=False) #inline이 False라면 다음줄로 넘깁니다.

            embed6 = discord.Embed(timestamp=ctx.message.created_at, color=m.re()[6][0][5][4],description="",title=f"{m.re()[5]}'s\nValorant Night Market 6th Offer")
            embed6.set_image(url=m.re()[6][1][5])
            embed6.set_thumbnail(url=m.re()[4])
            embed6.add_field(name=m.re()[6][0][5][0],value=f"Price : {m.re()[6][0][5][1]}vp\nBasic Price : {m.re()[6][0][5][2]}\nDiscount : {m.re()[6][0][5][3]}%", inline=False) #inline이 False라면 다음줄로 넘깁니다.
            await ctx.send(f"""{ctx.message.author.mention}""")
            await ctx.send(embeds = [embed1,embed2,embed3,embed4,embed5,embed6])
        else:
            await ctx.send(f"{ctx.message.author.mention}\n현재 이 닉네임으로 등록된 계정이 없습니다.")


@bot.command()
async def set(ctx,ID=None,Password=None,nickname=None):
    if (ID==None or Password == None or nickname==None):
        await ctx.send("!set [ID] [Password] [NickName]")
    else:
        if ctx.guild:
            return
        else:
            if(getpass(nickname) == (None,None)):
                wjson(ID,Password,nickname)
                await ctx.send(f"Your Account registered.\nYou can login with '{nickname}' from now on.")
                rt =str(time)[0:10]
                with open(f'{rt}.log.txt', 'a',encoding='UTF-8') as f:
                    f.write(f"[{time}] {ctx.message.author} registered Riot Account with 'Id : {ID}', 'NickName : {nickname}'\n")
            else:
                await ctx.send(f"{nickname} is already registerd by someone.\nRetry with other nickname.")
                re = str(time)[0:10]
                with open(f'{re}.log.txt', 'a',encoding='UTF-8') as f:
                    f.write(f"[{time}] {ctx.message.author} failed register account with {nickname} nickname.'\n")

@bot.command(aliases=["Balances","balances","Bl","bl","bc"])
async def vp(ctx,nick=None,c=None):
    if nick ==None or c == None:
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author.mention} 사용법 : !vp [NickName] [Your Region: na - North America, latam - Latin America, br -	Brazil, eu - Europe, ap - Asia Pacific, kr - Korea]")
    else:
        await ctx.message.delete()
        iii,ppp = getpass(nick)
        if iii != None and ppp != None:
            await asyncio.create_task(m.store(iii,ppp,c))
            name = ctx.message.author.name
            name = name.title()
            embed1 = discord.Embed(timestamp=ctx.message.created_at, color=discord.Color(0xFFFFFF),description="",title=f"{m.re()[5]}'s\nValorant Points")
            embed1.set_image(url=m.re()[8])
            embed1.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/9/9d/Valorant_Points.png/revision/latest?cb=20200408014952")
            embed1.add_field(name=m.re()[7][0] + "VP",value="", inline=False) #inline이 False라면 다음줄로 넘깁니다.

            embed2 = discord.Embed(timestamp=ctx.message.created_at, color=discord.Color(0xFFFFFF),description="",title=f"{m.re()[5]}'s\nKingdom Credits")
            embed2.set_image(url=m.re()[8])
            embed2.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/9/9f/Kingdom_Credits.png/revision/latest?cb=20230608160711")
            embed2.add_field(name=m.re()[7][1] + "KC",value=f"", inline=False) #inline이 False라면 다음줄로 넘깁니다.

            embed3 = discord.Embed(timestamp=ctx.message.created_at, color=discord.Color(0xFFFFFF),description="",title=f"{m.re()[5]}'s\nRadianite Points")
            embed3.set_image(url=m.re()[8])
            embed3.set_thumbnail(url="https://static.wikia.nocookie.net/valorant/images/4/47/Radianite_Points.png/revision/latest?cb=20200408015457")
            embed3.add_field(name=m.re()[7][2] + "RP",value=f"", inline=False)
            await ctx.send(f"""{ctx.message.author.mention}""")
            await ctx.send(embeds = [embed1,embed2,embed3])
        else:
            await ctx.send(f"{ctx.message.author.mention}\n현재 이 닉네임으로 등록된 계정이 없습니다.")

@bot.command()
async def info(ctx,nick=None,c=None):
    if nick ==None or c == None:
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author.mention} 사용법 : !info [NickName] [Your Region: na - North America, latam - Latin America, br -	Brazil, eu - Europe, ap - Asia Pacific, kr - Korea]")
    else:
        await ctx.message.delete()
        iii,ppp = getpass(nick)
        if iii != None and ppp != None:
            await asyncio.create_task(m.store(iii,ppp,c))
            name = ctx.message.author.name
            name = name.title()
            embed1 = discord.Embed(timestamp=ctx.message.created_at, color=discord.Color(0xFFFFFF),description="",title=f"{m.re()[5]}'s\nInformation")
            embed1.set_image(url=m.re()[8])
            embed1.set_thumbnail(url=m.re()[4])
            embed1.add_field(name=f"Level",value=f"{m.re()[9]}", inline=False)
            await ctx.send(f"""{ctx.message.author.mention}""")
            await ctx.send(embeds = [embed1])
        else:
            await ctx.send(f"{ctx.message.author.mention}\n현재 이 닉네임으로 등록된 계정이 없습니다.")

@bot.event
async def on_message(msg):
    # if msg.content == "/Set":
    #         if msg.author.dm_channel:
    #             await msg.author.dm_channel.send(msg.content)
    #         elif msg.author.dm_channel is None:
    #             channel = await msg.author.create_dm()
    #             await channel.send(msg)
    await bot.process_commands(msg)

bot.run("MTEzNjMxMjQ0NzgyNTg4NzQwNA.GE6zk1.PNXTgUxyZOMANuV9ZX07HNjpVTBYr-0b6xs_7o")

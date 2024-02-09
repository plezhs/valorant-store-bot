import aiohttp, json, requests
from fastapi import FastAPI
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

intents = discord.Intents.default()
intents.guilds = True
intents.members = True


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
async def valshop(ctx,a=None,b=None,c=None):
    if a ==None or b == None or c == None:
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author.mention} 사용법 : !valshop [Riot ID] [Password] [Your Region: na - North America, latam - Latin America, br -	Brazil, eu - Europe, ap - Asia Pacific, kr - Korea]")
    else:
        await ctx.message.delete()
        await asyncio.create_task(m.store(a,b,c))
        name = ctx.message.author.name
        name = name.title()
        embed1 = discord.Embed(timestamp=ctx.message.created_at, colour=discord.Colour.red(),description=m.re()[0][0],title=f"{m.re()[5]}'s\nValorant Shop 1st Offers")
        embed1.set_image(url=m.url1)
        embed1.set_thumbnail(url=m.re()[4])
        embed1.add_field(name="",value=f"Price : {m.re()[0][1]}vp", inline=False) #inline이 False라면 다음줄로 넘깁니다.

        embed2 = discord.Embed(timestamp=ctx.message.created_at, colour=discord.Colour.red(),description=m.re()[1][0],title=f"{m.re()[5]}'s\nValorant Shop 2nd Offers")
        embed2.set_image(url=m.url2)
        embed2.set_thumbnail(url=m.re()[4])
        embed2.add_field(name="",value=f"Price : {m.re()[1][1]}vp", inline=False) #inline이 False라면 다음줄로 넘깁니다.

        embed3 = discord.Embed(timestamp=ctx.message.created_at, colour=discord.Colour.red(),description=m.re()[2][0],title=f"{m.re()[5]}'s\nValorant Shop 3rd Offers")
        embed3.set_image(url=m.url3)
        embed3.set_thumbnail(url=m.re()[4])
        embed3.add_field(name="",value=f"Price : {m.re()[2][1]}vp", inline=False) #inline이 False라면 다음줄로 넘깁니다.

        embed4 = discord.Embed(timestamp=ctx.message.created_at, colour=discord.Colour.red(),description=m.re()[3][0],title=f"{m.re()[5]}'s\nValorant Shop 4th Offers")
        embed4.set_image(url=m.url4)
        embed4.set_thumbnail(url=m.re()[4])
        embed4.add_field(name="",value=f"Price : {m.re()[3][1]}vp", inline=False) #inline이 False라면 다음줄로 넘깁니다.
        await ctx.send(f"""{ctx.message.author.mention}""")
        await ctx.send(embeds = [embed1,embed2,embed3,embed4])
        # await ctx.send(embed = embed1)
        # await ctx.send(embed = embed2)
        # await ctx.send(embed = embed3)
        # await ctx.send(embed = embed4)

@bot.command(aliases=["mn","ㅜㅡ"])
async def nm(ctx,a=None,b=None,c=None):
    if a ==None or b == None or c == None:
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author.mention} 사용법 : !nm [Riot ID] [Password] [Your Region: na - North America, latam - Latin America, br -	Brazil, eu - Europe, ap - Asia Pacific, kr - Korea]")
    else:
        await ctx.message.delete()
        await asyncio.create_task(m.store(a,b,c))
        embed = discord.Embed(timestamp=ctx.message.created_at, colour=discord.Colour.red(), title="Valorant Night Market", description=m.nightm())
        # embed.set_thumbnail(url="https://prforest.ga/files/img/홍보숲.png")
        # embed.add_field(name="필트 제목", value="필드 설명", inline=False) #inline이 False라면 다음줄로 넘깁니다.
        await ctx.send(f"{ctx.message.author.mention}",embed = embed)


@bot.command(aliases=[""])
async def brief(ctx,a=None,b=None,c=None):
    if a ==None or b == None or c == None:
        await ctx.message.delete()
        await ctx.send(f"{ctx.message.author.mention} 사용법 : !nm [Riot ID] [Password] [Your Region: na - North America, latam - Latin America, br -	Brazil, eu - Europe, ap - Asia Pacific, kr - Korea]")
    else:
        await ctx.message.delete()
        await asyncio.create_task(m.store(a,b,c))
        embed1 = discord.Embed(timestamp=ctx.message.created_at, colour=discord.Colour.red(),description="",title=f"")
        embed1.set_image(url=m.url1)
        embed2 = discord.Embed(timestamp=ctx.message.created_at, colour=discord.Colour.red(),description="",title=f"")
        embed2.set_image(url=m.url2)
        embed3 = discord.Embed(timestamp=ctx.message.created_at, colour=discord.Colour.red(),description="",title=f"")
        embed3.set_image(url=m.url3)
        embed4 = discord.Embed(timestamp=ctx.message.created_at, colour=discord.Colour.red(),description="",title=f"")
        embed4.set_image(url=m.url4)
        await ctx.send(f"""{ctx.message.author.mention}""")
        await ctx.send(embed = embed1)
        await ctx.send(embed = embed2)
        await ctx.send(embed = embed3)
        await ctx.send(embed = embed4)






@bot.event
async def on_message(msg):
    cont = msg.content
    if msg.author == bot.user:
        return
    else:
        if isinstance(msg.channel, discord.channel.DMChannel):
            if msg == "!valshop":
                msg.author.send("a")
            return
    # if cont in badwords:
    #     await msg.channel.send(f'{msg.author.mention} 누가 비속어 사용하래!', reference=msg)
    await bot.process_commands(msg)

bot.run("")

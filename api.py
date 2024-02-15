api_key = "RGAPI-62c1d244-a9ea-4ef0-ac45-61866e05d062"
api_url1 = "https://kr.api.riotgames.com/val/status/v1/platform-data"

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

cw = os.get_terminal_size().columns
global a
global nm
global url1
global url2
global url3
global url4

async def Auth(username,password):
    global a
    
    build = requests.get('https://valorant-api.com/v1/version').json()['data']['riotClientBuild']
    print('Valorant Build '+build)

    RiotAuth.RIOT_CLIENT_USER_AGENT = build + '%s (Windows;10;;Professional, x64)'

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    CREDS = username,password

    auth = RiotAuth()
    try: 
        await auth.authorize(*CREDS)
    except auth_exceptions.RiotAuthenticationError:
        print('Error: Auth Failed, Please check credentials and try again.')
        a = "Error: Auth Failed, Please check credentials and try again."
    except auth_exceptions.RiotMultifactorError:
        print('Accounts with MultiFactor enabled are not supported at this time.')
        a="Accounts with MultiFactor enabled are not supported at this time."
    return auth
async def store(username,password,region):
  global a
  global nm
  global url1
  global url2
  global url3
  global url4

  auth = await Auth(username,password)
  
  token_type = auth.token_type
  access_token = auth.access_token
  entitlements_token = auth.entitlements_token
  user_id = auth.user_id

  conn = aiohttp.TCPConnector()
  session = aiohttp.ClientSession(connector=conn)

  headers = {
   'X-Riot-Entitlements-JWT' : entitlements_token,
   'Authorization': 'Bearer '+ access_token,
  }
  headersa = {
   'Authorization': 'Bearer '+ access_token,
  }

  async with session.get('https://pd.'+region+'.a.pvp.net/store/v1/offers/', headers=headers) as r:
    pricedata = await r.json()
  
  async with session.get('https://pd.'+ region +'.a.pvp.net/store/v2/storefront/'+ user_id, headers=headers) as r:
    data = json.loads(await r.text())
  allstore = data.get('SkinsPanelLayout')
  singleitems = allstore["SingleItemOffers"]
  skin1uuid = singleitems[0]
  skin2uuid = singleitems[1]
  skin3uuid = singleitems[2]
  skin4uuid = singleitems[3]

  async with session.get(f'https://pd.{region}.a.pvp.net/personalization/v2/players/{user_id}/playerloadout', headers=headers) as r:
    pl = json.loads(await r.text())
  player = pl.get('Identity')
  playercard = player['PlayerCardID']

  temp = []
  async with session.post('https://auth.riotgames.com/userinfo', headers=headersa, json={}) as r:
      asd = await r.json()
  userid = asd['acct']['game_name'] +"#"+ asd['acct']['tag_line']

  async with session.get('https://valorant-api.com/v1/weapons/skinlevels/'+ skin1uuid) as r:
    skin1 = json.loads(await r.text())['data']['displayName']
    skin1url = json.loads(await r.text())['data']['displayIcon']

  async with session.get('https://valorant-api.com/v1/weapons/skinlevels/'+ skin2uuid) as r:
    skin2 = json.loads(await r.text())['data']['displayName']
    skin2url = json.loads(await r.text())['data']['displayIcon']

  async with session.get('https://valorant-api.com/v1/weapons/skinlevels/'+ skin3uuid) as r:
    skin3 = json.loads(await r.text())['data']['displayName']
    skin3url = json.loads(await r.text())['data']['displayIcon']

  async with session.get('https://valorant-api.com/v1/weapons/skinlevels/'+ skin4uuid) as r:
    skin4 = json.loads(await r.text())['data']['displayName']
    skin4url = json.loads(await r.text())['data']['displayIcon']
  url1 = skin1url
  url2 = skin2url
  url3 = skin3url
  url4 = skin4url

  async with session.get(f' https://valorant-api.com/v1/playercards/{playercard}') as r:
    playercardurl = json.loads(await r.text())['data']['displayIcon']
  def getprice(uuid):
    for item in pricedata['Offers']:
      if item["OfferID"] == uuid:
        return item['Cost']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
  
  def getcolor(priceint):
    color = 0
    if priceint == 1775 or priceint == 3550:
      color = 16011413
    elif priceint == 875 or priceint == 1750:
      color = 6794488
    elif priceint == 1275 or priceint == 2550:
      color = 44167
    elif priceint == 2175 or priceint == 2675 or priceint == 4350 or priceint == 5350 or priceint == 2375:
      color = 16750685
    elif priceint == 2475 or priceint == 2975 or priceint == 4950:
      color = 16773764
    return color

  def nightmarket(datad):
    out = []
    try:
      for item in datad["BonusStore"]["BonusStoreOffers"]:
        r = requests.get(f'https://valorant-api.com/v1/weapons/skinlevels/'+item['Offer']['Rewards'][0]['ItemID'])
        skin = r.json()
        data = {
          'name':skin['data']['displayName'],
          'icon':skin['data']['displayIcon'],
          'uuid': item['Offer']['OfferID'],
          'price': {
            'oringinal':item['Offer']['Cost']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741'],
            'discount': item['DiscountPercent'],
            'final': item['DiscountCosts']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741'],
          }
        }
        out.append(data)
      return out
    except KeyError:
      return None
  nm = nightmarket(data)
  if nm != None:
    nm_uuid = list()
    result = list()
    for ghj in nm:
      nm_uuid.append(f"{ghj['uuid']}")
      nm_items = (f"{ghj['name']}")
      nm_finalprice = (f"{ghj['price']['final']}")
      nm_oringinalprice = (f"{ghj['price']['oringinal']}")
      nm_discoount = (f"{ghj['price']['discount']}")
      priceint = int(nm_oringinalprice)
      nm_color = getcolor(priceint)
      result.append([nm_items, nm_finalprice, nm_oringinalprice, nm_discoount,nm_color])
    
    nmskinurl = list()
    for jj in nm:
      nmskinurl.append(jj['icon'])

  a=list()
  a.append([skin1,getprice(skin1uuid),getcolor(getprice(skin1uuid))])
  a.append([skin2,getprice(skin2uuid),getcolor(getprice(skin2uuid))])
  a.append([skin3,getprice(skin3uuid),getcolor(getprice(skin3uuid))])
  a.append([skin4,getprice(skin4uuid),getcolor(getprice(skin4uuid))])
  a.append(playercardurl)
  a.append(userid)
  a.append([result,nmskinurl])
  await session.close()

def re():
   return a

def url1():
  global url1
  return url1
def url2():
  global url2
  return url2
def url3():
  global url3
  return url3
def url4():
  global url4
  return url4
api_key = "RGAPI-62c1d244-a9ea-4ef0-ac45-61866e05d062"
api_url1 = "https://kr.api.riotgames.com/val/status/v1/platform-data"

import aiohttp, json, requests
import os, sys
import asyncio
from riot_auth import RiotAuth, auth_exceptions
import base64
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
import datetime

cw = os.get_terminal_size().columns
global a
global nm
global url1
global url2
global url3
global url4

async def Auth(username,password):
    global a
    
    build = requests.get('https://valorant-api.com/v1/version').json()
    print('Valorant Build '+build['data']['riotClientBuild'])

    RiotAuth.RIOT_CLIENT_USER_AGENT = build['data']['riotClientBuild'] + '%s (Windows;10;;Professional, x64)'

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
    return auth,build
async def store(username,password,region,start=0,end=20):
  global a
  global nm
  global url1
  global url2
  global url3
  global url4
  if username != None and password != None:
    auth,bulid = await Auth(username,password)
    
    token_type = auth.token_type
    access_token = auth.access_token
    entitlements_token = auth.entitlements_token
    user_id = auth.user_id

    conn = aiohttp.TCPConnector()
    session = aiohttp.ClientSession(connector=conn)

    header = {
    'X-Riot-Entitlements-JWT' : entitlements_token,
    'Authorization': 'Bearer '+ access_token,
    'X-Riot-ClientPlatform': 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9',
    'X-Riot-ClientVersion': bulid['data']['riotClientVersion']
    }
    headers = {
    'X-Riot-Entitlements-JWT' : entitlements_token,
    'Authorization': 'Bearer '+ access_token,
    }
    headersa = {
    'Authorization': 'Bearer '+ access_token,
    }
    
    async with session.post('https://auth.riotgames.com/userinfo', headers=headersa, json={}) as r8:
        asd = await r8.json()
    userid = asd['acct']['game_name'] +"#"+ asd['acct']['tag_line']
    
    async with session.get(f'https://pd.{region}.a.pvp.net/match-history/v1/history/{user_id}?startIndex={start}&endIndex={end}', headers=headers) as r1:
      ata = json.loads(await r1.text())
      mid = list()
      for j in ata['History']:
        mid.append(j['MatchID'])
    gamedetail = list()
    for k in mid:
      namelist = list()
      async with session.get(f'https://pd.{region}.a.pvp.net/match-details/v1/matches/{k}', headers=header) as r:
        ddat = json.loads(await r.text())
        for plll in ddat['players']:
          namelist.append(plll['gameName'] + "#" + plll['tagLine'])
        gamedetail.append(namelist)
        # with open(f'.//test//{k}.json','w+',encoding='UTF-8') as kk:
        #   json.dump(ddat,kk,ensure_ascii=False,indent=4)
      
    async with session.get('https://pd.'+region+'.a.pvp.net/store/v1/offers/', headers=headers) as r2:
      # print(r2)
      pricedata = await r2.json()
    
    async with session.get(f'https://glz-{region}-1.{region}.a.pvp.net/core-game/v1/players/{user_id}',headers = headers) as rier:
      rierdata = await rier.read()
      try:
        eval(rierdata.decode('utf-8'))["message"]
        can = False
      except KeyError:
        finaldata = eval(rierdata.decode('utf-8'))["MatchID"]
        can = True
    vudrbs = dict()
    if can == True:    
      async with session.get(f'https://glz-{region}-1.{region}.a.pvp.net/core-game/v1/matches/{finaldata}/loadouts/',headers = headers) as currentmatch:
        matchdata = await currentmatch.read()
        finalmdata = eval(matchdata.decode('utf-8'))['Loadouts']
        z = list()
        for i in range(0,10):
          if finalmdata[i] != None:
            z.append(finalmdata[i]['Loadout']['Subject'])
        vudrbs[userid] = z
        print(z)

    async with session.get('https://pd.'+ region +'.a.pvp.net/store/v2/storefront/'+ user_id, headers=headers) as r3:
      data = json.loads(await r3.text())
    allstore = data.get('SkinsPanelLayout')
    singleitems = allstore["SingleItemOffers"]
    skin1uuid = singleitems[0]
    skin2uuid = singleitems[1]
    skin3uuid = singleitems[2]
    skin4uuid = singleitems[3]

    async with session.get(f'https://pd.{region}.a.pvp.net/account-xp/v1/players/{user_id}', headers=header) as r4:
      ddata = json.loads(await r4.text())
      mmr = ddata['Progress']['Level']
    async with session.get(f'https://pd.{region}.a.pvp.net/mmr/v1/players/{user_id}', headers=header) as r5:
      mdata = json.loads(await r5.text())
    async with session.get(f'https://pd.{region}.a.pvp.net/personalization/v2/players/{user_id}/playerloadout', headers=headers) as r6:
      pl = json.loads(await r6.text())
    player = pl.get('Identity')
    playercard = player['PlayerCardID']

    async with session.get(f'https://pd.{region}.a.pvp.net/store/v1/wallet/{user_id}', headers=headers) as r7:
      wallet = json.loads(await r7.text())
    vp = wallet['Balances']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
    kc = wallet['Balances']['85ca954a-41f2-ce94-9b45-8ca3dd39a00d']
    rp = wallet['Balances']['e59aa87c-4cbf-517a-5983-6e81511be9b7']

    temp = []

    async with session.get('https://valorant-api.com/v1/weapons/skinlevels/'+ skin1uuid) as r9:
      skin1 = json.loads(await r9.text())['data']['displayName']
      skin1url = json.loads(await r9.text())['data']['displayIcon']

    async with session.get('https://valorant-api.com/v1/weapons/skinlevels/'+ skin2uuid) as r10:
      skin2 = json.loads(await r10.text())['data']['displayName']
      skin2url = json.loads(await r10.text())['data']['displayIcon']

    async with session.get('https://valorant-api.com/v1/weapons/skinlevels/'+ skin3uuid) as r11:
      skin3 = json.loads(await r11.text())['data']['displayName']
      skin3url = json.loads(await r11.text())['data']['displayIcon']

    async with session.get('https://valorant-api.com/v1/weapons/skinlevels/'+ skin4uuid) as r12:
      skin4 = json.loads(await r12.text())['data']['displayName']
      skin4url = json.loads(await r12.text())['data']['displayIcon']
    url1 = skin1url
    url2 = skin2url
    url3 = skin3url
    url4 = skin4url

    async with session.get(f' https://valorant-api.com/v1/playercards/{playercard}') as r13:
      ddd = json.loads(await r13.text())['data']
      playercardurl = ddd['displayIcon']
      wideArt = ddd['wideArt']
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
    result = list()
    nmskinurl = list()
    if nm != None:
      nm_uuid = list()
      for ghj in nm:
        nm_uuid.append(f"{ghj['uuid']}")
        nm_items = (f"{ghj['name']}")
        nm_finalprice = (f"{ghj['price']['final']}")
        nm_oringinalprice = (f"{ghj['price']['oringinal']}")
        nm_discoount = (f"{ghj['price']['discount']}")
        priceint = int(nm_oringinalprice)
        nm_color = getcolor(priceint)
        result.append([nm_items, nm_finalprice, nm_oringinalprice, nm_discoount,nm_color])
      
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
    a.append([vp,kc,rp])
    a.append(wideArt)
    a.append(mmr)
    a.append(user_id)
    a.append(gamedetail)
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


from league_client.constants import LEAGUE_CLIENT_AUTH_PARAMS
from league_client.constants import RIOT_CLIENT_AUTH_PARAMS
from league_client.rso.auth import get_ledge_token
from league_client.rso.auth import get_login_queue_token
from league_client.rso.auth import login_using_credentials
from league_client.rso.auth import login_using_ssid
from league_client.rso.auth import process_access_token
from league_client.rso.constants import DISCOVEROUS_SERVICE_LOCATION
from league_client.rso.constants import InventoryTypes
from league_client.rso.constants import LEAGUE_EDGE_URL
from league_client.rso.constants import PLAYER_PLATFORM_EDGE_URL
from league_client.rso.auth import get_entitlements_token
from league_client.rso.inventory import get_inventory_data
from league_client.rso.inventory import get_inventory_data_v2
from league_client.rso.inventory import get_inventory_token
from league_client.rso.inventory import get_inventory_token_v2
from league_client.rso.missions import get_missions
from league_client.rso.rank import get_ranked_overview_token
from league_client.rso.rank import get_rank_data
from league_client.rso.userinfo import get_userinfo
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

class auth:
  def __init__(self):
    self.ssid = ''
    self.access_token = ''
    self.scope = ''
    self.iss = ''
    self.id_token = ''
    self.token_type = ''
    self.session_state = ''
    self.expires_in = ''
    self.entitlements_token = ''
    self.user_id = ''

async def Auth(ID,PW):
    global a
    
    build = requests.get('https://valorant-api.com/v1/version').json()
    print('Valorant Build '+build['data']['riotClientBuild'])

    params = RIOT_CLIENT_AUTH_PARAMS
    (
      ssid,
      access_token,
      scope,
      iss,
      id_token,
      token_type,
      session_state,
      expires_in
    ) = login_using_credentials(ID, PW, params)

    puuid, region, account_id = process_access_token(access_token)

    auth.ssid = ssid
    auth.access_token = access_token
    auth.scope = scope
    auth.iss = iss
    auth.id_token = id_token
    auth.token_type = token_type
    auth.session_state = session_state
    auth.expires_in = expires_in
    auth.entitlements_token = get_entitlements_token(access_token)
    auth.user_id = puuid
    
    return auth,build

async def nametag(auth):
  if auth != None:
    
    token_type = auth.token_type
    access_token = auth.access_token
    entitlements_token = auth.entitlements_token
    user_id = auth.user_id

    conn = aiohttp.TCPConnector()
    session = aiohttp.ClientSession(connector=conn)

    headersa = {
    'Authorization': 'Bearer '+ access_token,
    }

    async with session.post('https://auth.riotgames.com/userinfo', headers=headersa, json={}) as r8:
        asd = await r8.json()
    userid = asd['acct']['game_name'] +"#"+ asd['acct']['tag_line']
    await session.close()
  return userid

async def avgtier(auth,build,region):
  if auth != None and build != None:
    
    token_type = auth.token_type
    access_token = auth.access_token
    entitlements_token = auth.entitlements_token
    user_id = auth.user_id

    conn = aiohttp.TCPConnector()
    session = aiohttp.ClientSession(connector=conn)

    headers = {
    'X-Riot-Entitlements-JWT' : entitlements_token,
    'Authorization': 'Bearer '+ access_token,
    'X-Riot-ClientPlatform': 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9',
    'X-Riot-ClientVersion': build['data']['riotClientVersion']
    }

    async with session.get(f'https://glz-{region}-1.{region}.a.pvp.net/core-game/v1/players/{user_id}',headers = headers) as rier:
      rierdata = await rier.read()
      try:
        eval(rierdata.decode('utf-8'))["message"]
        can = False
      except KeyError:
        finaldata = eval(rierdata.decode('utf-8'))["MatchID"]
        can = True

    if can == True:    
      async with session.get(f'https://glz-{region}-1.{region}.a.pvp.net/core-game/v1/matches/{finaldata}/loadouts/',headers = headers) as currentmatch:
        matchdata = await currentmatch.read()
        finalmdata = eval(matchdata.decode('utf-8'))['Loadouts']
        z = list()
        for i in range(0,10):
          try:
            z.append(finalmdata[i]['Loadout']['Subject'])
            print(finalmdata[i]['Loadout']['Subject'])
          except:
            z.append(finalmdata[0]['Loadout']['Subject'])
    totaltiernumber = int()
    # test = ["1b1d3429-87cd-5590-994b-0cfe1f5808bf","f2ca85d0-7045-513c-8b24-73c0dbbbb072","818adb8c-a5df-56d4-bfa3-92f46f513963","02e13558-0757-5764-98d8-e1f718e656c6","d6146392-eba7-58da-a199-9df38ec03bf1","c1723de8-616c-5bbb-ae48-1be7670d089d","29e404d2-d043-5efe-992a-14771051a596","10fa6185-e073-555b-87b8-6e16f19d1bcf","7936192f-a2c4-55b4-9b95-5bec8225a48f","3376c026-7610-5768-a87d-f8c6f3b7e622"]
    for plmmr in z:
      async with session.get(f'https://api.henrikdev.xyz/valorant/v1/by-puuid/mmr-history/{region}/{plmmr}') as r5:
        ddid = await r5.json()
        
        tierNumber = ddid['data'][0]['currenttier']
        totaltiernumber += int(tierNumber)
    async with session.get(f'https://valorant-api.com/v1/competitivetiers') as apitier:
      listtier = await apitier.json()
      resulttier = listtier['data'][0]['tiers'][int(totaltiernumber/10)]['tierName']
      resulttiericon = listtier['data'][0]['tiers'][int(totaltiernumber/10)]['smallIcon']
      result = [resulttier,resulttiericon]
      await session.close()
  return result

async def delplay(auth,build,region):
  if auth != None and build != None:
    
    token_type = auth.token_type
    access_token = auth.access_token
    entitlements_token = auth.entitlements_token
    user_id = auth.user_id

    conn = aiohttp.TCPConnector()
    session = aiohttp.ClientSession(connector=conn)

    headers = {
    'X-Riot-Entitlements-JWT' : entitlements_token,
    'Authorization': 'Bearer '+ access_token,
    'X-Riot-ClientPlatform': 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9',
    'X-Riot-ClientVersion': build['data']['riotClientVersion']
    }
    async with session.delete(f'https://glz-{region}-1.{region}.a.pvp.net/parties/v1/players/{user_id}',headers=headers) as kkk:
      hahaha = kkk
      print(hahaha)
    await session.close()

async def balance(auth,build,region):
  if auth != None and build != None:
    
    token_type = auth.token_type
    access_token = auth.access_token
    entitlements_token = auth.entitlements_token
    user_id = auth.user_id

    conn = aiohttp.TCPConnector()
    session = aiohttp.ClientSession(connector=conn)

    headers = {
    'X-Riot-Entitlements-JWT' : entitlements_token,
    'Authorization': 'Bearer '+ access_token,
    'X-Riot-ClientPlatform': 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9',
    'X-Riot-ClientVersion': build['data']['riotClientVersion']
    }

    async with session.get(f'https://pd.{region}.a.pvp.net/store/v1/wallet/{user_id}', headers=headers) as r7:
      wallet = json.loads(await r7.text())
    vp = wallet['Balances']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
    kc = wallet['Balances']['85ca954a-41f2-ce94-9b45-8ca3dd39a00d']
    rp = wallet['Balances']['e59aa87c-4cbf-517a-5983-6e81511be9b7']
    result = [vp,kc,rp]
    await session.close()
  return result

async def playercard(auth,build,region):
  if auth != None and build != None:
    
    token_type = auth.token_type
    access_token = auth.access_token
    entitlements_token = auth.entitlements_token
    user_id = auth.user_id

    conn = aiohttp.TCPConnector()
    session = aiohttp.ClientSession(connector=conn)

    headers = {
    'X-Riot-Entitlements-JWT' : entitlements_token,
    'Authorization': 'Bearer '+ access_token,
    'X-Riot-ClientPlatform': 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9',
    'X-Riot-ClientVersion': build['data']['riotClientVersion']
    }

    async with session.get(f'https://pd.{region}.a.pvp.net/personalization/v2/players/{user_id}/playerloadout', headers=headers) as r6:
      pl = json.loads(await r6.text())
    player = pl.get('Identity')
    playercard = player['PlayerCardID']

    async with session.get(f' https://valorant-api.com/v1/playercards/{playercard}') as r13:
      ddd = json.loads(await r13.text())['data']
      playercardurl = ddd['displayIcon']
      wideArt = ddd['wideArt']
      result = [playercardurl,wideArt]
    await session.close()
  return result

async def lvl(auth,build,region):
  if auth != None and build != None:
    
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
    'X-Riot-ClientVersion': build['data']['riotClientVersion']
    }

    async with session.get(f'https://pd.{region}.a.pvp.net/account-xp/v1/players/{user_id}', headers=header) as r4:
      ddata = json.loads(await r4.text())
      mmr = ddata['Progress']['Level']
    await session.close()
  return mmr

async def pick(auth,build,region):
  if auth != None and build != None:
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
    
    header = {
    'X-Riot-Entitlements-JWT' : entitlements_token,
    'Authorization': 'Bearer '+ access_token,
    'X-Riot-ClientPlatform': 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9',
    'X-Riot-ClientVersion': build['data']['riotClientVersion']
    }
    
    async with session.get(f'https://glz-{region}-1.{region}.a.pvp.net/pregame/v1/players/{user_id}',headers = header) as df:
      mid = json.loads(await df.text())

    # async with session.get(f'https://glz-{region}-1.{region}}.a.pvp.net/pregame/v1/matches/{}/select/{}', headers=header) as r2:
    #   # print(r2)
    #   pricedata = await r2.json()

async def accst(auth,build,region):
  import humanfriendly
  if auth != None and build != None:
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
    
    header = {
    'X-Riot-Entitlements-JWT' : entitlements_token,
    'Authorization': 'Bearer '+ access_token,
    'X-Riot-ClientPlatform': 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9',
    'X-Riot-ClientVersion': build['data']['riotClientVersion']
    }

    async with session.get(f"https://pd.{region}.a.pvp.net/store/v2/storefront/{user_id}",headers = header) as acs:
      data = json.loads(await acs.text())
      allstore = data.get('AccessoryStore')
      sinitem = allstore['AccessoryStoreOffers']

      chtime = allstore['AccessoryStoreRemainingDurationInSeconds']

      pc1 = sinitem[0]['Offer']['Cost']['85ca954a-41f2-ce94-9b45-8ca3dd39a00d']
      pc2 = sinitem[1]['Offer']['Cost']['85ca954a-41f2-ce94-9b45-8ca3dd39a00d']
      pc3 = sinitem[2]['Offer']['Cost']['85ca954a-41f2-ce94-9b45-8ca3dd39a00d']
      pc4 = sinitem[3]['Offer']['Cost']['85ca954a-41f2-ce94-9b45-8ca3dd39a00d']

      of1it = sinitem[0]['Offer']['Rewards'][0]['ItemID']
      of2it = sinitem[1]['Offer']['Rewards'][0]['ItemID']
      of3it = sinitem[2]['Offer']['Rewards'][0]['ItemID']
      of4it = sinitem[3]['Offer']['Rewards'][0]['ItemID']

      of1ty = sinitem[0]['Offer']['Rewards'][0]['ItemTypeID']
      of2ty = sinitem[1]['Offer']['Rewards'][0]['ItemTypeID']
      of3ty = sinitem[2]['Offer']['Rewards'][0]['ItemTypeID']
      of4ty = sinitem[3]['Offer']['Rewards'][0]['ItemTypeID']

    def acst(tuuid,iuuid):
      if tuuid == "d5f120f8-ff8c-4aac-92ea-f2b5acbe9475": #spray
        a1= requests.get(f"https://valorant-api.com/v1/sprays/{iuuid}")
        skin1 =a1.json()['data']['displayName']
        skin1url =a1.json()['data']['fullTransparentIcon']
        return skin1,skin1url
        
      elif tuuid == "dd3bf334-87f3-40bd-b043-682a57a8dc3a": #gun buddies
        a1= requests.get(f"https://valorant-api.com/v1/buddies/levels/{iuuid}")
        skin1 =a1.json()['data']['displayName']
        skin1url =a1.json()['data']['displayIcon']
        return skin1,skin1url
        
      elif tuuid == "3f296c07-64c3-494c-923b-fe692a4fa1bd": #card
        a1= requests.get(f"https://valorant-api.com/v1/playercards/{iuuid}")
        skin1 =a1.json()['data']['displayName']
        skin1url =a1.json()['data']['wideArt']
        return skin1,skin1url

      elif tuuid == "de7caa6b-adf7-4588-bbd1-143831e786c6": #titles
        a1= requests.get(f"https://valorant-api.com/v1/playertitles/{iuuid}")
        skin1 =a1.json()['data']['displayName']
        skin1url =a1.json()['data']['displayIcon']
        return skin1,skin1url

      

    skin1,url1 = acst(of1ty,of1it)
    skin2,url2 = acst(of2ty,of2it)
    skin3,url3 = acst(of3ty,of3it)
    skin4,url4 = acst(of4ty,of4it)
    
    tim = datetime.timedelta(seconds=chtime)

    a=list()
    a.append([skin1,pc1]) #0
    a.append([skin2,pc2]) #1
    a.append([skin3,pc3]) #2
    a.append([skin4,pc4]) #3
    a.append([url1,url2,url3,url4]) #4
    a.append(humanfriendly.format_timespan(tim)) #5
    await session.close()
  return a

async def store(auth,build,region):
  if auth != None and build != None:
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
    
    header = {
    'X-Riot-Entitlements-JWT' : entitlements_token,
    'Authorization': 'Bearer '+ access_token,
    'X-Riot-ClientPlatform': 'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9',
    'X-Riot-ClientVersion': build['data']['riotClientVersion']
    }
    
    # async with session.get(f'https://pd.{region}.a.pvp.net/match-history/v1/history/{user_id}?startIndex={start}&endIndex={end}', headers=headers) as r1:
    #   ata = json.loads(await r1.text())
    #   mid = list()
    #   for j in ata['History']:
    #     mid.append(j['MatchID'])
    # gamedetail = list()
    # for k in mid:
    #   namelist = list()
    #   async with session.get(f'https://pd.{region}.a.pvp.net/match-details/v1/matches/{k}', headers=header) as r:
    #     ddat = json.loads(await r.text())
    #     for plll in ddat['players']:
    #       namelist.append(plll['gameName'] + "#" + plll['tagLine'])
    #     gamedetail.append(namelist)
    #     with open(f'.//test//{k}.json','w+',encoding='UTF-8') as kk:
    #       json.dump(ddat,kk,ensure_ascii=False,indent=4)
      
    async with session.get('https://pd.'+region+'.a.pvp.net/store/v1/offers/', headers=header) as r2:
      # print(r2)
      pricedata = await r2.json()

    async with session.get('https://pd.'+ region +'.a.pvp.net/store/v2/storefront/'+ user_id, headers=header) as r3:
      data = json.loads(await r3.text())
      allstore = data.get('SkinsPanelLayout')
      singleitems = allstore["SingleItemOffers"]
      skin1uuid = singleitems[0]
      skin2uuid = singleitems[1]
      skin3uuid = singleitems[2]
      skin4uuid = singleitems[3]  

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
    a.append([result,nmskinurl])
    a.append([url1,url2,url3,url4])
    await session.close()
  return a

# async def tst(name=None,pw=None):
#   conn = aiohttp.TCPConnector()
#   session = aiohttp.ClientSession(connector=conn)

#   body = {
#     'client_id': "play-valorant-web-prod",
#     'nonce' : "1",
#     'redirect_uri': "https://playvalorant.com/opt_in",
#     'response_type': "token id_token",
#     'scope': "account openid"
#   }

#   async with session.get("https://auth.riotgames.com/authorize?redirect_uri=https%3A%2F%2Fplayvalorant.com%2Fopt_in&client_id=play-valorant-web-prod&response_type=token%20id_token&nonce=1&scope=account%20openid") as r9:
#     print(r9)
#   session.close()

# asyncio.run(tst())
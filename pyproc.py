# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 23:27:34 2020

@author: Admin
"""
import os.path as op
import requests
import json
import pandas as pd

def find_summoner():
  if(op.isfile('users.txt')):
  
    use_name = input('Would you like to check a saved user? (y/n)\n')
    
    if(use_name == 'y'):
      print('Enter the number next to the name you want to use')
      f = open('users.txt', 'r')
      name_ind = 1
      
      for name in f:
        print('(%d) %s' % (name_ind, name))
        name_ind += 1
        
      select = input()
      while(int(select) > name_ind):
        select = input('Please enter the number associated with the user to check')

      f.seek(0)        
      names = f.readlines()
      summoner_name = names[int(select)-1]
      f.close
    
  else:
    summoner_name = input('Enter your summoner name:\n')
    
  return summoner_name

def save_summoner(summoner_name):
  with open('users.txt') as users:
    names = users.readlines()
    for name in names:
      if name == summoner_name:
        return
  
  save_name = input('Would you like to store this user? (y/n)\n')
  if save_name == 'y':
    f = open('users.txt', 'a')
    f.write(summoner_name)
    f.close

region_url = 'https://na1.api.riotgames.com/'
name_get = 'lol/summoner/v4/summoners/by-name/'
api_key = '?api_key=RGAPI-33b9272b-52ea-4be8-9d03-f12136f47baf'

summoner_name = find_summoner()

validName = False
while validName != True:

  request_string = region_url + name_get + summoner_name + api_key
  request = requests.get(request_string)
  
  try:
    request_json = json.loads(request.text)
    validName = True
  except:
    print("Invalid username\n")
    summoner_name = input('Enter your summoner name:\n')

save_summoner(summoner_name)
#print(request_json)
    
account_id = request_json['accountId']
matchlist_string = region_url + '/lol/match/v4/matchlists/by-account/'
matchlist_req = requests.get(matchlist_string + account_id + api_key)
matchlist_json = json.loads(matchlist_req.text)
#print(matchlist_json)
matchlist_df = pd.DataFrame(matchlist_json['matches'])
print(matchlist_df)

for game in matchlist_df['gameId']:
  match_info_url = region_url + '/lol/match/v4/matches/'
  match_request = requests.get(match_info_url + str(game) + api_key)
  match_json = json.loads(match_request.text)

  partDto_df = pd.DataFrame(match_json['participants'])

  partId_df = pd.DataFrame(match_json['participantIdentities'])
  print(partId_df)
  #player_series = partId_df['player'][x]['accountId']
  #print(player_series)
  
  df = pd.crosstab(partId_df.participantId, partId_df.player)
  print(df)
  #player_series = partId_df['participantId'][x for x in partId_df['player']]
  #print(player_series)
  #player = player_series[0]['accountId'] 
  #print(player)
  #playeracc = player['accountId']
  #print(playeracc)
  
  
  
  break






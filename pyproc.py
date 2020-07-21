# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 23:27:34 2020

@author: nuttyguy360
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
      while(int(select) > name_ind - 1):
        select = input('Please enter the number associated with the user to check\n')

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
    f.write(summoner_name + '\n')
    f.close
    
def validate_game(match):
    return match['gameVersion'][:5] == '10.14'
        
    
def count_match(participant):
    
    if( int(participant.get(key = 'spell1Id')) != 11 ) & ( int((participant.get(key = 'spell2Id')) != 11) ):
        return 0
    if( (participant['stats'][int(participant['participantId'])-1]['neutralMinionsKilled'] < 40 ) |
       (participant['stats'][int(participant['participantId'])-1]['neutralMinionsKilled'] < participant['stats'][int(participant['participantId'])-1]['totalMinionsKilled'] )):
           return 0
    return participant['stats'][int(participant['participantId'])-1]['kills'] + participant['stats'][int(participant['participantId'])-1]['assists']

def show_result(takedowns):
    print('Takedowns: %d/350' % (takedowns))
    if(takedowns >= 350):
        print('Congrats! You should have the Lillia shard!\n',
              'You can use it in 10.15')
    else:
        remain = 350 - takedowns
        print('Not there yet! You need %d more takedowns. Keep playing match-made games!' % (remain))
'''
Main starts here
'''

print('Note: Do the API limitiations, this app can currently only process',
      'the last 80 matchmade, SR games played. As such the result may be',
      'inaccurate')
region_url = 'https://na1.api.riotgames.com/'
name_get = "lol/summoner/v4/summoners/by-name/"
api_url = "?api_key="
api_inp =  input("Enter the api key:\n")
api_key = api_url + api_inp

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
queueFilter = {400, 420, 430, 440, 700, 830, 840, 850}
params = {
        'queue' : queueFilter,
        'endIndex' : 80
        }
matchlist_req = requests.get( (matchlist_string + account_id + api_key),
                             params)
matchlist_json = json.loads(matchlist_req.text)
#print(matchlist_json)
matchlist_df = pd.DataFrame(matchlist_json['matches'])
#print(matchlist_df)

total_takedown = 0
num_game = 1
print('Counting takedowns in games...')
for game in matchlist_df['gameId']:
  print('Game: %d/%d' % (num_game, matchlist_df['gameId'].size), end='.....')
  match_info_url = region_url + '/lol/match/v4/matches/'
  match_request = requests.get(match_info_url + str(game) + api_key)
  match_json = json.loads(match_request.text)
  
  if(validate_game(match_json) != True):
      num_game += 1
      print('Total takedowns so far: %d/350' % (total_takedown))
      continue

  partDto_df = pd.DataFrame(match_json['participants'])
  #print(partDto_df)
  partId_df = pd.DataFrame(match_json['participantIdentities'])
  #print(partId_df)
  
  partId = 1
  for player in partId_df['player']:
      if player['accountId'] == account_id:
          break
      partId += 1
      
  #print(partId)
  participant = partDto_df[partDto_df['participantId'] == partId]
  #print(participant.to_string())
  total_takedown += count_match(participant)
  print('Total takedowns so far: %d/350' % (total_takedown))
  if(total_takedown >= 350):
      break
  num_game += 1

show_result(total_takedown)




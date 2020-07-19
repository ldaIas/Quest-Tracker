# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 23:27:34 2020

@author: Admin
"""

import requests
import json

region_url = "https://na1.api.riotgames.com/"
name_get = "lol/summoner/v4/summoners/by-name/"
api_key = "?api_key=RGAPI-33b9272b-52ea-4be8-9d03-f12136f47baf"
summoner_name = input("Enter your summoner name:\n")

validName = False
while validName != True:

  request_string = region_url + name_get + summoner_name + api_key
  request = requests.get(request_string)
  
  try:
    request_json = json.loads(request.text)
    validName = True
  except:
    print("Invalid username\n")

request_json = json.loads(request.text)
print(request_json)

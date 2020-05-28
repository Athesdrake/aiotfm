import os
import re
import json
import requests
import datetime
from urllib.parse import quote


class Notifier:
  def __init__(self, string):
    self.pref = re.match("(.*?@)",string).group()
    self.args = string.replace(self.pref, '').split(";")
    self.manageContent()

  def manageContent(self):
    if self.pref == "x1Tz0@":
      room, reported_at, winner = self.args[0], int(self.args[1]), self.args[2]

      playerList = ""
      for i in range(len(self.args)-1):
        if i >= 3:
          name, camp = self.args[i].split(',')
          playerList += f"\n{name} {int(float(camp))}%"

      winnerInfo = f"Winner: [{winner}](https://atelier801.com/profile?pr={quote(winner)})" if winner != "-" else 'No one won'


      data = {
          "username": "NoFeet",
          "avatar_url": "https://i.imgur.com/EHVV6rR.png",
          "embeds": [
              {
                  "author": {
                      "name": room[3:],
                      "url": "https://discordapp.com",
                      "icon_url": f"https://atelier801.com/img/pays/{room[:2].replace('en','gb')}.png"
                  },
                  "color": 12370112,
                  "footer": {
                      "text": f'Room report | {datetime.datetime.fromtimestamp(reported_at/1000.0).strftime("%d %b %Y at %H:%M:%S")}'
                  },
                  "description": f"**{winnerInfo}**\n\n**`Camp List` **```css{playerList}```"
              }
          ]	
      }
      
      self.sendToDicord(data)            
    
  def sendToDicord(self, data):
    r = requests.post(os.environ.get('webhook'),  data=json.dumps(data), headers={"Content-Type": "application/json"})
    return r.text

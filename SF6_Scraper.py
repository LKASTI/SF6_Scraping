#!/usr/bin/env python
# coding: utf-8

# In[45]:


# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import os
import pandas as pd
import time
from lxml import etree
import re


# In[46]:


#Dictionary for Dataframe
Rankers = {"key":[],"CFN":[],"Rank":[],"MR":[],"Character":[],"Usercode":[],"Country":[],"League":[]}


# In[47]:


cookies = {
    'buckler_id': '7gChzq30hkCM3h7Khnui94I1IKyPXuM4ybazL7ma8TnUxwBTxBYvoO9gyOw1ihvE',
    'buckler_r_id': 'a3869b62-5f7a-40db-b681-bb5a70485f25',
    'buckler_praise_date': '1773280434557'
}


# In[48]:


#params = {
    #'page': '5',
    #'season_type': '1',
#}


# In[49]:


headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,es;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': '_ga_4BKH6S3JTF=GS1.1.1715630306.4.1.1715630312.54.0.0; _ga_LZJGXR1W9E=GS1.1.1715630306.4.1.1715630312.0.0.0; CookieConsent={stamp:%27Wwf0CKZX6AdYAs+WXd0vEx9ioXM8cAZL5DEPCD71nsdlg38I9tlXlg==%27%2Cnecessary:true%2Cpreferences:false%2Cstatistics:false%2Cmarketing:false%2Cmethod:%27explicit%27%2Cver:3%2Cutc:1715630313300%2Cregion:%27us-12%27}; buckler_id=l2NiWiZA70YcpknU0F30xsjG_ibfbx38Y3hK9d2hU2FxwxegQYOte7bExzk68Da9; buckler_r_id=fd0230d3-f9d1-428e-aaed-c77cf1cbe5c1; buckler_praise_date=1727493905759',
    'dnt': '1',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
}


# # Script

# In[50]:


params = ""
SF6_data = ""
SF6_scape = ""
Topplayers = ""
legend = ""
ranks= ""
usercodes = "" 
players= ""
characters = ""
usercodes = ""
flags = ""
leagues = ""


# In[51]:


key = 1
key_num = 2001
while key < key_num:
  Rankers['key'].append(key)
  key= key + 1


# In[52]:


page = 1
while page < 101:
    params = {
    'page': f'{page}',
    'season_type': '1',
    }
    SF6_data = requests.get('https://www.streetfighter.com/6/buckler/ranking/master', params=params, cookies=cookies, headers=headers)
    SF6_scape = bs(SF6_data.content, 'html.parser')
    Topplayers = SF6_scape.find_all('ul', {'class': 'ranking_ranking_list__szajj'})
    legend = Topplayers[1]
    
    ranks=legend.find_all('div', attrs={'class': 'ranking_time__teMP4'})
    usercodes = legend.find_all('ul', attrs={'class': 'ranking_ranking_list__szajj'})
    players=legend.find_all('span', {'class': 'ranking_name__El29_'})
    characters =legend.find_all('span', {'class': 'ranking_image__lFEYG'})
    usercodes = legend.findAll('li')
    flags = legend.find_all('span', {'class': 'ranking_frag__D7XnG'})
    leagues = legend.find_all('span', {'class': 'ranking_image__lFEYG undefined'})
    player = 0
    character = 0
    code = 0
    while player < len(players):
      try:
        champ = characters[character].find('img', alt=True)
        country = flags[player].find_all('img')
        MR = ranks[player].get_text(separator=' ').split(" ")
        user = usercodes[code].a.get('href').split("/")
        icon = leagues[player].find_all('img', alt=True)
        league = icon[1]['src'].split("/")
        
        Rankers['CFN'].append(players[player].get_text())
        Rankers['Rank'].append(int(MR[2][1:]))
        # Rankers['MR'].append(MR[3] + ' ' + MR[4])
        Rankers['MR'].append(int(MR[3]))
        Rankers['Character'].append(champ['alt'])
        Rankers['Usercode'].append(int(user[4]))
        Rankers['Country'].append(country[1]['alt'])
        Rankers['League'].append('Legend' if league[7] == 'rank37_l.png' else 'Master')
        
        player= player + 1
        character= character + 2
        code= code + 3
        
      except:
        print("An exception occurred")
        player= player + 1
        character= character + 2
        code= code + 3
        pass
    print(f"Page {page} completed")
    page = page + 1
    time.sleep(1)


# In[53]:


tmp = Rankers.copy()
print(tmp)


# # Exporting Files

# In[54]:


df = pd.DataFrame(tmp)


# In[ ]:





# In[55]:


# df.to_json('Players10_15_24.json', orient = 'split', compression = 'infer', index = 'true')


# In[ ]:


import datetime
current_date = datetime.datetime.now()
current_date
formatted_date = f"{current_date.month}-{current_date.day}-{current_date.year}"
df.to_json(f"C:\\Users\\LKASTI\\OneDrive\\UTD\\Coding Workspaces\\VS code Python\\my_programs\\labbinglegends_helpers\\rankedData\\RankedPlayers_P11_S3_{formatted_date}.json", orient = 'records', compression = 'infer', index = 'true')
df.to_json(orient = 'records', compression = 'infer', index = 'true')


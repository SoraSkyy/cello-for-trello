import requests
import json
import time

key = ''
token = ''

blacklist = ['', '']

info = {'key': key, 'token':token, 'fields':['name'], 'boards':'open', 'board_fields':['name']}

r = requests.get('https://api.trello.com/1/members/me', params=info)

root = {}
startTime = time.time()
boardLists = (json.loads(r.text))['boards']
for board in boardLists:
    if board['id'] in blacklist:
        continue
    root[board['id']] = {'name': board['name']}



for board in root.keys():
    info = {'key': key, 'token':token, 'fields':['name'], 'lists':'open', 'list_fields': ['name']}
    r = requests.get('https://api.trello.com/1/boards/%s' %(board), params=info)
    obtainedLists = json.loads(r.text)['lists']
    root[board]['lists'] = {}
    for singleList in obtainedLists:
        if singleList['id'] in blacklist:
            continue
        root[board]['lists'][singleList['id']] = {'name':singleList['name']}

for board in root.keys():
    for singleList in root[board]['lists'].keys():
        info = {'key': key, 'token':token, 'fields':['name'], 'cards': 'open', 'card_fields': ['name']}
        r = requests.get('https://api.trello.com/1/lists/%s' %(singleList), params=info)
        obtainedCards = json.loads(r.text)['cards']
        root[board]['lists'][singleList]['cards'] = []
        for card in obtainedCards:
            root[board]['lists'][singleList]['cards'].append({'name': card['name'], 'id':card['id']})

for board in root.keys():
    for singleList in root[board]['lists'].keys():
        for index,card in enumerate(root[board]['lists'][singleList]['cards']):
            info = {'key': key, 'token':token, 'actions': ['commentCard'], 'actions_limit':1000, 'member_fields':['username'], 'action_memberCreator_fields':['username'], 'action_fields': ['date','data','type'], 'attachments': 'true', 'attachment_fields': ['name', 'url'], 'members:': 'true', 'member_fields':['username'], 'fields':['name','desc']}
            r = requests.get('https://api.trello.com/1/cards/%s' %(card['id']), params=info)
            obtainedInfo = json.loads(r.text)
            root[board]['lists'][singleList]['cards'][index]['actions'] = obtainedInfo['actions']
            root[board]['lists'][singleList]['cards'][index]['attachments'] = obtainedInfo['attachments']
            root[board]['lists'][singleList]['cards'][index]['description'] = obtainedInfo['desc']
            #print(json.dumps(root[board]['lists'][singleList]['cards'][index], indent=4, sort_keys=True))

print('time elapsed: %d' %(time.time() - startTime))

f = open('data.json', 'wb')
f.write(json.dumps(root).encode('utf-8'))
f.close()

            
            


        
    

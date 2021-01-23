import re, json, requests
import base64


CATEGORIES={}
url = 'https://api.github.com/repos/cepdnaclk/projects/git/blobs/2166c8eba0801b62b539a23576a7b6fc46e7f4f7'
resp = requests.get(url)
#print(resp)
data = json.loads(resp.text)
#print(data)
#print(data['content'])

message_bytes = base64.b64decode(data['content'])
message = json.loads(message_bytes.decode('ascii'))

for i in message:
    CATEGORIES[message[i]['link']] = message[i]['name']
    #print(message[i]['link'])
print(CATEGORIES)


import requests 
import json
import sys

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01', 
'Accept-Encoding': 'gzip, deflate', 
'X-Requested-With': 'XMLHttpRequest', 
'Content-Type': 'application/json', 
'Accept-Language': 'en-US,en;q=0.5', 
'Cookie': 'username=root; kimchiLang=zh_CN', 
'X-Requested-With': 'XMLHttpRequest' 
} 

s = requests.Session() 
s.headers.update(headers) 
s.auth = ('root', 'root+-*/root') 
if len(sys.argv) == 2:
    url = sys.argv[1]
    r = s.post(url, verify=False)
    print r.ok
else:
    print "Error"

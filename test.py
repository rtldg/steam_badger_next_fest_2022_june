
import json
import time
import os
import subprocess
import requests

accountname = open("accountname.txt").read().strip()
appids = sorted(json.loads(open("appids2222.json").read()), reverse=True)
c = round(len(appids)/32)
for i in range(0, c):
	s = ""
	s2 = ""
	for x in range(0, 32):
		s = f"{s}, {appids[i*32+x]}"
		s2 = f"{s2}, a/{appids[i*32+x]}"
	api_url = "http://localhost:1242/Api/Command"
	todo = {"Command": f"!addlicense {accountname} {s2}"}
	headers = {"Content-Type":"application/json"}
	response = requests.post(api_url, data=json.dumps(todo), headers=headers)
	time.sleep(2.0)
	api_url = "http://localhost:1242/Api/Command"
	todo = {"Command": f"!play {accountname} {s}"}
	headers = {"Content-Type":"application/json"}
	response = requests.post(api_url, data=json.dumps(todo), headers=headers)
	print(s)
	time.sleep(2.0)

c = len(appids) - (c * 32)
s = ""
for x in range(0, c):
	if c in appids:
		s = f"{s}, {appids[c]}"
api_url = "http://localhost:1242/Api/Command"
todo = {"Command": f"!play {accountname} {s}"}
headers = {"Content-Type":"application/json"}
response = requests.post(api_url, data=json.dumps(todo), headers=headers)
print(s)
time.sleep(1.0)
"""
appids = json.loads(open("appids2222.json").read())
for v in appids:
	print(v)
	p = subprocess.Popen(["steam-idle.exe", v])
	time.sleep(0.3)
	p.kill()
"""
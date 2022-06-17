
import json
import time
import os
import subprocess
import requests

accountname = open("accountname.txt").read().strip()
#appids = sorted(json.loads(open("appids2222.json",).read()), reverse=True)
apps = json.loads(open("GetAppList.json", "rb").read())["applist"]["apps"]

def chunker(c, m):
	s = ""
	for x in range(0, m):
		idx = c*32+x
		appid = apps[idx]["appid"]
		if s == "":
			s = f"{appid}"
		else:
			s = f"{s}, {appid}"
	print(s)
	api_url = "http://localhost:1242/Api/Command"
	command = {"Command": f"!play {accountname} {s}"}
	headers = {"Content-Type":"application/json"}
	response = requests.post(api_url, data=json.dumps(command), headers=headers)

chunks = round(len(apps)/32)
for i in range(0, chunks):
	print(f"===== chunk {i}/{chunks}")
	chunker(i, 32)
	time.sleep(3.0)

remaining = len(apps) - (chunks * 32)
print(f"===== chunk {chunks}/{chunks}")
chunker(chunks, remaining)

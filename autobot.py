
import json
import time
import os
import subprocess
import requests
import sys
import steam
import steam.client
from steam.client import SteamClient

#lastchange = 15153982
lcf = open("lastchange.txt", "r+")
lastchange = int(lcf.read().strip())
creds = open("../steam_creds.txt").read().strip().splitlines()
client = SteamClient()

@client.on('logged_on')
def logged_on():
	print("Logged in!")

@client.on('new_login_key')
def key():
	print(f"New login key! '{client.login_key}'")

#client.cli_login()
res = client.login(creds[0], creds[1], two_factor_code=creds[2])
if res != 1:
	print(f"failed to login... {res}")
	sys.exit(1)
client.change_status(persona_state=0) # steam.enums.common.EPersonaState.Offline
print(f"starting with change number {lastchange}!")
#breakpoint()
while True:
	time.sleep(5)
	try:
		res = client.get_changes_since(lastchange, app_changes=True, package_changes=False)
	except:
		res = None
	if res is None:
		print("skip")
		continue

	print("{} package changes | {} app changes".format(len(res.package_changes), len(res.app_changes)))

	newlastchange = lastchange
	apps = []
	for vvv in res.app_changes:
		apps.append(vvv.appid)
		print("AAAAAA {} - #{}".format(vvv.appid, vvv.change_number))
		if vvv.change_number > newlastchange:
			newlastchange = vvv.change_number

	packages = []
	for vvv in res.package_changes:
		#packages.append(vvv.packageid)
		print("______ {} - #{}".format(vvv.packageid, vvv.change_number))
		if vvv.change_number > newlastchange:
			newlastchange = vvv.change_number

	if newlastchange > lastchange:
		lastchange = newlastchange
		lcf.seek(0)
		lcf.write(str(newlastchange))
		print(f"change number now = {newlastchange}")

	if len(apps) == 0 and len(packages) == 00:
		continue

	try:
		info = client.get_product_info(
			apps,
			packages
		)
	except:
		info = None

	if info is None:
		print("info = None")
		continue

	didstuff = False
	for app in info["apps"]:
		if "extended" in info["apps"][app] and "demoofappid" in info["apps"][app]["extended"]:
			#thing = info["apps"][app]["extended"]["demoofappid"]
			print("adding and playing {}".format(info["apps"][app]["appid"]))
			client.request_free_license([info["apps"][app]["appid"]])
			time.sleep(0.3)
			client.games_played([info["apps"][app]["appid"]])
			didstuff = True

	if didstuff:
		time.sleep(1)
		client.games_played([])
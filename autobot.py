
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
print(f"starting with change number {lastchange}!")
#breakpoint()
while True:
	time.sleep(5)
	res = client.get_changes_since(lastchange, app_changes=True, package_changes=False)
	if res is None:
		print("skip")
		continue

	print("{} package changes | {} app changes".format(len(res.package_changes), len(res.app_changes)))

	apps = []
	for vvv in res.app_changes:
		apps.append(vvv.appid)
		if len(apps) > 5: break
		print("AAAAAA {} - #{}".format(vvv.appid, vvv.change_number))
		if vvv.change_number > lastchange:
			lastchange = vvv.change_number

	packages = []
	for vvv in res.package_changes:
		#packages.append(vvv.packageid)
		print("______ {} - #{}".format(vvv.packageid, vvv.change_number))
		if vvv.change_number > lastchange:
			lastchange = vvv.change_number

	lcf.seek(0)
	lcf.write(str(lastchange))
	print(f"change number now = {lastchange}")

	info = client.get_product_info(
		apps,
		packages
	)

	if info is None:
		print("info was none????")
		continue

	for app in info["apps"]:
		if "extended" in info["apps"][app] and "demoofappid" in info["apps"][app]["extended"]:
			#thing = info["apps"][app]["extended"]["demoofappid"]
			print("adding and playing {}".format(info["apps"][app]["appid"]))
			client.request_free_license([info["apps"][app]["appid"]])
			time.sleep(0.3)
			client.games_played([info["apps"][app]["appid"]])

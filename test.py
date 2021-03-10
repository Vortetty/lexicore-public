import requests
import base64
import json
from datetime import datetime
from PIL import Image
import io

arg = 'v0rtetty'

uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{arg}")
if uuid.status_code != 200:
    uuid = arg
else:
    uuid = uuid.json()['id']

names = "\n".join(
    f" - {i['name']} ({'Changed to on ' + datetime.fromtimestamp(int(i['changedToAt'])/1000).strftime('%d-%m-%Y @ %H:%M:%S') if 'changedToAt' in i.keys() else 'Original'})" for i in requests.get(f"https://api.mojang.com/user/profiles/{uuid}/names").json()
)

profile = requests.get(
    f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}").json()
skin = json.loads(base64.b64decode(profile['properties'][0]['value']))
name = profile['name']

print(skin)

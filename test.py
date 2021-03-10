import requests
import randomcolor
import io
from PIL import Image, ImageDraw, ImageColor

r = requests.post(
    "https://api.deepai.org/api/facial-recognition",
    data={
        'image': "https://api.deepai.org/job-view-file/53839298-27bb-4821-8a50-6a35caffa50e/inputs/image.jpg",
    },
    headers={'api-key': 'e1b08947-ff17-4c62-941b-bb5bb174aa81'}
)

im = Image.open(io.BytesIO(requests.get("https://api.deepai.org/job-view-file/53839298-27bb-4821-8a50-6a35caffa50e/inputs/image.jpg").content)).convert("RGBA")
dr = ImageDraw.Draw(im)
print(r.json())
randc = randomcolor.RandomColor()

for i in r.json()["output"]["faces"]:
    dr.rectangle([i["bounding_box"][0], i["bounding_box"][1], i["bounding_box"][0]+i["bounding_box"][2], i["bounding_box"][1]+i["bounding_box"][3]], outline=randc.generate(format_="rgb")[0], width=2)

output = io.BytesIO()
im.save(output, format="PNG")
output.seek(0)
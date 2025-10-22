import requests

url = "https://www.ceskenoviny.cz/zpravy/babis-navrzene-zmeny-v-systemu-povolenek-jsou-nesmyslne-a-alibisticke/2737497"
r = requests.get(url)

r.status_code

r.url

r.text

r.content

headers = {'user-agent': 'tutorialBot'}

r = requests.get(url, headers = headers)

r.status_code

r.text

print(r)

type(r)

r.encoding

with open("Úlohy/Stahování_stránek/babis.html", "w", encoding=r.encoding) as file:
    file.write(r.text)

robots = "https://www.ceskenoviny.cz/robots.txt"

r_robots = requests.get(robots, headers = headers)

print(r_robots.text)

r_robots.encoding

with open("Úlohy/Stahování_stránek/robots.txt", "w", encoding=r_robots.encoding) as file:
    file.write(r_robots.text)

url = "https://i3.cn.cz/15/1760703434_P2025101705104.jpg"
headers = {'user-agent': 'tutorialBot'}
r = requests.get(url, headers = headers)

import PIL
from PIL import Image
from io import BytesIO
i = Image.open(BytesIO(r.content))

r.content

display(i)

i.save("Úlohy/Stahování_stránek/babis.jpg")

with open("Úlohy/Stahování_stránek/babis_2.jpg", "wb") as img_file:
   img_file.write(r.content)
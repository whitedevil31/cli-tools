
import argparse
import requests
import zipfile, io
from bs4 import BeautifulSoup
parser = argparse.ArgumentParser(description = "CLI TOOL TO DOWNLOAD SUBTITLES")

print("WELCOME VRO")

parser.add_argument("-m","--movie",
					help = "The name of the movie")
parser.add_argument("-l","--language",
				help = "The language of the subtitle")
args = parser.parse_args()



def get_imdb_id(name):
    response = requests.get(name)
  
    if response.ok:
        id = response.json()['results'][0]['id']
        return id

def getSubtitleList(table):
    rows = []
    trs = table.find_all('tr')

   
    headerow = [td.get_text(strip=True) for td in trs[0].find_all('th')] 
    if headerow:
        rows.append(headerow)
        trs = trs[1:]

    for tr in trs: 
        singleRow =[]
        for td in tr.find_all('td'):
            singleRow.append(td.get_text(strip=True))
        singleRow[-1]=tr.find('a')['href']
        rows.append(singleRow) 
      
    return rows
imdbId = get_imdb_id("https://imdb-api.com/en/API/SearchMovie/<PLACE YOUR IMDB KEY HERE>/"+args.movie)

baseURl ="https://yts-subs.com/movie-imdb/"+imdbId
html_content = requests.get(baseURl).text
soup = BeautifulSoup(html_content, "lxml")
htmltable = soup.find('table', { 'class' : 'table other-subs' })
data = getSubtitleList(htmltable)
min =-10000
best=[]
for sub in data[1:]:
    if(int(sub[0])>min and sub[1].lower() ==args.language):
        best = sub
        min=int(sub[0])

s = best[-1]
s = s[:9] + s[9 + 1:]

url = "https://yifysubtitles.org"+s+'.zip'

import  zipfile, io
r = requests.get(url)
z = zipfile.ZipFile(io.BytesIO(r.content))
print(z)
print("SRT FILE DOWNLOADED")
z.extractall("./")

    
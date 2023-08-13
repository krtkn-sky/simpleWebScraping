import requests
from bs4 import BeautifulSoup

r = requests.get("https://pythonizing.github.io/data/real-estate/rock-springs-wy/LCWYROCKSPRINGS/")
c = r.content
soup = BeautifulSoup(c,"html.parser")
all = soup.find_all("div",{"class":"propertyRow"})

pno = int(soup.find_all("a",{"class":"Page"})[-1].text)*10

l=[]

base_url = "https://pythonizing.github.io/data/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="

for page in range(0,pno,10):
    r = requests.get(base_url+str(page)+".html")
    c = r.content
    soup = BeautifulSoup(c,"html.parser")
    all = soup.find_all("div",{"class":"propertyRow"})
    
    for i in all:
        d = {}
        d["Price"]=i.find("h4",{"class":"propPrice"}).text.replace("/n","").strip()
        d["Address"]=i.find_all("span",{"class":"propAddressCollapse"})[0].text
        d["Locality"]=i.find_all("span",{"class":"propAddressCollapse"})[1].text
        try:
            d["Beds"]=i.find("span",{"class":"infoBed"}).find("b").text
        except:
            d["Beds"]=None
        try:
             d["Area"]=i.find("span",{"class":"infoSqft"}).find("b").text
        except:
            d["Area"]=None
        try:
            d["Full Baths"]=i.find("span",{"class":"infoValueFullBath"}).find("b").text
        except:
            d["Full Baths"]=None
        try:
            d["Half Baths"]=i.find("span",{"class":"infoValueHalfBath"}).find("b").text
        except:
            d["Half Baths"]=None
    
        for cg in i.find_all("div",{"class","columnGroup"}):
            for fg,fn in zip(cg.find_all("span",{"class":"featureGroup"}),cg.find_all("span",{"class":"featureName"})):
                if "Lot Size" in fg.text:
                    d["Lot Size"]=fn.text
        l.append(d)

import pandas
df = pandas.DataFrame(l)
df.to_csv("Output.csv")
df

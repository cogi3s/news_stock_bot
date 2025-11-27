import requests 
from bs4 import BeautifulSoup as bs

response = requests.get("https://finance.naver.com/item/main.naver?code=000660")

#print(response.text)

soup = bs(response.text, "html.parser")
blind = soup.find("dl", "blind")
#print(blind)

ddData = blind.find_all("dd")
print(ddData)

type(ddData)


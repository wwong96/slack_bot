import requests
from bs4 import BeautifulSoup

url = 'http://ncov.mohw.go.kr/'
response = requests.get(url)
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    num = soup.select_one(".occur_graph > table:nth-child(1) > tbody:nth-child(4) > tr:nth-child(1) > td:nth-child(5) > span:nth-child(1)")
    num = int(num.get_text().replace(',',''))
    print(num)


else:
    print(response.status_code)
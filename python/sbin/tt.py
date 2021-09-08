#!/usr/bin/python3
from bs4 import BeautifulSoup
soup = BeautifulSoup(open("index.html"))
alist = soup.find(id="list").find_all("a")
for line in alist:
    print(line.get('href'),":",line.get_text())


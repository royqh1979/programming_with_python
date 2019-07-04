from bs4 import BeautifulSoup
from urllib.request import urlopen

html = urlopen("http://www.pythonscraping.com/pages/page3.html")
bs = BeautifulSoup(html.read(),'html5lib')

for image in bs.find('table',{'id':'giftList'}).tbody.find_all('img'):
    print("lala -- ")
    print(image)
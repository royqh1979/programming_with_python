from requests_html import HTMLSession, HTMLResponse
from urllib import parse

session = HTMLSession()
r : HTMLResponse = session.get("http://www.bjfu.edu.cn")

page = r.html
for link in page.links:
    print(link)

links = page.find("a")
for link in links:
    full_url = parse.urljoin(r.url,link.attrs['href'])
    title = link.attrs.get('title','')

    print(full_url, title)
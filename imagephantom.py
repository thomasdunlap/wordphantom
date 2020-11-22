from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import requests
from PIL import Image

def scrape_images(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    print(soup.find_all('img'))
    images = soup.find_all('img', {'src':re.compile('.jpg|.png')})
    for image in images[:3]: 
        print(image['src']+'\n')
    
        image_url = image['src']
        try:
            
            if image_url[:4] == 'http':
                img = Image.open(requests.get(image_url, stream = True).raw)
            else:
                domain = urlparse(url).netloc
                img = Image.open(requests.get("http://"+ domain + image_url, stream = True).raw)
        except Exception as e:
            print(f"\nIMAGE ERROR for {url}: {e}\n")
            continue
        img.save("./images/" + image_url[-10:])
        
        yield img

if __name__ == '__main__':
    scrape_images("https://www.yahoo.com")
    

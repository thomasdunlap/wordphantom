import os
import requests
from itertools import zip_longest
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib.parse import urlparse
from transformers import pipeline
import docx
import math
from wordphantom.imagephantom import scrape_images

def get_links(query):
    g_clean = [ ] #this is the list we store the search results
    url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query)
    try:
        html = requests.get(url)
        if html.status_code == 200:
            soup = BeautifulSoup(html.text, 'lxml')
            a = soup.find_all('a')
            for i in a:
                k = i.get('href')
                try:
                    m = re.search("(?P<url>https?://[^\s]+)", k)
                    n = m.group(0)
                    rul = n.split('&')[0]
                    domain = urlparse(rul)
                    if(re.search('google.com', domain.netloc)):
                        continue
                    else:
                        g_clean.append(rul)
                except:
                    continue
    except Exception as ex:
        print(str(ex))
    finally:
        return g_clean

def get_soup(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')
    return soup

def get_text(query, n=9):
    BAD_URLS = {"youtube.com"}
    urls = get_links(query)
    d = {}
    for url in urls[:n]:
        url = url.split("%")[0]
        article = url.split('/')[-1]
        print(f"\n\n{url}, {d.keys()}\n{url}\n\n")

        if url[-3:] == 'pdf':
            print(f"Gross. {url} is a pdf file.")
            continue
        elif len({burl for burl in BAD_URLS if burl in url}):
            print(f"{url} in set {BAD_URLS}")
            continue
        elif len({s for s in d.keys() if article != '' \
                and article in s.split('/')[:-1] \
                and len(s.split('/')[:-1]) - len(article) < 6}):

            print(f"{url} similar to other in {d.keys()}")
            continue

        else:
            print(f"Getting soup for {url}")
            soup = get_soup(url)
            d[url] = soup.get_text()

    return d

def zip_concat_text(text_list):
    return '\n'.join(' '.join(tup) for tup in zip_longest(*text_list, fillvalue=' '))

def get_summaries(full_text, summarizer, batch_size=3000):
    N = len(full_text)


    # maker sure n_batches is always at least 1
    n_batches = math.ceil((N+1) / batch_size)
    batch = N // n_batches

    summaries = []
    for i in range(0, N, batch):
        print(i, batch+i)
        section = full_text[i:(i+batch)]
        try:
            if len(section) < 50:
                print("section too short")
                continue

            summary = summarizer(section, min_length=90, max_length=200)
            summaries.append(summary[0]['summary_text'])
            print(summary)
        except Exception as e:
            print(f"\nFAILURE: {e}")
            continue

    return summaries

def clean_summaries(summaries):
    cleaned_summaries = ". ".join(sentence[0].upper() + sentence[1:] for sentence in "\n".join(summaries).split(" . "))
    return cleaned_summaries

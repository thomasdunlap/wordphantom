import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from urllib.parse import urlparse
import argparse
import asyncio
import tensorflow as tf
from transformers import pipeline
import docx
import math
from imagephantom import scrape_images

def get_links(query):
    g_clean = [ ] #this is the list we store the search results
    url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8'.format(query)    
    try:
        html = requests.get(url)
        if html.status_code==200:
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

def get_text(query):
    urls = get_links(query)
    d = {}
    for url in urls[:9]:
        if url[-3:] == 'pdf':
            print(f"Gross. {url} is a pdf file.")
            continue
        else:
            soup = get_soup(url)
            d[url] = soup.get_text()

    return d

def create_text_section(filepath, query, summarizer):
    # read or create word document and make query the heading
    try:
        doc = docx.Document(filepath)
    except:
        doc = docx.Document()
    doc.add_heading(query, 1)

    # scrape text
    text = get_text(query)
    print(text, type(text))
    for url, t in text.items():
        
        for img_path, img in scrape_images(url):
            print(f"Attempting to add img from {url}")

            try:
                doc.add_picture(img_path)
            except Exception as e:
                print(f"Nope: {e}")
                continue

        
        try:
            remove_short = " ".join(line for line in t.split('\n') if len(line) > 20 or " [ " in line)
            print(f"Summarizing {url} ...")
            summary = get_summaries(remove_short, summarizer)
            doc.add_paragraph(summary)
            doc.add_paragraph(url)
            doc.save(filepath)

        except Exception as e:

            print(f"boo {url} ...")
            print(e)
    
            continue
    
def get_summaries(full_text, summarizer):
    N = len(full_text)

    if N < 18000:
        # maker sure n_batches is always at least 1
        n_batches = math.ceil((N + 1) / 6000)
        batch = N // n_batches
    else:
        batch = N // 3

    summaries = []
    for i in range(0, N, batch):
        print(i, batch+i)
        section = full_text[i:(i+batch)]
        try:
            summary = summarizer(section, min_length=90, max_length=200)
            #pprint(named_entity(section))
            summaries.append(summary[0]['summary_text'])
            print(summary)
        except Exception as e:
            print(f"\nFAILURE: {e}")
            continue
    cleaned_summaries = ". ".join(sentence[0].upper() + sentence[1:] for sentence in "\n".join(summaries).split(" . "))
    return cleaned_summaries

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrape the googs!")
    parser.add_argument('filepath', type=str, help="Word Document full filepath")
    
    parser.add_argument('queries', type=str, nargs='*', help="Your google queries")
    args = parser.parse_args()
    summarizer = pipeline("summarization")
    for query in args.queries:
        create_text_section(args.filepath, query, summarizer)
    

import os
import requests
from itertools import zip_longest
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


def create_text_section(filepath, query, summarizer):
    # read or create word document and make query the heading
    print("Creating document.")
    try:
        doc = docx.Document(filepath)
    except:
        doc = docx.Document()
    doc.add_heading(query, 1)
    all_summaries = []
    text_exp = []
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
            remove_short = remove_short.split('\n')
            text_exp.append(remove_short)
            #print(f"Summarizing {url} ...")
            #summaries = get_summaries(remove_short, summarizer)
            #all_summaries.append(summaries)
            print(f"\n\nALL SUMMARIES:\n{all_summaries}")
            #summary = clean_summaries(summaries)
            #doc.add_paragraph(summary)
            doc.add_paragraph(url)
            #doc.save(filepath)

        except Exception as e:

            print(f"boo {url} ...")
            print(f"\n\nEXCEPTION: {e}\n\n")

            continue

    all_text = zip_concat_text(text_exp)
    all_summed = get_summaries(all_text, summarizer, batch_size=3000)
    final_text = clean_summaries(all_summed)
    print(f"All Summaries: {all_text}")
    doc.add_paragraph(final_text)
    doc.save(filepath)

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Scrape the googs!")
    parser.add_argument('filepath', type=str, help="Word Document full filepath")

    parser.add_argument('queries', type=str, nargs='*', help="Your google queries")
    args = parser.parse_args()
    summarizer = pipeline("summarization")
    for query in args.queries:
        create_text_section(args.filepath, query, summarizer)

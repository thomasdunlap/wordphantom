# WordPhantom

**Under Construction**

I love building machine learning software, however real-world jobs also require significant work time devoted to writing proposals, creating PowerPoints, writing blog posts, and other business oriented tasks where I stare longingly at my computer wishing to dive back into the code.

That's where WordPhantom comes in. It searches Google for related links, scrapes and summarizes the text from each site with BeatifulSoup and a BERT transformers pipeline, and creates rough drafts of your business documents (just a rough draft of MS Word via python-docx right now)


Current state usage:

* `git clone https://github.com/thomasdunlap/wordphantom.git`
* Set up a clean Python3 virtual environment (conda, virtualenv, etc.)
* `pip install -r requirements.txt`
* `python wordphantom.py "docs/<your MS Word doc>.docx" "<your google search 1>" "<your google search 2>" ... "<your google search n>"`  

Stay tuned! :D

Currently implementing:
* Scraping relevant images to insert into blog post
* Scraping pdfs with text in a two-column structure (so I can scrape ML publication pdfs as well as websites)

Future ideas:
* Adding citations
* Improved useful text preprocessing and identification
* Meme generator based on content (Medium-style articles seem to enjoy memes and gifs)

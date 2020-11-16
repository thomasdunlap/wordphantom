# WordPhantom

**Under Construction**

I love building machine learning software, however real-world jobs also require significant work time devoted to writing proposals, creating PowerPoints, writing blog posts, and other business oriented tasks where I stare longingly at my computer wishing to dive back into the code.

That's where WordPhantom comes in. It searches Google for related links, scrapes and summarizes the text from each site with BeatifulSoup and a BERT transformers pipeline, and creates rough drafts of your business documents (just a *very rough* draft of MS Word via python-docx right now)


Current state usage:

* `git clone https://github.com/thomasdunlap/wordphantom.git`
* `cd wordphantom`
* Set up a clean Python3 virtual environment (conda, virtualenv, etc.)
* `pip install -r requirements.txt`
* `python wordphantom.py "your google search" "/path/to/WordDoc.docx"` 

Stay tuned! :D




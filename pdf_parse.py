import requests
import pdftotext

def download_pdf(url):
    response = requests.get(url)
    filepath = './pdfs/' + url.split('/')[-1]
    with open(filepath, 'wb') as f:
        f.write(response.content)
    return filepath

def extract_pdf_text(filepath):
    with open(filepath, 'rb') as f:
        text = pdftotext.PDF(f)
    print(text[0])

if __name__ == '__main__':
    filepath = download_pdf("https://arxiv.org/pdf/2009.05959.pdf")
    extract_pdf_text(filepath)


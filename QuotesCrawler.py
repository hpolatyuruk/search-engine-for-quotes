from bs4 import BeautifulSoup
import requests
import re


class Quote:
    def __init__(self, text, author, title, tags):
        self.Text = text
        self.Author = author
        self.Title = title
        self.Tags = tags


def fetchQuotesHTML(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print("Error: Server returned error. StatusCode: {}, Response{}".format(
                response.status_code, response.text))
        return response.text
    except Exception as ex:
        print(ex)


def parseQuotes(html):
    parser = BeautifulSoup(html, 'html.parser')
    quoteDetailsDivs = parser.find_all('div', attrs={'class': 'quoteDetails'})
    quotes = []
    for quoteDetailDiv in quoteDetailsDivs:
        quoteTextDiv = quoteDetailDiv.find('div', attrs={'class', 'quoteText'})
        quoteText = parseQuoteTextDiv(quoteTextDiv)
        quoteAuthor = parseQuoteAuthor(quoteTextDiv)
        quoteTitle = parseQuoteTitle(quoteTextDiv)
        quoteTags = parseQuoteTags(quoteDetailDiv.find(
            'div', attrs={'class', 'quoteFooter'}))
        quote = Quote(quoteText, quoteAuthor, quoteTitle, quoteTags)
        quotes.append(quote)

    return quotes


def parseQuoteTextDiv(div):
    return div.next_element.strip().lstrip('“').rstrip('”')


def parseQuoteAuthor(quoteTextDiv):
    return quoteTextDiv.find('span', attrs={'class', 'authorOrTitle'}).get_text().replace('\n', '').strip()


def parseQuoteTitle(quoteTextDiv):
    titleSpan = quoteTextDiv.find('span', id=re.compile('^quote_book_link'))
    if titleSpan == None:
        return ''
    return titleSpan.get_text().replace('\n', '').strip()


def parseQuoteTags(quoteFooterDiv):
    tags = []
    tagDiv = quoteFooterDiv.find(
        'div', attrs={'class', 'greyText smallText left'})
    if tagDiv == None:
        return tags
    for tagAnchor in tagDiv.find_all('a'):
        tags.append(tagAnchor.get_text().strip())
    return tags


url = 'https://www.goodreads.com/quotes'

html = fetchQuotesHTML(url)
quotes = parseQuotes(html)
print(len(quotes))
for quote in quotes:
    print('Text: {}, Author: {}, Title: {}, Tags: [{}]'.format(
        quote.Text, quote.Author, quote.Title, ','.join(quote.Tags)))

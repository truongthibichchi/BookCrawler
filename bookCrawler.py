from lxml import html
import requests
import csv

class BookCrawler:

    def __init__(self, starting_url, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.books = []

    def crawl(self):
        self.get_book_link_from_main_page(self.starting_url)
        return

    def get_book_link_from_main_page(self, url):
        start_page = requests.get(url)
        tree = html.fromstring(start_page.text)

        links = tree.xpath('//div[@class="div_book_name_list"]/a/@href')

        for link in links:
            book_link = 'http://anybooks.vn'+link
            self.get_book_details_from_link(book_link)
        return

    def get_book_details_from_link(self, link):
        book_page = requests.get(link)
        tree = html.fromstring(book_page.text)

        title = (tree.xpath('//h1[@itemprop="name"]/text()')[0]).strip()
        author = tree.xpath('//span[@itemprop="author"]/span/a/text()')[0]
        public_year = tree.xpath('//meta[@itemprop="datePublished"]/@content')[0]
        publisher = tree.xpath('//div[@class="clearfix"]/p/text()')[0]
        summary = tree.xpath('//div[@style="text-align: justify;"]/text()')

        book_item = Book(link, title, author, public_year, publisher, summary)
        self.books.append(book_item)
        self.write_data_to_csv_file(self.books)
        return

    def write_data_to_csv_file(self, book_list):
        csvData = [['No', 'link', 'title', 'author', 'publisher_date', 'publisher', 'summary']]
        num = 1
        for book in book_list:
            csvData.append([num, book.link, book.title, book.author, book.published_date, book.publisher, book.summary])
            num += 1
        with open('output/books.csv', 'w') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerows(csvData)
        csvFile.close()

class Book:

    def __init__(self, link, title, author, published_date, publisher, summary):
        self.link = link
        self.title = title
        self.author = author
        self.published_date = published_date
        self.publisher = publisher
        self.summary = summary

categories = []
crawler = BookCrawler('http://anybooks.vn/book/Tieu_thuyet_viet_nam/page_1.html', 1)
crawler.crawl()



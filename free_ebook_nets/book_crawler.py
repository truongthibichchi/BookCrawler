from lxml import html
import requests
import csv
import os


class FreeEbookCrawler:
    categories = []

    def __init__(self, depth):
        self.depth = depth
        self.home_page = 'https://www.free-ebooks.net'
        self.csv_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'output',
            'full_books.csv'
        )
        self.writer = None

    def read_categories_from_csv_file(self):
        category_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'output',
            'categories_pages.csv'
        )

        with open(category_file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.categories.append([row[0], row[1]])
        print(self.categories)
        print(len(self.categories))
        self.crawl()

    def crawl(self):
        count = 1
        csv_titles = []
        csv_titles.append([
                        'book_links',
                        'book_images',
                        'book_sub_categories',
                        'book_ids',
                        'book_titles',
                        'book_authors',
                        'book_public_dates',
                        'book_ratings',
                        'book_rated_times',
                        'book_downloads',
                        'book_pages',
                        'book_desciptions'
                        ])
        with open(self.csv_file_path, 'a+') as csvFile:
            print("open file")
            self.writer = csv.writer(csvFile)
            self.writer.writerows(csv_titles)
            for category in self.categories:
                category_url = category[0]
                page_number = int(category[1])
                print("starting crawling data from ", category_url, ' ', page_number, '     ', count)
                self.crawl_book_from_category(category_url, page_number)
                count += 1
            print("write done")
        csvFile.close()
        return

    def crawl_book_from_category(self, category_url, page_number):
        if page_number <= 0:
            print('page <= 0')
            return
        num = 1
        while num <= page_number:
            url = f'{category_url}/{num}'
            self.get_book_detail_from_single_page(url)
            num += 1

    def get_book_detail_from_single_page(self, url):
        print(url)
        start_page = requests.get(url)
        tree = html.fromstring(start_page.text)

        book_links = tree.xpath('//div[@class="row laText"]/div/a[@class="img"]/@href')
        book_ids = tree.xpath('//div[@class="row laText"]/@data-id')
        book_titles = tree.xpath('//div[@class="row laText"]/div/h3/a[@class="title"]/text()')
        book_descriptions = tree.xpath('//p[@class="book-description"]/text()')
        ratings = (tree.xpath('//div[@class="col-sm-12 padIt"]/span/@title'))
        rated_times = (tree.xpath('//div[@class="col-sm-12 padIt"]/b/text()'))
        author_category = tree.xpath('//div[@class="col-sm-12 padIt"]/a/text()')
        date_download_page = tree.xpath('//div[@class="col-sm-12 hidden-xs padIt"]/b/text()')
        book_images = tree.xpath('//a[@class="img"]/@href')

        book_ratings = []
        book_rated_times = []
        book_authors = []
        book_sub_categories = []
        book_public_dates = []
        book_downloads = []
        book_pages = []

        for index, item in enumerate(ratings):
            if index % 5 == 0:
                book_ratings.append(item)
                continue

        for index, item in enumerate(rated_times):
            if index % 2 == 0:
                book_rated_times.append(item)
                continue

        for index, item in enumerate(author_category):
            if index % 2 == 0:
                book_authors.append(item)
                continue

            book_sub_categories.append(item)

        for index, item in enumerate(date_download_page):
            num = index % 3
            if num == 0:
                book_public_dates.append(item)
                continue

            if num == 1:
                book_downloads.append(item)
                continue

            book_pages.append(item)

        print(len(book_links), len(book_ids), len(book_titles), len(book_descriptions),
                 len(book_ratings), len(book_rated_times), len(book_authors), len(book_sub_categories), len(book_public_dates),
              len(book_downloads), len(book_pages), len(book_images))

        if( len(book_links)<= 0):
            print("no data, return")
            return

        if (len(book_links) == len(book_ids) == len(book_titles) == len(book_descriptions)
                == len(book_ratings) == len(book_rated_times) == len(book_authors)
                == len(book_sub_categories) == len(book_public_dates) == len(book_downloads) == len(book_pages) == len(book_images)):
            print('data available')
            csv_data = []
            i = 0
            while i < len(book_links):
                csv_data.append([self.home_page+book_links[i], self.home_page+book_images[i], book_sub_categories[i],
                                 book_ids[i], book_titles[i], book_authors[i],  book_public_dates[i], book_ratings[i],
                                 book_rated_times[i], book_downloads[i], book_pages[i], book_descriptions[i]
                                 ])

                i += 1
                print(f'{i} books was appended')
            print(csv_data)
            self.writer.writerows(csv_data)
            print(f'{len(csv_data)} books was written')
            return
        print(f'can not crawl data from {url}')


crawler = FreeEbookCrawler(0)
crawler.read_categories_from_csv_file()

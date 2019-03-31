from lxml import html
import requests
import csv
import os


class FreeEbookCrawler:
    categories = []
    ratings = []
    rated_times = []
    author_category = []
    date_download_page = []

    book_links = []
    book_ids = []
    book_titles = []
    book_authors = []
    book_sub_categories = []
    book_public_dates = []
    book_downloads = []
    book_pages = []
    book_descriptions = []
    book_images = []
    book_ratings = []
    book_rated_times = []

    csvData = []

    def __init__(self, depth):
        self.depth = depth
        self.home_page = 'https://www.free-ebooks.net'

    def get_categories(self):
        start_page = requests.get(self.home_page)
        tree = html.fromstring(start_page.text)

        self.categories = tree.xpath('//div[@class="row"]/div/ul/li/a/@href')
        # categories = tree.xpath('//div[@class="row"]/div/ul/li/a/@title')
        print(self.categories)

        # csv_file_path = os.path.join(
        #     os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        #     'output',
        #     'categories.csv'
        # )

        # self.write_categories_to_csv_file(self.categories, csv_file_path)

    def write_categories_to_csv_file(self, category_list, file_path):
        with open(file_path, 'w') as csvFile:
            writer = csv.writer(csvFile)
            csv_data = []
            for category in category_list:
                csv_data.append(['', '', self.home_page + category])
            writer.writerows(csv_data)
        csvFile.close()

    def read_categories_from_csv_file(self):
        csv_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'output',
            'categories_pages.csv'
        )

        with open(csv_file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            pages = []
            for row in csv_reader:
                pages.append([row[0], row[1]])
        print(pages)
        print(len(pages))
        self.crawl_book_details(pages)


    def crawl_book_details(self, pages):
        count_category = 0
        for page in pages:
            print(f'Starting to crawl data from category {count_category+1} : {page[1]} pages')
            if int(page[1]) <= 0:
                continue
            num = 1
            while num <= int(page[1]):
                print(f'get data from page {num}: ')
                self.get_book_detail_from_single_page(f'{page[0]}/{num}')
                print("done")
                num += 1
            count_category += 1

        if (len(self.book_links) > 0):
            print(f'number of book: {len(self.book_links)}')

            for index, item in enumerate(self.ratings):
                if index % 5 == 0:
                    self.book_ratings.append(item)
                    continue

            for index, item in enumerate(self.rated_times):
                if index % 2 == 0:
                    self.book_rated_times.append(item)
                    continue

            for index, item in enumerate(self.author_category):
                if index % 2 == 0:
                    self.book_authors.append(item)
                    continue

                self.book_sub_categories.append(item)

            for index, item in enumerate(self.date_download_page):
                num = index % 3
                if num == 0:
                    self.book_public_dates.append(item)
                    continue

                if num == 1:
                    self.book_downloads.append(item)
                    continue

                self.book_pages.append(item)

            print(f'number of book_ratings: {len(self.book_ratings)}')
            print(f'number of book_rated_times: {len(self.book_rated_times)}')
            print(f'number of book_authors: {len(self.book_authors)}')
            print(f'number of book_sub_categories: {len(self.book_sub_categories)}')
            print(f'number of book_public_dates: {len(self.book_public_dates)}')
            print(f'number of book_downloads: {len(self.book_downloads)}')
            print(f'number of book_pages: {len(self.book_pages)}')

            self.csvData.append(['No',
                                 'book_links',
                                 'book_ids',
                                 'book_titles',
                                 'book_authors',
                                 'book_sub_categories',
                                 'book_ratings',
                                 'book_rated_times',
                                 'book_public_dates',
                                 'book_downloads',
                                 'book_pages',
                                 'book_desciptions',
                                 'book_images']
                                )
            no = 0
            for book in self.book_links:
                self.csvData.append([no + 1,
                                     book,
                                     self.book_ids[no],
                                     self.book_titles[no],
                                     self.book_authors[no],
                                     self.book_sub_categories[no],
                                     self.book_ratings[no],
                                     self.book_rated_times[no],
                                     self.book_public_dates[no],
                                     self.book_downloads[no],
                                     self.book_pages[no],
                                     self.book_descriptions[no],
                                     self.book_images[no]]
                                    )
                print(f'{no + 1} was appended to csv data')
                no += 1
            csv_file_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                'output',
                'books.csv'
            )
            with open(csv_file_path, 'w') as csvFile:
                print("open file")
                writer = csv.writer(csvFile)
                writer.writerows(self.csvData)
                print("write done")
            csvFile.close()
            return

    def get_book_detail_from_single_page(self, url):
        print(url)
        start_page = requests.get(url)
        tree = html.fromstring(start_page.text)

        self.book_links += tree.xpath('//div[@class="row laText"]/div/a[@class="img"]/@href')
        self.book_ids += tree.xpath('//div[@class="row laText"]/@data-id')
        self.book_titles += tree.xpath('//div[@class="row laText"]/div/h3/a[@class="title"]/text()')
        self.book_descriptions += tree.xpath('//p[@class="book-description"]/text()')
        self.ratings += (tree.xpath('//div[@class="col-sm-12 padIt"]/span/@title'))
        self.rated_times += (tree.xpath('//div[@class="col-sm-12 padIt"]/b/text()'))
        self.author_category += tree.xpath('//div[@class="col-sm-12 padIt"]/a/text()')
        self.date_download_page += tree.xpath('//div[@class="col-sm-12 hidden-xs padIt"]/b/text()')
        self.book_images += tree.xpath('//a[@class="img"]/@href')

        print(len(self.book_links), len(self.book_ids), len(self.book_titles), len(self.book_descriptions),
              len(self.ratings), len(self.rated_times),
              len(self.author_category), len(self.date_download_page), len(self.book_images))


class Book:

    def __init__(self, book_id, title, author, sub_category, public_date, downloads, pages, summary, small_image, link):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.sub_category = sub_category
        self.public_date = public_date
        self.downloads = downloads
        self.pages = pages
        self.summary = summary
        self.small_image = small_image
        self.link = link


crawler = FreeEbookCrawler(0)
crawler.read_categories_from_csv_file()

# print('https://www.free-ebooks.net/drama/5')
# start_page = requests.get('https://www.free-ebooks.net/drama/5')
# tree = html.fromstring(start_page.text)
#
# book_links = []
# book_ids = []
# book_titles = []
# book_descriptions = []
# ratings = []
# rated_times = []
# author_category = []
# date_download_page = []
# book_images = []
#
# book_links += tree.xpath('//div[@class="row laText"]/div/a[@class="img"]/@href')
# book_ids.append(tree.xpath('//div[@class="row laText"]/@data-id'))
# book_titles.append(tree.xpath('//div[@class="row laText"]/div/h3/a[@class="title"]/text()'))
# book_descriptions.append(tree.xpath('//p[@class="book-description"]/text()'))
# ratings.append(tree.xpath('//div[@class="col-sm-12 padIt"]/span/@title'))
# rated_times.append(tree.xpath('//div[@class="col-sm-12 padIt"]/b/text()'))
# author_category.append(tree.xpath('//div[@class="col-sm-12 padIt"]/a/text()'))
# date_download_page.append(tree.xpath('//div[@class="col-sm-12 hidden-xs padIt"]/b/text()'))
# book_images.append(tree.xpath('//a[@class="img"]/@href'))
#
# print(book_links)
# print(len(book_links), len(book_ids), len(book_titles), len(book_descriptions),
#               len(ratings), len(rated_times),len(author_category), len(date_download_page), len(book_images))
# book_descriptions = tree.xpath('//p[@class="book-description"]/text()')
# print(book_descriptions)

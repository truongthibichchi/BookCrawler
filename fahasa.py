import os
import csv
import requests
from lxml import html


class FahasaCrawler:
    category = []

    def __init__(self, depth):
        self.depth = depth
        self.home_page = 'https://www.fahasa.com/'
        self.csv_file_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'output',
            'fahasa_books.csv'
        )
        self.writer = None

    def read_categories_from_csv_file(self):
        category_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'input',
            'category.csv'
        )

        with open(category_file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                # self.category.append([row[0], row[1], row[2]])
                self.crawl_book_from_category(row[0], row[1], row[2])

    def crawl_book_from_category(self, name, page_number, category_url):
        if int(page_number) <= 0:
            print('page <= 0')
            return
        num = 1
        while num <= int(page_number):
            url = f'{category_url}/page/{num}.html'
            self.get_book_items(name, url)
            num += 1

    def get_book_items(self, name, url):
        try:
            print(url)
            start_page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            tree = html.fromstring(start_page.text)
            print(start_page.text)
            links = tree.xpath('//div[@class="product images-container"]/a[@class="product-image"]/@href')

            print(links)
            if links is None:
                return

            links_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'input',
                'links.csv'
            )

            with open(links_path) as csv_file:
                for link in links:
                    self.writer = csv.writer(csv_file)
                    self.writer.writerows([name, link])

            csv_file.close()
        except Exception as e:
            print(e)


    def crawl(self):
        data = []
        data.append([
            'link',
            'title',
            'rating',
            'rated_time',
            'author',
            'public_date',
            'page',
            'summary'
            ])
        with open(self.csv_file_path, 'a+') as csvFile:
                    print("open file")
                    self.writer = csv.writer(csvFile)
                    self.writer.writerows(data)
                    for item in self.category:
                        name = item[0]
                        category_url = item[2]
                        page_number = int(item[1])
                        print("starting crawling data from ", name, '   ', category_url, ' ', page_number)
                        self.crawl_book_from_category(name, category_url, page_number)
                    print("write done")
        csvFile.close()
        return

# crawler = FahasaCrawler(0)
# crawler.read_categories_from_csv_file()
import bs4 as bs
import urllib.request as resquest
from selenium import webdriver

url = 'https://www.fahasa.com/sach-trong-nuoc/tieu-su-hoi-ky/page/12.html'
# driver = webdriver.Chrome()
# driver.get(url=url)
# res = driver.execute_script("return document.documentElement.outerHTML")
# driver.quit()

res = resquest.urlopen(url)
soup = bs.BeautifulSoup(res, 'lxml')
print(soup)
links = soup.find('a', {'class': 'product-image'})
print(links)


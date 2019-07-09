import requests
from lxml import html
import os
import csv
import re
import datetime


def read_category_html():
    filename = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    'fahasa_html', 'fahasa_html_data.csv'
                )

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            write_book_data(str(row[0]), str(row[1]))


def write_book_data(folder, html_file):
    html_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'fahasa_html', folder, html_file
    )

    output_file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'fahasa_html', 'output_fahasa.csv'
    )

    etcd_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'fahasa_etcd.txt'
    )

    f = open(html_file_path, "r").read()
    tree = html.fromstring(f)
    book_category = str(folder)
    book_title = tree.xpath('//img[@id="image"]/@title')[0]
    print(book_title)
    infos = tree.xpath('//td[@class="data"]/text()')
    book_id = re.sub(r"[\n ]", "", infos[0])
    book_author = re.sub(r"\n                            ", "", infos[3])
    book_author = re.sub(r"                        ", "", book_author)
    book_public_date = "2017"
    book_rating = tree.xpath('//div[@class="rating"]/@style')[0]
    book_rating = re.sub(r"[width:%]", "", book_rating)
    book_rated_time = str(tree.xpath('//p[@class="rating-links"]/a/text()')[0])
    book_rated_time = re.sub(r"[()]", "", book_rated_time)
    book_download = "10"
    book_page = "100"
    # description = tree.xpath('//p[@style="text-align: justify;"]/text()')
    description = tree.xpath('//div[@class="std"]/p/text()')
    book_description = '\n'.join(re.sub(r'[“”!"?]', '', des) for des in description)
    book_image = tree.xpath('//img[@id="image"]/@src')[0]
    book_file = f'/static/books/book_file.pdf'

    # book_title = tree.xpath('//h1/text()')[0]
    # book_title = re.sub(r"\n                        ", "", book_title)
    # book_title = re.sub(r" \n                    ", "", book_title)

    with open(output_file_path, 'a+') as csvFile:
        with open(etcd_file, 'a+') as txt_file:
            writer = csv.writer(csvFile)
            writer.writerow([book_category, book_title, book_id, book_author, book_public_date,
                             book_rating, book_rated_time, book_download, book_page, book_description,
                             book_image, book_file])

            key = f'/book/{book_id}'
            txt_file.write(f'etcdctl put "{key}" "{book_id}"\n')
            txt_file.write(f'etcdctl put "{key}/book_category" "{book_category}"\n')
            txt_file.write(f'etcdctl put "{key}/book_type" "ebook"\n')
            txt_file.write(f'etcdctl put "{key}/book_title" "{book_title}"\n')
            txt_file.write(f'etcdctl put "{key}/book_author" "{book_author}"\n')
            txt_file.write(f'etcdctl put "{key}/book_public_date" "{book_public_date}"\n')
            txt_file.write(f'etcdctl put "{key}/book_rating" "{book_rating}"\n')
            txt_file.write(f'etcdctl put "{key}/book_rated_time" "{book_rated_time}"\n')
            txt_file.write(f'etcdctl put "{key}/book_download" "{book_download}"\n')
            txt_file.write(f'etcdctl put "{key}/book_read_time" "10"\n')
            txt_file.write(f'etcdctl put "{key}/book_page" "{book_page}"\n')
            txt_file.write(f'etcdctl put "{key}/book_image" "{book_image}"\n')
            txt_file.write(f'etcdctl put "{key}/book_file" "{book_file}"\n')
            txt_file.write(f'etcdctl put "{key}/book_is_deleted" "0"\n')
            txt_file.write(f'etcdctl put "{key}/book_description" """{book_description}"""\n')
            txt_file.write(f'etcdctl put "{key}/book_created_time" """{str(datetime.datetime.now())}"""\n')
            txt_file.write('\n')


read_category_html()


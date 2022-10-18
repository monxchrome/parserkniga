import os
import datetime
import random

from bs4 import BeautifulSoup
import requests
from slugify import slugify


from parser2.models import Series2, Years2, Translators2, Books2, Pages2, Genres2, BookGenre2, Authors2, AuthorToBooks2, \
    BookTranslator2

# storage_number = 1
# link = f"https://knigavuhe.org/new/?page='{storage_number}"
#
# response = requests.get(f'{link}/{storage_number}').text
# soup = BeautifulSoup(response, 'lxml')
# block = soup.find_all('div', class_="bookkitem")
#
# for block2 in block:
#     block1 = soup.find_all('img', class_="bookkitem_cover_img", src=all)
#
#     print(block1)


class KnigavuheParser:
    url = "https://knigavuhe.org/"
    storage_url = "/api.foxbooks.ec/storage/app/public/audiobook/covers/default"

    def __init__(self, book_id, book_in_db=None):
        self.book_id = book_id
        self.pages = []
        self.last_page = None
        self.book_link = self.url + "book/" + str(book_id)
        html = self.get_html_from_link(self.book_link)
        self.soup = BeautifulSoup(html, "lxml")
        self.book = {}
        self.book_in_db = book_in_db

    def get_cover(self, year):
        image = self.soup.find('div', id='books_updates_list')
        for i in image:
            if i.get([item['src'] for item in image.select('img')]) != -1:
                self.image = i.get([item['src'] for item in image.select('img')])
                filename = self.image.split("/")[-1]
                url_in_db = f"/audio/covers/{filename}"
                if not os.path.exists(f"{self.storage_url}/audio/covers/"):
                    os.mkdir(f"{self.storage_url}/audio/covers")
                if not os.path.exists(f"{self.storage_url}/audio/covers/"):
                    os.mkdir(f"{self.storage_url}/audiobooks/covers/")

                with open(self.storage_url + url_in_db, "wb") as f:
                    url = self.url + self.image
                    r = requests.get(url)
                    if r.status_code == 200:
                        f.write(r.content)
                return url_in_db

    def get_page(self, page_number: int = 1):
        url = f"{self.url}books/{self.book_id}"
        html = self.get_html_from_link(url)
        if not html:
            return None
        page_soup = BeautifulSoup(html, "lxml")
        images = page_soup.find('div', id='books_updates_list')
        for i in images:
            if i.get([item['src'] for item in images.select('img')]) != -1:
                self.save_image_from_page(i.get([item['src'] for item in images.select('img')]))

    def save_image_from_page(self, link):
        filename = link.split("/")[-1]
        url_in_db = f"/img/photo_audiobooks/{self.book_id}/{filename}"
        if not os.path.exists(f"{self.storage_url}"):
            os.mkdir(f"{self.storage_url}")
        if not os.path.exists(f"{self.storage_url}/img/"):
            os.mkdir(f"{self.storage_url}/img")
        if not os.path.exists(f"{self.storage_url}/img/photo_audiobooks/"):
            os.mkdir(f"{self.storage_url}/img/photo_audiobooks")
        if not os.path.exists(f"{self.storage_url}/img/photo_audiobooks/{self.book_id}"):
            os.mkdir(f"{self.storage_url}/img/photo_audiobooks/{self.book_id}")

        with open(self.storage_url + url_in_db, "wb") as f:
            url = self.url + link
            r = requests.get(url)
            if r.status_code == 200:
                f.write(r.content)
        return url_in_db

    def parse_pages(self):
        i = 1
        while not self.last_page and i < 10000:
            self.get_page(i)
            i += 1

    def write_book_to_db(self):
        self.get_info()
        self.parse_pages()

        year = self.info.pop("Год") if self.info.get("Год") else None
        cover_year = year if year else "0000"
        if year:
            year_in_db = Years2.objects.using("mysql").filter(year=year).first()
            if year_in_db:
                year = year_in_db
            else:
                year = Years2.objects.using("mysql").create(year=year)

        cover = self.get_cover(cover_year)

        authors = self.info.pop("Автор") if self.info.get("Автор") else None

        self.book = {
            "donor_id": self.book_id,
            "count_pages": self.last_page,
            "slug": slugify(f'{self.info.get("Название")}-{int(self.book_id * 0.95)}'),
            "active": True,
            "params": self.info,
            "cover_url": cover
        }
        book = Books2.objects.using("mysql").filter(donor_id=self.book_id).first()
        if not book:
            book = Books2.objects.using("mysql").create(**self.book)
        else:
            Books2.objects.using("mysql").filter(donor_id=self.book_id).update(**self.book)

    def write_pages(self):
        Pages2.objects.using("mysql").filter(book_id=self.book_in_db).delete()

        if not self.book_in_db:
            self.book_in_db = Books2.objects.using("mysql").filter(donor_id=self.book_id).first()
        for index, i in enumerate(self.pages):
            self.pages[index] = Pages2(
                book_id=self.book_in_db,
                link=self.book_link,
                content=i,
                page_number=index + 1,
                fixed=0
            )

        Pages2.objects.using("mysql").bulk_create(self.pages)

    @staticmethod
    def get_html_from_link(link):
        r = requests.get(link)
        if r.status_code == 200:
            return r.text
        return None

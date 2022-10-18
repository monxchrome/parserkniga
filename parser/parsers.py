import os
import datetime
import random

from bs4 import BeautifulSoup
import requests
from slugify import slugify

from parser.legacy_models import Series, Years, Translators, Books, Pages, Genres, BookGenre, Authors, AuthorToBooks, \
    BookTranslator


class LovereadParser:
    url = "http://loveread.ec/"
    storage_url = "/var/www/www-root/data/www/api.foxbooks.ec/storage/app/public"

    def __init__(self, book_id, book_in_db=None):
        self.book_id = book_id
        self.pages = []
        self.last_page = None
        self.book_link = self.url + "view_global.php?id=" + str(book_id)
        html = self.get_html_from_link(self.book_link)
        self.soup = BeautifulSoup(html, "lxml")
        self.book = {}
        self.book_in_db = book_in_db

    def get_title(self):
        title = self.soup.find("h2")
        return title.contents[0].split('-')[-1].strip()

    def get_description(self):
        desc = self.soup.find("p", class_="span_str")
        return desc.text.replace("<strong>", "").replace("</strong>", "").replace("\t", "").replace("\r", "").replace(
            "\n", "")

    def get_cover(self, year):
        image = self.soup.find_all("img")
        for i in image:
            if i.get("src").find("img/photo_books/") != -1:
                self.image = i.get("src")
                filename = self.image.split("/")[-1]
                url_in_db = f"/books/covers/{year}/{filename}"
                if not os.path.exists(f"{self.storage_url}/books/covers/"):
                    os.mkdir(f"{self.storage_url}/books/covers")
                if not os.path.exists(f"{self.storage_url}/books/covers/{year}/"):
                    os.mkdir(f"{self.storage_url}/books/covers/{year}")

                with open(self.storage_url + url_in_db, "wb") as f:
                    url = self.url + self.image
                    r = requests.get(url)
                    if r.status_code == 200:
                        f.write(r.content)
                return url_in_db

    def get_info(self):
        info = self.soup.find("td", class_="span_str")
        genre = self.soup.find("tr", class_="td_top_color").p
        info_as_list = [i.strip() for i in info.text.split("\n") if i != ""]
        res = {
            "Жанр": genre.text.replace("Жанр ", "")
        }
        k = None

        for el in info_as_list:
            if el == "" or el == ",":
                continue
            if el[-1] == ":":
                k = el[:-1]
            elif el.find(":") == -1:
                if res.get(k):
                    value = res.get(k)
                    if isinstance(value, str):
                        value = [value]
                    value.append(el)
                    res[k] = value
                else:
                    res[k] = el
            else:
                res[el.split(":")[0]] = el.split(":")[1].strip()
        self.info = res

    def get_page(self, page_number: int = 1):
        url = f"{self.url}read_book.php?id={self.book_id}&p={page_number}"
        html = self.get_html_from_link(url)
        if not html:
            return None
        page_soup = BeautifulSoup(html, "lxml")
        page = page_soup.find("div", class_="MsoNormal")
        images = page_soup.find_all("img")
        for i in images:
            if i.get("src").find("img/photo_books/") != -1:
                self.save_image_from_page(i.get("src"))

        # remove forms
        form_tag = page_soup.form
        while form_tag:
            if form_tag.parent:
                form_tag.parent.extract()
            form_tag.extract()
            form_tag = page_soup.form
        self.pages.append(str(page).replace(f"img/photo_books/{self.book_id}.jpg",
                                            f"img/photo_books/{self.book_id}/{self.book_id}.jpg"))

        if page_soup.find("a", text="Вперед") == None:
            self.last_page = page_number

    def save_image_from_page(self, link):
        filename = link.split("/")[-1]
        url_in_db = f"/img/photo_books/{self.book_id}/{filename}"
        if not os.path.exists(f"{self.storage_url}"):
            os.mkdir(f"{self.storage_url}")
        if not os.path.exists(f"{self.storage_url}/img/"):
            os.mkdir(f"{self.storage_url}/img")
        if not os.path.exists(f"{self.storage_url}/img/photo_books/"):
            os.mkdir(f"{self.storage_url}/img/photo_books")
        if not os.path.exists(f"{self.storage_url}/img/photo_books/{self.book_id}"):
            os.mkdir(f"{self.storage_url}/img/photo_books/{self.book_id}")

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

        series = self.info.pop("Серия") if self.info.get("Серия") else None
        if series:
            series_in_db = Series.objects.using("mysql").filter(series=series).first()
            if series_in_db:
                series = series_in_db
            else:
                series = Series.objects.using("mysql").create(series=series)

        year = self.info.pop("Год") if self.info.get("Год") else None
        cover_year = year if year else "0000"
        if year:
            year_in_db = Years.objects.using("mysql").filter(year=year).first()
            if year_in_db:
                year = year_in_db
            else:
                year = Years.objects.using("mysql").create(year=year)

        cover = self.get_cover(cover_year)

        translators = self.info.pop("Перевод книги") if self.info.get("Перевод книги") else None

        genre = self.info.pop("Жанр") if self.info.get("Жанр") else None
        authors = self.info.pop("Автор") if self.info.get("Автор") else None

        self.book = {
            "title": self.info.get("Название"),
            "text": self.get_description(),
            "series": series if series else None,
            "year": year if year else None,
            "donor_id": self.book_id,
            "count_pages": self.last_page,
            "created_at": datetime.datetime.now(),
            "slug": slugify(f'{self.info.get("Название")}-{int(self.book_id * 0.95)}'),
            "active": True,
            "params": self.info,
            "cover_url": cover
        }
        book = Books.objects.using("mysql").filter(donor_id=self.book_id).first()
        if not book:
            book = Books.objects.using("mysql").create(**self.book)
        else:
            Books.objects.using("mysql").filter(donor_id=self.book_id).update(**self.book)

        if genre:
            genre_in_db = Genres.objects.using("mysql").filter(name=genre).first()
            if genre_in_db:
                genre = genre_in_db
            else:
                genre = Genres.objects.using("mysql").create(name=genre, slug=slugify(genre), is_hidden=0)
            BookGenre.objects.using("mysql").filter(book_id=book.id).delete()
            BookGenre.objects.using("mysql").create(book_id=book.id, genre_id=genre.id)

        if authors:
            if isinstance(authors, str):
                authors = [authors]
            for author in authors:
                author_in_db = Authors.objects.using("mysql").filter(author=author).first()
                if not author_in_db:
                    author_in_db = Authors.objects.using("mysql").create(author=author, slug=slugify(author))
                AuthorToBooks.objects.using("mysql").create(author=author_in_db, book=book)
        self.book_in_db = book

        if translators:
            translators.replace(" // ", ", ")
            if translators.find(",") != -1:
                translators = translators.split(", ")
            else:
                translators = [translators]
            for translator in translators:
                translator_in_db = Translators.objects.using("mysql").filter(name=translator).first()
                if translator_in_db:
                    translator = translator_in_db
                else:
                    translator = Translators.objects.using("mysql").create(name=translator,
                                                                           created_at=datetime.datetime.now())
                BookTranslator.objects.using("mysql").create(book=book, translator=translator)

    def write_pages(self):
        Pages.objects.using("mysql").filter(book_id=self.book_in_db).delete()

        if not self.book_in_db:
            self.book_in_db = Books.objects.using("mysql").filter(donor_id=self.book_id).first()
        for index, i in enumerate(self.pages):
            self.pages[index] = Pages(
                book_id=self.book_in_db,
                link=self.book_link,
                content=i,
                page_number=index + 1,
                fixed=0
            )

        Pages.objects.using("mysql").bulk_create(self.pages)

    @staticmethod
    def get_html_from_link(link):
        r = requests.get(link)
        if r.status_code == 200:
            return r.text
        return None


class AuthorParser:
    url = 'http://loveread.ec/letter_author.php?let=1'
    storage_url = '/var/www/www-root/data/www/api.foxbooks.ec/storage/app/public/authors/{first_letter}/{author_id}'

    def __init__(self, author_id, book_in_db=None):
        self.author_id = author_id
        self.pages = []
        self.last_page = None
        self.author_link = self.url + "http://loveread.ec/biography-author.php?author=" + str(author_id)
        html = self.get_html_from_link(self.author_link)
        self.soup = BeautifulSoup(html, "lxml")
        self.name = {}
        self.name_in_db = book_in_db

    def get_name(self):
        name = self.soup.find("a")
        return name.contents[0].split('-')[-1].strip()

    def get_page(self, page_number: int = 1):
        url = f"{self.url}letter_author.php?let={self.author_id}&p={page_number}"
        html = self.get_html_from_link(url)
        if not html:
            return None
        page_soup = BeautifulSoup(html, "lxml")
        page = page_soup.find("div", class_="contents")
        images = page_soup.find_all("h2")
        for i in images:
            if i.get("h2") != -1:
                self.save_authors_from_page(i.get_text("h2"))
        # remove forms
        form_tag = page_soup.form
        while form_tag:
            if form_tag.parent:
                form_tag.parent.extract()
            form_tag.extract()
            form_tag = page_soup.form
        self.pages.append(str(page))

        if page_soup.find("a", text="Вперед") is None:
            self.last_page = page_number

    def get_info(self):
        info = self.soup.find("a", class_="letter_author")
        name = self.soup.find("a", class_="letter_author").get_text()
        info_as_list = [i.strip() for i in info.text.split("\n") if i != ""]
        res = {
            "Автор": name.replace("Автор ", "")
        }
        k = None

        for el in info_as_list:
            if el == "" or el == ",":
                continue
            if el[-1] == ":":
                k = el[:-1]
            elif el.find(":") == -1:
                if res.get(k):
                    value = res.get(k)
                    if isinstance(value, str):
                        value = [value]
                    value.append(el)
                    res[k] = value
                else:
                    res[k] = el
            else:
                res[el.split(":")[0]] = el.split(":")[1].strip()
        self.info = res

    def parse_pages(self):
        i = 1
        while not self.last_page and i < 10000:
            self.get_page(i)
            i += 1

    def write_book_to_db(self):
        self.parse_pages()
        authors = self.info.pop("Автор") if self.info.get("Автор") else None
        name = self.info.pop("Автор") if self.info.get("Автор") else None

        self.book = {
            "title": self.info.get("Название"),
            "donor_id": self.author_id,
            "count_pages": self.last_page,
            "slug": slugify(f'{self.info.get("Название")}-{int(self.author_id * 0.95)}'),
            "active": True,
        }
        author = Books.objects.using("mysql").filter(donor_id=self.author_id).first()
        if not author:
            author = Books.objects.using("mysql").create(**self.book)
        else:
            Books.objects.using("mysql").filter(donor_id=self.author_id).update(**self.book)

        if name:
            name_in_db = Genres.objects.using("mysql").filter(name=name).first()
            if name_in_db:
                name = name_in_db
            else:
                name = Genres.objects.using("mysql").create(name=name, slug=slugify(name), is_hidden=0)
            BookGenre.objects.using("mysql").filter(book_id=author.id).delete()
            BookGenre.objects.using("mysql").create(book_id=author.id, genre_id=name.id)

        if authors:
            if isinstance(authors, str):
                authors = [authors]
            for author in authors:
                author_in_db = Authors.objects.using("mysql").filter(author=author).first()
                if not author_in_db:
                    author_in_db = Authors.objects.using("mysql").create(author=author, slug=slugify(author))
                AuthorToBooks.objects.using("mysql").create(author=author_in_db, book=author)
        self.book_in_db = author

    def write_pages(self):
        Pages.objects.using("mysql").filter(author_id=self.name_in_db).delete()

        if not self.name_in_db:
            self.name_in_db = Books.objects.using("mysql").filter(donor_id=self.author_id).first()
        for index, i in enumerate(self.pages):
            self.pages[index] = Pages(
                book_id=self.name_in_db,
                link=self.author_link,
                content=i,
                page_number=index + 1,
                fixed=0
            )

        Pages.objects.using("mysql").bulk_create(self.pages)

    @staticmethod
    def get_html_from_link(link):
        r = requests.get(link)
        if r.status_code == 200:
            return r.text
        return None

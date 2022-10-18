import logging

import requests
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils import timezone

from parser2.models import AudioBooksLinks2, AudioBooks2
from parser.legacy_models import BookLinks, Books, Years, Series, Pages
from parser.parsers import LovereadParser
from parser2.parser import KnigavuheParser


@admin.action(description='Parse selected links (only info+covers)')
def parse(modeladmin, request, queryset):
    if len(queryset) > 999:
        queryset = BookLinks.objects.using("mysql").all()
    for qs in queryset:
        try:
            book_id = qs.donor_id
            parser = LovereadParser(book_id)
            parser.write_book_to_db()
        except BaseException as e:
            print(e)


@admin.action(description='Parse selected links with pages')
def parse_all(modeladmin, request, queryset):
    if len(queryset) > 999:
        queryset = BookLinks.objects.using("mysql").all()
    for qs in queryset:
        try:
            book_id = qs.donor_id
            parser = LovereadParser(book_id)
            parser.write_book_to_db()
            parser.write_pages()
            qs.doparse = 0
            qs.save()
        except BaseException as e:
            print(e)


@admin.action(description='UPDATE')
def update_books_to_parse(modeladmin, request, queryset):
    index = BookLinks.objects.using("mysql").last().donor_id

    while index < 175000:
        new = BookLinks.objects.using("mysql").filter(donor_id=index).first()
        if index % 1000 == 0:
            print("=" * 20, index)
        if new:
            index += 1
            continue
        else:
            url = f"http://loveread.ec/view_global.php?id={index}"
            r = requests.get(url)
            if r.status_code == 200:
                BookLinks.objects.using("mysql").create(donor_id=index, doparse=1, link=url)
                print(f"created new link {index}")
                index += 1
            else:
                print(f"{index} returns {r.status_code}")
                break


# @admin.register(BookLinks)
# class PageLinksAdmin(admin.ModelAdmin):
#     list_display = ("link", "doparse")
#     list_filter = ("doparse",)
#     search_fields = ("link",)
#     actions = [parse, parse_all, update_books_to_parse]
#     list_per_page = 1000
#
#     def get_queryset(self, request):
#         return BookLinks.objects.all().using("mysql")


@admin.action(description='Parse selected (only info + covers)')
def parse_selected(modeladmin, request, queryset):
    count = 0
    for book in queryset:
        if book.donor_id:
            try:
                parser = LovereadParser(book.donor_id)
                parser.write_book_to_db()
                count += 1
            except BaseException as e:
                logging.error(e)

    modeladmin.message_user(request, f"Updated {count} rows")


@admin.action(description='Parse selected (only pages)')
def parse_pages_books(modeladmin, request, queryset):
    count = 0
    for book in queryset:
        if book.donor_id:
            try:
                parser = LovereadParser(book_id=book.donor_id, book_in_db=book.id)
                print("PARSER:", parser)
                parser.parse_pages()
                print("parsed pages")
                parser.write_pages()
                print("writed pages")
                count += 1
            except BaseException as e:
                logging.error(e)

    modeladmin.message_user(request, f"Updated {count} rows")


@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "series_id", "year", "donor_id", "slug", "count_pages", "cover_url")
    list_per_page = 1000
    list_filter = ("cover_url", admin.EmptyFieldListFilter),
    change_list_template = "books_admin_changelist.html"
    search_fields = ("id",)
    actions = [parse_selected, parse_pages_books]

    def get_queryset(self, request):
        return Books.objects.all().using("mysql")

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('add_covers/', self.add_covers),
        ]
        return my_urls + urls

    def add_covers(self, request):
        books = Books.objects.all().using("mysql").filter(cover_url__isnull=True)
        for book in books:
            try:
                parser = LovereadParser(book.donor_id)
                year = book.year.year if book.year.year else "0000"
                cover = parser.get_cover(year)
                book.cover_url = cover
                book.save()
            except BaseException as e:
                logging.warning(e, timezone.now())
        self.message_user(request, "Covers were updated")
        return HttpResponseRedirect("../")


@admin.action(description='Parse selected (only info + covers)')
def parse_selected(modeladmin, request, queryset):
    count = 0
    for book in queryset:
        if book.link:
            try:
                parser = KnigavuheParser(book.link)
                parser.write_book_to_db()
                count += 1
            except BaseException as e:
                logging.error(e)

    modeladmin.message_user(request, f"Updated {count} rows")


@admin.action(description='Parse selected (only pages)')
def parse_pages_books(modeladmin, request, queryset):
    count = 0
    for book in queryset:
        if book.link:
            try:
                parser = KnigavuheParser(book_id=book.link, book_in_db=book.id)
                print("PARSER:", parser)
                parser.parse_pages()
                print("parsed pages")
                parser.write_pages()
                print("writed pages")
                count += 1
            except BaseException as e:
                logging.error(e)


@admin.action(description='Parse selected links (only info+covers)')
def parse(modeladmin, request, queryset):
    if len(queryset) > 999:
        queryset = AudioBooksLinks2.objects.using("mysql").all()
    for qs in queryset:
        try:
            book_id = qs.donor_id
            parser = KnigavuheParser(book_id)
            parser.write_book_to_db()
        except BaseException as e:
            print(e)


@admin.action(description='Parse selected links with pages')
def parse_all(modeladmin, request, queryset):
    if len(queryset) > 999:
        queryset = AudioBooksLinks2.objects.using("mysql").all()
    for qs in queryset:
        try:
            book_id = qs.donor_id
            parser = KnigavuheParser(book_id)
            parser.write_book_to_db()
            parser.write_pages()
            qs.doparse = 0
            qs.save()
        except BaseException as e:
            print(e)


@admin.action(description='UPDATE')
def update_books_to_parse(modeladmin, request, queryset, self, book_id, book_in_db=None):
    index = AudioBooksLinks2.objects.using("mysql").last().donor_id

    while index < 175000:
        new = AudioBooksLinks2.objects.using("mysql").filter(donor_id=index).first()
        if index % 1000 == 0:
            print("=" * 20, index)
        if new:
            index += 1
            continue
        else:
            url = f"https://knigavuhe.org/new/?page={index}"
            r = requests.get(url)
            if r.status_code == 200:
                AudioBooksLinks2.objects.using("mysql").create(donor_id=index, doparse=1, link=url)
                print(f"created new link {index}")
                index += 1
            else:
                print(f"{index} returns {r.status_code}")
                break


@admin.action(description='test parse cover')
def parse_selected(modeladmin, request, queryset):
    count = 0
    for book in queryset:
        if book.link:
            try:
                parser = KnigavuheParser(book.link)
                parser.write_book_to_db()
                count += 1
            except BaseException as e:
                logging.error(e)

    modeladmin.message_user(request, f"Updated {count} rows")


@admin.action(description='test parse pages')
def parse_pages_books(modeladmin, request, queryset):
    count = 0
    for book in queryset:
        if book.link:
            try:
                parser = KnigavuheParser(book_id=book.link, book_in_db=book.id)
                print("PARSER:", parser)
                parser.parse_pages()
                print("parsed pages")
                parser.write_pages()
                print("writed pages")
                count += 1
            except BaseException as e:
                logging.error(e)


@admin.register(AudioBooks2)
class AudioBooksAdmin2(admin.ModelAdmin):
    list_display = ("id", "slug", "cover_url")
    list_per_page = 1000
    list_filter = ("cover_url", admin.EmptyFieldListFilter),
    change_list_template = "books_admin_changelist2.html"
    search_fields = ("id",)
    actions = [parse_selected, parse_pages_books]

    def get_queryset(self, request):
        return AudioBooks2.objects.all().using("mysql")

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('add_covers/', self.add_covers),
        ]
        return my_urls + urls

    def add_covers(self, request):
        books = AudioBooks2.objects.all().using("mysql").filter(cover_url__isnull=True)
        for book in books:
            try:
                parser = KnigavuheParser(book.donor_id)
                year = book.year.year if book.year.year else "0000"
                cover = parser.get_cover(year)
                book.cover_url = cover
                book.save()
            except BaseException as e:
                logging.warning(e, timezone.now())
        self.message_user(request, "Covers were updated")
        return HttpResponseRedirect("../")
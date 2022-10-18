# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AudioAudiobooks(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=1000, blank=True, null=True)
    book = models.ForeignKey('AudioBooks', models.DO_NOTHING)
    index = models.PositiveSmallIntegerField()
    link = models.CharField(max_length=1000)
    doparse = models.IntegerField(db_column='doParse')  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    extension = models.CharField(max_length=20, blank=True, null=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)
    duration = models.PositiveIntegerField(blank=True, null=True)
    public_path = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_audiobooks'
        unique_together = (('book', 'index'),)


class AudioAuthors(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=300)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_authors'


class AudioAuthorsLinks(models.Model):
    id = models.BigAutoField(primary_key=True)
    link = models.CharField(unique=True, max_length=300)
    doparse = models.IntegerField(db_column='doParse')  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_authors_links'


class AudioAuthorsToBooks(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(AudioAuthors, models.DO_NOTHING)
    book = models.ForeignKey('AudioBooks', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_authors_to_books'
        unique_together = (('author', 'book'),)


class AudioBookCommentLikes(models.Model):
    audio_book_comment = models.ForeignKey('AudioBookComments', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audio_book_comment_likes'


class AudioBookComments(models.Model):
    id = models.BigAutoField(primary_key=True)
    hidden = models.IntegerField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    audio_book = models.ForeignKey('AudioBooks', models.DO_NOTHING)
    content = models.TextField()
    parent_comment_id = models.PositiveBigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_book_comments'


class AudioBookGenre(models.Model):
    audio_book = models.ForeignKey('AudioBooks', models.DO_NOTHING)
    genre = models.ForeignKey('Genres', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audio_book_genre'


class AudioBookReviewCommentLikes(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    audio_review_comment = models.ForeignKey('AudioBookReviewComments', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audio_book_review_comment_likes'


class AudioBookReviewComments(models.Model):
    id = models.BigAutoField(primary_key=True)
    hidden = models.IntegerField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    audio_book_review = models.ForeignKey('AudioBookReviews', models.DO_NOTHING)
    content = models.TextField()
    parent_comment = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_book_review_comments'


class AudioBookReviewLikes(models.Model):
    audio_book_review = models.ForeignKey('AudioBookReviews', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'audio_book_review_likes'


class AudioBookReviews(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.IntegerField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    audio_book = models.ForeignKey('AudioBooks', models.DO_NOTHING)
    review_type = models.ForeignKey('ReviewTypes', models.DO_NOTHING)
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_book_reviews'


class AudioBookUser(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    audio_book = models.ForeignKey('AudioBooks', models.DO_NOTHING)
    status = models.PositiveIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_book_user'
        unique_together = (('user', 'audio_book'),)


class AudioBooks(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.PositiveIntegerField()
    title = models.CharField(max_length=1000)
    description = models.TextField(blank=True, null=True)
    params = models.JSONField(blank=True, null=True)
    series = models.ForeignKey('AudioSeries', models.DO_NOTHING, blank=True, null=True)
    link = models.OneToOneField('AudioBooksLinks', models.DO_NOTHING, blank=True, null=True)
    year_id = models.PositiveBigIntegerField()
    litres = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    image_name = models.CharField(max_length=64, blank=True, null=True)
    meta_description = models.CharField(max_length=191, blank=True, null=True)
    meta_keywords = models.CharField(max_length=191, blank=True, null=True)
    alias_url = models.CharField(unique=True, max_length=191, blank=True, null=True)
    genre = models.ForeignKey('Genres', models.DO_NOTHING, blank=True, null=True)
    slug = models.CharField(max_length=1000, blank=True, null=True)
    listeners_count = models.PositiveBigIntegerField(blank=True, null=True)
    rate_avg = models.FloatField(blank=True, null=True)
    reviews_count = models.PositiveBigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_books'


class AudioBooksLinks(models.Model):
    id = models.BigAutoField(primary_key=True)
    link = models.CharField(unique=True, max_length=500)
    doparse = models.IntegerField(db_column='doParse')  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_books_links'


class AudioCategoryTabs(models.Model):
    id = models.BigAutoField(primary_key=True)
    show = models.IntegerField()
    genre = models.OneToOneField('Genres', models.DO_NOTHING)
    order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'audio_category_tabs'


class AudioGenres(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=300)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_genres'


class AudioImages(models.Model):
    id = models.BigAutoField(primary_key=True)
    link = models.CharField(max_length=300)
    book = models.ForeignKey(AudioBooks, models.DO_NOTHING)
    doparse = models.IntegerField(db_column='doParse')  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    public_path = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_images'
        unique_together = (('link', 'book'),)


class AudioLetters(models.Model):
    id = models.BigAutoField(primary_key=True)
    link = models.CharField(unique=True, max_length=300)
    doparse = models.IntegerField(db_column='doParse')  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_letters'


class AudioParsingStatuses(models.Model):
    id = models.BigAutoField(primary_key=True)
    site = models.ForeignKey('AudioSites', models.DO_NOTHING)
    status_id = models.IntegerField()
    doparse = models.IntegerField(db_column='doParse')  # Field name made lowercase.
    status = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    min_count = models.PositiveIntegerField()
    max_count = models.PositiveIntegerField()
    last_parsing = models.DateTimeField(blank=True, null=True)
    paused = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'audio_parsing_statuses'
        unique_together = (('site', 'status_id'),)


class AudioReaders(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=300)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_readers'


class AudioReadersToBooks(models.Model):
    id = models.BigAutoField(primary_key=True)
    reader = models.ForeignKey(AudioReaders, models.DO_NOTHING)
    book = models.ForeignKey(AudioBooks, models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_readers_to_books'
        unique_together = (('reader', 'book'),)


class AudioSeries(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=300)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_series'


class AudioSites(models.Model):
    id = models.BigAutoField(primary_key=True)
    site = models.CharField(max_length=100)
    site_url = models.CharField(unique=True, max_length=300)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audio_sites'


class AuthorToBooks(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey('Authors', models.DO_NOTHING)
    book = models.ForeignKey('Books', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'author_to_books'


class Authors(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.CharField(max_length=120)
    avatar = models.CharField(max_length=191, blank=True, null=True)
    about = models.CharField(max_length=191, blank=True, null=True)
    slug = models.CharField(unique=True, max_length=191, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'authors'


class AuthorsToAudioBooks(models.Model):
    id = models.BigAutoField(primary_key=True)
    author = models.ForeignKey(Authors, models.DO_NOTHING)
    book = models.ForeignKey(AudioBooks, models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'authors_to_audio_books'
        unique_together = (('author', 'book'),)


class BannerGenre(models.Model):
    banner = models.ForeignKey('Banners', models.DO_NOTHING)
    genre = models.ForeignKey('Genres', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'banner_genre'


class BannerPageName(models.Model):
    banner = models.ForeignKey('Banners', models.DO_NOTHING)
    page_name = models.ForeignKey('PageNames', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'banner_page_name'


class BannerSitePageName(models.Model):
    banner = models.ForeignKey('Banners', models.DO_NOTHING)
    site_page_name = models.ForeignKey('SitePageNames', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'banner_site_page_name'


class Banners(models.Model):
    id = models.BigAutoField(primary_key=True)
    is_active = models.IntegerField()
    type = models.CharField(max_length=10)
    name = models.CharField(max_length=1000, blank=True, null=True)
    image = models.CharField(max_length=3500, blank=True, null=True)
    alt = models.CharField(max_length=140, blank=True, null=True)
    text = models.CharField(max_length=2000, blank=True, null=True)
    link = models.CharField(max_length=3500)
    content = models.TextField(blank=True, null=True)
    display_params = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'banners'


class BookAnchors(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey('Books', models.DO_NOTHING)
    page_num = models.PositiveSmallIntegerField()
    anchor = models.CharField(max_length=191)
    anchor_index = models.PositiveSmallIntegerField()
    name = models.CharField(max_length=5000)

    class Meta:
        managed = False
        db_table = 'book_anchors'
        unique_together = (('book', 'page_num', 'anchor'),)


class BookAnchorsLinks(models.Model):
    id = models.BigAutoField(primary_key=True)
    link = models.CharField(max_length=120)
    book = models.ForeignKey('Books', models.DO_NOTHING)
    doparse = models.IntegerField(db_column='doParse')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'book_anchors_links'


class BookBookGenre(models.Model):
    book = models.ForeignKey('Books', models.DO_NOTHING)
    book_genre = models.ForeignKey('BookGenres', models.DO_NOTHING)
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'book_book_genre'


class BookCategoryTabs(models.Model):
    id = models.BigAutoField(primary_key=True)
    show = models.IntegerField()
    genre = models.OneToOneField('Genres', models.DO_NOTHING)
    order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'book_category_tabs'


class BookCommentLikes(models.Model):
    book_comment = models.ForeignKey('BookComments', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'book_comment_likes'


class BookComments(models.Model):
    id = models.BigAutoField(primary_key=True)
    hidden = models.IntegerField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    book = models.ForeignKey('Books', models.DO_NOTHING)
    content = models.TextField()
    parent_comment_id = models.PositiveBigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book_comments'


class BookCompilation(models.Model):
    compilation = models.ForeignKey('Compilations', models.DO_NOTHING)
    compilationable_id = models.PositiveBigIntegerField()
    compilationable_type = models.CharField(max_length=191)

    class Meta:
        managed = False
        db_table = 'book_compilation'


class BookGenre(models.Model):
    book = models.ForeignKey('Books', models.DO_NOTHING)
    genre = models.ForeignKey('Genres', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'book_genre'


class BookGenres(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=191)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book_genres'


class BookLikes(models.Model):
    book = models.ForeignKey('Books', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book_likes'


class BookLinks(models.Model):
    id = models.BigAutoField(primary_key=True)
    link = models.CharField(unique=True, max_length=120)
    doparse = models.IntegerField(db_column='doParse')  # Field name made lowercase.
    donor_id = models.PositiveBigIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book_links'


class BookReviewCommentLikes(models.Model):
    book_review_comment = models.ForeignKey('BookReviewComments', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'book_review_comment_likes'


class BookReviewComments(models.Model):
    id = models.BigAutoField(primary_key=True)
    hidden = models.IntegerField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    book_review = models.ForeignKey('BookReviews', models.DO_NOTHING)
    content = models.TextField()
    parent_comment = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book_review_comments'


class BookReviewLikes(models.Model):
    book_review = models.ForeignKey('BookReviews', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'book_review_likes'


class BookReviews(models.Model):
    id = models.BigAutoField(primary_key=True)
    active = models.IntegerField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    book = models.ForeignKey('Books', models.DO_NOTHING)
    review_type = models.ForeignKey('ReviewTypes', models.DO_NOTHING)
    title = models.CharField(max_length=150)
    content = models.TextField()
    parent_review_id = models.PositiveBigIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book_reviews'


class BookTranslator(models.Model):
    book = models.ForeignKey('Books', models.DO_NOTHING)
    translator = models.ForeignKey('Translators', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'book_translator'


class BookUser(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    book = models.ForeignKey('Books', models.DO_NOTHING)
    status = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'book_user'
        unique_together = (('book', 'user'),)


class Bookmarks(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey('Books', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    page = models.ForeignKey('Pages', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'bookmarks'


class Books(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=1000)
    text = models.TextField()
    series = models.ForeignKey('Series', models.DO_NOTHING, blank=True, null=True)
    year = models.ForeignKey('Years', models.DO_NOTHING, blank=True, null=True)
    params = models.JSONField()
    active = models.IntegerField()
    donor_id = models.PositiveBigIntegerField(unique=True, blank=True, null=True)
    count_pages = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    alias_url = models.CharField(unique=True, max_length=191, blank=True, null=True)
    readers_count = models.PositiveBigIntegerField(blank=True, null=True)
    rate_avg = models.FloatField(blank=True, null=True)
    reviews_count = models.PositiveBigIntegerField(blank=True, null=True)
    slug = models.CharField(unique=True, max_length=191, blank=True, null=True)
    cover_url = models.CharField(max_length=255, blank=True, null=True)
    seo_title = models.CharField(max_length=120, blank=True, null=True)
    seo_description = models.CharField(max_length=240, blank=True, null=True)
    seo_keywords = models.CharField(max_length=300, blank=True, null=True)
    og_title = models.CharField(max_length=120, blank=True, null=True)
    og_description = models.CharField(max_length=240, blank=True, null=True)
    og_img = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'books'

    def __str__(self):
        return f"{self.id}"


class Chapters(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Books, models.DO_NOTHING)
    page = models.ForeignKey('Pages', models.DO_NOTHING)
    title = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chapters'


class ClaimForms(models.Model):
    id = models.BigAutoField(primary_key=True)
    subject = models.CharField(max_length=191)
    link_source = models.CharField(max_length=191)
    link_content = models.CharField(max_length=191)
    name = models.CharField(max_length=191)
    email = models.CharField(max_length=191)
    agreement = models.IntegerField()
    copyright_holder = models.IntegerField()
    interaction = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'claim_forms'


class CommentLikes(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    comment = models.ForeignKey('Comments', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'comment_likes'


class Comments(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'


class CompilationType(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=191)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'compilation_type'


class CompilationUser(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    compilation = models.ForeignKey('Compilations', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'compilation_user'


class Compilations(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    background = models.CharField(max_length=255)
    description = models.CharField(max_length=10000)
    created_by = models.ForeignKey('Users', models.DO_NOTHING, db_column='created_by')
    type = models.ForeignKey(CompilationType, models.DO_NOTHING, blank=True, null=True)
    location = models.IntegerField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    slug = models.CharField(unique=True, max_length=191, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'compilations'


class DefaultOrderSettings(models.Model):
    id = models.BigAutoField(primary_key=True)
    page_name = models.ForeignKey('PageNames', models.DO_NOTHING)
    sort_by = models.IntegerField()
    order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'default_order_settings'
        unique_together = (('page_name', 'sort_by'),)


class DefaultReaderSettings(models.Model):
    setting = models.CharField(unique=True, max_length=191)
    value = models.CharField(max_length=191)

    class Meta:
        managed = False
        db_table = 'default_reader_settings'


class Duplicates(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Books, models.DO_NOTHING, blank=True, null=True)
    fixed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'duplicates'


class Errors(models.Model):
    id = models.BigAutoField(primary_key=True)
    site_id = models.IntegerField()
    url = models.CharField(db_column='Url', max_length=300)  # Field name made lowercase.
    body = models.JSONField()
    proxy_ip = models.CharField(max_length=30)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'errors'


class FailedJobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=191)
    connection = models.TextField()
    queue = models.TextField()
    payload = models.TextField()
    exception = models.TextField()
    failed_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'failed_jobs'


class FeedbackFormAttachments(models.Model):
    id = models.BigAutoField(primary_key=True)
    feedback_form = models.ForeignKey('FeedbackForms', models.DO_NOTHING)
    file_name = models.CharField(max_length=191)
    storage_path = models.CharField(max_length=191)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback_form_attachments'


class FeedbackForms(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=191)
    email = models.CharField(max_length=191)
    subject = models.CharField(max_length=191)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback_forms'


class Genres(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=300)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    is_hidden = models.IntegerField()
    description = models.CharField(max_length=5000, blank=True, null=True)
    slug = models.CharField(unique=True, max_length=191, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'genres'


class HeaderMenus(models.Model):
    id = models.BigAutoField(primary_key=True)
    show = models.IntegerField()
    order = models.IntegerField()
    name = models.CharField(max_length=20)
    icon = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=200)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'header_menus'


class IdSocialNetworks(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField('Users', models.DO_NOTHING)
    yandex_id = models.PositiveBigIntegerField(blank=True, null=True)
    google_id = models.PositiveBigIntegerField(blank=True, null=True)
    vkontakte_id = models.PositiveBigIntegerField(blank=True, null=True)
    odnoklassniki_id = models.PositiveBigIntegerField(blank=True, null=True)
    temp_token = models.CharField(unique=True, max_length=191, blank=True, null=True)
    token_valid_until = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'id_social_networks'


class Images(models.Model):
    id = models.BigAutoField(primary_key=True)
    page = models.ForeignKey('Pages', models.DO_NOTHING, blank=True, null=True)
    book = models.ForeignKey(Books, models.DO_NOTHING, blank=True, null=True)
    link = models.CharField(max_length=256)
    doparse = models.IntegerField(db_column='doParse')  # Field name made lowercase.
    public_path = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'images'
        unique_together = (('link', 'book'),)


class Jobs(models.Model):
    id = models.BigAutoField(primary_key=True)
    queue = models.CharField(max_length=191)
    payload = models.TextField()
    attempts = models.PositiveIntegerField()
    reserved_at = models.PositiveIntegerField(blank=True, null=True)
    available_at = models.PositiveIntegerField()
    created_at = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'jobs'


class Likes(models.Model):
    id = models.BigAutoField(primary_key=True)
    like_type = models.CharField(max_length=191)
    like_id = models.PositiveBigIntegerField()
    user = models.ForeignKey('Users', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'likes'


class Migrations(models.Model):
    migration = models.CharField(max_length=191)
    batch = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'migrations'


class Modulables(models.Model):
    module = models.ForeignKey('Modules', models.DO_NOTHING)
    modulable_id = models.PositiveBigIntegerField()
    modulable_type = models.CharField(max_length=100)
    order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'modulables'
        unique_together = (('module', 'modulable_id', 'modulable_type'),)


class ModulePageName(models.Model):
    module = models.ForeignKey('Modules', models.DO_NOTHING)
    page_name = models.ForeignKey('PageNames', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'module_page_name'


class Modules(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=100)
    slug = models.CharField(max_length=100)
    module_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'modules'


class NotificationUser(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    notification = models.ForeignKey('Notifications', models.DO_NOTHING)
    read = models.IntegerField()
    type = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'notification_user'


class Notifications(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    notificationable_type = models.CharField(max_length=191)
    notificationable_id = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'


class OauthAccessTokens(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    user_id = models.PositiveBigIntegerField(blank=True, null=True)
    client_id = models.PositiveBigIntegerField()
    name = models.CharField(max_length=191, blank=True, null=True)
    scopes = models.TextField(blank=True, null=True)
    revoked = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_access_tokens'


class OauthAuthCodes(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    user_id = models.PositiveBigIntegerField()
    client_id = models.PositiveBigIntegerField()
    scopes = models.TextField(blank=True, null=True)
    revoked = models.IntegerField()
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_auth_codes'


class OauthClients(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.PositiveBigIntegerField(blank=True, null=True)
    name = models.CharField(max_length=191)
    secret = models.CharField(max_length=100, blank=True, null=True)
    provider = models.CharField(max_length=191, blank=True, null=True)
    redirect = models.TextField()
    personal_access_client = models.IntegerField()
    password_client = models.IntegerField()
    revoked = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_clients'


class OauthPersonalAccessClients(models.Model):
    id = models.BigAutoField(primary_key=True)
    client_id = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_personal_access_clients'


class OauthRefreshTokens(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    access_token_id = models.CharField(max_length=100)
    revoked = models.IntegerField()
    expires_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'oauth_refresh_tokens'


class Options(models.Model):
    id = models.BigAutoField(primary_key=True)
    parameter = models.CharField(max_length=60)
    value = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'options'


class PageLinks(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Books, models.DO_NOTHING)
    link = models.CharField(unique=True, max_length=120)
    doparse = models.IntegerField(db_column='doParse')  # Field name made lowercase.
    page_num = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'page_links'


class PageNames(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.CharField(max_length=100)
    meta_title = models.CharField(max_length=500, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keyword = models.TextField(blank=True, null=True)
    og_title = models.TextField(blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    og_image = models.CharField(max_length=191, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'page_names'


class Pages(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Books, models.DO_NOTHING)
    link = models.CharField(max_length=120)
    content = models.TextField()
    page_number = models.IntegerField()
    fixed = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pages'
        unique_together = (('book', 'page_number'),)


class ParsingStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    site_id = models.IntegerField()
    progress = models.IntegerField(db_column='Progress', blank=True, null=True)  # Field name made lowercase.
    count = models.IntegerField(db_column='Count', blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status', blank=True, null=True)  # Field name made lowercase.
    last_parsing = models.DateTimeField(blank=True, null=True)
    parse_type = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'parsing_status'


class PasswordResets(models.Model):
    email = models.CharField(max_length=191)
    token = models.CharField(max_length=191)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'password_resets'


class Proxies(models.Model):
    id = models.BigAutoField(primary_key=True)
    proxy = models.CharField(max_length=20)
    blocked = models.IntegerField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'proxies'


class PublisherToBooks(models.Model):
    id = models.BigAutoField(primary_key=True)
    publisher = models.ForeignKey('Publishers', models.DO_NOTHING)
    book = models.ForeignKey(Books, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'publisher_to_books'


class Publishers(models.Model):
    id = models.BigAutoField(primary_key=True)
    publisher = models.CharField(max_length=120)

    class Meta:
        managed = False
        db_table = 'publishers'


class QuoteLikes(models.Model):
    quote = models.ForeignKey('Quotes', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'quote_likes'


class Quotes(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    book = models.ForeignKey(Books, models.DO_NOTHING)
    page_id = models.IntegerField()
    text = models.CharField(max_length=1000)
    color = models.CharField(max_length=10, blank=True, null=True)
    start_key = models.CharField(max_length=191)
    start_offset = models.PositiveIntegerField()
    end_key = models.CharField(max_length=191)
    end_offset = models.PositiveIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'quotes'


class Rates(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Books, models.DO_NOTHING, blank=True, null=True)
    audio_book = models.ForeignKey(AudioBooks, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    rating = models.FloatField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rates'
        unique_together = (('audio_book', 'user'), ('book', 'user'),)


class ReadingSettings(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    is_two_columns = models.IntegerField()
    font_size = models.PositiveIntegerField()
    screen_brightness = models.PositiveIntegerField()
    font_name = models.CharField(max_length=191)
    field_size = models.PositiveIntegerField()
    row_height = models.PositiveIntegerField()
    is_center_alignment = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reading_settings'


class ReadingStatuses(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    book = models.ForeignKey(Books, models.DO_NOTHING)
    page_number = models.PositiveBigIntegerField()
    reading_progress = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reading_statuses'


class ReviewTypes(models.Model):
    id = models.BigAutoField(primary_key=True)
    type = models.CharField(max_length=191)

    class Meta:
        managed = False
        db_table = 'review_types'


class Seos(models.Model):
    id = models.BigAutoField(primary_key=True)
    meta_title = models.TextField(blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    meta_keyword = models.TextField(blank=True, null=True)
    og_title = models.TextField(blank=True, null=True)
    og_description = models.TextField(blank=True, null=True)
    seoable_type = models.CharField(max_length=191)
    seoable_id = models.PositiveBigIntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seos'
        unique_together = (('seoable_type', 'seoable_id'),)


class Series(models.Model):
    id = models.BigAutoField(primary_key=True)
    series = models.CharField(max_length=120)
    slug = models.CharField(unique=True, max_length=191, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'series'


class SidebarItems(models.Model):
    id = models.BigAutoField(primary_key=True)
    show = models.IntegerField()
    genre = models.OneToOneField(Genres, models.DO_NOTHING)
    order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sidebar_items'


class SimilarAuthors(models.Model):
    author_id_from = models.PositiveBigIntegerField()
    author_id_to = models.PositiveBigIntegerField()

    class Meta:
        managed = False
        db_table = 'similar_authors'


class SitePageNames(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=1000)
    slug = models.CharField(max_length=1000)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'site_page_names'


class Sites(models.Model):
    id = models.BigAutoField(primary_key=True)
    site = models.CharField(max_length=100)
    site_url = models.CharField(max_length=300)
    doparselinks = models.IntegerField(db_column='doParseLinks')  # Field name made lowercase.
    doparsebooks = models.IntegerField(db_column='doParseBooks')  # Field name made lowercase.
    doparsepages = models.IntegerField(db_column='doParsePages')  # Field name made lowercase.
    doparseimages = models.IntegerField(db_column='doParseImages')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'sites'


class TelescopeEntries(models.Model):
    sequence = models.BigAutoField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=36)
    batch_id = models.CharField(max_length=36)
    family_hash = models.CharField(max_length=191, blank=True, null=True)
    should_display_on_index = models.IntegerField()
    type = models.CharField(max_length=20)
    content = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'telescope_entries'


class TelescopeEntriesTags(models.Model):
    entry_uuid = models.ForeignKey(TelescopeEntries, models.DO_NOTHING, db_column='entry_uuid')
    tag = models.CharField(max_length=191)

    class Meta:
        managed = False
        db_table = 'telescope_entries_tags'


class TelescopeMonitoring(models.Model):
    tag = models.CharField(max_length=191)

    class Meta:
        managed = False
        db_table = 'telescope_monitoring'


class Translators(models.Model):
    name = models.CharField(unique=True, max_length=50)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'translators'


class UserAuthor(models.Model):
    author = models.ForeignKey(Authors, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_author'


class UserSettings(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField('Users', models.DO_NOTHING)
    likes = models.IntegerField()
    commented = models.IntegerField()
    commentedothers = models.IntegerField(db_column='commentedOthers')  # Field name made lowercase.
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_settings'


class Users(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(unique=True, max_length=191, blank=True, null=True)
    is_admin = models.IntegerField()
    email_verified_at = models.DateTimeField(blank=True, null=True)
    password = models.CharField(max_length=191, blank=True, null=True)
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    verify_token = models.CharField(unique=True, max_length=191, blank=True, null=True)
    surname = models.CharField(max_length=191, blank=True, null=True)
    avatar = models.CharField(max_length=191, blank=True, null=True)
    nickname = models.CharField(unique=True, max_length=191, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)
    is_blocked_for_comments = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'users'


class UsersRecommended(models.Model):
    id = models.BigAutoField(primary_key=True)
    book = models.ForeignKey(Books, models.DO_NOTHING, blank=True, null=True)
    audio_book = models.ForeignKey(AudioBooks, models.DO_NOTHING, blank=True, null=True)
    content = models.CharField(max_length=250)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_recommended'


class Views(models.Model):
    user = models.ForeignKey(Users, models.DO_NOTHING, blank=True, null=True)
    ip_address = models.CharField(max_length=191, blank=True, null=True)
    viewable_id = models.PositiveBigIntegerField()
    viewable_type = models.CharField(max_length=191)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'views'


class Years(models.Model):
    id = models.BigAutoField(primary_key=True)
    year = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = 'years'

    def __str__(self):
        return self.year
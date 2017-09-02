# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from DouBanBook.items import DouBanBookCategoryItem, DouBanBookTagsItem, DouBanBookCommentItem
from DouBanBook.settings import MYSQL_HOST, MYSQL_PORT, MYSQL_USR, MYSQL_PWD, MYSQL_DB, MYSQL_CHARSET

class DouBanBookPipeline(object):

    def __init__(self):
        self.conn = pymysql.connect(
            host    =   MYSQL_HOST,
            port    =   MYSQL_PORT,
            user    =   MYSQL_USR,
            passwd  =   MYSQL_PWD,
            db      =   MYSQL_DB,
            charset = MYSQL_CHARSET,
        )
        self.insert_categories = "insert into categories(category, tag, url, num) values('%s', '%s', '%s', '%s')"
        self.insert_books = "insert into books(tag, title, book_id, book_url, author, author_url, publish_company, subtitle, original_name, translator, translator_url, publish_year, pages, price, binding, series, series_url, ISBN, comment_score, comment_quantity, summary) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
        self.insert_comments = "insert into comments(title, book_id, comment_score, comment_quantity, recommend_strongly, recommend, just_so_so, a_little_bad, so_bad, already_read, reading_now, wish_read) values('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"

    def process_item(self, item, spider):
        self.cur = self.conn.cursor()
        if isinstance(item, DouBanBookCategoryItem):
            try:
                self.cur.execute(self.insert_categories % (item['category'], item['tag'], item['url'], item['num']))
                self.conn.commit()
            except Exception as e:
                print e
                self.conn.rollback()
        elif isinstance(item, DouBanBookTagsItem):
            try:
                self.cur.execute(self.insert_books % (item['tag'], item['title'], item['book_id'], item['book_url'], item['author'], item['author_url'], item['publish_company'], item['subtitle'], item['original_name'], item['translator'], item['translator_url'], item['publish_year'], item['pages'], item['price'], item['binding'], item['series'], item['series_url'], item['ISBN'], item['comment_score'], item['comment_quantity'], item['summary']))
                self.conn.commit()
            except Exception as e:
                print e
                self.conn.rollback()
        elif isinstance(item, DouBanBookCommentItem):
            try:
                self.cur.execute(self.insert_comments % (item['title'], item['book_id'], item['comment_score'], item['comment_quantity'], item['recommend_strongly'], item['recommend'], item['just_so_so'], item['a_little_bad'], item['so_bad'], item['already_read'], item['reading_now'], item['wish_read']))
                self.conn.commit()
            except Exception as e:
                print e
                self.conn.rollback()
        return item

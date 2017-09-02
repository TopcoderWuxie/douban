# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class DouBanBookCategoryItem(scrapy.Item):
    category = scrapy.Field()           # 分类
    tag = scrapy.Field()                # 标签
    url = scrapy.Field()                # 每个标签的连接
    num = scrapy.Field()                # 数量

class DouBanBookTagsItem(scrapy.Item):
    tag = scrapy.Field()                # 所属标签
    title = scrapy.Field()              # 书名
    book_id = scrapy.Field()            # 书籍ID
    book_url = scrapy.Field()           # 书籍链接
    author = scrapy.Field()             # 作者
    author_url = scrapy.Field()         # 作者url
    publish_company = scrapy.Field()    # 出版社
    subtitle = scrapy.Field()           # 副标题
    original_name = scrapy.Field()      # 原作名
    translator = scrapy.Field()         # 译者
    translator_url = scrapy.Field()     # 译者url
    publish_year = scrapy.Field()       # 出版年
    pages = scrapy.Field()              # 页数
    price = scrapy.Field()              # 定价
    binding = scrapy.Field()            # 装帧
    series = scrapy.Field()             # 丛书
    series_url = scrapy.Field()         # 丛书url
    ISBN = scrapy.Field()               # ISBN
    comment_score = scrapy.Field()      # 评分
    comment_quantity = scrapy.Field()   # 评论数量
    summary = scrapy.Field()            # 简介

class DouBanBookCommentItem(scrapy.Item):
    title = scrapy.Field()              # 书名
    book_id = scrapy.Field()            # 书籍ID
    comment_score = scrapy.Field()      # 评分
    comment_quantity = scrapy.Field()   # 评论数量
    recommend_strongly = scrapy.Field() # 力荐
    recommend = scrapy.Field()          # 推荐
    just_so_so = scrapy.Field()         # 还行
    a_little_bad = scrapy.Field()       # 有点差
    so_bad = scrapy.Field()             # 很差
    already_read = scrapy.Field()       # 已读
    reading_now = scrapy.Field()        # 在读
    wish_read = scrapy.Field()          # 想读
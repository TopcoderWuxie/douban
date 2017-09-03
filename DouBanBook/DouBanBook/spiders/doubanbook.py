# -*- coding: utf-8 -*-

import copy
import scrapy
from DouBanBook.items import DouBanBookCategoryItem, DouBanBookTagsItem, DouBanBookCommentItem

class DoubanbookSpider(scrapy.Spider):
    name = "doubanbook"
    allowed_domains = ["book.douban.com"]

    def start_requests(self):
        url = "https://book.douban.com/tag/?view=type&icn=index-sorttags-all"
        yield scrapy.Request(url, callback= self.parse, dont_filter= True)

    def parse(self, response):
        for resp in response.xpath("//div[@class='article']/div")[-1].xpath(".//div"):
            category = resp.xpath(".//a/h2/text()").extract_first().replace(u"·", "").replace(u" ", "")
            for td in resp.xpath(".//table/tbody/tr/td"):
                url = td.xpath(".//a/@href").extract_first()
                url = None if url is None else response.urljoin(url)
                tag = td.xpath(".//a/text()").extract_first()
                num = td.xpath(".//b/text()").extract_first().replace(u"(", "").replace(u")", "")

                item = DouBanBookCategoryItem()
                item['category'], item['tag'], item['num'], item['url'] = category, tag, num, url
                yield item

                yield scrapy.Request(url, callback= self.parse_tag, meta = {'tag': tag},  dont_filter= True)

    def parse_tag(self, response):
        tag = response.meta['tag']
        resp = response.xpath("//div[@class='article']/div[@id='subject_list']/ul[@class = 'subject-list']/li")
        if len(resp) != 0:
            for data in resp:
                title = data.xpath(".//div[@class='info']/h2/a/text()").extract_first().strip()
                book_url = data.xpath(".//div[@class='info']/h2/a/@href").extract_first()
                book_id = book_url.split("/")[-2]
                # 评论很少的时候不存在评分
                comment_score = data.xpath(".//div[@class='star clearfix']/span[@class='rating_nums']/text()").extract_first()
                comment_score = comment_score.strip() if comment_score != None else None
                comment_quantity = data.xpath(".//div[@class='star clearfix']/span[@class='pl']/text()").extract_first().strip().replace(u"(", "").replace(u")", "")
                item = DouBanBookTagsItem()
                item['tag'], item['title'], item['book_id'], item['book_url'], item['comment_score'], item['comment_quantity'] = tag, title, book_id, book_url, comment_score, comment_quantity
                response.meta['item'] = item
                yield scrapy.Request(book_url, callback= self.parse_book, meta= copy.deepcopy(response.meta), dont_filter= True)

        next_page_url = response.xpath("//div[@class='paginator']/span[@class='next']/a/@href").extract_first()
        next_page_url = response.urljoin(next_page_url) if next_page_url != None else None
        if next_page_url:
            yield scrapy.Request(next_page_url, callback= self.parse_tag, meta= {'tag' : tag}, dont_filter= True)

    def parse_book(self, response):
        item = response.meta['item']
        datas = []
        for resp in response.xpath("//div[@class='subject clearfix']/div[@id='info']//text()").extract():
            data = resp.replace(u":", "").strip()
            if len(data) != 0:
                datas.append(data)
        item = book_info(item, datas)

        author_url, translator_url, series_url = [], [], []
        urls = response.xpath("//div[@class='subject clearfix']/div[@id='info']//a/@href").extract()
        for url in urls:
            if url.find("search") != -1:
                translator_url.append(response.urljoin(url))
            elif url.find("author") != -1:
                author_url.append(url)
            elif url.find("series") != -1:
                series_url.append(url)

        item['author_url'] = "|".join(author_url) if len(author_url) != 0 else None
        item['translator_url'] = "|".join(translator_url) if len(translator_url) != 0 else None
        item['series_url'] = "|".join(series_url) if len(series_url) != 0 else None

        comment_summary = response.xpath("//div[@class='related_info']/div[@id='link-report']/div/div[@class='intro']")
        if len(comment_summary) == 0:
            comment_summary = "\n".join([resp.strip() for resp in response.xpath("//div[@id='link-report']/span[@class='all hidden']/div/div[@class='intro']//p/text()").extract() if resp.strip() != 0])
        else:
            comment_summary = "\n".join([r.strip() for r in comment_summary.xpath(".//p//text()").extract() if r.strip() != 0])
        # if len(comment_summary) != 0:
        #     comment_summary = u"内 容 简 介  · · · · · ·\n" + comment_summary
        # else:
        #     comment_summary = ""
        comment_summary = u"\n内容简介  · · · · · ·\n" + comment_summary if len(comment_summary) != 0 else ""

        author_summary = response.xpath("//div[@class='related_info']/div[@class='indent ']/div/div[@class='intro']//p/text()").extract()
        if len(author_summary) != 0:
            author_summary = u"\n作 者 简 介  · · · · · ·\n" + "\n".join([resp.strip() for resp in author_summary if resp.strip() != 0])
        else:
            author_summary = ""

        s = "//div[@class=\'related_info\']/div[@id=\'dir_%s_full\']/text()"
        s = s % item['book_id']
        catalog_summary = response.xpath(s).extract()
        # if len(catalog_summary) != 0:
        #     catalog_summary = u"目 录  · · · · · ·\n" + "\n".join([resp.strip() for resp in catalog_summary if resp.strip() != 0])
        # else:
        #     catalog_summary = ""
        catalog_summary = u"\n目录  · · · · · ·\n" + "\n".join([resp.strip() for resp in catalog_summary if resp.strip() != 0]) if len(catalog_summary) != 0 else ""

        summary = comment_summary + author_summary + catalog_summary
        item['summary'] = summary.replace(u"(\n)", "")

        yield item

        url = response.xpath("//div[@class='rating_sum']/span/a/@href").extract_first()
        yield scrapy.Request(response.urljoin(url), callback= self.parse_comment, meta= {'tag' : item['tag'], 'title' : item['title'], 'book_id' : item['book_id'], 'comment_score' : item['comment_score'], 'comment_quantity' : item['comment_quantity']}, dont_filter= True)

    def parse_comment(self, response):
        item = DouBanBookCommentItem()
        item['tag'], item['title'], item['book_id'], item['comment_score'], item['comment_quantity'] = response.meta['tag'], response.meta['title'], response.meta['book_id'], response.meta['comment_score'], response.meta['comment_quantity']

        types = response.xpath("//div[@class='rating_detail_wrap clearfix']/div[@class='rating_detail_star']/text()").extract()
        datas = [t.strip() for t in types if len(t.strip()) != 0]
        recommend_strongly, recommend, just_so_so, a_little_bad, so_bad = datas
        resp = response.xpath("//div[@class='zbar clearfix']/div/span")
        already_read = resp[0].xpath(".//span/text()").extract_first().strip()
        reading_now = resp[1].xpath(".//span/a/text()").extract_first()
        wish_read = resp[2].xpath(".//span/a/text()").extract_first()
        item['recommend_strongly'], item['recommend'], item['just_so_so'], item['a_little_bad'], item['so_bad'], item['already_read'], item['reading_now'], item['wish_read'] = recommend_strongly, recommend, just_so_so, a_little_bad, so_bad, already_read, reading_now, wish_read

        yield item

def book_info(item, datas):
    item['author'] = item["publish_company"] = item["subtitle"] = item['original_name'] = item['translator'] = item["publish_year"] = item['pages'] = item['price'] = item['binding'] = item['series'] = item['ISBN'] = None
    for x in range(0, len(datas), 2):
        if datas[x] == u"作者":
            item['author'] = datas[x + 1]
        elif datas[x] == u"出版社":
            item["publish_company"] = datas[x + 1]
        elif datas[x] == u"副标题":
            item["subtitle"] = datas[x + 1]
        elif datas[x] == u"原作名":
            item['original_name'] = datas[x + 1]
        elif datas[x] == u"译者":
            item['translator'] = datas[x + 1]
        elif datas[x] == u"出版年":
            item["publish_year"] = datas[x + 1]
        elif datas[x] == u"页数":
            item['pages'] = datas[x + 1]
        elif datas[x] == u"定价":
            item['price'] = datas[x + 1]
        elif datas[x] == u"装帧":
            item['binding'] = datas[x + 1]
        elif datas[x] == u"丛书":
            item['series'] = datas[x + 1]
        elif datas[x] == u"ISBN":
            item['ISBN'] = datas[x + 1]

    return item

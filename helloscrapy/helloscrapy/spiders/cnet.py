# coding: utf-8
from datetime import datetime

import scrapy
import re

# SitemapSpiderを継承する
class CNETSpider(scrapy.spiders.SitemapSpider):
    name = "cnet"
    allowed_domains = ["ja.scp-wiki.net"]
    sitemap_urls = (
        # ここにはrobots.txtのURLを指定してもよいが、
        # 無関係なサイトマップが多くあるので、今回はサイトマップのURLを直接指定する。
        'http://ja.scp-wiki.net/sitemap_page_1.xml',
    )
    sitemap_rules = (
        # 正規表現 '/news/' にマッチするページをparse_news()メソッドでパースする
        #(r'/scp-[0-9]+$', 'parse_news'),
        #(r'/scp-[0-9]+-jp$', 'parse_news'),
        (r'/scp-2521$', 'parse_news'),
        (r'/scp-055$', 'parse_news'),
    )

    def parse_news(self, response):
        try:
            page_content = ''.join(response.css('#page-content ::text').extract())
            item_no = re.search('アイテム番号:.*\n?', page_content)\
                .group(0).split(':')[1].strip()
            object_class = re.search('オブジェクトクラス:.*\n?', page_content)\
                .group(0).split(':')[1].strip()
            protocol = re.search('特別収容プロトコル:(\n|.)*説明:?', page_content)\
                .group(0).split(':')[1].strip().replace('\n説明', '').replace('\n', '')
            description = re.search('説明:(\n|.)*', page_content)\
                .group(0).strip().replace('\n', '')

            yield {
                # h1要素の文字列を取得する
                'item_no': item_no,
                'object_class': object_class,
                'protocol': protocol,
                'description': description,
                # div[itemprop="articleBody"]の直下のp要素以下にある全要素から文字列を取得して結合する
                #'body': ''.join(response.css('div[itemprop="articleBody"] > p ::text').extract()),
            }
        except AttributeError:
            pass

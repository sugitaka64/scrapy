#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""get scp."""

import re
import scrapy

class GetScpSpider(scrapy.spiders.SitemapSpider):
    """scp spider."""

    name = 'get_scp'
    allowed_domains = ['ja.scp-wiki.net']

    # design sitemap.xml
    sitemap_urls = (
        'http://ja.scp-wiki.net/sitemap_page_1.xml',
    )
    sitemap_rules = (
        # (r'/scp-[0-9]+$', 'parse_scp'),
        # (r'/scp-[0-9]+-jp$', 'parse_scp'),
        (r'/scp-2521$', 'parse_scp'),
        (r'/scp-055$', 'parse_scp'),
    )

    def parse_scp(self, response):
        """parse scp."""
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
                'item_no': item_no,
                'object_class': object_class,
                'protocol': protocol,
                'description': description,
            }
        except AttributeError:
            pass

#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

import pywikibot
from pywikibot import config

from utils import (
    SITE_NAMES,
    create_links_string,
    read_log,
    generate_list_page,
)


def main():
    site = pywikibot.Site()
    for site_name in SITE_NAMES:
        page_name, site_regexp, list_page = generate_list_page(site, site_name)

        good_pages = set(re.findall(r"\[\[(.+?)\]\]", list_page.text))
        bad_pages_count = int(re.findall(r"Текущее количество: (\d+)", list_page.text)[0])
        read_pages_count = 0

        for page in site.search("insource:\"{}\"".format(site_name), [0], content=True):
            if page.title() in good_pages:
                continue
            links = [link for link in re.findall(site_regexp, page.text, flags=re.I)]

            if links:
                bad_pages_count += 1
                links_string = create_links_string(links, page)
                list_page.text = list_page.text + config.line_separator + links_string[:-1:]
            read_pages_count += 1
            read_log(read_pages_count)

        list_page.text = re.sub(r"Текущее количество: (\d+)", r"Текущее количество: {}".format(bad_pages_count),
                                list_page.text)
        list_page.save(u"обновление списка")


if __name__ == "__main__":
    main()

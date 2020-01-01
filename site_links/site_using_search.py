#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
import re
import pywikibot
from pywikibot import config
from pywikibot import output

REGEXP = r"(https?://(?:www\.)?{}.*?)/?[\s|}}\]#<>]"
SITE_NAMES = [
    "headbanger.ru",
    "mastersland.com",
]


def main():
    site = pywikibot.Site()
    for site_name in SITE_NAMES:
        page_name = site_name[0].upper() + site_name[1:]
        site_regexp = REGEXP.format(site_name.replace(".", "\."))

        #list_page = pywikibot.Page(site, u"Проект:Музыка/Неавторитетные источники/{}".format(page_name))
        list_page = pywikibot.Page(site, u"Участник:NPBot/Черновик")
        good_pages = set(re.findall(r"\[\[(.+?)\]\]", list_page.text))
        bad_pages_count = int(re.findall(r"Текущее количество: (\d+)", list_page.text)[0])
        read_pages_count = 0

        for page in site.search("insource:\"{}\"".format(site_name), [0], content=True):
            if page.title() in good_pages:
                continue
            links = [link for link in re.findall(site_regexp, page.text, flags=re.I)]
            if links:
                bad_pages_count += 1
                clink = Counter(links)
                new_string = "# [[{}]]: ".format(page.title())
                for link in sorted(clink.most_common()):
                    new_string += "[{}] ".format(link[0])
                    if link[1] > 1:
                        new_string += "(x{}) ".format(link[1])
                list_page.text = list_page.text + config.line_separator + new_string[:-1:]

            read_pages_count += 1
            if read_pages_count % 50 == 0:
                output("%i pages read..." % read_pages_count)

        list_page.text = re.sub(r"Текущее количество: (\d+)", r"Текущее количество: {}".format(bad_pages_count),
                                list_page.text)
        list_page.save(u"обновление списка")


if __name__ == "__main__":
    main()

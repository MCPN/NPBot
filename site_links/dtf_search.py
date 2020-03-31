#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from urllib.request import urlopen

import pywikibot

from utils import (
    create_links_string,
    read_log,
)

REGEXP = r"(https?://(?:www\.)?dtf\.ru/games/.+?)/?[\s|}\]#<>]"


def check_user(link):
    try:
        return "<span class=\"content-editorial-tick\">" not in urlopen(link).read().decode("utf-8")
    except:
        return False


def main():
    site = pywikibot.Site()
    dtf = pywikibot.Page(site, u"Проект:Компьютерные игры/Списки/Пользовательские обзоры DTF")
    good_pages = set(re.findall(r"\[\[(.+?)\]\]", dtf.text))
    bad_pages_count = int(re.findall(r"Текущее количество: (\d+)", dtf.text)[0])
    read_pages_count = 0

    for page in site.search("insource:\"dtf.ru/games/\"", [0], content=True):
        if page.title() in good_pages:
            continue
        links = [re.sub(r"http://", "https://", link) for link in re.findall(REGEXP, page.text, flags=re.I)
                 if check_user(link)]

        if links:
            bad_pages_count += 1
            links_string = create_links_string(links, page)
            dtf.text = dtf.text + '\n' + links_string[:-1:]
        read_pages_count += 1
        read_log(read_pages_count)

    dtf.text = re.sub(r"Текущее количество: (\d+)", r"Текущее количество: {}".format(bad_pages_count), dtf.text)
    dtf.save(u"обновление списка")


if __name__ == "__main__":
    main()

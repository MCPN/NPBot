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
    dtf.text = dtf.text + '\n'
    bad_pages_count = int(re.findall(r"Текущее количество: (\d+)", dtf.text)[0])
    read_pages_count = 0

    for string in dtf.text.split("\n"):
        if not string or string[0] != "#":
            continue
        title = re.findall(r"\[\[(.+?)\]\]", string)[0]
        page = pywikibot.Page(site, u"{}".format(title))
        links = [re.sub(r"http://", "https://", link) for link in re.findall(REGEXP, page.text, flags=re.I)
                 if check_user(link)]

        if not links:
            dtf.text = dtf.text.replace("{}\n".format(string), "")
            bad_pages_count -= 1
        else:
            links_string = create_links_string(links, page)
            dtf.text = dtf.text.replace(string, links_string[:-1:])
        read_pages_count += 1
        read_log(read_pages_count, modulo=10)

    dtf.text = re.sub(r"Текущее количество: (\d+)", r"Текущее количество: {}".format(bad_pages_count), dtf.text)
    dtf.save(u"обновление ссылок")


if __name__ == "__main__":
    main()

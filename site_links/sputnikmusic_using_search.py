#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from urllib.request import urlopen

import pywikibot
from pywikibot import config

from utils import (
    create_links_string,
    read_log,
)

REGEXP = r"(https?://(?:www\.)?sputnikmusic\.com/(?:review/|album\.php).+?)/?[\s|}\]#<>]"


def check_user(link):
    try:
        return "<font size=1 face=Arial class=brighttext>USER</font>" in urlopen(link).read().decode("iso-8859-1")
    except:
        return False
    

def main():
    site = pywikibot.Site()
    sputnik = pywikibot.Page(site, u"Проект:Музыка/Неавторитетные источники/Sputnikmusic")
    whitelist = pywikibot.Page(site, u"Проект:Музыка/Неавторитетные источники/Sputnikmusic/Whitelist")
    good_links = set(whitelist.text.split())
    good_pages = set(re.findall(r"\[\[(.+?)\]\]", sputnik.text))
    bad_pages_count = int(re.findall(r"Текущее количество: (\d+)", sputnik.text)[0])
    read_pages_count = 0
    
    for page in site.search("insource:\"sputnikmusic.com\"", [0], content=True):
        if page.title() in good_pages:
            continue
        links = [re.sub(r"http://", "https://", link) for link in re.findall(REGEXP, page.text, flags=re.I) 
                 if re.sub(r"http://", "https://", link) not in good_links and check_user(link)]

        if links:
            bad_pages_count += 1
            links_string = create_links_string(links, page)
            sputnik.text = sputnik.text + '\n' + links_string[:-1:]
        read_pages_count += 1
        read_log(read_pages_count)
            
    sputnik.text = re.sub(r"Текущее количество: (\d+)", r"Текущее количество: {}".format(bad_pages_count), sputnik.text)
    sputnik.save(u"обновление списка")


if __name__ == "__main__":
    main()

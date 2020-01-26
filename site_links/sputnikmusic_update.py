#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from urllib.request import urlopen

import pywikibot

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
    sputnik.text = sputnik.text + '\n'
    whitelist = pywikibot.Page(site, u"Проект:Музыка/Неавторитетные источники/Sputnikmusic/Whitelist")
    good_links = set(whitelist.text.split())
    bad_pages_count = int(re.findall(r"Текущее количество: (\d+)", sputnik.text)[0])
    read_pages_count = 0
    
    for string in sputnik.text.split("\n"):
        if not string or string[0] != "#":
            continue
        title = re.findall(r"\[\[(.+?)\]\]", string)[0]
        page = pywikibot.Page(site, u"{}".format(title))
        links = [re.sub(r"http://", "https://", link) for link in re.findall(REGEXP, page.text, flags=re.I) 
                 if re.sub(r"http://", "https://", link) not in good_links and check_user(link)]
        
        if not links:
            sputnik.text = sputnik.text.replace("{}\n".format(string), "")
            bad_pages_count -= 1
        else:   
            links_string = create_links_string(links, page)
            sputnik.text = sputnik.text.replace(string, links_string[:-1:])
        read_pages_count += 1
        read_log(read_pages_count, modulo=10)
    
    sputnik.text = re.sub(r"Текущее количество: (\d+)", r"Текущее количество: {}".format(bad_pages_count), sputnik.text)
    sputnik.save(u"обновление ссылок")


if __name__ == "__main__":
    main()

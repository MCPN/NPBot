#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
import re
from urllib.request import urlopen
import pywikibot
from pywikibot import config
from pywikibot import output

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
            clink = Counter(links)
            new_string = "# [[{}]]: ".format(page.title())
            for link in sorted(clink.most_common()):
                new_string += "[{}] ".format(link[0])
                if link[1] > 1:
                    new_string += "(x{}) ".format(link[1])                
                sputnik.text = sputnik.text + config.line_separator + new_string

        read_pages_count += 1
        if read_pages_count % 50 == 0:
            output("%i pages read..." % read_pages_count)
            
    sputnik.text = re.sub(r"Текущее количество: (\d+)", r"Текущее количество: {}".format(bad_pages_count), sputnik.text)
    sputnik.save(u"обновление списка")


if __name__ == "__main__":
    main()
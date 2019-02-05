#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
import re
import pywikibot
from pywikibot import config
from pywikibot import output

REGEXP = r"(https?://(?:www\.)?mastersland\.com.*?)/?[\s|}\]]"

def main():
    site = pywikibot.Site()
    mastersland = pywikibot.Page(site, u"Проект:Музыка/Неавторитетные источники/Mastersland.com")
    goodPages = set(re.findall(r"\[\[(.+?)\]\]", mastersland.text))
    badPagesCount = int(re.findall(r"Текущее количество: (\d+)", mastersland.text)[0])
    readPagesCount = 0
    added = 0
    
    for page in site.search("insource:\"mastersland.com\"", [0], content=True):
        if page.title() in goodPages:
            continue
        links = [link for link in re.findall(REGEXP, page.text, flags=re.I)]
        if links:
            added += 1
            clink = Counter(links)
            new_string = "# [[{}]]: ".format(page.title())
            for link in clink.most_common():
                new_string += "[{}] ".format(link[0])
                if link[1] > 1:
                    new_string += "(x{}) ".format(link[1])                
            mastersland.text = mastersland.text + config.line_separator + new_string

        readPagesCount += 1
        if readPagesCount % 50 == 0:
            output("%i pages read..." % readPagesCount)
            
    mastersland.text = re.sub(r"Текущее количество: (\d+)", r"Текущее количество: {}".format(badPagesCount + added), mastersland.text)
    mastersland.save(u"список обновлен через поиск")

if __name__ == "__main__":
    main()
#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
import re
import pywikibot
from pywikibot import output

REGEXP = r"(https?://(?:www\.)?mastersland\.com.*?)/?[\s|}\]#<>]"

def main():
    site = pywikibot.Site()
    mastersland = pywikibot.Page(site, u"Проект:Музыка/Неавторитетные источники/Mastersland.com")
    badPagesCount = int(re.findall(r"Текущее количество: (\d+)", mastersland.text)[0])
    readPagesCount = 0
    done = 0
    
    for string in mastersland.text.split("\n"):
        if not string or string[0] != "#":
            continue
        
        title = re.findall(r"\[\[(.+?)\]\]", string)[0]
        page = pywikibot.Page(site, u"{}".format(title))
        links = [link for link in re.findall(REGEXP, page.text, flags=re.I)]
        
        if not links:
            if readPagesCount == badPagesCount - 1:
                mastersland.text = mastersland.text.replace("{}".format(string), "")
            else:
                mastersland.text = mastersland.text.replace("{}\n".format(string), "")
            done += 1
        else:   
            clink = Counter(links)
            new_string = "# [[{}]]: ".format(title)
            for link in sorted(clink.most_common()):
                new_string += "[{}] ".format(link[0])
                if link[1] > 1:
                    new_string += "(x{}) ".format(link[1])
            mastersland.text = mastersland.text.replace(string, new_string[:-1:])
            
        readPagesCount += 1
        if readPagesCount % 50 == 0:
            output("%i pages read..." % readPagesCount)
    
    mastersland.text = re.sub(r"Текущее количество: (\d+)", r"Текущее количество: {}".format(badPagesCount - done), mastersland.text)
    mastersland.save(u"убраны отработанные ссылки")

if __name__ == "__main__":
    main()

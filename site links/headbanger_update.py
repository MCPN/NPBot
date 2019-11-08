#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
import re
import pywikibot
from pywikibot import config
from pywikibot import output

REGEXP = r"(https?://(?:www\.)?headbanger\.ru.*?)/?[\s|}\]]"

def main():
    site = pywikibot.Site()
    headbanger = pywikibot.Page(site, u"Проект:Музыка/Неавторитетные источники/Headbanger.ru")
    badPagesCount = int(re.findall(r"Текущее количество: (\d+)", headbanger.text)[0])
    readPagesCount = 0
    done = 0
    
    for string in headbanger.text.split("\n"):
        if not string or string[0] != "#":
            continue
        title = re.findall(r"\[\[(.+?)\]\]", string)[0]
        page = pywikibot.Page(site, u"{}".format(title))
        links = [link for link in re.findall(REGEXP, page.text, flags=re.I)]
        
        if not links:
            if readPagesCount == badPagesCount - 1:
                headbanger.text = headbanger.text.replace("{}".format(string), "")
            else:
                headbanger.text = headbanger.text.replace("{}\n".format(string), "")
            done += 1
        else:   
            clink = Counter(links)
            new_string = "# [[{}]]: ".format(title)
            for link in sorted(clink.most_common()):
                new_string += "[{}] ".format(link[0])
                if link[1] > 1:
                    new_string += "(x{}) ".format(link[1])
            headbanger.text = headbanger.text.replace(string, new_string[:-1:])
            
        readPagesCount += 1
        if readPagesCount % 50 == 0:
            output("%i pages read..." % readPagesCount)
    
    headbanger.text = re.sub(r"Текущее количество: (\d+)", r"Текущее количество: {}".format(badPagesCount - done), headbanger.text)
    headbanger.save(u"убраны отработанные ссылки")

if __name__ == "__main__":
    main()

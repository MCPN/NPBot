#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
import re
import pywikibot
from pywikibot import config
from pywikibot import xmlreader
from pywikibot import output

REGEXP = r"(https?://(?:www\.)?headbanger\.ru.*?)/?[\s|}\]]"

def main():
    dump = xmlreader.XmlDump("c:\\Users\\mcpn\\PyWikiBot\\dump\\ruwiki.xml.bz2")
    site = pywikibot.Site()
    headbanger = pywikibot.Page(site, u"Проект:Музыка/Неавторитетные источники/Headbanger.ru")
    goodPages = set(re.findall(r"\[\[(.+?)\]\]", headbanger.text))
    badPagesCount = int(re.findall(r"Текущее количество: (\d+)", headbanger.text)[0])
    readPagesCount = 0
    added = 0
    
    for entry in dump.parse():
        match_obj = re.search(REGEXP, entry.text, flags=re.I | re.M | re.DOTALL)
        if entry.ns == "0" and entry.title not in goodPages and match_obj:
            links = [link for link in re.findall(REGEXP, entry.text, flags=re.I)]
            if links:
                added += 1
                clink = Counter(links)
                new_string = "# [[{}]]: ".format(entry.title)
                for link in clink.most_common():
                    new_string += "[{}] ".format(link[0])
                    if link[1] > 1:
                        new_string += "(x{}) ".format(link[1])                
                headbanger.text = headbanger.text + '\n' + new_string

        readPagesCount += 1
        if readPagesCount % 10000 == 0:
            output("%i pages read..." % readPagesCount)
            
    headbanger.text = re.sub(r"Текущее количество: (\d+)", r"Текущее количество: {}".format(badPagesCount + added), headbanger.text)
    headbanger.save(u"список обновлен через дамп")

if __name__ == "__main__":
    main()

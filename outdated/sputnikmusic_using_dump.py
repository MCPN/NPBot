#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
import re
from urllib.request import urlopen
import pywikibot
from pywikibot import config
from pywikibot import xmlreader
from pywikibot import output

REGEXP = r"(https?://(?:www\.)?sputnikmusic\.com/(?:review/|album\.php).+?)/?[\s|}\]]"


def check_user(link):
    try:
        return "<font size=1 face=Arial class=brighttext>USER</font>" in urlopen(link).read().decode("iso-8859-1")
    except:
        return False
    

def check_contributor(link):
    try:
        return re.search(r"Review </h2>by <b>\n(?:.+?)<font size=1 face=Arial class=brighttext>CONTRIBUTOR</font>", 
                          urlopen(link).read().decode("iso-8859-1"))
    except:
        return False
    

def main():
    dump = xmlreader.XmlDump("c:\\Users\\mcpn\\PyWikiBot\\dump\\ruwiki.xml.bz2")
    site = pywikibot.Site()
    sputnik = pywikibot.Page(site, u"Проект:Музыка/Неавторитетные источники/Sputnikmusic")
    whitelist = pywikibot.Page(site, u"Проект:Музыка/Неавторитетные источники/Sputnikmusic/Whitelist")
    goodLinks = set(whitelist.text.split())
    goodPages = set(re.findall(r"\[\[(.+?)\]\]", sputnik.text))
    badPagesCount = int(re.findall(r"Текущее количество: (\d+)", sputnik.text)[0])
    readPagesCount = 0
    added = 0
    
    for entry in dump.parse():
        match_obj = re.search(REGEXP, entry.text, flags=re.I | re.M | re.DOTALL)
        if entry.ns == "0" and entry.title not in goodPages and match_obj:
            links = [re.sub(r"http://", "https://", link) for link in re.findall(REGEXP, entry.text, flags=re.I) 
                     if re.sub(r"http://", "https://", link) not in goodLinks and (check_user(link) or check_contributor(link))]
            
            if links:
                added += 1
                clink = Counter(links)
                new_string = "# [[{}]]: ".format(entry.title)
                for link in clink.most_common():
                    new_string += "[{}] ".format(link[0])
                    if link[1] > 1:
                        new_string += "(x{}) ".format(link[1])                
                sputnik.text = sputnik.text + '\n' + new_string

        readPagesCount += 1
        if readPagesCount % 10000 == 0:
            output("%i pages read..." % readPagesCount)
            
    sputnik.text = re.sub(r"Текущее количество: (\d+)", r"Текущее количество: {}".format(badPagesCount + added), sputnik.text)
    sputnik.save(u"список обновлен через дамп")

if __name__ == "__main__":
    main()

#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
import re
from urllib.request import urlopen
import pywikibot
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
    goodLinks = set(whitelist.text.split())
    badPagesCount = int(re.findall(r"Текущее количество: (\d+)", sputnik.text)[0])
    readPagesCount = 0
    done = 0
    
    for string in sputnik.text.split("\n"):
        if not string or string[0] != "#":
            continue
        title = re.findall(r"\[\[(.+?)\]\]", string)[0]
        page = pywikibot.Page(site, u"{}".format(title))
        links = [re.sub(r"http://", "https://", link) for link in re.findall(REGEXP, page.text, flags=re.I) 
                 if re.sub(r"http://", "https://", link) not in goodLinks and check_user(link)]
        
        if not links:
            if readPagesCount == badPagesCount - 1:
                sputnik.text = sputnik.text.replace("{}".format(string), "")
            else:
                sputnik.text = sputnik.text.replace("{}\n".format(string), "")
            done += 1
        else:   
            clink = Counter(links)
            new_string = "# [[{}]]: ".format(title)
            for link in sorted(clink.most_common()):
                new_string += "[{}] ".format(link[0])
                if link[1] > 1:
                    new_string += "(x{}) ".format(link[1])
            sputnik.text = sputnik.text.replace(string, new_string[:-1:])
            
        readPagesCount += 1
        if readPagesCount % 10 == 0:
            output("%i pages read..." % readPagesCount)
    
    sputnik.text = re.sub(r"Текущее количество: (\d+)", r"Текущее количество: {}".format(badPagesCount - done), sputnik.text)
    sputnik.save(u"убраны отработанные ссылки")

if __name__ == "__main__":
    main()

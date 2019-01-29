#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import Counter
import re
from urllib.request import urlopen
import pywikibot
from pywikibot import config
from pywikibot import output

REGEXP = r"(https?://(?:www\.)?sputnikmusic\.com/(?:review/|album\.php).+?)/?[\s|}\]]"


def check_user(link):
    try:
        return "<font size=1 face=Arial class=brighttext>USER</font>" in urlopen(link).read().decode("iso-8859-1")
    except:
        return False
    

'''
def check_contributor(link):
    try:
        return re.search(r"Review </h2>by <b>\n(?:.+?)<font size=1 face=Arial class=brighttext>CONTRIBUTOR</font>", 
                          urlopen(link).read().decode("iso-8859-1"))
    except:
        return False
'''
    

def main():
    site = pywikibot.Site()
    sputnik = pywikibot.Page(site, u"Проект:Музыка/Неавторитетные источники/Sputnikmusic")
    whitelist = pywikibot.Page(site, u"Проект:Музыка/Неавторитетные источники/Sputnikmusic/Whitelist")
    goodLinks = set(whitelist.text.split())
    goodPages = set(re.findall(r"\[\[(.+?)\]\]", sputnik.text))
    badPagesCount = int(re.findall(r"Текущее количество: (\d+)", sputnik.text)[0])
    readPagesCount = 0
    added = 0
    
    for page in site.search("insource:\"sputnikmusic.com\"", [0], content=True):
        if page.title() in goodPages:
            continue
        links = [re.sub(r"http://", "https://", link) for link in re.findall(REGEXP, page.text, flags=re.I) 
                 if re.sub(r"http://", "https://", link) not in goodLinks and (check_user(link))]
            
        if links:
            added += 1
            clink = Counter(links)
            new_string = "# [[{}]]: ".format(page.title())
            for link in clink.most_common():
                new_string += "[{}] ".format(link[0])
                if link[1] > 1:
                    new_string += "(x{}) ".format(link[1])                
                sputnik.text = sputnik.text + config.line_separator + new_string

        readPagesCount += 1
        if readPagesCount % 50 == 0:
            output("%i pages read..." % readPagesCount)
            
    sputnik.text = re.sub(r"Текущее количество: (\d+)", r"Текущее количество: {}".format(badPagesCount + added), sputnik.text)
    sputnik.save(u"список обновлен через поиск")

if __name__ == "__main__":
    main()
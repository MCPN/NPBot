#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from urllib.request import urlopen
import pywikibot
from pywikibot import config
from pywikibot import output

REGEXP = r"https?://(?:www\.)?sputnikmusic\.com/(?:review/|album.php)[^ |\n]+"


def check_user(link):
    try:
        return "<font size=1 face=Arial class=brighttext>USER</font>" in urlopen(link).read().decode("utf-8")
    except:
        return False
    

def check_contributor(link):
    try:
        if re.findall(r"Review\s?</h2>by(?:.+?)<font size=1 face=Arial class=brighttext>CONTRIBUTOR</font>", 
                          urlopen(link).read().decode("utf-8")):
            output("CONTRIBUTOR God dammit!!!!")
            return True
    except:
        return False
    

def main():
    site = pywikibot.Site()
    sputnik = pywikibot.Page(site, u"Участник:NPBot/Sputnikmusic Upgrade")
    
    readPagesCount = 0
    for string in sputnik.text.split("\n"):
        if string[0] == "=":
            continue
        title = re.findall(r"\[\[(.+?)\]\]", string)[0]
        page = pywikibot.Page(site, u"{}".format(title))
        links = [link for link in re.findall(REGEXP, page.text, flags=re.I) if (check_user(link) or check_contributor(link))]
        if not links:
            sputnik.text = sputnik.text.replace("{}\n".format(string), "")
            
        readPagesCount += 1
        if readPagesCount % 10 == 0:
            output("%i pages read..." % readPagesCount)
    
    sputnik.save(u"Убраны отработанные ссылки")

if __name__ == "__main__":
    main()    
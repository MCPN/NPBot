#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import pywikibot
from urllib.request import urlopen
from pywikibot import config
from pywikibot import pagegenerators


def check_user(link):
    try:
        return "<font size=1 face=Arial class=brighttext>USER</font>" in urlopen(link).read().decode("utf-8")
    except:
        return False
    

def check_contributor(link):
    try:
        return "<font size=1 face=Arial class=brighttext>CONTRIBUTOR</font>" in urlopen(link).read().decode("utf-8")
    except:
        return False
    

site = pywikibot.Site()
sputnik = pywikibot.Page(site, u"Участник:NPBot/Sputnikmusic Upgrade")
regex = r"https?://(?:www\.)?sputnikmusic\.com/(?:review/|album.php)[^ |\n]+"

for page in site.search("insource:\"sputnikmusic.com/\"", [0], content=True):
    links = {link for link in re.findall(regex, page.text, flags=re.I) if (check_user(link) or check_contributor(link))}
    if links:
        sputnik.test = sputnik.text + config.line_separator + "* [[{}]]: {}\n".format(page.title(), " ".join(links))
    #pywikibot.output("{} - {}".format(page.title(), bool(links)))
#open("result.txt", "w", encoding="utf-8").write(result)
page.save(u"done!")

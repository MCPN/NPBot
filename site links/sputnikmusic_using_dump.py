#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
from urllib.request import urlopen
import pywikibot
from pywikibot import config
from pywikibot import xmlreader
from pywikibot import output

REGEXP = r"https?://(?:www\.)?sputnikmusic\.com/(?:review/|album.php)[^ |\n]+"


def check_user(link):
    try:
        return "<font size=1 face=Arial class=brighttext>USER</font>" in urlopen(link).read().decode("utf-8")
    except:
        return False
    

def check_contributor(link):
    try:
        return re.findall(r"Review\s?</h2>by(?:.+?)<font size=1 face=Arial class=brighttext>CONTRIBUTOR</font>", 
                          urlopen(link).read().decode("utf-8"))
    except:
        return False
    

def main():
    site = pywikibot.Site()
    sputnik = pywikibot.Page(site, u"Участник:NPBot/Sputnikmusic Upgrade")

    dump = xmlreader.XmlDump("c:\\Users\\mcpn\\PyWikiBot\\dump\\ruwiki.xml.bz2")
    readPagesCount = 0
    for entry in dump.parse():
        match_obj = re.search(REGEXP, entry.text, flags=re.I | re.M | re.DOTALL)
        if entry.ns == "0" and match_obj:
            links = ["[{}]".format(link) for link in re.findall(REGEXP, entry.text, flags=re.I) if (check_user(link) or check_contributor(link))]
            if links:
                sputnik.text = sputnik.text + config.line_separator + "# [[{}]]: {}".format(entry.title, " ".join(links))

        readPagesCount += 1
        if readPagesCount % 10000 == 0:
            output("%i pages read..." % readPagesCount)
            
    sputnik.save(u"done parsing sputnikmusic links using dump")

if __name__ == "__main__":
    main()
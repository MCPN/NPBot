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
        return re.search(r"Review </h2>by <b>\n(?:.+?)<font size=1 face=Arial class=brighttext>CONTRIBUTOR</font>", 
                          urlopen(link).read().decode("utf-8"))
    except:
        return False
    

def main():
    site = pywikibot.Site()
    sputnik = pywikibot.Page(site, u"Участник:NPBot/Sputnikmusic Upgrade")
    whitelist = pywikibot.Page(site, u"Участник:NPBot/Sputnikmusic Upgrade/Whitelist")
    goodPages = {link for link in whitelist.text.split()}
    badPagesCount = int(re.findall(r"Текущее количество: (\d+)", sputnik.text)[0])
    readPagesCount = 0
    done = 0
    
    for string in sputnik.text.split("\n"):
        if not string or string[0] != "#":
            continue
        title = re.findall(r"\[\[(.+?)\]\]", string)[0]
        page = pywikibot.Page(site, u"{}".format(title))
        links = [re.sub(r"http://", "https://", link) for link in re.findall(REGEXP, page.text, flags=re.I) 
                 if re.sub(r"http://", "https://", link) not in goodPages and (check_user(link) or check_contributor(link))] 
        
        if not links:
            if readPagesCount == badPagesCount - 1:
                sputnik.text = sputnik.text.replace("{}".format(string), "")
            else:
                sputnik.text = sputnik.text.replace("{}\n".format(string), "")
            done += 1
        else:
            dlink = dict()
            for link in links:
                if link[-1] == "/":
                    link = link[:len(link) - 1]
                dlink[link] = dlink.get(link, 0) + 1
                
            new_string = "# [[{}]]: ".format(title)
            for link in dlink.keys():
                new_string += "[{}] ".format(link)
                if dlink[link] > 1:
                    new_string += "(x{}) ".format(dlink[link])
            sputnik.text = sputnik.text.replace(string, new_string)
            
        readPagesCount += 1
        if readPagesCount % 10 == 0:
            output("%i pages read..." % readPagesCount)
    
    sputnik.text = re.sub(r"Текущее количество: (\d+)", r"Текущее количество: {}".format(badPagesCount - done), sputnik.text)
    sputnik.save(u"Убраны отработанные ссылки")

if __name__ == "__main__":
    main()    

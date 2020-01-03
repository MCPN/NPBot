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
    sputnik.text = sputnik.text + '\n'
    whitelist = pywikibot.Page(site, u"Проект:Музыка/Неавторитетные источники/Sputnikmusic/Whitelist")
    good_links = set(whitelist.text.split())
    bad_pages_count = int(re.findall(r"Текущее количество: (\d+)", sputnik.text)[0])
    read_pages_count = 0
    
    for string in sputnik.text.split("\n"):
        if not string or string[0] != "#":
            continue
        title = re.findall(r"\[\[(.+?)\]\]", string)[0]
        page = pywikibot.Page(site, u"{}".format(title))
        links = [re.sub(r"http://", "https://", link) for link in re.findall(REGEXP, page.text, flags=re.I) 
                 if re.sub(r"http://", "https://", link) not in good_links and check_user(link)]
        
        if not links:
            sputnik.text = sputnik.text.replace("{}\n".format(string), "")
            bad_pages_count -= 1
        else:   
            clink = Counter(links)
            new_string = "# [[{}]]: ".format(title)
            for link in sorted(clink.most_common()):
                new_string += "[{}] ".format(link[0])
                if link[1] > 1:
                    new_string += "(x{}) ".format(link[1])
            sputnik.text = sputnik.text.replace(string, new_string[:-1:])
            
        read_pages_count += 1
        if read_pages_count % 10 == 0:
            output("%i pages read..." % read_pages_count)
    
    sputnik.text = re.sub(r"Текущее количество: (\d+)", r"Текущее количество: {}".format(bad_pages_count), sputnik.text)
    sputnik.save(u"обновление ссылок")


if __name__ == "__main__":
    main()

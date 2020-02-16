from collections import Counter

import pywikibot
from pywikibot import output

REGEXP = r"(https?://(?:www\.)?{}.*?)/?[\s|}}\]#<>]"
SITE_NAMES = [
    "headbanger.ru",
    "mastersland.com",
    "rockcult.ru",
    "astartaview.ru",
    "metalfan.nl",
    "heavymusic.ru",
    "metallibrary.ru",
    "metalkings.ru",
    "metalrus.ru",
    "metalfront.org",
    "metalscript.net",
    "metalunderground.com",
]


def generate_list_page(site, site_name):
    page_name = site_name[0].upper() + site_name[1:]
    site_regexp = REGEXP.format(site_name.replace(".", "\."))
    list_page = pywikibot.Page(site, u"Проект:Музыка/Неавторитетные источники/{}".format(page_name))
    return page_name, site_regexp, list_page


def create_links_string(links, page):
    clink = Counter(links)
    new_string = "# [[{}]]: ".format(page.title())
    for link in sorted(clink.most_common()):
        new_string += "[{}] ".format(link[0])
        if link[1] > 1:
            new_string += "(x{}) ".format(link[1])
    return new_string


def read_log(read_pages_count, modulo=50):
    if read_pages_count % modulo == 0:
        output("%i pages read..." % read_pages_count)

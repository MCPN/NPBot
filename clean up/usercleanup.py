#!/usr/bin/python
# -*- coding: utf-8 -*-

import pywikibot
from pywikibot import config
import re


site = pywikibot.Site()
page = pywikibot.Page(site, u"Участник:NPBot/Черновик")
summary = ""
cleanup = ""

if re.search(r"{{[З,з]аголовок курсивом}}\s*\n?", page.text):
    page.text = re.sub(r"{{[З,з]аголовок курсивом}}\s*\n?", "", page.text)
    summary += "убран шаблон {{Заголовок курсивом}}, "
if re.search(r"\|\s*Название\s*=\s*''.+?''", page.text):
    for title in re.findall(r"\|\s*Название\s*=\s*''.+?''", page.text):
        new_title = re.sub(r"''", "", title)
        page.text = page.text.replace(title, new_title)
    summary += "убрано курсивное написание названий альбомов, "
    
if re.search(r"Peak\s?<br\s?\/?>\s?position", page.text):
    page.text = re.sub(r"Peak\s?<br\s?\/?>\s?position", "Высшая <br> позиция", page.text)
    cleanup += "Peak position → Высшая позиция, "
if re.search(r"<br\s?\/>", page.text):
    page.text = re.sub(r"<br\s?\/>", "<br>", page.text)
    cleanup += "<br /> → <br>, "
    
if re.search(r"==\s?References\s?==", page.text):
    page.text = re.sub(r"==\s?References\s?==", "== Примечания ==", page.text)
    cleanup += "References → Примечания, "
if re.search(r"{{[R,r]eflist}}", page.text):
    page.text = re.sub(r"{{[R,r]eflist}}", "{{Примечания}}", page.text)
    cleanup += "{{Reflist}} → {{Примечания}}, "
if re.search(r"==\s?External links\s?==", page.text):
    page.text = re.sub(r"==\s?External links\s?==", "== Ссылки ==", page.text)
    cleanup += "External links → Ссылки, "

if cleanup:
    summary += "замены: " + cleanup
if summary:
    summary = summary[:len(summary) - 2]
    page.save(u"{}".format(summary))

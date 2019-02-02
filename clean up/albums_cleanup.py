#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import pywikibot
from pywikibot import pagegenerators
from pywikibot import output

def main():
    site = pywikibot.Site()
    cat = pywikibot.Category(site, "Категория:Альбомы по алфавиту")
    readPagesCount = 0
    
    for page in pagegenerators.CategorizedPageGenerator(cat):
        summary = ""
        cleanup = ""
        
        if re.search(r"{{[З,з]аголовок курсивом}}\s*\n?", page.text):
            page.text = re.sub(r"{{[З,з]аголовок курсивом}}\s*\n?", "", page.text)
            summary += "убран шаблон {{[[Шаблон:Заголовок курсивом|Заголовок курсивом]]}}, "
            
        titles_changed = False
        for i in range(2):
            if re.search(r"({{[М,м]узыкальный альбом.*?\|\s*(?:Название|Предыдущий|Следующий)\s*=\s*)('{5}|'{2,3})(.+?)\2", page.text, re.DOTALL):
                page.text = re.sub(r"({{[М,м]узыкальный альбом.*?\|\s*(?:Название|Предыдущий|Следующий)\s*=\s*)('{5}|'{2,3})(.+?)\2", "\\1\\3", page.text, re.DOTALL)
                titles_changed = True
            if re.search(r"({{[М,м]узыкальный альбом.*?\|\s*(?:Название|Предыдущий|Следующий)\s*=\s*)«(.+?)»", page.text, re.DOTALL):
                page.text = re.sub(r"({{[М,м]узыкальный альбом.*?\|\s*(?:Название|Предыдущий|Следующий)\s*=\s*)«(.+?)»", "\\1\\2", page.text, re.DOTALL)
                titles_changed = True
            if re.search(r"({{[М,м]узыкальный альбом.*?\|\s*(?:Название|Предыдущий|Следующий)\s*=\s*)„(.+?)“", page.text, re.DOTALL):
                page.text = re.sub(r"({{[М,м]узыкальный альбом.*?\|\s*(?:Название|Предыдущий|Следующий)\s*=\s*)„(.+?)“", "\\1\\2", page.text, re.DOTALL)
                titles_changed = True
        if titles_changed:
            summary += "убрано оформление названий альбомов, "
            
        if re.search(r"\[\[[К, к]атегория:\s?[А,а]льбомы по алфавиту\]\]\s*\n?", page.text):
            page.text = re.sub(r"\[\[[К, к]атегория:\s?[А,а]льбомы по алфавиту\]\]\s*\n?", "", page.text)
            summary += "убрана [[Категория: Альбомы по алфавиту]], "
            
        br = "</?\s?br\s?/?>"
        if re.search(r"Peak\s?{}\s?position".format(br), page.text):
            page.text = re.sub(r"Peak\s?{}\s?position".format(br), "Высшая<br>позиция", page.text)
            cleanup += "Peak position → Высшая позиция, "
        if len(re.findall(r"{}".format(br), page.text)) != len(re.findall(r"<br>", page.text)):
            page.text = re.sub(r"{}".format(br), "<br>", page.text)
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
            
        readPagesCount += 1
        if readPagesCount % 100 == 0:
            output("%i pages read..." % readPagesCount)
    
if __name__ == "__main__":
    main()

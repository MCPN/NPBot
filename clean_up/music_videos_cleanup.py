#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import pywikibot
from pywikibot import pagegenerators
from pywikibot import output

def main():
    site = pywikibot.Site()
    cat = pywikibot.Category(site, "Категория:Музыкальные видео по алфавиту")
    readPagesCount = 0
    
    for page in pagegenerators.CategorizedPageGenerator(cat):
        if not re.search(r"{{[М,м]узыкальн(?:ое видео|ый DVD)", page.text):
            continue
        summary = ""
        cleanup = ""
        
        if re.search(r"{{[З,з]аголовок курсивом}}\s*\n?", page.text):
            page.text = re.sub(r"{{[З,з]аголовок курсивом}}\s*\n?", "", page.text)
            summary += "убран шаблон {{[[Шаблон:Заголовок курсивом|Заголовок курсивом]]}}, "
            
        titles_changed = False
        for i in range(2):
            if re.search(r"((?:{{[М,м]узыкальн(?:ое видео|ый DVD)[^{}]*?\|\s*Название|\|\s*Предыдущий|\|\s*Следующий)\s*=\s*)('{5}|'{2,3})(.+?)\2(\s*[\n|])", page.text):
                page.text = re.sub(r"((?:{{[М,м]узыкальн(?:ое видео|ый DVD)[^{}]*?\|\s*Название|\|\s*Предыдущий|\|\s*Следующий)\s*=\s*)('{5}|'{2,3})(.+?)\2(\s*[\n|])", "\\1\\3\\4", page.text)
                titles_changed = True
            if re.search(r"((?:{{[М,м]узыкальн(?:ое видео|ый DVD)[^{}]*?\|\s*Название|\|\s*Предыдущий|\|\s*Следующий)\s*=\s*)«(.+?)»(\s*[\n|])", page.text):
                page.text = re.sub(r"((?:{{[М,м]узыкальн(?:ое видео|ый DVD)[^{}]*?\|\s*Название|\|\s*Предыдущий|\|\s*Следующий)\s*=\s*)«(.+?)»(\s*[\n|])", "\\1\\2\\3", page.text)
                titles_changed = True
            if re.search(r"((?:{{[М,м]узыкальн(?:ое видео|ый DVD)[^{}]*?\|\s*Название|\|\s*Предыдущий|\|\s*Следующий)\s*=\s*)„(.+?)“(\s*[\n|])", page.text):
                page.text = re.sub(r"((?:{{[М,м]узыкальн(?:ое видео|ый DVD)[^{}]*?\|\s*Название|\|\s*Предыдущий|\|\s*Следующий)\s*=\s*)„(.+?)“(\s*[\n|])", "\\1\\2\\3", page.text)
                titles_changed = True
        if titles_changed:
            summary += "убрано оформление названий музыкальных видео (обновление шаблона {{[[Шаблон:Музыкальное видео|Музыкальное видео]]}}), "
            
        br = "</?\s?br\s?/?>"
        if re.search(r"Peak\s?{}\s?position".format(br), page.text):
            page.text = re.sub(r"Peak\s?{}\s?position".format(br), "Высшая<br>позиция", page.text)
            cleanup += "Peak position → Высшая позиция, "
        if len(re.findall(r"{}".format(br), page.text)) > len(re.findall(r"<br>", page.text)):
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
        
        if summary:
            if cleanup:
                summary += "замены: " + cleanup
            summary = summary[:len(summary) - 2]
            page.save(u"{}".format(summary))
            
        readPagesCount += 1
        if readPagesCount % 50 == 0:
            output("%i pages read..." % readPagesCount)
    
if __name__ == "__main__":
    main()
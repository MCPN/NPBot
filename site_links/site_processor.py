import multiprocessing
import re
import requests
from collections import Counter
from functools import partial

import pywikibot
from pywikibot import output


class SiteProcessor:
    REGEXP = r'(https?://(?:www\.)?{}.*?)/?[\s|}}\]#<>]'

    def __init__(self, wiki, domain, list_page=None, regexp=None, logging_modulo=50):
        self.wiki = wiki
        self.domain = domain
        self.logging_modulo = logging_modulo

        self.list = pywikibot.Page(wiki, list_page if list_page else f'Проект:Музыка/Неавторитетные источники/'
                                                                     f'{domain[0].upper() + domain[1:]}')
        self.whitelist = set(pywikibot.Page(wiki, f'{self.list.title()}/Whitelist').text.split())

        self.regexp = regexp or self.REGEXP.format(domain.replace('.', '\.'))
        self.bad_pages_count = int(re.findall(r'Текущее количество: (\d+)', self.list.text)[0])
        self.read_pages_count = 0

    def get_links(self, pages):
        result = {}
        for page in pages:
            result[page.title()] = [link.replace('http://', 'https://') for link in
                                    re.findall(self.regexp, page.text, flags=re.I) if
                                    link.replace('http://', 'https://') not in self.whitelist]
        return result

    @staticmethod
    def create_links_string(title, links):
        clink = Counter(links)
        new_string = f'# [[{title}]]: '
        for link in clink.most_common():
            new_string += f'[{link[0]}] '
            if link[1] > 1:
                new_string += f'(x{link[1]}) '
        return new_string[:-1]

    def log_read_count(self):
        self.read_pages_count += 1
        if self.read_pages_count % self.logging_modulo == 0:
            output('%i pages read...' % self.read_pages_count)

    def commit(self, msg):
        self.list.text = re.sub(r'Текущее количество: (\d+)', fr'Текущее количество: {self.bad_pages_count}',
                                self.list.text)
        self.list.save(msg)

    def update_from_search(self):
        current_pages = set(re.findall(r'\[\[(.+?)]]', self.list.text))
        pages_links = self.get_links(self.wiki.search(f'insource:\'{self.domain}\'', namespaces=[0], content=True))

        for title, links in pages_links.items():
            if title in current_pages:
                continue
            if links:
                self.bad_pages_count += 1
                self.list.text += '\n' + self.create_links_string(title, links)
            self.log_read_count()

        self.commit('обновление списка')

    def update_from_page(self):
        self.list.text += '\n'  # a small hack for the string deletion (allows to remove the last string)
        strings = [string for string in self.list.text.split('\n') if string and string[0] == '#']
        titles = [re.findall(r'\[\[(.+?)]]', string)[0] for string in strings]
        pages_links = self.get_links([pywikibot.Page(self.wiki, title) for title in titles])

        for string, page in zip(strings, pages_links.items()):
            title, links = page
            if not links:
                self.list.text = self.list.text.replace(f'{string}\n', '')
                self.bad_pages_count -= 1
            else:
                links_string = self.create_links_string(title, links)
                self.list.text = self.list.text.replace(string, links_string)
            self.log_read_count()

        self.commit('обновление ссылок')


class UsersProcessor(SiteProcessor):
    def __init__(self, wiki, domain, user_string, check_inclusion, list_page=None, regexp=None, logging_modulo=50,
                 thread_cnt=4):
        self.user_string = user_string
        self.check_inclusion = check_inclusion
        self.thread_cnt = thread_cnt
        super().__init__(wiki, domain, list_page=list_page, regexp=regexp, logging_modulo=logging_modulo)

    @staticmethod
    def _check(link, user_string, check_inclusion):
        try:
            r = requests.get(link)
            r.raise_for_status()
        except requests.RequestException as e:
            print(f'Failed request for {link}: {e}')
            return
        if bool(re.search(user_string, r.text, flags=re.DOTALL)) == check_inclusion:
            return link

    def get_links(self, pages):
        pages_links = super().get_links(pages)
        all_links = set(sum(pages_links.values(), []))

        processor = partial(self._check, user_string=self.user_string, check_inclusion=self.check_inclusion)
        with multiprocessing.Pool(self.thread_cnt) as pool:
            validated_links = set(pool.imap_unordered(processor, all_links))
        return {title: [link for link in links if link in validated_links] for title, links in pages_links.items()}

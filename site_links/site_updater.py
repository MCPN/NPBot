import argparse

import pywikibot

from site_processor import SiteProcessor, UsersProcessor
from utils import (
    DOMAINS,
    REGEXPS,
    USER_STRINGS,
    LIST_PAGES,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--domains', nargs='*', default=DOMAINS, help='The list of bad domains')
    parser.add_argument('--source', choices=['page', 'search'], required=True,
                        help='Update the existing titles or use the search to find the new ones')
    args = parser.parse_args()

    wiki = pywikibot.Site()
    for domain in args.domains:
        regexp = REGEXPS.get(domain, None)
        user_string, check_inclusion = USER_STRINGS.get(domain, (None, None))
        list_page = LIST_PAGES.get(domain, None)

        if user_string:
            thread_cnt = 1 if domain == 'dtf.ru' else 4  # to avoid HTTP 429 on DTF
            processor = UsersProcessor(wiki, domain, user_string, check_inclusion, regexp=regexp, list_page=list_page,
                                       thread_cnt=thread_cnt)
        else:
            processor = SiteProcessor(wiki, domain, regexp=regexp, list_page=list_page)
        (processor.update_from_page if args.source == 'page' else processor.update_from_search)()


if __name__ == '__main__':
    main()

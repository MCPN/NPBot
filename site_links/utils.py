DOMAINS = [
    'headbanger.ru',
    'mastersland.com',
    'rockcult.ru',
    'astartaview.ru',
    'metalfan.nl',
    'heavymusic.ru',
    'metallibrary.ru',
    'metalkings.ru',
    'metalkings.org',
    'metalkings.com',
    'metalrus.ru',
    'metalfront.org',
    'metalscript.net',
    'metalunderground.com',
    'outstyle.org',
    'sputnikmusic.com',
    'dtf.ru',
]

REGEXPS = {
    'headbanger.ru': r'(https?://(?:www\.)?headbanger\.ru/(?:reviews|concerts|reports).*?)/?[\s|}}\]#<>]',
    'sputnikmusic.com': r'(https?://(?:www\.)?sputnikmusic\.com/(?:review/|album\.php).+?)/?[\s|}\]#<>]',
    'dtf.ru': r'(https?://(?:www\.)?dtf\.ru/games/.+?)/?[\s|}\]#<>]',
}

USER_STRINGS = {
    'sputnikmusic.com': ('<font size=1 face=Arial class=brighttext>USER</font>', True),
    'dtf.ru': ('<h1 class="content-title" itemprop="headline">.{1,10000}'  # TODO: lxml?
               '<span class="content-title__last-word">', False),
}

LIST_PAGES = {
    'sputnikmusic.com': 'Проект:Музыка/Неавторитетные источники/Sputnikmusic',
    'dtf.ru': 'Проект:Компьютерные игры/Списки/Пользовательские обзоры DTF',
}
from urllib import parse

targets = [
    ('a', 'href'), ('applet', 'codebase'), ('area', 'href'), ('base', 'href'),
    ('blockquote', 'cite'), ('body', 'background'), ('del', 'cite'),
    ('form', 'action'), ('frame', 'longdesc'), ('frame', 'src'),
    ('head', 'profile'), ('iframe', 'longdesc'), ('iframe', 'src'),
    ('img', 'longdesc'), ('img', 'src'), ('img', 'usemap'), ('input', 'src'),
    ('input', 'usemap'), ('ins', 'cite'), ('link', 'href'),
    ('object', 'classid'), ('object', 'codebase'), ('object', 'data'),
    ('object', 'usemap'), ('q', 'cite'), ('script', 'src'), ('audio', 'src'),
    ('button', 'formaction'), ('command', 'icon'), ('embed', 'src'),
    ('html', 'manifest'), ('input', 'formaction'), ('source', 'src'),
    ('video', 'poster'), ('video', 'src'),
]


def rebase_one(base, url):
    """Rebase one url according to base"""

    parsed = parse.urlparse(url)
    if parsed.scheme == parsed.netloc == '':
        return parse.urljoin(base, url)
    else:
        return url


def rebase(base, soup):
    """Rebase the HTML blob data according to base"""

    for (tag, attr) in targets:
        for link in soup.findAll(tag):
            try:
                url = link[attr]
            except KeyError:
                pass
            else:
                link[attr] = rebase_one(base, url)
                if tag == 'a':
                    link['target'] = '_blank'
    return soup

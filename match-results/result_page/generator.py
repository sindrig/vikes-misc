import requests
import bs4

from .rebaser import rebase

PAGES = {
    'kk': {
        'overview': (
            'https://www.ksi.is/mot/felog/leikir-felaga/?Search=True&'
            'felag=103&vollur=&flokkur=111&kyn=1&dagsfra=27.04.2018&'
            'dagstil=07.10.2018'
        ),
        'competition': (
            'https://www.ksi.is/mot/stakt-mot/?motnumer=37403'
        )
    },
    'kvk': {
        'overview': (
            'https://www.ksi.is/mot/felog/leikir-felaga/?Search=True&'
            'felag=8099&vollur=&flokkur=111&kyn=0&dagsfra=27.04.2018&'
            'dagstil=07.10.2018'
        ),
        'competition': (
            'https://www.ksi.is/mot/stakt-mot/?motnumer=37365'
        )
    }
}

JS_VARS = {
    'DIV_CLASS': 'sex_part',
    'A_CLASS': 'sex_selector'
}

SCRIPT = '''
    function for_class(classname, cb) {
        elements = document.getElementsByClassName(classname);
        for (var i = 0; i < elements.length; i++) {
            cb(elements[i])
        }
    }
    function show_result_page_part(id) {
        for_class('%(DIV_CLASS)s', function(element){
            element.style.display = 'none';
        });
        for_class('%(A_CLASS)s', function(element){
            element.style['font-weight'] = 'normal';
        });
        document.getElementById(id).style.display = 'block';
        selector_link = document.getElementById('selector_' + id);
        selector_link.style['font-weight'] = 'bold';
    }
    show_result_page_part('vik_kk');
''' % JS_VARS


class Target:
    def __init__(self, target, remove=[]):
        self.target = target
        self.remove = remove

    def get_target(self):
        for r in self.remove:
            self.target.find(*r).decompose()
        return self.target


def get_soup(url):
    soup = bs4.BeautifulSoup(
        requests.get(url).text,
        'html.parser'
    )
    rebase(url[:url.find('?')], soup)
    return soup


def generate_mainpage(kk, kvk):
    soup = bs4.BeautifulSoup('<div></div>', 'html.parser')
    selector = get_selector(soup, kk='vik_kk', kvk='vik_kvk')
    kk = get_wrapper(soup, 'vik_kk', kk)
    kvk = get_wrapper(soup, 'vik_kvk', kvk)
    soup.append(selector)
    soup.append(kk)
    soup.append(kvk)
    return soup


def get_selector(parent, kk, kvk):
    def get_link(name, target_div):
        a = parent.new_tag('a', id='selector_%s' % (target_div))
        a['href'] = '#'
        a['onClick'] = 'show_result_page_part("%s")' % (target_div)
        a['class'] = JS_VARS['A_CLASS']
        a.string = name
        return a
    div = parent.new_tag('div')
    div.append(get_link('Karlar', kk))
    div.append(' / ')
    div.append(get_link('Konur', kvk))
    return div


WRAPPER_STYLE = (
    'float: left; '
    # 'max-width: {width}; '
    'margin: 20px; '
)


def get_wrapper(parent, wrapper_id, targets):
    assert len(targets) == 3
    soup = parent.new_tag('div', id=wrapper_id)
    soup['class'] = JS_VARS['DIV_CLASS']
    left_wrapper = parent.new_tag('div')
    right_wrapper = parent.new_tag('div')

    left_wrapper['style'] = WRAPPER_STYLE.format(width='800px')
    right_wrapper['style'] = WRAPPER_STYLE.format(width='600px')

    left_wrapper.append(targets[0].get_target())
    right_wrapper.append(targets[1].get_target())
    right_wrapper.append(targets[2].get_target())
    soup.append(left_wrapper)
    soup.append(right_wrapper)
    return soup


def strip_fixtures(fixture_soup):
    table = fixture_soup.find('table')
    for i, row in enumerate(table.findAll('tr')):
        if i > 7:
            row.decompose()
    return fixture_soup


def get_data(sex):
    overview = get_soup(PAGES[sex]['overview'])
    competition = get_soup(PAGES[sex]['competition'])
    return {
        'overview': overview,
        'competition': competition,
        'targets': [
            Target(
                overview.find('div', {'class': 'table-responsive'})
            ),
            Target(
                competition.find('div', {'class': 'results-area style2'}),
                remove=[
                    ('ul', {'class': 'nav-pills'})
                ]
            ),
            Target(
                strip_fixtures(competition.find('div', {'id': 'fixtures'}))
            ),
        ]
    }


def generate_page():
    kk_data = get_data('kk')
    kvk_data = get_data('kvk')
    page_to_use = kk_data['overview']
    for to_remove in ('header', 'footer'):
        for h in kk_data['overview'].findAll(to_remove):
            h.decompose()
    page = generate_mainpage(kk=kk_data['targets'], kvk=kvk_data['targets'])
    page_to_use.find('div', {'class': 'wrapper'}).replaceWith(page)
    script = page_to_use.new_tag('script')
    script['type'] = 'text/javascript'
    script.string = SCRIPT
    page_to_use.find('body').append(script)
    return str(page_to_use)

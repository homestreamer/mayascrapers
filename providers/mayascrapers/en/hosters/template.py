# -*- coding: utf-8 -*-

from providerModules.mayascrapers import core

class source(core.DefaultHosterSources):
    def __init__(self):
        self.priority = 1
		self.language = ['en']
        self.domains = ['https://tamilyogi.beer']
        self.base_link = 'https://tamilyogi.beer/'
		self.search_link = 'https://tamilyogi.beer/?s='

    def movie(self, imdb, title, localtitle, aliases, year):
        self.query_type = 'movie'

        simple_info = {}
        simple_info['title'] = source_utils.clean_title(title)
        simple_info['query_title'] = simple_info['title']
        simple_info['year'] = year
        return simple_info

    def tvshow(self, imdb, tvdb, tvshowtitle, localtvshowtitle, aliases, year):
        self.query_type = 'episode'

        simple_info = {}
        simple_info['show_title'] = re.sub(r'\s+', ' ', source_utils.clean_title(tvshowtitle).replace(year, ''))
        simple_info['query_title'] = simple_info['show_title']
        simple_info['year'] = year
        return simple_info

    def episode(self, simple_info, imdb, tvdb, title, premiered, season, episode):
        if simple_info is None:
            return None

        simple_info['episode_title'] = title
        simple_info['episode_number'] = episode
        simple_info['season_number'] = season
        simple_info['episode_number_xx'] = episode.zfill(2)
        simple_info['season_number_xx'] = season.zfill(2)
        simple_info['show_aliases'] = []

        return simple_info

    def search(self, query, search_id=None):
            if self.is_movie_query():
        query = '%s %s' % (source_utils.clean_title(simple_info['title']), simple_info['year'])
    else:
        query = '%s S%sE%s' % (source_utils.clean_title(simple_info['show_title']), simple_info['season_number_xx'], simple_info['episode_number_xx'])

    search_path = self.search_link % core.quote_plus(query)
    search_url = '%s%s' % (self.base_link, search_path)

    response = self._request.get(search_url)
    if response.status_code != 200:
        return None

    result_content = response.text

    # Extract movies from the result content
    html = result_content
    regex = r"<iframe\s*srcdoc.+?iframe>"
    html = re.sub(regex, '', html, 0, re.MULTILINE)
    mlink = SoupStrainer("div", {"id": "archive"})
    mdiv = BeautifulSoup(html, "html.parser", parse_only=mlink)
    plink = SoupStrainer("div", {"class": "navigation"})
    Paginator = BeautifulSoup(html, "html.parser", parse_only=plink)
    items = mdiv.find_all('li')

    reults = []

    # Iterate through items until the first result is found
    for item in items:
        if '"cleaner"' not in str(item):
            title = self.unescape(item.text)
            title = self.clean_title(title)
            url = item.a.get('href')
            try:
                thumb = item.img.get('src')
            except:
                thumb = self.icon

            # Append title and URL to movies list
            results.append((title, url))

            # Break the loop after processing the first item
            break

    return results

    def resolve(self, url):
        return url
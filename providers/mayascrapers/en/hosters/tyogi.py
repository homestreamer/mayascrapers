# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup, SoupStrainer
from providerModules import core, source_utils, client, base

import requests
from bs4 import BeautifulSoup, SoupStrainer
import urllib.parse as urlparse

class Source:
    def __init__(self):
        self.priority = 1
        self.language = ['en']
        self.domains = ['https://tamilyogi.beer']
        self.base_link = 'https://tamilyogi.beer/'
        self.search_link = '?s='

    def movie(self, imdb, title, localtitle, aliases, year):
        self.query_type = 'movie'
        simple_info = {
            'title': title,
            'query_title': title,
            'year': year
        }
        return simple_info

    def search(self, simple_info):
        query = '%s %s' % (self.clean_title(simple_info['title']), simple_info['year'])
        search_url = self.base_link + self.search_link + urlparse.quote_plus(query)

        # Extract movies from the result content
        results = []
        html = requests.get(search_url).text
        mlink = SoupStrainer("div", {"id": "archive"})
        mdiv = BeautifulSoup(html, "html.parser", parse_only=mlink)
        items = mdiv.find_all('li')
        for item in items:
            if 'cleaner' not in item.get('class', []):
                title = self.clean_title(item.text)
                url = item.a.get('href')
                results.append((title, url))

        return results

    def sources(self, simple_info):
        sources = []
        results = self.search(self, simple_info)  # Use the search function to populate the results list
        if not results:
            return sources

        for result in results:
            title, url = result
            release_title = title
            domain = self.domains[0]  # Use the first domain from self.domains
            quality = 'SD'  # Placeholder, needs actual quality detection

            sources.append({
                'release_title': release_title,
                'source': domain,
                'quality': quality,
                'language': 'en',
                'url': url,
                'info': [],
                'direct': True,
                'debridonly': False
            })
        sources.reverse()
        return sources



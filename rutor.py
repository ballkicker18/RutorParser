import requests
from bs4 import BeautifulSoup
import config
from config import logger
from datetime import datetime
from furl import furl

class Torrent:
    def __init__(self, name: str, date: str, size: str, peers: list, links: list):
        self.name = name
        self.date = date # "dd.mm.yy"
        self.size = size
        self.peers = peers
        self.links = links
    
    def get_torrent_link(self) -> str:
        return self.links[0]
    def get_magnet_link(self) -> str:
        return self.links[1]
    def get_up_peers(self) -> int:
        return self.peers[0]
    def get_down_peers(self) -> int:
        return self.peers[1]

class Rutor:
    def __init__(self):
        self.RUTOR_LINK = furl(config.RUTOR_LINK)
        self.SEARCH_LINK = self.RUTOR_LINK.copy()
        self.SEARCH_LINK.path.segments = ['search', '1', '0', '000', '0']
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': config.USER_AGENT})
        self.pages = 0

        if config.USE_TOR:
            proxies = {
                'http': f'socks5://127.0.0.1:{config.TOR_PORT}',
                'https': f'socks5://127.0.0.1:{config.TOR_PORT}',
            }
            self.session.proxies.update(proxies)
        elif config.USE_PROXY:
            self.session.proxies.update(config.PROXIES)

    def get_html(self, link: str) -> str:
        logger.debug(f'Connecting to: {link}')
        resp = self.session.get(link).text
        logger.debug(f'Returning response: {resp}')
        return resp

    def datetime_from_str(self, string: str) -> datetime:
        months = {
                'Янв': 1, 'Фев': 2, 'Мар': 3, 'Апр': 4,
                'Май': 5, 'Июн': 6, 'Июл': 7, 'Авг': 8,
                'Сен': 9, 'Окт': 10, 'Ноя': 11, 'Дек': 12
            }

        date_string = string

        day, month_str, year = date_string.split()

        month = months[month_str]

        year = int(year) + 2000 if int(year) < 50 else int(year) + 1900

        return datetime(year, month, int(day))

    def get_results_from_resp(self, response: str) -> list:
        soup = BeautifulSoup(response, 'lxml')
        logger.debug(soup)
        pages = 0
        try:
            pages = int(soup.find('p', style='margin-top: 30px;').find_all('a', style='font-weight: bold; padding: 0 5px;')[-2].text)
        except:
            logger.info("Not found!")
            return []
        div_index = soup.find('div', id='index')
        table_body = div_index.find('table').find('tbody')
        torrents_html = table_body.find_all('tr')[1::]
        torrents = []
        for torrent in torrents_html:
            date = self.datetime_from_str(torrent.find('td').text)
            name = torrent.find_all('a')[2].text
            size = torrent.find_all('td')[3].text
            peers = [int(torrent.find('span', class_='green').text), int(torrent.find('span', class_='red').text)]
            links = [torrent.find_all('a')[0].get('href'), torrent.find_all('a')[1].get('href')]
            torrent = Torrent(name, date, size, peers, links)
            torrents.append(torrent)
        self.pages = pages
        self.current_page = int(self.current_link.path.segments[1])
        return torrents

    def search(self, query: str, link: furl = None) -> list:
        logger.debug(f"Searching: {query}")
        if link is None:
            self.current_link = self.SEARCH_LINK.copy()
            self.current_link.path.segments.append(query)
        else:
            self.current_link = link
        
        resp = self.get_html(self.current_link.url)
        results = self.get_results_from_resp(resp)
        return results

    # def __next__(self):
    #     if self.pages >= self.current_page:
    #         self.current_link.path.segments[1] = str(int(self.current_link.path.segments[1]) + 1)
    #         self.current_page += 1
    #         return self.search('', self.current_link)
    #     else:
    #         raise StopIteration
    
    # def __iter__(self):
    #     return self
        
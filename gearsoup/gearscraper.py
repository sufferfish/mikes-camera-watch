from bs4 import BeautifulSoup
import requests
import json

class GearScraper:
    def __init__(self, url):
        self.url = url

    def _get_google_doc_url(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup.find('iframe', title='California used gear table').attrs['src']

    def _get_gear_soup_table(self, doc_url):
        gear_list = requests.get(doc_url)
        gear_soup = BeautifulSoup(gear_list.content, 'html.parser')
        return gear_soup.table

    def _clean_table_contents(self, gtable):
        for th in gtable("th"):
            th.decompose()
        return gtable.find_all('tr')[1:]

    def __cleanup(self, i):
        if '$' in i:
            return float(i.replace('$ ', '').replace(',', ''))
        else:
            try:
                return int(i)
            except ValueError:
                return i

    def __item_dict(self, clean_gtable):
        headers = ['ref', 'name', 'price', 'loc', 'num'] 
        values = []
        for string in clean_gtable.stripped_strings:
            values.append(self.__cleanup(string))
        return dict(zip(headers, values))

    def _build_mega_list(self, table_contents):
        mega_list = []
        for tag in table_contents:
            mega_list.append(self.__item_dict(tag))
        return mega_list

    def dump_json(self, mega_list):
        with open('mike.json', 'w') as f:
            json.dump(mega_list, f, indent=2)

    def scrape_to_disk(self):
        doc_url = self._get_google_doc_url()
        gtable = self._get_gear_soup_table(doc_url)
        table_contents = self._clean_table_contents(gtable)
        mega_list = self._build_mega_list(table_contents)
        self.dump_json(mega_list)

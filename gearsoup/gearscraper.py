from typing import Any
from bs4 import BeautifulSoup, Tag
import requests
import json

class GearScraper:
    def __init__(self, url: str) -> None:
        self.url = url

    def _get_google_doc_url(self) -> Tag:
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup.find('iframe', title='California used gear table').attrs['src']

    def _get_gear_soup_table(self, doc_url: str) -> Tag:
        gear_list = requests.get(doc_url)
        gear_soup = BeautifulSoup(gear_list.content, 'html.parser')
        return gear_soup.table

    def _clean_table_contents(self, gtable: Tag):
        for th in gtable("th"):
            th.decompose()
        return gtable.find_all('tr')[1:]

    def __clean_value(self, i: str) -> (float|int|str):
        if '$' in i:
            return float(i.replace('$ ', '').replace(',', ''))
        else:
            try:
                return int(i)
            except ValueError:
                return i
            
    def __clean_final_list(self, flist: list[dict]) -> list[int|str]:
        for gear_dict in flist:
            if len(gear_dict) != 5:
                flist.pop(flist.index(gear_dict))
        return flist

    def __item_dict(self, clean_gtable: Tag) -> dict[str, Any]:
        headers = ['ref', 'name', 'price', 'loc', 'num'] 
        values = []
        for string in clean_gtable.stripped_strings:
            values.append(self.__clean_value(string))
        return dict(zip(headers, values))

    def _build_mega_list(self, table_contents: Tag) -> list[dict[str, Any]]:
        mega_list = []
        for tag in table_contents:
            mega_list.append(self.__item_dict(tag))
        return mega_list

    def _dump_json(self, mega_list: list[dict]) -> None:
        with open('mike.json', 'w') as f:
            json.dump(mega_list, f, indent=2)

    def scrape_to_disk(self) -> None:
        doc_url = self._get_google_doc_url()
        gtable = self._get_gear_soup_table(doc_url)
        table_contents = self._clean_table_contents(gtable)
        mega_list = self._build_mega_list(table_contents)
        final_list = self.__clean_final_list(mega_list)
        self._dump_json(final_list)

    def scrape_to_mem(self) -> None:
        doc_url = self._get_google_doc_url()
        gtable = self._get_gear_soup_table(doc_url)
        table_contents = self._clean_table_contents(gtable)
        mega_list = self._build_mega_list(table_contents)
        return self.__clean_final_list(mega_list)
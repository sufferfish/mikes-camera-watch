from bs4 import BeautifulSoup
import requests
import json


# Global vars
URL = "https://mikescamera.com/used-gear#used-gear-california"

def get_google_doc_url():

    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")

    return soup.find('iframe', title='California used gear table').attrs['src']

def get_gear_soup_table(doc_url):

    gear_list = requests.get(doc_url)

    gear_soup = BeautifulSoup(gear_list.content, 'html.parser')
    return gear_soup.table

def clean_table_contents(gtable):

    for th in gtable("th"):
        th.decompose()

    return gtable.find_all('tr')[1:]

def cleanup(i: str) -> str|int:
    if '$' in i:
        return float(i.replace('$ ', '').replace(',', ''))
    else:
        try:
            return int(i)
        except ValueError:
            return i

def item_dict(clean_gtable):
    headers = ['ref', 'name', 'price', 'loc', 'num'] 
    values = []
    for string in clean_gtable.stripped_strings:
        values.append(cleanup(string))

    return dict(zip(headers, values))

def build_mega_list(table_contents):

    mega_list = []
    for tag in table_contents:
        mega_list.append(item_dict(tag))

    return mega_list

def dump_json(mega_list):

    with open('mike.json', 'w') as f:
        json.dump(mega_list, f, indent = 2)

def main():
    doc_url = get_google_doc_url()
    gtable = get_gear_soup_table(doc_url)
    table_contents = clean_table_contents(gtable)
    mega_list = build_mega_list(table_contents)
    dump_json(mega_list)


if __name__ == "__main__":
    main()
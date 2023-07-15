import sys
from gearsoup.gearscraper import GearScraper
from gearsoup.gearcheck import GearCheck
import json
from os.path import exists

def compare(old_stuff: dict, new_stuff: dict) -> list|None:
    comparitor = GearCheck(new_stuff, old_stuff)
    if comparitor.compare_jsons():
        return comparitor.get_new_listings()
    else:
        return None

def get_old_data():
    with open('mike.json', 'r') as f:
        return json.load(f)

def main():
    
    gear = GearScraper("https://mikescamera.com/used-gear#used-gear-california")
    
    if exists('mike.json'):
        new_stuff = gear.scrape_to_mem()
    else:
        gear.scrape_to_disk()
        sys.exit(1)

    old_stuff = get_old_data()

    compare(old_stuff, new_stuff)
    
    

if __name__ == "__main__":
    main()
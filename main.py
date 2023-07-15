from gearsoup.gearscraper import GearScraper

def main():

    gear = GearScraper("https://mikescamera.com/used-gear#used-gear-california")

    gear.scrape_to_disk()

if __name__ == "__main__":
    main()
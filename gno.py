import time
from dotenv import load_dotenv
from utils.rss import ThreatIntel, GovThreatIntel, Reuters, TreasuryGovRss, handle_rss_feed_list

load_dotenv()

# List of RSS feeds to scrape
rss_feeds = ThreatIntel + GovThreatIntel + Reuters + TreasuryGovRss

def gno():
    while True:
        handle_rss_feed_list(rss_feeds)
        time.sleep(1800)

if __name__ == '__main__':
    gno()
import os
import feedparser
import time

from .format import tweetify_article
from dotenv import load_dotenv
from .twitter import oauth, create_tweet

load_dotenv()
DISCORD_STATUS_WEBHOOK = os.getenv("STATUS_WEBHOOK")
#status_messages = Webhook.from_url(DISCORD_STATUS_WEBHOOK, adapter=RequestsWebhookAdapter())
twitterAuth = oauth()

def get_news_from_rss(rss_item):
    feed_entries = feedparser.parse(rss_item[0]).entries

    # This is needed to ensure that the oldest articles are proccessed first. See https://github.com/vxunderground/ThreatIntelligenceDiscordBot/issues/9 for reference
    for rss_object in feed_entries:
        rss_object["source"] = rss_item[1]
        try:
            rss_object["publish_date"] = time.strftime(
                "%Y-%m-%dT%H:%M:%S", rss_object.published_parsed
            )
        except:
            rss_object["publish_date"] = time.strftime(
                "%Y-%m-%dT%H:%M:%S", rss_object.updated_parsed
            )

    return feed_entries

def send_messages(hook, messages, articles, batch_size=10):
    for i in range(0, len(messages), batch_size):
        try:
            hook.send(embeds=messages[i : i + batch_size])
        except:
            print("Empty embed for ", messages[i : i + batch_size])
        
        time.sleep(3)

def process_source(post_gathering_func, source):
    raw_articles = post_gathering_func(source)
    processed_articles, new_raw_articles = proccess_articles(raw_articles)

def proccess_articles(articles):
    posts, new_articles = [], []
    articles.sort(key=lambda article: article["publish_date"])

    for article in articles:
        #posts.append(format_single_article(article))
        create_tweet(twitterAuth, tweetify_article(article))
        time.sleep(180)
        #new_articles.append(article)

    #return posts, new_articles

def handle_rss_feed_list(rss_feed_list):
    for rss_feed in rss_feed_list:
        #status_messages.send(f"> {rss_feed[1]}")
        process_source(get_news_from_rss, rss_feed)





























ThreatIntel = [
    ['https://grahamcluley.com/feed/', 'Graham Cluley'],
    ['https://threatpost.com/feed/', 'Threatpost'],
    ['https://krebsonsecurity.com/feed/', 'Krebs on Security'],
    ['https://www.darkreading.com/rss.xml', 'Dark Reading'],
    ['http://feeds.feedburner.com/eset/blog', 'We Live Security'],
    ['https://davinciforensics.co.za/cybersecurity/feed/', 'DaVinci Forensics'],
    ['https://blogs.cisco.com/security/feed', 'Cisco'],
    ['https://www.infosecurity-magazine.com/rss/news/', 'Information Security Magazine'],
    ['http://feeds.feedburner.com/GoogleOnlineSecurityBlog', 'Google'],
    ['http://feeds.trendmicro.com/TrendMicroResearch', 'Trend Micro'],
    ['https://www.bleepingcomputer.com/feed/', 'Bleeping Computer'],
    ['https://www.proofpoint.com/us/rss.xml', 'Proof Point'],
    ['http://feeds.feedburner.com/TheHackersNews?format=xml', 'Hacker News'],
    ['https://www.schneier.com/feed/atom/', 'Schneier on Security'],
    ['https://www.binarydefense.com/feed/', 'Binary Defense'],
    ['https://securelist.com/feed/', 'Securelist'],
    ['https://research.checkpoint.com/feed/', 'Checkpoint Research'],
    ['https://www.virusbulletin.com/rss', 'VirusBulletin'],
    ['https://modexp.wordpress.com/feed/', 'Modexp'],
    ['https://www.tiraniddo.dev/feeds/posts/default', 'James Forshaw'],
    ['https://blog.xpnsec.com/rss.xml', 'Adam Chester'],
    ['https://msrc-blog.microsoft.com/feed/', 'Microsoft Security'],
    ['https://www.recordedfuture.com/feed', 'Recorded Future'],
    ['https://www.sentinelone.com/feed/', 'SentinelOne'],
    ['https://redcanary.com/feed/', 'RedCanary'],
    ['https://cybersecurity.att.com/site/blog-all-rss', 'ATT']
]

GovThreatIntel = [
    ['https://www.cisa.gov/uscert/ncas/alerts.xml', 'US-CERT CISA'],
    ['https://www.ncsc.gov.uk/api/1/services/v1/report-rss-feed.xml', 'NCSC'],
    ['https://www.cisecurity.org/feed/advisories', 'Center of Internet Security']
]

Reuters = [
    ['https://www.reutersagency.com/feed/?best-types=the-big-picture&post_type=best', 'Reuters Big Picture'],
    ['https://www.reutersagency.com/feed/?best-topics=tech&post_type=best', 'Reuters Tech'],
    ['https://www.reutersagency.com/feed/?best-topics=business-finance&post_type=best', 'Reuters Business & Finance']
]

TreasuryGovRss = [
    ['https://treasurydirect.gov/TA_WS/securities/announced/rss', 'US Treasury Offering Announcement'],
    ['https://treasurydirect.gov/TA_WS/securities/auctioned/rss', 'US Treasury Auction Results'],
    ['https://treasurydirect.gov/NP_WS/debt/feeds/recent', 'US Treasury Debt to Penny'],
    ['https://www.treasurydirect.gov/rss/mspd.xml', 'US Treasury Monthly Statement of the Public Debt'],
    ['https://www.treasurydirect.gov/rss/sbpro.xml', 'US Savings Bond Pro Updates']
]
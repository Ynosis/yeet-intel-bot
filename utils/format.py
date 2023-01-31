from datetime import datetime
import dateutil.parser


MAIN_COLOR = 0x000000
THUMBNAIL_URL = "https://avatars.githubusercontent.com/u/87911852?s=280&v=4"


def cut_string(string, length):
    return (string[: (length - 3)].strip() + "...") if len(string) > length else string


def format_datetime(article_datetime):
    if not isinstance(article_datetime, datetime):
        try:
            article_datetime = dateutil.parser.isoparse(article_datetime)
        except ValueError:
            return article_datetime.split("T")

    return [article_datetime.strftime("%d, %b %Y"), article_datetime.strftime("%H:%M")]

def tweetify_article(article):
    description = ""

    if "summary" in article:
        for text_part in article["summary"].split("."):
            if not (len(description) + len(text_part)) > 250:
                description += text_part + "."
            else:
                description += ".."
                break

    source_text = f"Source: {article['source']}"
    date_text = "Date: " + " | ".join(format_datetime(article["publish_date"]))

    if "link" in article:
        link = article["link"]
        tweet = f"{article['title']}\n\n{link}\n\n{source_text}\n#Gnosis"

    else:
        tweet = f"{article['title']}\n\n{description}\n\n{source_text}\n{date_text}\n\n#Gnosis"

    print(f"Tweeting: \n{tweet}")
    return tweet

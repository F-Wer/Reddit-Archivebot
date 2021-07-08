import urllib.parse
import requests
import json
outline_api = "https://api.outline.com/v3/parse_article?source_url="
input_url = "https://old.reddit.com/r/redditdev/comments/5fyjg4/praw_how_to_get_top_rising_and_new_posts_from/"
outline = "https://outline.com/"
escapedinputurl = urllib.parse.quote_plus(input_url)
print(escapedinputurl)
response = requests.get(outline_api + escapedinputurl)
textresponse = json.dumps(response.json(), indent=4, sort_keys=True)
resp = json.loads(textresponse)
short_code = (resp['data']['short_code'])
url = outline + short_code
print(url)

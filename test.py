# import urllib.parse
# import requests
# import json
# outline_api = "https://api.outline.com/v3/parse_article?source_url="
# input_url = "https://old.reddit.com/r/redditdev/comments/5fyjg4/praw_how_to_get_top_rising_and_new_posts_from/"
# outline = "https://outline.com/"
# escapedinputurl = urllib.parse.quote_plus(input_url)
# print(escapedinputurl)
# response = requests.get(outline_api + escapedinputurl)
# textresponse = json.dumps(response.json(), indent=4, sort_keys=True)
# resp = json.loads(textresponse)
# short_code = (resp['data']['short_code'])
# url = outline + short_code
# print(url)

# import sqlite3

# connection = sqlite3.connect("posts.db")

# cursor = connection.cursor()

# sql = "CREATE TABLE personen(""posts ID PRIMARY KEY)"
# cursor.execute(sql)

#  def create_outline_url_old(self, url):
#         start_old = time.time()
#         """[summary]
#             Läuft momentan über Selenium mit Firefox, da meine Pathvariables nicht wirklich funktionieren, ist dies über env variables gelöst.
#             Da Chrome manchmal random abgestützt ist, ist nur Firefox implementiert.

#             Dauert ungefähr 15 sekunden abzulaufen
#         Args:
#             url ([url]): Input für die URL um diese an Outline weiterzugeben
#             title ([str]): Der Titel des Posts um diesen

#         Returns:
#             [url]: Outlineurl
#         """
#         concaturl = outline + url
#         options = Options()
#         options.headless = True
#         driver = webdriver.Firefox(
#             executable_path=config.geckodriver, options=options)
#         driver.get(concaturl)
#         time.sleep(5)
#         if concaturl != driver.current_url:
#             time.sleep(2)
#             outlineurl = driver.current_url
#             driver.close()
#         end_old = time.time()
#         print(end_old - start_old)
#         return outlineurl

# submissions = reddit.submission(id=id)
# for comment in submissions.comments:
#     # https://praw.readthedocs.io/en/latest/tutorials/comments.html#extracting-comments-with-praw
#     if isinstance(comment, MoreComments):
#         continue
#     if comment.author == config.botname:
#         pass
#     else:

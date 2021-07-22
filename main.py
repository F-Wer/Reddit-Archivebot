import praw
import config
import time
import waybackpy
import urllib.parse
import requests
import json
from praw.models import MoreComments
import sqlite3
import os
outline = 'https://outline.com/'
class Reddit:

    def get_submissions(self):
        """[summary]
        Gets all submissions and looks which are not archivable via outline.com
        Link Posts ==> outline
        Rest ==> archive.org
        """
        try:
            not_supported = ['nytimes.com', 'wsj.com',
                             'redd.it', 'youtube.com', 'youtu.be', 'imgur.com']
            for submission in reddit.subreddit(config.subreddit).stream.submissions():
                if submission.__dict__.get('post_hint', None) == 'link':
                    if submission.archived != True:
                        # Did the bot already comment?
                        result = select_db(self, submission.id)
                        if result != 0:  # If yes skip!
                            pass
                        else:  
                            # If URL not supported then use archive.org
                            if any([x in submission.url for x in not_supported]):
                                print("This url isn't supported by outline.com" +
                                      ' ' + submission.url + ' ' + submission.id)
                                currenturl = 'Diese URL wird bei Outline nicht unterstützt'
                            else:  
                                if submission.url in "outline.com":
                                    currenturl = submission.url
                                else:
                                    print('URL wird unterstützt' +
                                          ' ' + submission.url)
                                    currenturl = self.create_outline_url(
                                        submission.url)
                            archiveurl = self.create_archive_url(  # As a backup for the backup use archive.org
                                submission.url)
                            self.comment(currenturl, archiveurl, submission.id)
        except Exception as e:
            print(e)

    def create_outline_url(self, url):
        """[summary]
        Create Outline link via direct API access.
        Args:
            url ([url]): Input for outline

        Returns:
             [url]: URL from outline
        """
        try:
            outline_api = "https://api.outline.com/v3/parse_article?source_url="
            escapedinputurl = urllib.parse.quote_plus(
                url)  # matches htmlencode
            response = requests.get(outline_api + escapedinputurl)
            textresponse = json.dumps(
                response.json(), indent=4, sort_keys=True)
            resp = json.loads(textresponse)  # sample json in data.json
            short_code = (resp['data']['short_code'])
            # Create url. E.g: outline = https://outline.com/ short_code = XF6Fvz
            outlineurl = outline + short_code
            return outlineurl
        except Exception as e:
            print(e)

    def create_archive_url(self, url):
        """[summary]

        Args:
            url ([type]): Input for archive

        Returns:
            [type]: URL from archive
        """
        try:
            print("Archive.org link is made")
            user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
            wayback = waybackpy.Url(url, user_agent)
            archive = wayback.save()
            archiveurl = archive.archive_url
            return archiveurl
        except Exception as e:
            archiveurl = " this link can't be archived. Becaus it forwards to another site!"
            print(e)
            return archiveurl

    def comment(self, outline, archive, id):
        """[summary]
            Comments the archive and outline link, if it hasn't before.
        Args:
            outline ([url]): URL from outline
            archive ([url]): URL from archive
            id ([submission.id]): submission ID to get a post
        """

        create_db(self)
        try:
            insert_db(self, id)
            reply_template = "This is a bot to create outline links " + \
                str(outline) + " and archive links " + str(archive)
            submission = reddit.submission(id=id)
            submission.reply(reply_template)
            print("Comment got posted" + ' ' +
                  "https://old.reddit.com/r/" + config.subreddit + "/comments/" + id)
        except Exception as e:
            print(e)
        else:
            pass


def create_db(self):
    """[summary]
    Checks if db exists, if not create db.
    """
    try:
        if os.path.exists("posts.db"):
            pass
        else:
            connection = sqlite3.connect("posts.db")
            cursor = connection.cursor()
            sql = "CREATE TABLE Submissions(""posts ID PRIMARY KEY)"
            cursor.execute(sql)
    except Exception as e:
        print(e)
        print("create_db")


def select_db(self, id):
    """[summary]
    Checks if the bot already commented
    Args:
        id ([id]): submissionID

    Returns:
        [bool]: If already commented return 1 otherwise 0
    """
    try:
        create_db(self)
        connection = sqlite3.connect("posts.db")
        cursor = connection.cursor()
        cursor.execute("SELECT posts from Submissions where posts=?", (id,))
        result = cursor.fetchone()
        if result:
            return 1
        else:
            return 0
    except Exception as e:
        print("select_db")
        print(e)
        pass


def insert_db(self, id):
    """[summary]
    Insert db
    Args:
        id ([id]): SubmissionID
    """
    try:
        connection = sqlite3.connect("posts.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Submissions (posts) VALUES (?)", (id,))
        connection.commit()
        connection.close()
    except Exception as e:
        print(e)
        print("insert_db")


if __name__ == "__main__":
    """[summary]
    Instance of the class and read the config data
    """
    try:
        r = Reddit()
        reddit = praw.Reddit(
            client_id=config.client_id,
            client_secret=config.client_secret,
            user_agent=config.user_agent,
            username=config.username,
            password=config.password,
        )
        r.get_submissions()
    except Exception as e:
        print(e)

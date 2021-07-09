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
        Besorgt sich alle Submissions, die noch nicht archived sind, eines spezifischen Subreddits und schaut welche per outline und welche archive.org archivierbar sind.
        Link Posts ==> outline
        Rest ==> archive.org
        """
        try:
            not_supported = ['nytimes.com', 'wsj.com',
                             'redd.it', 'youtube.com', 'youtu.be', 'imgur.com']
            for submission in reddit.subreddit("TESTFORABOT01").stream.submissions():
                time.sleep(2)
                if submission.__dict__.get('post_hint', None) == 'link':
                    if submission.archived != True:
                        if any([x in submission.url for x in not_supported]):
                            print("Diese URL wird bei Outline nicht unterstützt" +
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
                        archiveurl = self.create_archive_url(
                            submission.url)
                        self.comment(currenturl, archiveurl, submission.id)
        except Exception as e:
            print(e)

    def create_outline_url(self, url):
        """[summary]
        Erstellen von Outline Links über direkten API Zugriff.
        Dauert <1 Sekunde
        Args:
            url ([url]): Input für die URL um diese an Outline weiterzugeben

        Returns:
             [url]: Outlineurl
        """
        try:
            outline_api = "https://api.outline.com/v3/parse_article?source_url="
            escapedinputurl = urllib.parse.quote_plus(url)
            response = requests.get(outline_api + escapedinputurl)
            textresponse = json.dumps(
                response.json(), indent=4, sort_keys=True)
            resp = json.loads(textresponse)  # Beispiel json in data.json
            short_code = (resp['data']['short_code'])
            outlineurl = outline + short_code
            return outlineurl
        except Exception as e:
            print(e)

    def create_archive_url(self, url):
        """[summary]

        Args:
            url ([type]): Input für die URL um diese an Archive weiterzugeben

        Returns:
            [type]: Archiveurl
        """
        try:
            print("Archive.org Link wird erstellt")
            # user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
            # wayback = waybackpy.Url(url, user_agent)
            # archive = wayback.save()
            # archiveurl = archive.archive_url
            # return archiveurl
            archiveurl = 'TEST'
            return archiveurl
        except Exception as e:
            archiveurl = ' dieser Link kann nicht archiviert werden, da er auf eine andere Seite weiterleitet!'
            print(e)
            return archiveurl

    def comment(self, outline, archive, id):
        """[summary]
            Kommentiert einen Link zu Outline und Archive.org und zwar nur, wenn zuvor noch nicht kommentiert wurde.
        Args:
            outline ([url]): URL von Outline
            archive ([url]): URL von Archive
            id ([submission.id]): Submission ID um einen Post zu bekommen
        """
        submissions = reddit.submission(id=id)
        # for comment in submissions.comments:
        #     # https://praw.readthedocs.io/en/latest/tutorials/comments.html#extracting-comments-with-praw
        #     if isinstance(comment, MoreComments):
        #         continue
        #     if comment.author == config.botname:
        #         pass
        #     else:
        create_db(self)
        result = select_db(self, id)
        if result == 1:
            pass
        if result == 0:
            try:
                insert_db(self, id)
                reply_template = "Dies ist ein Bot für die Erstellung von Outlinelinks " + \
                    str(outline) + " und Archive Links " + str(archive)
                submission = reddit.submission(id=id)
                submission.reply(reply_template)
                print("Kommentar wurde gepostet" + ' ' +
                      "https://old.reddit.com/r/TESTFORABOT01/comments/" + id)
            except Exception as e:
                print(e)
        else:
            pass


def create_db(self):
    try:
        if os.path.exists("posts.db"):
            print("DB vorhanden")
        else:
            connection = sqlite3.connect("posts.db")
            cursor = connection.cursor()
            sql = "CREATE TABLE Submissions(""posts ID PRIMARY KEY)"
            cursor.execute(sql)
    except Exception as e:
        print(e)
        print("create_db")


def select_db(self, id):
    try:
        connection = sqlite3.connect("posts.db")
        cursor = connection.cursor()
        print(id)
        cursor.execute("SELECT posts from Submissions where posts=?", (id,))
        # cursor.execute("SELECT * from Submissions")
        result = cursor.fetchone()
        print(result)
        if result:
            return 1
        else:
            return 0
    except Exception as e:
        print("select_db")
        print(e)
        pass


def insert_db(self, id):
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
    Instanz der Klasse erzeugen und Config Daten laden
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

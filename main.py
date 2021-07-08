import praw
import config
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import waybackpy
import urllib.parse
import requests
import json
from praw.models import MoreComments
outline = 'https://outline.com/'


class Reddit:

    def get_submissions(self):
        """[summary]
        Besorgt sich alle Submissions, die noch nicht archived sind, eines spezifischen Subreddits und schaut welche per outline und welche archive.org archivierbar sind.
        Link Posts ==> outline
        Rest ==> archive.org
        """
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
                        submission.url, submission.title)
                    self.comment(currenturl, archiveurl, submission.id)

    def create_outline_url_old(self, url):
        start_old = time.time()
        """[summary]
            Läuft momentan über Selenium mit Firefox, da meine Pathvariables nicht wirklich funktionieren, ist dies über env variables gelöst.
            Da Chrome manchmal random abgestützt ist, ist nur Firefox implementiert.

            Dauert ungefähr 15 sekunden abzulaufen
        Args:
            url ([url]): Input für die URL um diese an Outline weiterzugeben
            title ([str]): Der Titel des Posts um diesen

        Returns:
            [url]: Outlineurl
        """
        concaturl = outline + url
        options = Options()
        options.headless = True
        driver = webdriver.Firefox(
            executable_path=config.geckodriver, options=options)
        driver.get(concaturl)
        time.sleep(5)
        if concaturl != driver.current_url:
            time.sleep(2)
            outlineurl = driver.current_url
            driver.close()
        end_old = time.time()
        print(end_old - start_old)
        return outlineurl

    def create_outline_url(self, url):
        """[summary]
        Erstellen von Outline Links über direkten API Zugriff.
        Dauert <1 Sekunde
        Args:
            url ([url]): Input für die URL um diese an Outline weiterzugeben

        Returns:
             [url]: Outlineurl
        """
        outline_api = "https://api.outline.com/v3/parse_article?source_url="
        escapedinputurl = urllib.parse.quote_plus(url)
        response = requests.get(outline_api + escapedinputurl)
        textresponse = json.dumps(response.json(), indent=4, sort_keys=True)
        resp = json.loads(textresponse)  # Beispiel json in data.json
        short_code = (resp['data']['short_code'])
        outlineurl = outline + short_code
        return outlineurl

    def create_archive_url(self, url, title):
        try:
            print("Archive.org Link wird erstellt")
            user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
            wayback = waybackpy.Url(url, user_agent)
            archive = wayback.save()
            archiveurl = archive.archive_url
            return archiveurl
        except Exception as e:
            print(e)
            archiveurl = ' dieser Link kann nicht archiviert werden, da er auf eine andere Seite weiterleitet!'
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
        for comment in submissions.comments:
            # https://praw.readthedocs.io/en/latest/tutorials/comments.html#extracting-comments-with-praw
            if isinstance(comment, MoreComments):
                continue
            if comment.author == config.botname:
                pass
            else:
                try:
                    reply_template = "Dies ist ein Bot für die Erstellung von Outlinelinks " + \
                        str(outline) + " und Archive Links " + str(archive)
                    submission = reddit.submission(id=id)
                    submission.reply(reply_template)
                    print("Kommentar wurde gepostet" + ' ' +
                          "https://old.reddit.com/r/TESTFORABOT01/comments/" + id)
                except Exception as e:
                    print(e)
                    pass


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

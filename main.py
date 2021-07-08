import praw
import config
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import waybackpy
import os


class Reddit:

    def get_submissions(self):
        not_supported = ['nytimes.com', 'wsj.com',
                         'redd.it', 'youtube.com', 'youtu.be', 'imgur.com']
        for submission in reddit.subreddit("TESTFORABOT01").stream.submissions():
            time.sleep(2)
            if submission.__dict__.get('post_hint', None) == 'link' and submission.archived == 'False':
                if any([x in submission.url for x in not_supported]):
                    print("Diese URL wird bei Outline nicht unterstützt" +
                          ' ' + submission.url + ' ' + submission.id)
                    currenturl = 'Diese URL wird bei Outline nicht unterstützt'
                else:
                    print('URL wird unterstützt' + ' ' + submission.url)
                    currenturl = self.create_outline_url(
                        submission.url, submission.title)
                    print(str(submission.title) + ' ' + str(submission.url))
                    #      + ' ' + str(currenturl))
                    # os.system('cls' if os.name == 'nt' else 'clear')
                    # print(currenturl)
                    # link = currenturl
                    # title = submission.title
                    # self.comment(
                    #     link, title)
                print(str(submission.title) + ' ' + str(submission.url))
                archiveurl = self.create_archive_url(
                submission.url, submission.title)
                self.comment(currenturl, archiveurl, submission.id)

    def create_outline_url(self, url, title):
        outline = 'https://outline.com/'
        concaturl = outline + url
        options = Options()
        # if random.randint(0, 1) == 0:
        options.headless = True
        driver = webdriver.Firefox(
            executable_path=config.geckodriver, options=options)
        driver.get(concaturl)
        time.sleep(10)
        if concaturl != driver.current_url:
            time.sleep(2)
            outlineurl = driver.current_url
            driver.close()
        return outlineurl

    def create_archive_url(self, url, title):
        print("Archive.org Link wird erstellt")
        user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
        wayback = waybackpy.Url(url, user_agent)
        archive = wayback.save()
        archiveurl = archive.archive_url
        print(archiveurl)
        return archiveurl

    def comment(self, link1, link2, id):
        reply_template = "Dies ist ein Bot für die Erstellung von Outlinelinks " + str(link1) + " und Archive Links" + str(link2)
        submission = reddit.submission(id=id)
        submission.reply(reply_template)
        # reddit.subreddit("TESTFORABOT01").submit(title, url=link)


if __name__ == "__main__":
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
        if os.name == "nt":
            os.system("taskkill /f /im firefox.exe")
        else:
            os.system("killall firefox")

# Reddit Bot for archiving Posts via outline.com and archive.org

I observed that some news outlets are putting some of their posts behind a paywall. Therfore some discussions on reddit will be pretty useless.

Therefore I wrote a bot that scrapes a subreddit and comments a a backup that will be made via [outline](https://outline.com) and via [archive](https://archive.org).

I tested this with the Python 3.8.10 on Windows 10 and on Ubuntu, but I think it should work on other versions as well.

To use it please create a file that looks like the sample_config.py.

To use it you have to register a script on [reddit](https://old.reddit.com/prefs/apps/).

There you can obtain the client_id and client_secret and add in the variable user_agent your username or something where you can be contacted, if the bot goes postal. In the other variables add the matching values. 


```python
pip install requirements.txt
python main.py 
```


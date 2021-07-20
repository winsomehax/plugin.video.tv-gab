import json
import pickle
import requests
from bs4 import BeautifulSoup
from cache import data_cache
import re

class Gab_episode:

    def __init__(self, url: str, title: str, thumb: str, channel:str, duration: int):
        self.page_url=url
        self.title=title
        self.thumb=thumb
        self.duration=duration
        self.channel=channel

class Gab_episode_page:

    def __init__(self, url: str, title: str, thumb: str, channel:str, duration: int):
        self.page_url=url
        self.title=title
        self.thumb=thumb
        self.duration=duration
        self.channel=channel

""" def GabLogin(username, password):

    token  = ""
    logged_in = False
    agent="tv.gab Kodi-Addon/1"

    url = "https://www.bitchute.com/accounts/login/"
    headers = {"User-Agent": agent}
    req = requests.get(url, headers=headers)

    if (req.status_code!=200):
        return None, False

    token = req.cookies["csrftoken"]
    csrfJar=req.cookies

    baseURL = "https://www.bitchute.com"
    post_data = {'csrfmiddlewaretoken': token,
                    'username': username, 'password': password}
    headers = {'Referer': baseURL + "/", 'Origin': baseURL, "User-Agent": agent}
    response = requests.post(
        baseURL + "/accounts/login/", data=post_data, headers=headers, cookies=csrfJar)

    # it's the cookies that carry forward the token/ids
    if 200 == response.status_code:
        if json.loads(response.text)['success'] == True:
            csrfJar = response.cookies
            logged_in = True

    # the cookies object has to be pickled or Kodi's cache will never recognise it as cache and keep refreshing it
    return pickle.dumps(csrfJar), logged_in
 """

""" def gab_login():
    global login_cache
    username = xbmcaddon.Addon().getSetting("user")
    password = xbmcaddon.Addon().getSetting("password")
    pickled_cookies, success = login_cache.cacheFunction(
        BitchuteLogin, username, password)

    if not success:

        login_cache.delete('%')
        data_cache.delete('%')   # clear out the login/data caches
        q = Dialog()
        q.ok("Login failed", "Unable to login to Bitchute with the details provided")

        return [], False

    cookies=pickle.loads(pickled_cookies)
    return cookies, True """


def _get_live(url):

    req = requests.get(url, cookies=None, headers={"User-Agent": "tv-gab Kodi-Addon/1"})

    soup = BeautifulSoup(req.text, "html.parser")

    sp = soup.find("video")
    thumb="https://tv.gab.com"+sp.attrs["poster"]

    duration = soup.find(id="tv-time-duration").get_text()

    channel=soup.find("h4").get_text()

    studio_player=soup.find(id="tv-player")
    data_key=studio_player.attrs["data-view-key"]
    data_episode_id=studio_player.attrs["data-episode-id"]
    title=studio_player.attrs["data-episode-title"]

    u="https://tv.gab.com/media/"+data_episode_id+"?viewKey="+data_key

    e=Gab_episode_page(url=u,title=title,thumb=thumb,channel=channel,duration=duration)
    return (pickle.dumps(e))

def _get_guide():

    guide = []
    url="https://tv.gab.com/guide"

    req = requests.get(url, cookies=None, headers={"User-Agent": "tv-gab Kodi-Addon/1"})

    entries = []
    soup = BeautifulSoup(req.text, "html.parser")

    episodes=soup.find_all(id=re.compile("^tv-episode*"))

    for e in episodes:
        url="https://tv.gab.com"+e.attrs["data-episode-url"]

        img=e.find("img")
        thumburl="https://tv.gab.com"+img.attrs["src"]
        channel=e.find("div", class_="uk-text-truncate uk-text-bold").get_text()
        #playURL=get_live(url)
        g=Gab_episode(url=url,title=e.attrs["title"], thumb=thumburl, channel=channel, duration=0)
        guide.append(g)
    
    return (pickle.dumps(guide))

# Wrappers to ensure the subs, notifications, playlists are cached for 15 minutes

def get_guide():

    global data_cache
    return pickle.loads(data_cache.cacheFunction(_get_guide))

def get_live(url):

    global data_cache
    return pickle.loads(data_cache.cacheFunction(_get_live, url))
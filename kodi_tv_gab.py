import routing
import json
import urllib3
from xbmcgui import Dialog, INPUT_ALPHANUM
import xbmcaddon
import KODIMenu as kodi_menu
import requests
from tv_gab_access import get_guide, get_live
import base64

plugin = routing.Plugin()

menu = kodi_menu.KODIMenu(plugin)


#    urls_string = requests.get('https://raw.githubusercontent.com/winsomehax/plugin.video.banned/master/banned.json')
#    return json.loads(urls_string)

#https://raw.githubusercontent.com/winsomehax/plugin.video.bitchute/master/KODIMenu.py

@plugin.route('/')
def index():

    global menu
    #eps = get_guide(page=0)
    menu.start_folder()
    menu.new_folder_item("Recommended", func=open_recommended, iconURL=None, description=None, item_val=1, label2="")
    menu.end_folder()


"""     for e in eps:

        #menu.new_folder_item(item_name=e.title, func=play, iconURL=e.thumb, description=e.title, item_val=None, label2=""):
        print("page_url", e.page_url)
        i=base64.urlsafe_b64encode(bytes(e.page_url, 'utf-8')).decode('utf-8')
        print("i ", i)

        menu.new_folder_item(item_name=e.title, func=open_item, iconURL=e.thumb, description=e.title, item_val=i, label2="")
        #menu.new_video_item(displayName=e.channel, title=e.title, description=e.title, playURL="", thumbURL=e.thumb, duration=e.duration)

    menu.end_folder()
 """
@plugin.route('/recommended/<item_val>')
def open_recommended(item_val):
    global menu
    page=int(item_val)
    eps = get_guide(page=page)
    menu.start_folder()
    if page>1:        
        menu.new_folder_item("<<<< Previous page", func=open_recommended, iconURL=None, description=None, item_val=page-1, label2="")

    for e in eps:

        #menu.new_folder_item(item_name=e.title, func=play, iconURL=e.thumb, description=e.title, item_val=None, label2=""):
        print("page_url", e.page_url)
        i=base64.urlsafe_b64encode(bytes(e.page_url, 'utf-8')).decode('utf-8')
        print("i ", i)

        menu.new_folder_item(item_name=e.title, func=open_item, iconURL=e.thumb, description=str(e.duration)+"\n"+e.channel+"\n"+e.title, item_val=i, label2="")
        #menu.new_video_item(displayName=e.channel, title=e.title, description=e.title, playURL="", thumbURL=e.thumb, duration=e.duration)

    menu.new_folder_item(">>>> Next page", func=open_recommended, iconURL=None, description=None, item_val=page+1, label2="")

    menu.end_folder()

@plugin.route('/open_item/<item_val>')
def open_item(item_val):
    global menu
    print("*** item_val", item_val, type(item_val))
    x=bytes(item_val, 'ascii')
    print("!!! x", x, type(x))

#    print(x, type(x))
    url=base64.urlsafe_b64decode(x).decode('utf-8')

    e=get_live(url)
    menu.start_folder()

    menu.new_video_item(displayName=e.channel, title=e.title, description=e.title, playURL=e.page_url, thumbURL=e.thumb, duration=e.duration)

    menu.end_folder()

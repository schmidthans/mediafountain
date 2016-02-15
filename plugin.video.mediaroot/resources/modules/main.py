# -*- coding: utf-8 -*-
#Main MediaRoot module by o9r1sh

#Imports_____________________________________________________________________________________________________________________________
import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,urlresolver,xbmc,os,xbmcaddon
from metahandler import metahandlers

from t0mm0.common.addon import Addon
from t0mm0.common.net import Net

try:
    import StorageServer
except:
    import storageserverdummy as StorageServer

import threading

class Thread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
    def run(self):
        if self._args:
            self._target(*self._args)

#Define common.addon_____________________________________________________________________________________________________________________________
addon_id = 'plugin.video.mediaroot'
addon = Addon(addon_id, sys.argv)
#print dir(addon)
#print addon.get_path()
#print "### path.join(addon.getAddonInfo('path'),'fanart.jpg')", addon.get_path()+'/artwork/main/movie.jpg'


#Define Cache for favorites_____________________________________________________________________________________________________________________________
cache = StorageServer.StorageServer("MediaRoot", 0)

#Define queries for common.addon_____________________________________________________________________________________________________________________________
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
year = addon.queries.get('year', '')
season = addon.queries.get('season', '')
episode = addon.queries.get('episode', '')
show = addon.queries.get('show', '')
types = addon.queries.get('types', '')
fanart = addon.queries.get('fanart', '')
rmode = addon.queries.get('rmode', '')
imdb_id = addon.queries.get('imdb_id', '')
host = addon.queries.get('host', '')

#Define other needed global variables_____________________________________________________________________________________________________________________________
settings = xbmcaddon.Addon(id=addon_id)
#artwork = addon.get_path()+'/artwork'
artwork = 'https://raw.githubusercontent.com/schmidthans/mediafountain/master/plugin.video.mediaroot/resources/artwork'
grab=metahandlers.MetaData()
net = Net()
net.set_user_agent('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0')

def resolvable(url):
    status = False
    hmf = urlresolver.HostedMediaFile(url)
    if hmf:
       status = True

    if 'uploadcrazy' in url:
       status = True

    if 'vidcrazy' in url:
       status = True

    if 'vidx.to' in url:
       status = True

    if 'epornik' in url:
       status = True

    if 'video44' in url:
       status = True

    if 'play44' in url:
       status = True

    if 'cheesestream' in url:
       status = True

    if 'flashx' in url:
       status = True

    if 'paradisehill' in url:
       status = True

    if 'streamcloud' in url:
       status = True

    if 'played' in url:
       status = True

    if 'spankbang' in url:
       status = True

    return(status)

def getHost(url, disk=''):
    host = None
    hmf = urlresolver.HostedMediaFile(url)
    if hmf:
       host = hmf.get_host()
       hosterstring = re.search('//(www.|)(.+?)\..+?/', url)
       host = hosterstring.group(2)

    if 'vidcrazy' in url:
       host = 'vidcrazy'

    if 'vidx.to' in url:
       host = 'vidx'

    if 'epornik' in url:
       host = 'epornik'

    if 'video44' in url:
       host = 'video44'

    if 'play44' in url:
       host = 'play44'

    if 'cheesestream' in url:
       host = 'cheesestream'

    if 'uploadc' in url:
       host = 'uploadc'

    if 'filefactory' in url:
       host = 'filefactory'

    if 'go4up' in url:
       host = 'go4up'

    if 'netload' in url:
       host = 'netload'

    if 'turbobit' in url:
       host = 'turbobit'

    if 'uploaded' in url:
       host = 'uploaded'

    if 'videobam' in url:
       host = 'videobam'

    if 'mixturecloud' in url:
       host = 'mixturecloud'

    if 'nowvideo' in url:
       host = 'nowvideo'

    if 'uploadcrazy' in url:
       host = 'uploadcrazy'

    if 'ul.to' in url:
       host = 'uploaded'

    if 'bitshare' in url:
       host = 'bitshare'

    if 'flashx' in url:
       host = 'flashx'

    if 'paradisehill' in url:
       host = 'paradisehill' + disk

    if 'streamcloud' in url:
       host = 'streamcloud'

    if 'played' in url:
       host = 'played'

    if 'spankbang' in url:
       host = 'spankbang'

    if 'rapidvideo' in url:
       host = 'rapidvideo'

    if host == None:
        host = url

    if host.endswith('.com'):
       host = host[:-4]
    if host.endswith('.com/'):
       host = host[:-5]
    if host.endswith('.org'):
       host = host[:-4]
    if host.endswith('.eu'):
       host = host[:-3]
    if host.endswith('.ch'):
       host = host[:-3]
    if host.endswith('.in'):
       host = host[:-3]
    if host.endswith('.es'):
       host = host[:-3]
    if host.endswith('.tv'):
       host = host[:-3]
    if host.endswith('.net'):
       host = host[:-4]
    if host.endswith('.me'):
       host = host[:-3]
    if host.endswith('.ws'):
       host = host[:-3]
    if host.endswith('.sx'):
       host = host[:-3]
    if host.startswith('www.'):
      host = host[4:]
    if host.startswith('http://'):
      host = host[7:]
    if host.startswith('https://'):
      host = host[8:]

    host = host.title()

    return(host)

def nameCleaner(name):
       name = name.replace('&#8211;','')
       name = name.replace("&#8217;","")
       return(name)
    
#Functions for handling favorites_____________________________________________________________________________________________________________________________
def addFavorite():
    saved_favs = cache.get('favourites_' + types)
    favs = []
    if saved_favs:
       favs = eval(saved_favs)
       if favs:
          if (name, url ,rmode, thumb, show, year, season, episode) in favs:
             addon.show_small_popup(title='Item Already In Favorites', msg=name + ' Is Already In Your Favorites', delay=int(5000), image=thumb)
             return
    favs.append((name, url ,rmode, thumb, show, year, season, episode))       
    cache.set('favourites_' + types, str(favs))
    addon.show_small_popup(title='Item Added To Favorites', msg=name + ' Was Added To Your Favorites', delay=int(5000), image=thumb)

def removeFavorite():
    saved_favs = cache.get('favourites_' + types)
    if saved_favs:
      favs = eval(saved_favs)
      favs.remove((name, url ,rmode, thumb, show, year, season, episode))   
      cache.set('favourites_' + types, str(favs))
      xbmc.executebuiltin("XBMC.Container.Refresh")

def getFavorites(url):
    if url == 'movie':
       saved_favs = cache.get('favourites_' + 'movie')
       if saved_favs:
          favs = sorted(eval(saved_favs), key=lambda fav: fav[1])
          for fav in favs:
                addMDir(fav[0], fav[1] ,fav[2], fav[3], fav[4], True)
       AUTOVIEW('movies')

    elif url == 'tvshow':
       saved_favs = cache.get('favourites_' + 'tvshow')
       if saved_favs:
          favs = sorted(eval(saved_favs), key=lambda fav: fav[1])
          for fav in favs:
                addSDir(fav[0], fav[1] ,fav[2], fav[3], True)
             
       AUTOVIEW('tvshows')

    elif url == 'cartoon':
       saved_favs = cache.get('favourites_' + 'cartoon')
       if saved_favs:
          favs = sorted(eval(saved_favs), key=lambda fav: fav[1])
          for fav in favs:
                addToonDir(fav[0], fav[1] ,fav[2], fav[3], True)
             
       AUTOVIEW('tvshows')

    elif url == 'anime':
       saved_favs = cache.get('favourites_' + 'anime')
       if saved_favs:
          favs = sorted(eval(saved_favs), key=lambda fav: fav[1])
          for fav in favs:
                addAnimeDir(fav[0], fav[1] ,fav[2], fav[3], True)
             
       AUTOVIEW('tvshows')

#Metadata Function_____________________________________________________________________________________________________________________________    
def getMeta(types,name,year,show,season,episode):
    show_meta = 0
    meta = 0
    if types=='movie':
       meta = grab.get_meta('movie',name,year)
    elif types=='tvshow':
       meta = grab.get_meta('tvshow',name)
    elif types=='episode':
       try:
          show_meta = grab.get_meta('tvshow',show)
       except:
          show_meta = 0
       if show_meta == 0:
          return 0
       else:
          imdb_id = show_meta['imdb_id']
          meta = grab.get_episode_meta(show,imdb_id,season,episode)
    return(meta)

#Directory Functions_____________________________________________________________________________________________________________________________

#Standard directory funtion to be used when not doing scrapes on the directory_____________________________________________________________________________________________________________________________
def addDir(name,url,mode,thumb):
    name = nameCleaner(name)
    if thumb == '':
       thumb = artwork + '/main/noepisode.png'
    params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'year':year, 'types':'movie'}
    addon.add_directory(params, {'title':name}, img= thumb, fanart= artwork + '/main/fanart.jpg')

#Movie directory function to be used when adding a movie, all metadata scrapes and context menu items are handled within_____________________________________________________________________________________________________________________________
def addMDir(name,url,mode,thumb,year,isfav):
    name = nameCleaner(name)
    meta = {}
    contextMenuItems = []

    title = re.split('\d\d\d\d',name)

    if title[0] == '':
       title = name
    if settings.getSetting('metadata') == 'true':
       meta = getMeta('movie',title[0],year,'','','')
    year = re.sub('[()]','',year)
    if year == '':
       try:
          year = meta['year']
       except:
          year = ''
    if year == 0:
       year = ''
    if settings.getSetting('metadata') == 'true':

        if year == '':
            meta['title'] = name

        else:
            meta['title'] = name + ' ' + '(' + str(year) + ')'
    
        if thumb == '':
            thumb = meta['cover_url']

        if meta['backdrop_url'] == '':
               fanart = artwork + '/main/fanart.jpg'
        else:
               fanart = meta['backdrop_url']
               
    params = {'url':url, 'mode':mode, 'name':title[0], 'thumb':thumb, 'year':year, 'types':'movie'}

    if isfav == False:
        contextMenuItems.append(('Add To MediaRoot Favourites', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'addFavorite', 'name':name, 'thumb':thumb, 'year':year, 'types':'movie', 'rmode':mode})))

    elif isfav == True:
        contextMenuItems.append(('Remove From MediaRoot Favourites', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'removeFavorite', 'name':name, 'thumb':thumb, 'year':year, 'types':'movie', 'rmode':mode})))

    contextMenuItems.append(('Movie Information', 'XBMC.Action(Info)'))
    
    if os.path.exists(xbmc.translatePath("special://home/addons/plugin.video.collective")):
                    contextMenuItems.append(('Search The Collective', 'XBMC.Container.Update(%s?mode=51&url=url&name=%s)' % ('plugin://plugin.video.collective/', name)))
    if settings.getSetting('metadata') == 'true':
        addon.add_directory(params, meta, contextMenuItems, img= thumb, fanart=fanart)
    else:
        addon.add_directory(params, {'title':name},contextMenuItems, img=thumb, fanart= artwork + '/main/fanart.jpg')

#TV Show directory function to be used when adding a TV Show, all metadata scrapes and context menu items are handled within__________
def addSDir(name,url,mode,thumb,isfav):
    name = nameCleaner(name)
    contextMenuItems = []
    meta = {}
    
    params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'year':year, 'types':types, 'show':name}

    if settings.getSetting('metadata') == 'true':
        meta = grab.get_meta('tvshow',name)
        if meta['backdrop_url'] == '':
            fanart = artwork + '/main/fanart.jpg'
        else:
            fanart = meta['backdrop_url']
    else:
        fanart = artwork + '/main/fanart.jpg'
        

    if settings.getSetting('metadata') == 'true':
            if settings.getSetting('banners') == 'false':
                if thumb == '':
                    thumb = meta['cover_url']
            else:
                thumb = meta['banner_url']
    if thumb == '':
        thumb = artwork + '/main/noepisode.png'
    
    contextMenuItems.append(('Show Information', 'XBMC.Action(Info)'))

    if isfav == False:
        contextMenuItems.append(('Add To MediaRoot Favourites', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'addFavorite', 'name':name, 'thumb':thumb, 'types':'tvshow', 'rmode':mode})))

    if isfav == True:
        contextMenuItems.append(('Remove From MediaRoot Favourites', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'removeFavorite', 'name':name, 'thumb':thumb, 'types':'tvshow', 'rmode':mode})))


    if os.path.exists(xbmc.translatePath("special://home/addons/plugin.video.collective")):
                    contextMenuItems.append(('Search The Collective', 'XBMC.Container.Update(%s?mode=52&url=url&name=%s)' % ('plugin://plugin.video.collective/', name)))
    if settings.getSetting('metadata') == 'true':
        addon.add_directory(params, meta, contextMenuItems, img=thumb, fanart=fanart)
    else:
        addon.add_directory(params, {'title':name}, contextMenuItems, img= thumb, fanart=fanart)

#Cartoon directory function to be used when adding a Cartoon Series, all metadata scrapes and context menu items are handled within___
def addToonDir(name,url,mode,thumb,isfav):
    name = nameCleaner(name)
    contextMenuItems = []
    meta = {}
    
    params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'year':year, 'types':'cartoon', 'show':name}

    if settings.getSetting('metadata') == 'true':
        meta = grab.get_meta('tvshow',name)
        if meta['backdrop_url'] == '':
            fanart = artwork + '/main/fanart.jpg'
        else:
            fanart = meta['backdrop_url']
    else:
        fanart = artwork + '/main/fanart.jpg'
        
    
    if settings.getSetting('metadata') == 'true':
            if settings.getSetting('banners') == 'false':
                if thumb == '':
                    thumb = meta['cover_url']
            else:
                thumb = meta['banner_url']
    if thumb == '':
        thumb = artwork + '/main/noepisode.png'
    
    contextMenuItems.append(('Show Information', 'XBMC.Action(Info)'))

    if isfav == False:
        contextMenuItems.append(('Add To MediaRoot Favourites', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'addFavorite', 'name':name, 'thumb':thumb, 'types':'cartoon', 'rmode':mode})))

    if isfav == True:
        contextMenuItems.append(('Remove From MediaRoot Favourites', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'removeFavorite', 'name':name, 'thumb':thumb, 'types':'cartoon', 'rmode':mode})))


    if os.path.exists(xbmc.translatePath("special://home/addons/plugin.video.collective")):
                    contextMenuItems.append(('Search The Collective', 'XBMC.Container.Update(%s?mode=52&url=url&name=%s)' % ('plugin://plugin.video.collective/', name)))
    if settings.getSetting('metadata') == 'true':
        addon.add_directory(params, meta, contextMenuItems, img=thumb, fanart=fanart)
    else:
        addon.add_directory(params, {'title':name},contextMenuItems , img= thumb, fanart=fanart)

#Anime directory function to be used when adding a Anime Series, all metadata scrapes and context menu items are handled within______
def addAnimeDir(name,url,mode,thumb, isfav):
    name = nameCleaner(name)
    contextMenuItems = []
    meta = {}
    
    params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'year':year, 'types':'anime', 'show':name}

    if settings.getSetting('metadata') == 'true':
        meta = grab.get_meta('tvshow',name)
        if meta['backdrop_url'] == '':
            fanart = artwork + '/main/fanart.jpg'
        else:
            fanart = meta['backdrop_url']
    else:
        fanart = artwork + '/main/fanart.jpg'

    if settings.getSetting('metadata') == 'true':
        if meta['backdrop_url'] == '':
            fanart = artwork + '/main/fanart.jpg'
        else:
            fanart = meta['backdrop_url']
    
    if settings.getSetting('metadata') == 'true':
            if settings.getSetting('banners') == 'false':
                if thumb == '':
                    thumb = meta['cover_url']
            else:
                thumb = meta['banner_url']
    if thumb == '':
        thumb = artwork + '/main/noepisode.png'
    
    contextMenuItems.append(('Show Information', 'XBMC.Action(Info)'))

    if isfav == False:
        contextMenuItems.append(('Add To MediaRoot Favourites', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'addFavorite', 'name':name, 'thumb':thumb, 'types':'anime', 'rmode':mode})))

    if isfav == True:
        contextMenuItems.append(('Remove From MediaRoot Favourites', 'XBMC.RunPlugin(%s)' % addon.build_plugin_url({'url':url, 'mode':'removeFavorite', 'name':name, 'thumb':thumb, 'types':'anime', 'rmode':mode})))


    if os.path.exists(xbmc.translatePath("special://home/addons/plugin.video.collective")):
                    contextMenuItems.append(('Search The Collective', 'XBMC.Container.Update(%s?mode=52&url=url&name=%s)' % ('plugin://plugin.video.collective/', name)))
    if settings.getSetting('metadata') == 'true':
        addon.add_directory(params, meta, contextMenuItems, img=thumb, fanart=fanart)
    else:
        addon.add_directory(params, {'title':name},contextMenuItems, img= thumb, fanart=fanart)

#Host directory function to be used when adding a file Host, hthumb stands for host thumb and should be grabbed using the 'GETHOSTTHUMB(host)' function before hand
def addHDir(name,url,mode,thumb, disk=''):
    host = getHost(url, disk)
    if thumb == '':
        thumb = GETHOSTTHUMB(host)
    fanart = artwork + '/main/fanart.jpg'
    name = re.sub('[()]','',name)
    params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'year':year, 'types':types, 'season':season, 'episode':episode, 'show':show}
    addon.add_directory(params, {'title':host}, img=thumb, fanart=fanart)

#Episode directory function to be used when adding a Episode, all metadata scrapes and context menu items are handled within_________
def addEDir(name,url,mode,thumb,show):
    name = nameCleaner(name)
    ep_meta = None
    show_id = None
    meta = None
    othumb = thumb
             
    if settings.getSetting('metadata') == 'true':
        meta = grab.get_meta('tvshow',show)
        show_id = meta['imdb_id']

    else:
        fanart = artwork + '/main/fanart.jpg'
    
    s,e = GET_EPISODE_NUMBERS(name)

    if settings.getSetting('metadata') == 'true':
        try:
            ep_meta = grab.get_episode_meta(show,show_id,int(s),int(e))
            if ep_meta['cover_url'] == '':
                thumb = artwork + '/main/noepisode.png'
            else:
                thumb = str(ep_meta['cover_url'])
        except:
            ep_meta=None
            thumb = artwork + '/main/noepisode.png'
           
    else:
        thumb = othumb
        if thumb == '':
            thumb = artwork + '/main/noepisode.png'
    
    params = {'url':url, 'mode':mode, 'name':name, 'thumb':thumb, 'season':s, 'episode':e, 'show':show, 'types':'episode'}       
    if settings.getSetting('metadata') == 'true':

        if ep_meta==None:
            fanart = artwork + '/main/fanart.jpg'
            addon.add_directory(params, {'title':name}, img=thumb, fanart=fanart) 
        else:
            if meta['backdrop_url'] == '':
                fanart = artwork + '/main/fanart.jpg'
            else:
                fanart = meta['backdrop_url']
            ep_meta['title'] = name
            addon.add_directory(params, ep_meta, fanart=fanart, img=thumb)
    else:
        addon.add_directory(params, {'title':name},fanart=fanart, img=thumb) 

#Called within the addEDir function, returns needed season and episode numbers needed for metadata scraping___________________________

def GET_EPISODE_NUMBERS(ep_name):
    s = None
    e = None
    ep_name = re.sub('×','X',ep_name)

    S00E00 = re.findall('[Ss]\d\d[Ee]\d\d',ep_name)
    SXE = re.findall('\d[Xx]\d',ep_name)
    SXEE = re.findall('\d[Xx]\d\d',ep_name)
    SXEEE = re.findall('\d[Xx]\d\d\d',ep_name)

    SSXE = re.findall('\d\d[Xx]\d',ep_name)
    SSXEE = re.findall('\d\d[Xx]\d\d',ep_name)
    SSXEEE = re.findall('\d\d[Xx]\d\d\d',ep_name)
    
    if S00E00:
        print 'Naming Style Is S00E00'
        S00E00 = str(S00E00)
        S00E00.strip('[Ss][Ee]')
        S00E00 = S00E00.replace("u","")
        e = S00E00[-4:]
        e = e[:-2]
        s = S00E00[:5]
        s = s[-2:]
        
    if SXE:
        print 'Naming Style Is SXE'
        SXE = str(SXE)
        SXE = SXE.replace("u","")
        print 'Numer String is ' + SXE
        s = SXE[2]
        e = SXE[4]

    if SXEE:
        print 'Naming Style Is SXEE'
        SXEE = str(SXEE)
        SXEE = SXEE.replace("u","")
        print 'Numer String is ' + SXEE
        s = SXEE[2]
        e = SXEE[4] + SXEE[5]

    if SXEEE:
        print 'Naming Style Is SXEEE'
        SXEEE = str(SXEEE)
        SXEEE = SXEEE.replace("u","")
        print 'Numer String is ' + SXEEEE
        s = SXEEE[2]
        e = SXEEE[4] + SXEEE[5] + SXEEE[6]

    if SSXE:
        print 'Naming Style Is SSXE'
        SSXE = str(SSXE)
        SSXE = SSXE.replace("u","")
        print 'Numer String is ' + SSXE
        s = SSXE[2] + SSXE[3]
        e = SSXE[5]

    if SSXEE:
        print 'Naming Style Is SSXEE'
        SSXEE = str(SSXEE)
        SSXEE = SSXEE.replace("u","")
        print 'Numer String is ' + SSXEE
        s = SSXEE[2] + SSXEE[3]
        e = SSXEE[5] + SSXEE[6]

    if SSXEEE:
        print 'Naming Style Is SSXEEE'
        SSXEEE = str(SSXEEE)
        SSXEEE = SSXEEE.replace("u","")
        print 'Numer String is ' + SSXEEE
        s = SSXEEE[2] + SSXEE[3]
        e = SSXEEE[5] + SSXEEE[6] + SSXEEE[7]

    return s,e

#Returns the host thumbnail so that you can pass it as and argument to the addHDir function__________________________________________
def GETHOSTTHUMB(host):
    if host.endswith('.com'):
        host = host[:-4]
    if host.endswith('.org'):
        host = host[:-4]
    if host.endswith('.eu'):
        host = host[:-3]
    if host.endswith('.ch'):
        host = host[:-3]
    if host.endswith('.in'):
        host = host[:-3]
    if host.endswith('.es'):
        host = host[:-3]
    if host.endswith('.tv'):
        host = host[:-3]
    if host.endswith('.net'):
        host = host[:-4]
    if host.endswith('.me'):
        host = host[:-3]
    if host.endswith('.ws'):
        host = host[:-3]
    if host.endswith('.sx'):
        host = host[:-3]
    if host.startswith('www.'):
           host = host[4:]
    if 'movzap' in host:
        host = 'movzap'

    if 'go4up' in host:
        host = 'go4up'

    if 'uploadcrazy' in host:
        host = 'uploadcrazy'

    if 'vidcrazy' in host:
        host = 'vidcrazy'

    if 'epornik' in host:
        host = 'epornik'

    if host == '':
        host = 'nowvideo'
    
    host = artwork + '/hosts/' + host +'.png'
    host = host.lower()
    return(host)

#Function used for resolving video urls before  playback_____________________________________________________________________________    
def RESOLVE(name,url,thumb):
    meta=0
    try:
        meta = getMeta(types,name,year,show,season,episode)
    except:
        meta=0
    hmf = urlresolver.HostedMediaFile(url)
    host = ''
    if 'openload' in url:
        url = OPENLOAD(url)
    elif hmf:
        url = urlresolver.resolve(url)
        host = hmf.get_host()
    else:
        url = OTHER_RESOLVERS(url)

    params = {'url':url, 'name':name, 'thumb':thumb}
    if meta == 0:
        addon.add_video_item(params, {'title':name}, img=thumb)
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=thumb)

    else:
        addon.add_video_item(params, {'title':name}, img=meta['cover_url'])
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=meta['cover_url'])
        liz.setInfo('video',infoLabels=meta)
    if str(type(url)) == "<type 'instance'>" or url == False:
        xbmc.executebuiltin("Notification('ERROR','File Not Found or removed')")
        print "error not found"
        dialog = xbmcgui.Dialog()
        #dialog.notification('Movie Trailers', 'Finding Nemo download finished.', xbmcgui.NOTIFICATION_INFO, 5000)
        dialog.select('Error message', ['File Not Found or removed'], 5000)
        #dialog.ok(" Error message ", " File Not Found or removed ")
        #xbmc.sleep(1000)
        #xbmc.Player ().play(url, liz, False)
    else:
        #xbmc.Notification(header,message["################# ERROR",5,None])
        xbmc.sleep(1000)
        xbmc.Player ().play(url, liz, False)

#Used to resolve urls that urlresolver doesn't support________________________________________________________________________________
def OPENLOAD(url):
    link = url
    embed = re.search('http[s]?://openload\...\/f\/(.*?)\/', link, re.S)
    if embed:
        link = 'https://openload.co/embed/' + embed.group(1)
    result = net.http_GET(link).content
    parse = re.search('videocontainer.*?text/javascript">(.*?);</script>', result, re.S)
    if parse:
        dataout = ''
        todecode = parse.group(1).split(';')
        todecode = todecode[-1].replace(' ','')

        code = {
            "(ﾟДﾟ) [1]" : "f",
            "(ﾟДﾟ) [c]" : "c",
            "(ﾟДﾟ) [constructor]" : '"',
            "(ﾟДﾟ)[ﾟoﾟ]" : "o",
            "(ﾟДﾟ) [return]" : "\\",
            "(ﾟДﾟ) [ ﾟΘﾟ]" : "_",
            "(ﾟДﾟ) [ ﾟΘﾟﾉ]" : "b",
            "(ﾟДﾟ) [ ﾟωﾟﾉ]" : "a",
            "(ﾟДﾟ) [ ﾟДﾟﾉ]" : "e",
            "(ﾟДﾟ) [ﾟｰﾟﾉ]" : "d",
            "(ﾟДﾟ) ['_']"  : "Function()",
            "(ﾟДﾟ)[ﾟεﾟ]": "/",
            "(ﾟｰﾟ)": "4",
            "(c^_^o)": "0",
            "(o^_^o)": "3",
            "c": "0",
            "o": "3",
            "ol": "undefined",
            "oﾟｰﾟo": "u",
            "ﾟoﾟ": "constructor",
            "(ﾟΘﾟ)": "1",
            "ﾟεﾟ": "return",
            "ﾟωﾟﾉ": "undefined",
            "_": "3",
            }

        try:
            todecode = todecode.encode('utf-8')
            for searchword,isword in code.iteritems():
                todecode = todecode.replace(searchword,isword)
            todecode = todecode.replace('!+[]','1').replace('-~','1+').replace('[]','0')
            todecode = re.sub(r'\((\d)\+(\d)\)', lambda m: '{0}'.format(int(m.group(1)) + int(m.group(2))), todecode.replace(" ","")).replace(" ","")
            todecode = re.sub(r'\((\d)\^(\d)\^(\d)\)', lambda m: '{0}'.format(int(m.group(1)) ^ int(m.group(2))^ int(m.group(3))), todecode).replace(" ","")
            todecode = re.sub(r'\((\d)\+(\d)\)', lambda m: '{0}'.format(int(m.group(1)) + int(m.group(2))), todecode).replace(" ","")
            todecode = re.sub(r'\((\d)\-(\d)\)', lambda m: '{0}'.format(int(m.group(1)) - int(m.group(2))), todecode).replace(" ","")
            todecode = re.sub(r'\((\d)\+(\d)\+(\d)\)', lambda m: '{0}'.format(int(m.group(1)) + int(m.group(2))+ int(m.group(3))), todecode).replace(" ","")
            todecode = re.sub(r'\((\d)\-(\d)\+(\d)\)', lambda m: '{0}'.format(int(m.group(1)) - int(m.group(2))+ int(m.group(3))), todecode).replace(" ","")
            todecode = re.sub(r'\((\d)\+(\d)\-(\d)\)', lambda m: '{0}'.format(int(m.group(1)) + int(m.group(2))- int(m.group(3))), todecode).replace(" ","")

            thestring =  re.search("return3(.*?)\'\d\'", todecode.replace("+","").replace(")","").replace("(",""))
            if thestring:
                items = thestring.group(1).split("/")
                for charcode in items:
                    if charcode:
                        if int(charcode) < 256:
                            dataout += chr(int(charcode, 8))
                url = re.search('window.vr=\'(http.*?)\'', dataout)
                if url:
                    return str(url.group(1))

        except Exception as e:
            print "ERROR parsing openload code"

def OTHER_RESOLVERS(url):
    if 'uploadcrazy' in url:
        link = net.http_GET(url).content
        links=re.compile("file': '(.+?)'").findall(link)
        if len(links) > 0:
                url = links[0]

    if 'vidcrazy' in url:
        link = net.http_GET(url).content
        links=re.compile("file': '(.+?)'").findall(link)
        if len(links) > 0:
                url = links[0]

    if 'animeonair' in url:
        link = net.http_GET(url).content
        links=re.compile("file': '(.+?)'").findall(link)
        if len(links) > 0:
                url = links[0]

    if 'epornik' in url:
        link = net.http_GET(url).content
        links=re.compile('s1.addVariable(.+?);').findall(link)
        dirty = re.sub("[',)(]", '', (links[5]))
        url =   dirty[7:-1]

    if 'video44' in url:
        url = url.replace('&#038;','&')
        link = net.http_GET(url).content
        match=re.compile('file: "(.+?)"').findall(link)
        url = match[0]

    if 'play44' in url:
        url = url.replace('&#038;','&')
        link = net.http_GET(url).content
        match=re.compile("\n\t\t\t\t\t\t\t\t\t\t\t\turl: \'(.+?)'").findall(link)
        url = match[0]
        url = url.replace('%2F','/')
        url = url.replace('%3F','?')
        url = url.replace('%3D','=')
        url = url.replace('%26','&')

    if 'cheesestream' in url:
        link = net.http_GET(url).content
        match=re.compile('<source src="(.+?)"').findall(link)
        url = match[0]

#     if 'flashx' in url and 'embed_player' in url:
#         link = net.http_GET(url).content
#         yes=re.compile('name="yes".*?value="(.+?)"').findall(link)
#         sec=re.compile('name="sec".*?value="(.+?)"').findall(link)
#         if yes and sec:
#            dataPost = {'yes': yes[0], 'sec': sec[0]}
#            data1=net.http_POST('http://play.flashx.tv/player/player.php', dataPost).content
#            if data1:
#               player=re.compile('value="(http://.+?\.flashx.tv/nuevo/player/.+?\.swf.*?)"').findall(data1)
#               if player:
#                  data2 = net.http_GET(player[0], {'Content-Type':'application/x-www-form-urlencoded', 'Referer': 'http://play.flashx.tv/player/player.php'}).content
#                  if data2:
#                     playerurl = player[0].split('config=')
#                     data3 = net.http_GET(playerurl[1],{'Referer': player[0]} ).content
#                     if data3:
#                         stream_url=re.compile('<file>(.+?)</file>').findall(data3)
#                         if stream_url:
#                            url=stream_url[0]
#                         else:
#                            print "flashx data2 steam not found"
#               else:
#                  print "flashx player not found"
#            else:
#               print "flashx data1 not found"
#         else:
#            print "flashx no yes and sec found"

    return str(url)

#Sets the desired view type___________________________________________________________________________________________________________    
def AUTOVIEW(content):
       if content:
             xbmcplugin.setContent(int(sys.argv[1]), content)
             if settings.getSetting('auto-view') == 'true':
                    if content == 'movies':
                          xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('movies-view'))
                    elif content == 'tvshows':
                          xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('shows-view'))
                    elif content == 'episodes':
                          xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('episodes-view'))     
                    else:
                          xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('default-view'))
             else:
                    xbmc.executebuiltin("Container.SetViewMode(%s)" % settings.getSetting('default-view') )

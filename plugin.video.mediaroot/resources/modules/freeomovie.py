#FreeMoviesAddict Module by o9r1sh September 2013, changer by mediafountain 2015-05

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os
import urlresolver

from t0mm0.common.net import Net
net = Net()

artwork = main.artwork
base_url = 'http://www.freeomovie.com'
settings = main.settings

def CATEGORIES():
        main.addDir('Search','none','freeOMovieSearch',artwork + '/main/search.png')
        main.addDir('Recent Videos',base_url,'freeOMovieIndex',artwork + '/main/recentvideos.png')
        main.addDir('Full Movies',base_url,'freeOMovieIndex',artwork + '/main/movie.png')
        main.addDir('Categories','none','freeOMovieGenres',artwork + '/main/categories.png')

def GENRES():
        url = base_url
        link = net.http_GET(url).content
        genre=re.compile('<li><a href="(.+?)" rel="tag">(.+?)</a></li>', re.S).findall(link)
        if genre:
            for (phUrl, phTitle) in genre:
                try: 
                    main.addDir(phTitle,phUrl,'freeOMovieIndex',artwork + '/main/video.png')
                except:
                    continue

def INDEX(url):
        np_url = ''
        link = net.http_GET(url).content
        match=re.compile('class="boxtitle">.+?<a href="(.+?)".+?title="(.+?)".+?<img src="(.+?)"', re.S).findall(link)
        np=re.compile("<link rel='next' href='(.+?)'/>").findall(link)
        if len(np) > 0:
                np_url = np[0]
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',np_url,'freeOMovieIndex',artwork + '/main/next.png')
        for url,name,thumbnail in match:
                name = name.encode('UTF-8')
                try:
                        main.addDir(name,url,'freeOMovieVideoLinks',thumbnail)
                except:
                        continue
        if len(np) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',np_url,'freeOMovieIndex',artwork + '/main/next.png')
        main.AUTOVIEW('movies')

def VIDEOLINKS(name,url,thumb):
        
        link = net.http_GET(url).content
        match=re.compile('class="videosection">(.+?)class="textsection">', re.S).search(link)
        match1=re.compile('(http[s]?://.+?\/.*?)[\'|"|\&|<]', re.S).findall(match.group(0))
        for url in match1:
                if main.resolvable(url):
                        try:
                                main.addHDir(name,url,'resolve','')
                        except:
                                continue

def SEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = search.replace(' ','+')
                
                url = base_url + '/?s=' + search 
                INDEX(url)
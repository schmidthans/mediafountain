##Pornmvz Module by mediafountain 2015-05
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os,cgi
import urlresolver

from t0mm0.common.net import Net
net = Net()

artwork = main.artwork
base_url = 'http://pornmvz.com'
settings = main.settings

def CATEGORIES():
        main.addDir('Search','none','pornmvzSearch',artwork + '/main/search.png')
        main.addDir('Newest Videos',base_url +'/','pornmvzIndex',artwork + '/main/recentvideos.png')
        link = net.http_GET(base_url).content
        match=re.compile('>Categories<(.+?)</div>', re.S).findall(link)
        if match:
            match1=re.compile('<a href="(.+?)">(.+?)<', re.S).findall(match[0])
            if len(match1) > 0:
                for (Url, Title) in match1:
                    main.addDir(Title, Url,'pornmvzIndex',artwork + '/main/video.png')

def INDEX(url):
        next_page = ''
        link = net.http_GET(url).content
        match=re.compile('<div class="respl-item.+?<a href="http://pornmvz.com/(.+?)"\s+title="(.+?)"\s>.+?src="(.+?)"', re.S).findall(link)
        np=re.compile('<li class="selected">.+?<li class="page"><a href="http://pornmvz.com/(.+?paged=.+?)">').findall(link)
        if len(np) > 0:
                npc = str(np[0]).replace('&#038;','&').replace('&amp;','&')
                next_page = base_url + "/" + npc
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'pornmvzIndex',artwork + '/main/next.png')
        for url,name,thumbnail in match:
                        url = base_url + "/" + url
                        try: 
                                main.addDir(name,url,'pornmvzVideoLinks',thumbnail)
                        except:
                                continue
        if len(np) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'pornmvzIndex',artwork + '/main/next.png')
        main.AUTOVIEW('movies')

def VIDEOLINKS(name,url,thumb):
        streamcounter = 0
        newList =[]
        link = net.http_GET(url).content
        match=re.compile('class="itemFullText">(.+?)id="content_right"', re.S).findall(link)
        match1=re.compile('(http[s]?://(.*?)\/.*?)[\'|"|\&|<]').findall(match[0])
        for url,hoster in match1:
            url = str(url).replace('&#038;','&').replace('&amp;','&')
            if main.resolvable(url):
                #hmf = urlresolver.HostedMediaFile(url)
                streamcounter += 1
                newList.append((name, url, hoster,'resolve',thumb))
        if streamcounter == 1:
            main.RESOLVE(newList[0][0],newList[0][1],newList[0][3])
        elif newList:
            for name,url, hoster, resolve,thumb in newList:
                try:
                    main.addHDir(name,url,resolve,thumb)
                except:
                    pass

def SEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = search.replace(' ','+')
                
                url = base_url + '/?s=' + search
                
                INDEX(url)

def MASTERSEARCH(search):
        url = base_url + '/?s=' + search
        INDEX(url)
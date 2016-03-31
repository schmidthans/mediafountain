##xxxstreams Module by mediafountain 2016-02
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os,cgi
import urlresolver

from t0mm0.common.net import Net
net = Net()

artwork = main.artwork
base_url = 'http://xxxstreams.org'
settings = main.settings
net.set_user_agent('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0')

def CATEGORIES():
    main.addDir('Search','none','xxxstreamsSearch',artwork + '/main/search.png')
    main.addDir('Newest Videos',base_url +'/new-porn-streaming/page/0','xxxstreamsIndex',artwork + '/main/recentvideos.png')
    main.addDir('Full Movies',base_url +'/full-movies-streaming/page/0','xxxstreamsIndex',artwork + '/main/recentvideos.png')
    main.addDir('HD',base_url +'/tag/hd/page/0','xxxstreamsIndex',artwork + '/main/recentvideos.png')
    link = net.http_GET(base_url).content
    match1=re.compile('menu-item menu-item-type-(taxonomy|custom).*?<a href=[\'|"](http://xxxstreams.org.+?)[\'|"]\s*>(.+?)<', re.S).findall(link)
    if len(match1) > 0:
        cat = []
        for (x, Url, Title) in match1:
            Title = Title.encode('utf-8')
            cat.append((Title, Url,'xxxstreamsIndex',artwork + '/main/video.png'))
        cat.sort(key=lambda t : t[0].lower())
        for item in cat:
            main.addDir(*item)

def INDEX(url):
    next_page = ''
    link = net.http_GET(url).content
    match=re.compile('content-area">(.+?)<h1 class="screen-reader-text"', re.S).findall(link)
    if match:
        match1=re.compile('"entry-title"><a href="(.+?)" rel="bookmark">(.*?)<.*?<div class="entry-(summary|content)">\s*<p>(.+?)</div>', re.S).findall(link)
        lastpage=re.compile('<a class=\'page-numbers\' href=.+?>(\d+)<', re.S).findall(link)
        np=re.compile('<a class="next page-numbers" href="(.+?page/(.+?))/.*?"').findall(link)
        if len(np) > 0:
            next_page = np[0][0]
            if settings.getSetting('nextpagetop') == 'true':
                if lastpage:
                    lastpage = "/" + str(lastpage[-1])
                else:
                    lastpage = ''
                main.addDir('[COLOR blue]Next Page %s%s[/COLOR]' % (str(np[0][1]),lastpage),next_page,'xxxstreamsIndex',artwork + '/main/next.png')
        for url,name,x,thumbnail in match1:
            try:
                thumbnail = re.search('<img src="(http.+?)"', thumbnail)
                if thumbnail:
                    thumbnail = thumbnail.group(1)
                else:
                    thumbnail = None
                name = name.encode('utf-8')
                main.addDir(name,url,'xxxstreamsVideoLinks',thumbnail)
            except:
                continue
        if len(np) > 0:
            if settings.getSetting('nextpagebottom') == 'true':
                main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'xxxstreamsIndex',artwork + '/main/next.png')
        main.AUTOVIEW('movies')

def VIDEOLINKS(name,url,thumb):
    link = net.http_GET(url).content
    match=re.compile('<div class="entry-content">(.+?)class="navigation post-navigation"', re.S).findall(link)
    if match:
        match1=re.compile('href="(http[s]?://[^www.pix|^www.theteen].*?)["<\s].*? target="_blank">([^<]+?)<', re.S).findall(match[0].replace('/tttr/1out2.php?s=0,100,100,100:*&amp;u=',''))
        for url,hoster in match1:
            hoster1 = re.match('http[s]?://(.+?)/', hoster)
            if hoster1:
                hoster = hoster1.group(1)
            if not re.search('(Download|SPEEDVID|moviecloud|datafile)', hoster):
                hoster = hoster.replace('Streaming ','')
                main.addDir(hoster,url,'xxxstreamsPlayLinks',thumb)

def PLAYLINKS(name,url,thumb):
    link = net.http_HEAD(url)
    if link.get_url():
        link = link.get_url()
        if main.resolvable(link):
            try:
                main.RESOLVE(name,link,thumb)
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
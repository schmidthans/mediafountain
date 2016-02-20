##xxxstreams Module by mediafountain 2016-02
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os,cgi
import urlresolver

from t0mm0.common.net import Net
net = Net()

artwork = main.artwork
base_url = 'http://xxxstreams.org'
settings = main.settings

def CATEGORIES():
    main.addDir('Search','none','xxxstreamsSearch',artwork + '/main/search.png')
    main.addDir('Newest Videos',base_url +'/new-porn-streaming/page/0','xxxstreamsIndex',artwork + '/main/recentvideos.png')
    main.addDir('Full Movies',base_url +'/full-movies-streaming/page/0','xxxstreamsIndex',artwork + '/main/recentvideos.png')
    main.addDir('HD',base_url +'/tag/hd/page/0','xxxstreamsIndex',artwork + '/main/recentvideos.png')
    link = net.http_GET(base_url).content
    match=re.compile('<div id="primary-sidebar"(.+?)option', re.S).findall(link)
    if match:
        match1=re.compile('href="(http.+?)".+?title="\d+ topics">(.+?)<', re.S).findall(match[0])
        if len(match1) > 0:
            for (Url, Title) in match1:
                main.addDir(Title, Url +'/','xxxstreamsIndex',artwork + '/main/video.png')

def INDEX(url):
    next_page = ''
    link = net.http_GET(url).content
    match=re.compile('content-area">(.+?)wp-pagenavi', re.S).findall(link)
    if match:
        match1=re.compile('data-lazy-src="(.+?)".+?<a href="(http[s]?://.*?)["|#].+?data-item_title="(.+?)"', re.S).findall(match[0])
        lastpage=re.compile('<span class=\'pages\'>Page (\d+) of (\d+)<', re.S).findall(link)
        np=re.compile('<link rel="next" href="(.+?)"').findall(link)
        if len(np) > 0:
            next_page = np[0]
            if settings.getSetting('nextpagetop') == 'true':
                main.addDir('[COLOR blue]Next Page %s/%s[/COLOR]' % (str(int(lastpage[0][0])+1),str(lastpage[0][1])),next_page,'xxxstreamsIndex',artwork + '/main/next.png')
        for thumbnail,url,name in match1:
            try:
                if not re.search('Siterip', name):
                    main.addDir(name,url,'xxxstreamsVideoLinks',thumbnail)
            except:
                continue
        if len(np) > 0:
            if settings.getSetting('nextpagebottom') == 'true':
                main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'xxxstreamsIndex',artwork + '/main/next.png')
        main.AUTOVIEW('movies')

def VIDEOLINKS(name,url,thumb):
    link = net.http_GET(url).content
    match=re.compile('<div class="entry-content">(.+?)</br>', re.S).findall(link)
    if match:
        match1=re.compile('(<br />|<p>) <a href="(http[s]?://[^www.pix].*?)" target="_blank">([^<]+?)<', re.S).findall(match[0])
        for x,url,hoster in match1:
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
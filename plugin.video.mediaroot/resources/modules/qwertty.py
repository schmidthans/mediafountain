##qwertty Module by mediafountain 2016-02
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os,cgi
import urlresolver
import json

from t0mm0.common.net import Net
net = Net()

artwork = main.artwork
base_url = 'http://www.qwertty.net'
settings = main.settings

def CATEGORIES():
    main.addDir('Search','none','qwerttySearch',artwork + '/main/search.png')
    main.addDir('Newest Videos',base_url,'qwerttyIndex',artwork + '/main/recentvideos.png')
    main.addDir('Amateur', base_url +'/tags/Amateur/','qwerttyIndex',artwork + '/main/video.png')
    main.addDir('Big+Tits', base_url +'/tags/Big+Tits/','qwerttyIndex',artwork + '/main/video.png')
    main.addDir('Bizarre', base_url +'/tags/Bizarre/','qwerttyIndex',artwork + '/main/video.png')
    main.addDir('Black', base_url +'/tags/Black/','qwerttyIndex',artwork + '/main/video.png')
    main.addDir('Bonnie+Rotten', base_url +'/tags/Bonnie+Rotten/','qwerttyIndex',artwork + '/main/video.png')
    main.addDir('Germany', base_url +'/tags/GERMANY/','qwerttyIndex',artwork + '/main/video.png')
    main.addDir('Fetish', base_url +'/tags/Fetish/','qwerttyIndex',artwork + '/main/video.png')
    main.addDir('Fisting', base_url +'/tags/Fisting/','qwerttyIndex',artwork + '/main/video.png')
    link = net.http_GET(base_url).content
    match=re.compile('main-menu clearfix(.+?)</ul>', re.S).findall(link)
    if match:
        match1=re.compile('<li><a href="(/.+?)/">(.+?)</a></li>', re.S).findall(match[0])
        if len(match1) > 0:
            for (Url, Title) in match1:
                Url = base_url + Url
                main.addDir(Title, Url +'/','qwerttyIndex',artwork + '/main/video.png')

def INDEX(url, post=None):
    if type(url) == str:
        if re.match("\('http", url):
            url=re.compile("\('(.*?)', (.*?\}), '(.*?)'").findall(url)
            post = eval(url[0][1])
            url = (url[0][0], post)

    next_page = ''
    if type(url) == str:
        link = net.http_GET(url).content
        np=re.compile('pnext"><a href="(http://qwertty.net/.*?page/(\d+))/">').findall(link)
        lastpage=re.compile('<a href="http://qwertty.net/.*?page/\d+/">(\d+)<', re.S).findall(link)
    else:
        link = net.http_POST(url[0], url[1]).content
        np=re.compile('pnext">.*? href="(#)">(.+?)<').findall(link)
        lastpage=re.compile(' href="#">(\d+)<', re.S).findall(link)
    match=re.compile('<div class="short-item">.+?href="(.*?)".+?<img src="(.+?)"\salt="(.+?)"', re.S).findall(link)
    if len(np) > 0:
        if type(url) == str:
            page = np[0][1]
            next_page = np[0][0]
        else:
            page = int(url[1]['search_start'])+1
            next_page = (base_url, {'do': 'search', 'subaction': 'search', 'story': url[1]['story'], 'search_start': str(page), 'result_from': str(int(url[1]['result_from'])+12)}, url[1]['story'])
        if settings.getSetting('nextpagetop') == 'true':
                main.addDir('[COLOR blue]Next Page %s/%s[/COLOR]' % (str(page),str(lastpage[-1])),next_page,'qwerttyIndex',artwork + '/main/next.png')
    for urllink,thumbnail,name in match:
        try:
            if not re.match("http.+?", thumbnail):
                thumbnail = base_url + thumbnail
            main.addDir(name,urllink,'qwerttyVideoLinks',thumbnail)
        except:
            continue
    if len(np) > 0:
        if settings.getSetting('nextpagebottom') == 'true':
            if next_page != '':
                main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'qwerttyIndex',artwork + '/main/next.png')
    main.AUTOVIEW('movies')

def VIDEOLINKS(name,url,thumb):
    link = net.http_GET(url).content
    match=re.compile('<div class="full-text clearfix desc-text">(.+?)</div>', re.S).findall(link)
    if match:
        match1=re.compile('<a href="(http[s]?://(.*?)/.*?)"\s+target="_blank', re.S).findall(match[0])
        for url,hoster in match1:
            print "###url,hoster"+url+"##"+hoster
            main.addDir(hoster,url,'qwerttyPlayLinks',thumb)

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
        url = base_url
        post = {'do': 'search', 'subaction': 'search', 'story': search}
        urldata = (url,{'do': 'search', 'subaction': 'search', 'story': search, 'search_start': '1', 'result_from': '1'}, search)
        INDEX(urldata)

def MASTERSEARCH(search):
    url = base_url + '/en/search/0?title=' + search
    INDEX(url)
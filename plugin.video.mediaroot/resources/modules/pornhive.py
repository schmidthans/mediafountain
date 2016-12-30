##pornhive Module by mediafountain 2015-05
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os,cgi
import urlresolver

from t0mm0.common.net import Net
net = Net()

artwork = main.artwork
base_url = 'http://www.pornhive.tv'
settings = main.settings

def CATEGORIES():
    main.addDir('Search','none','pornhiveSearch',artwork + '/main/search.png')
    main.addDir('Newest Videos',base_url +'/en/page/0','pornhiveIndex',artwork + '/main/recentvideos.png')
    main.addDir('StreamCloud',  base_url + '/en/hoster/streamcloud.eu','pornhiveIndex',artwork + '/main/video.png')
    main.addDir('FlashX',  base_url + '/en/hoster/flashx.tv','pornhiveIndex',artwork + '/main/video.png')
    #main.addDir('NowVideo',  base_url + '/en/hoster/nowvideo.sx','pornhiveIndex',artwork + '/main/video.png')
    #main.addDir('PrimeShare',  base_url + '/en/hoster/primeshare','pornhiveIndex',artwork + '/main/video.png')
    #main.addDir('SockShare',  base_url + '/en/hoster/sockshare.tv','pornhiveIndex',artwork + '/main/video.png')
    main.addDir('Openload',  base_url + '/en/hoster/openload.co','pornhiveIndex',artwork + '/main/video.png')
    #main.addDir('UserPorn',  base_url + '/en/hoster/userporn','pornhiveIndex',artwork + '/main/video.png')
    main.addDir('Videomega',  base_url + '/en/hoster/videomega.tv','pornhiveIndex',artwork + '/main/video.png')
    main.addDir('Videowood',  base_url + '/en/hoster/videowood.tv','pornhiveIndex',artwork + '/main/video.png')
    #main.addDir('Vidxden',  base_url + '/en/hoster/vidxden.tv','pornhiveIndex',artwork + '/main/video.png')
    link = net.http_GET(base_url).content
    match=re.compile('All\sTitles(.+?)</ul>', re.S).findall(link)
    if match:
        match1=re.compile('<a\shref="(.+?)">(.+?)</a', re.S).findall(match[0])
        if len(match1) > 0:
            for (Url, Title) in match1:
                main.addDir(Title, Url +'/','pornhiveIndex',artwork + '/main/video.png')
    match=re.compile('"dropdown">Categories(.+?)</ul>', re.S).findall(link)
    if match:
        match1=re.compile('<a\shref="(.+?)"\stitle=".*?">(.+?)</a', re.S).findall(match[0])
        if len(match1) > 0:
            for (Url, Title) in match1:
                main.addDir(Title, Url +'/','pornhiveIndex',artwork + '/main/video.png')

def INDEX(url):
    next_page = ''
    link = net.http_GET(url).content
    match=re.compile('<div\sclass="vid-panel-img">.*?<a\shref="(.*?)"><img data-src="(.*?)".*?"vid-title vid-marquee">(.*?)<', re.S).findall(link)
    lastpage=re.compile('data-ci-pagination-page="(\d+)">Last', re.S).findall(link)
    np=re.compile('<li class="active">.+?href=".".+?<a href="(.+?)"').findall(link)
    
    if len(np) > 0 and np[0] != "#":
        next_page = np[0]
        pageparse = re.search('http://www.pornhive.tv.*?/(\d+)$', url)
        if pageparse:
            page = str(int(pageparse.group(1))/20 +1)
        else:
            page = '2'
        if lastpage:
            lastpage = "/" + str(int(lastpage[-1])/20)
        else:
            lastpage = ''
        if settings.getSetting('nextpagetop') == 'true':
            main.addDir('[COLOR blue]Next Page %s%s[/COLOR]' % (page,lastpage),next_page,'pornhiveIndex',artwork + '/main/next.png')
    for url,thumbnail,name in match:
        try:
            if "///" in thumbnail:
                thumbnail = "http://" + thumbnail.split("///")[1]
            main.addDir(name,url,'pornhiveVideoLinks',thumbnail)
        except:
            continue
    if len(np) > 0:
        if settings.getSetting('nextpagebottom') == 'true':
            main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'pornhiveIndex',artwork + '/main/next.png')
    main.AUTOVIEW('movies')

def VIDEOLINKS(name,url,thumb):
    link = net.http_GET(url).content
    match1=re.compile('data-id="(.*?)".*?Watch\sit\son\s+(.*?)"', re.S).findall(link)
    for url,hoster in match1:
        url = "%s/en/out/%s" % (base_url, url)
        main.addDir(hoster,url,'pornhivePlayLinks',thumb)

def PLAYLINKS(name,url,thumb):
    link = net.http_HEAD(url)
    if link.get_url():
        link = link.get_url()
        if main.resolvable(link):
            try:
                main.RESOLVE(name,link,thumb)
            except:
                pass
        else:
            link = net.http_GET(url).content
            match1=re.compile('<iframe\ssrc="(.+?)"', re.S).findall(link)
            link = match1[0]
            hmf = urlresolver.HostedMediaFile(link)
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
        url = base_url + '/en/search/0?title=' + search
        INDEX(url)

def MASTERSEARCH(search):
    url = base_url + '/en/search/0?title=' + search
    INDEX(url)
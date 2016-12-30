##mykino Module by mediafountain 2015-05
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os,cgi
import urlresolver
import json

from t0mm0.common.net import Net
net = Net()

artwork = main.artwork
base_url = 'http://mykino.to'
settings = main.settings

def CATEGORIES():
        main.addDir('Kinofilme',base_url +'/aktuelle-kinofilme','mykinoIndex',artwork + '/main/movie.png')
        main.addDir('Neue Filme',base_url +'/filme/','mykinoIndex',artwork + '/main/recentvideos.png')
        main.addDir('Genres','none','mykinoGenres',artwork + '/main/categories.png')
        main.addDir('Suche','none','mykinoSearch',artwork + '/main/search.png')

def SERIES():
        main.addDir('Neue Serien',base_url +'/serien/','mykinoSeriesIndex',artwork + '/main/recentvideos.png')
        main.addDir('Genres Serien','none','mykinoSeriesGenres',artwork + '/main/categories.png')
        main.addDir('Suche','none','mykinoSearch',artwork + '/main/search.png')#TODO series und movies in der suche unterscheiden

def SERIESGENRES():
    url = base_url
    link = net.http_GET(url).content
    parse=re.search('<div class="contab" id="tabln2">(.+?)</div>', link, re.S)
    genre=re.compile('<li><a href="(.+?)">(.+?)</a></li>', re.S).findall(parse.group(1))
    if genre:
        for (phUrl, phTitle) in genre:
            url = base_url + phUrl
            try: 
                main.addDir(phTitle.encode('utf-8'),url,'mykinoSeriesIndex',artwork + '/main/video.png')
            except:
                continue

def SERIESINDEX(url):
        next_page = ''
        if re.match("http", url):
            issearch=False
        else:
            issearch=True
        if issearch:
            urlparts = url.split('#')
            search_start = urlparts[1]
            result_from = str(int(urlparts[1])*10+1)
            dataPost = {'do':'search','subaction':'search','story':urlparts[0], 'search_start':search_start, 'result_from':result_from}
            link=net.http_POST(base_url+'/index.php', dataPost).content
        else:
            link = net.http_GET(url).content
        match=re.compile('<div class="boxgrid2 caption2">\n<a href="(.+?.html)">\n<img class="images3" src="(.+?)".*?<div class="boxgridtext">\n(.+?)\n</div>',re.S).findall(link)
        parse=re.compile('<div class="pagenavigation ">(.+?)>Weiter', re.S).search(link)
        if parse:
            np=re.compile('<a href="(.+?)"', re.S).findall(parse.group(1))
            next_page = np[-1]
        if len(np) > 0:
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'mykinoSeriesIndex',artwork + '/main/next.png')
        if match:
            for url,thumbnail,name in match:
                name=name.encode('utf-8')
                try: 
                    main.addDir(name,url,'mykinoSeriesSeason',thumbnail)
                except:
                    continue
        if len(np) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'mykinoSeriesIndex',artwork + '/main/next.png')
        main.AUTOVIEW('tvshows')

def SERIESSEASON(url,thumb):
    seriesid = re.search('(\w+)-',url)
    link = net.http_GET(url).content
    parse = re.search('<div class="season-selector">(.+?)<div class="season-selector-np">', link, re.S)
    if parse:
        match=re.compile('<option value="(\d+)">(Staffel .+?)</option',re.S).findall(parse.group(1))
        if match:
            for urlid, name in match:
                try: 
                    dataPost = {'news_id':seriesid.group(1),'season': str(urlid)}
                    main.addDir(name,dataPost,'mykinoSeriesSeries',thumb)
                except:
                    continue

def SERIESSERIES(name, dataPost,thumb):
    if dataPost:
        dataPostdic = eval(dataPost)
        link=net.http_POST(base_url+'/engine/ajax/a.sseries.php', dataPostdic).content
        match=re.compile('<option value=."(.+?).">(.+?)<',re.S).findall(link)
        if match:
            for urlid,name in match:
                try: 
                    dataPost = {'news_id':dataPostdic['news_id'],'series': str(urlid)}
                    main.addDir(name,dataPost,'mykinoSeriesLinks',thumb)
                except:
                    continue

def SERIESLINKS(name, dataPost,thumb):
    if dataPost:
        streamcounter = 0
        newList =[]
        dataPostdic = eval(dataPost)
        link=net.http_POST(base_url+'/engine/ajax/a.sseries.php', dataPostdic).content
        match=re.compile('(http[s]?:\\\/\\\/(.+?)\\\/.+?)[#|"]',re.S).findall(link)
        if match:
            for url,hoster in match:
                link = str(url).replace('&#038;','&').replace('&amp;','&').replace('\/','/')
                if main.resolvable(link):
                    try:
                        main.addHDir(name,link,'resolve',thumb)
                    except:
                        continue

def GENRES():
    url = base_url
    link = net.http_GET(url).content
    parse=re.search('<div class="contab" id="tabln1">(.+?)</div>', link, re.S)
    genre=re.compile('<li><a href="(.+?)">(.+?)</a></li>', re.S).findall(parse.group(1))
    if genre:
        for (phUrl, phTitle) in genre:
            url = base_url + phUrl
            try: 
                main.addDir(phTitle.encode('utf-8'),url,'mykinoIndex',artwork + '/main/video.png')
            except:
                continue

def INDEX(url):
        next_page = ''
        np = {}
        if re.match("http", url):
            issearch=False
        else:
            issearch=True
        if issearch:
             urlparts = url.split('#')
             search_start = urlparts[1]
             result_from = str(int(urlparts[1])*10+1)
             dataPost = {'do':'search','subaction':'search','story':urlparts[0], 'search_start':search_start, 'result_from':result_from}
             link=net.http_POST(base_url+'/index.php', dataPost).content
        else:
             link = net.http_GET(url).content
        match=re.compile('<div class="boxgrid2 caption2">\n<a href="(.+?.html)">\n<img class="images3" src="(.+?)".*?<div class="boxgridtext">\n(.+?)\n</div>',re.S).findall(link)
        if issearch:
            parse=re.compile('<div class="pagenavigation ">(.+?)>Weiter', re.S).search(link)
            if parse:
                np=re.compile('id="nextlink" onclick="javascript:list_submit\((.+?)\)', re.S).findall(parse.group(1))
                lp=re.compile('>(\d+)<').findall(parse.group(1))
                if np:
                    next_page = urlparts[0] + "#" + np[0]
                    page = str(np[0])
                if lp:
                    lastpage = "/" + str(lp[-1])
                else:
                    lastpage = ""
        else:
            parse=re.compile('<div class="pagenavigation ">(.+?)>Weiter', re.S).search(link)
            if parse:
                np=re.compile('<span>\d+</span>.*?<a href="([^\s]+?/(\d+)/)"').findall(parse.group(1))
                lp=re.compile('>(\d+)<').findall(parse.group(1))
                if np:
                    next_page = np[0][0]
                    page = str(np[0][1])
                if lp:
                    lastpage = "/" + str(lp[-1])
                else:
                    lastpage = ""
        if len(np) > 0:
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page %s%s[/COLOR]' % (page,lastpage),next_page,'mykinoIndex',artwork + '/main/next.png')
        if match:
            for url,thumbnail,name in match:
                name=name.encode('utf-8')
                try: 
                    main.addDir(name,url,'mykinoVideoLinks',thumbnail)
                except:
                    continue
        if len(np) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'mykinoIndex',artwork + '/main/next.png')
        main.AUTOVIEW('movies')

def VIDEOLINKS(name,url,thumb):
        link = net.http_GET(url).content
        parse = re.search('<div class="season-selector">(.+?)<div class="season-selector-np">', link, re.S)
        if parse:
            SERIESSEASON(url,thumb)
        else:
            match1=re.compile('data-href="(.+?)".*?<span>(.+?)</span>', re.S).findall(link)
            for urls,hoster in match1:
                streams = urls.split("#,")
                if streams:
                    for url in streams:
                        main.addHDir(name, url,'resolve',thumb)

def FILTER(url):
        url = url + '?length=long'
        INDEX(url)

def SEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Suche')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = re.sub(' ','+', search)
                url = search+"#"+'0'
                INDEX(url)

def MASTERSEARCH(search):
        url = search+"#"+'0'
        INDEX(url)
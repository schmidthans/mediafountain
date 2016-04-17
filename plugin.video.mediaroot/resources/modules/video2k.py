##video2k Module by mediafountain 2016-04
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os,cgi
import urlresolver
import json

from t0mm0.common.net import Net
mycookiefile = '/tmp/' + 'video2k.cookies'
net = Net(cookie_file=mycookiefile)

artwork = main.artwork
base_url = 'http://video2k.is'
settings = main.settings

def CATEGORIES():
        url = base_url + '/index.php/ajax/cookieLang?lang=2&url=http://video2k.is/&cookies=no'
        link = net.http_GET(url).content
        test = net.save_cookies(mycookiefile)
        main.addDir('Kinofilme',base_url +'/?c=movie&m=cinema','video2kIndex',artwork + '/main/movie.png')
        main.addDir('Neue Filme',base_url +'/?c=movie&m=releases','video2kIndex',artwork + '/main/recentvideos.png')
        main.addDir('Genres','none','video2kGenres',artwork + '/main/categories.png')
        main.addDir('Suche','none','video2kSearch',artwork + '/main/search.png')

def GENRES():
    url = base_url
    link = net.http_GET(url).content
    parse=re.search('class="sorter"(.+?)</div>', link, re.S)
    genre=re.compile('value=\'(.+?)\'>(.+?)<', re.S).findall(parse.group(1))
    if genre:
        for (phUrl, phTitle) in genre:
            url = base_url + "/?c=movie&m=filter&genre=" + phUrl + "&order_by=all"
            try: 
                main.addDir(phTitle.encode('utf-8'),url,'video2kIndex',artwork + '/main/video.png')
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
        print "#### link"
        print url
        #print link
        match=re.compile('<a title="(.+?)"\s*href=\'[^\']*?-(\d+)\.html\'.*?<img src=\'(.+?)\'',re.S).findall(link)
        if issearch:
            parse=re.compile('<div class="pagenavigation ">(.+?)>Weiter', re.S).search(link)
            if parse:
                np=re.compile('id="nextlink" onclick="javascript:list_submit\((.+?)\)', re.S).findall(parse.group(1))
                lp=re.compile('>(\d+)<').findall(parse.group(1))
                if np:
                    next_page = urlparts[0][0] + "#" + np[0]
                    page = str(int(np[0][1])/20+1)
                if lp:
                    lastpage = "/" + str(lp[-1])
                else:
                    lastpage = ""
        else:
            parse=re.compile('class=\'pagination\'>(.+?)</div></div>', re.S).search(link)
            if parse:
                np=re.compile('<a href="([^<]+?per_page=(\d+))">Next').findall(parse.group(1))
                if np:
                    next_page = base_url + "/" + np[0][0].replace("&amp;", "&")
                    page = str(int(np[0][1])/20+1)
                lp=re.compile('=(\d+)">Last').findall(parse.group(1))
                if not lp:
                    lp=re.compile('per_page=(\d+)">\d').findall(parse.group(1))
                if lp:
                    lastpage = "/" + str(int(lp[-1])/20+1)
                else:
                    lastpage = ""
        if len(np) > 0:
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page %s%s[/COLOR]' % (page,lastpage),next_page,'video2kIndex',artwork + '/main/next.png')
        if match:
            for name,url,thumbnail in match:
                name=name#.encode('utf-8')
                url = 'http://video2k.is/?c=ajax&m=movieStreams2&id=' + url + '&lang=2&links=250'
                try:
                    main.addDir(name,url,'video2kVideoLinks',thumbnail)
                except:
                    continue
        if len(np) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'video2kIndex',artwork + '/main/next.png')
        main.AUTOVIEW('movies')

def VIDEOLINKS(name,url,thumb):
        link = net.http_GET(url).content
        print "######### links"
        #print link
        match=re.compile('</li></a><a (id=\'.*?|)title=\'(.*?)\'.*?(http.*?)["|\'].*?class=\'url\'>(.+?)<', re.S).findall(link)
        for x, dateinfo,url,hoster in match:
            name = hoster + " " + dateinfo
            print url.encode('utf-8')
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
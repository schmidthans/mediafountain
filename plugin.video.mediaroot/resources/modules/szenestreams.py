##szenestreams Module by mediafountain 2016-01-05
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os,cgi
import urlresolver
import json

from t0mm0.common.net import Net
net = Net()

artwork = main.artwork
base_url = 'http://www.szene-streams.com'
settings = main.settings

def CATEGORIES():
        main.addDir('Kinofilme',base_url +'/publ/aktuelle_kinofilme/1','szenestreamsIndex',artwork + '/main/video.png')
        main.addDir('Neue Filme',base_url + '/publ','szenestreamsIndex',artwork + '/main/recentvideos.png')
        main.addDir('Genres','none','szenestreamsGenres',artwork + '/main/categories.png')
        main.addDir('Suche','none','szenestreamsSearch',artwork + '/main/search.png')

def GENRES():
    main.addDir('720p',base_url +'/publ/720p/26','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Action',base_url +'/publ/action/2','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Abenteuer',base_url +'/publ/abenteuer/3','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Asia',base_url +'/publ/asia/4','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Bollywood',base_url +'/publ/bollywood/5','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Biografie',base_url +'/publ/biografie/6','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Drama / Romantik',base_url +'/publ/drama_romantik/8','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Doku',base_url +'/publ/dokus_shows/9','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Familie',base_url +'/publ/familie/11','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Geschichte',base_url +'/publ/geschichte/12','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('HDRiP',base_url +'/publ/hd/13','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Horror',base_url +'/publ/horror/14','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('History',base_url +'/publ/history/15','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Komoedie',base_url +'/publ/komodie/16','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Krieg',base_url +'/publ/krieg/17','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Klassiker',base_url +'/publ/klassiker/18','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Mystery',base_url +'/publ/mystery/19','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Musik',base_url +'/publ/musik/20','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Scifi / Fantasy',base_url +'/publ/scifi_fantasy/22','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Thriller / Crime',base_url +'/publ/thriller_crime/23','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Western',base_url +'/publ/western/25','szenestreamsIndex',artwork + '/main/video.png')
    main.addDir('Zechentrick / Animation',base_url +'/publ/zeichentrick_animation/24','szenestreamsIndex',artwork + '/main/video.png')

def INDEX(url):
        next_page = ''
        np = []
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
        match=re.compile('<div class="ImgWrapNews"><a href="(.+?)".*?(/publ/.+?)">(.+?)</a></b>.*?<div class="MessWrapsNews" align="center"> <div class="MessWrapsNews2" style="height:110px;">(.+?)<',re.S).findall(link)
        if issearch:
                pass
        else:
            if re.compile('[0-9]', re.S).match(url[-1]):
                np=re.compile('<span>(\d*?)</span>', re.S).findall(link)

        ispage = None
        if len(np) > 0:
                ispage=re.compile('(.+?-)(\d)').findall(url)
                if ispage and int(ispage[0][1]) == int(np[-1]):
                    next_page = ''
                else:
                    if ispage:
                        nextpagestr = str(int(ispage[0][1])+1)
                        next_page = ispage[0][0] + nextpagestr
                    else:
                        nextpagestr = 2
                        next_page = url + "-2"
                    if issearch:
                        next_page=next_page.replace("?page","&page")
                    if settings.getSetting('nextpagetop') == 'true':
                            main.addDir('[COLOR blue]Next Page %s/%s[/COLOR]' % (nextpagestr,str(np[-1])),next_page,'szenestreamsIndex',artwork + '/main/next.png')

        if match:
            for thumbnail,url,name,h in match:
                thumbnail = "http://www.szene-streams.com%s" % thumbnail
                name=name.encode('utf-8')
                url = 'http://szene-streams.com' + url
                try: 
                    main.addDir(name,url,'szenestreamsVideoLinks',thumbnail)
                except:
                    continue
        if settings.getSetting('nextpagebottom') == 'true':
            if len(np) > 0:
                if ispage and int(ispage[0][1]) == int(np[-1]):
                    pass
                else:
                    main.addDir('[COLOR blue]Next Page %s/%s[/COLOR]' % (nextpagestr,str(np[-1])),next_page,'szenestreamsIndex',artwork + '/main/next.png')
        main.AUTOVIEW('movies')

def VIDEOLINKS(name,url,thumb):
        link = net.http_GET(url).content
        parse = re.compile('class="eBlock"(.*?)class="MessWrapsNews"', re.S).search(link)
        if parse:
            match1=re.compile('(http[s]?://(?!fs..directupload)(?!szene-streams)(?!www.szene-streams)(?!flash-moviez.ucoz)(?!www.youtube.com)(.*?)\/.*?)[\'|"|\&|<|\s]', re.S).findall(parse.group(1))
            for url, hoster in match1:
                hoster = hoster.replace('play.','').replace('www.','').replace('embed.','')
                main.addHDir(name, url,'resolve',thumb)

def SEARCH():
        search = ''#
        keyboard = xbmc.Keyboard(search,'Suche')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = re.sub(' ','+', search)
                postString = {'a': "2", 'query': search}
                headers = {'User-agent': 'Mozilla/5.0'}
                url = base_url +'/publ'
                html = net.http_POST(url, form_data=postString, headers=headers).content
                match=re.compile('<div class="ImgWrapNews"><a href="(.*?)".*?(http://www.szene-streams.com/publ/.*?)">(.*?)<', re.S).findall(html)
                if match:
                    for thumbnail,url,name in match:
                        name=name.encode('utf-8')
                        url = 'http://szene-streams.com' + url
                        try: 
                            main.addDir(name,url,'szenestreamsVideoLinks',thumbnail)
                        except:
                            continue
                main.AUTOVIEW('movies')

def MASTERSEARCH(search):
        postString = {'a': "2", 'query': search}
        headers = {'User-agent': 'Mozilla/5.0'}
        url = base_url +'/publ'
        html = net.http_POST(url, form_data=postString, headers=headers).content
        match=re.compile('<div class="ImgWrapNews"><a href="(.*?)".*?(http://www.szene-streams.com/publ/.*?)">(.*?)<', re.S).findall(html)
        if match:
            for thumbnail,url,name in match:
                name=name.encode('utf-8')
                url = 'http://szene-streams.com' + url
                try: 
                    main.addDir(name,url,'szenestreamsVideoLinks',thumbnail)
                except:
                    continue
        main.AUTOVIEW('movies')
##Spankbang Module by mediafountain 2015-05
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os,cgi
import urlresolver

from t0mm0.common.net import Net
net = Net()

artwork = main.artwork
base_url = 'http://spankbang.com'
settings = main.settings

def CATEGORIES():
        main.addDir('Genres','none','spankbangGenres',artwork + '/main/categories.png')
        main.addDir('Newest',base_url +'/new_videos/','spankbangIndex',artwork + '/main/recentvideos.png')
        main.addDir('Search','none','spankbangSearch',artwork + '/main/search.png')

def GENRES():
    url = base_url + '/categories'
    link = net.http_GET(url).content
    genre=re.compile('<a href="(/category/.+?)"><img src="(.+?)"><span>(.+?)</span></a>', re.S).findall(link)
    if genre:
        for (phUrl, phThumb, phTitle) in genre:
            url = base_url + phUrl
            phThumb = base_url + phThumb
            try: 
                main.addDir(phTitle,url,'spankbangIndex',phThumb)
            except:
                continue

def INDEX(url):
        next_page = ''
        if re.match(".*?/s/", url):
            issearch=True
        else:
            issearch=False
        link = net.http_GET(url).content
        match=re.compile('<div class="video-item".+?<a href="(.+?)".+?<img src="(.+?)".*?title="(.+?)".+?fa-clock-o"></i>\s(.+?)<',re.S).findall(link)
        np=re.compile('<span class="status">page.+?<a href="(.+?)" class="next">Next page', re.S).findall(link)
        if issearch:
            main.addDir('[COLOR blue]filter >20min[/COLOR]',url,'spankbangFilter',artwork + '/main/filter.png')
        if len(np) > 0:
                next_page = base_url + np[0]
                pageparse = re.search('http://spankbang.com/.*?/(\d+)/', url)
                if pageparse:
                    print "### page", str(int(pageparse.group(1))+1)
                    page = str(int(pageparse.group(1))+1)
                else:
                    page = '2'
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue] Next Page %s [/COLOR]' % page,next_page,'spankbangIndex',artwork + '/main/next.png')
        if match:
            for url,thumbnail,name, lenght in match:
                name=name.encode('utf-8') + " " + str(lenght) + "min"
                url = base_url + url
                thumbnail="http://"  + thumbnail
                try: 
                    main.addDir(name,url,'spankbangVideoLinks',thumbnail)
                except:
                    continue
        if len(np) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page %s [/COLOR]' % page,next_page,'spankbangIndex',artwork + '/main/next.png')
        main.AUTOVIEW('movies')

def VIDEOLINKS(name,url,thumb):
        link = net.http_GET(url).content
        stream_quality=re.findall('<span class="ft-button ft-light-blue tt q_(.+?)"', link)
        stream_id=re.search("var stream_id\s+=\s+'(.+?)';", link)
        stream_key=re.search("var stream_key\s+=\s+'(.+?)';", link)
        if stream_quality and stream_id and stream_key:
            url= 'http://spankbang.com/_%s/%s/title/%s__mp4' % (stream_id.group(1), stream_key.group(1), stream_quality[0])
            try:
                main.RESOLVE(name,url,thumb)
            except:
                pass

def FILTER(url):
        url = url + '?length=long'
        INDEX(url)

def SEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = re.sub(' ','+', search)
                url = base_url + '/s/' + search
                INDEX(url)
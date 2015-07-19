#Paradisehill Module by mediafountain 2015-05
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os,cgi
import urlresolver

from t0mm0.common.net import Net
net = Net()

artwork = main.artwork
base_url = 'http://www.paradisehill.tv'
settings = main.settings

def CATEGORIES():
        main.addDir('Genres','none','paradisehillGenres',artwork + '/main/categories.png')
        main.addDir('Newest',base_url +'/en/','paradisehillIndex',artwork + '/main/recentvideos.png')
        main.addDir('Search',base_url +'/?cat=4362','paradisehillSearch',artwork + '/main/search.png')

def GENRES():
    url = base_url + '/en/'
    link = net.http_GET(url).content
    match=re.compile('<h2>Categories</h2>(.+?)<script type="', re.S).findall(link)
    genre=re.compile('\shref="(.+?)"\stitle="(.+?)".+?src="(.+?)".+?Films:(.+?)<', re.S).findall(match[0])
    if genre:
        for (phUrl, phTitle, phThumb, phCount) in genre:
            url = base_url + phUrl
            phThumb = base_url + phThumb
            try: 
                main.addDir(phTitle,url,'paradisehillIndex',phThumb)
            except:
                continue

def INDEX(url):
        next_page = ''
        if re.match(".*?search", url):
            issearch=True
        else:
            issearch=False
        link = net.http_GET(url).content
        parse = re.search('class="row new-collect(.+?)class="pagination', link, re.S)
        match = re.compile('bci(-title|)-link" href="(.+?)".+?bci-title">(.+?)<.+?img["]? src="(.+?)"', re.S).findall(parse.group(1))
        pagination=re.compile('class="pagination(.+?)</div>', re.S).findall(link)
        lastpage=re.compile('.*page=(\d+)">', re.S).findall(pagination[0])
        np=re.compile('page\sactive.+?<li class="page"><a href=".+?page=(.+?)">', re.S).findall(pagination[0])

        if len(np) > 0:
                ispage=re.compile('(.+?page=)\d').findall(url)
                if ispage:
                    next_page = ispage[0] + str(np[0])
                else:
                    next_page = url + "?page=" + str(np[0])
                if issearch:
                    next_page=next_page.replace("?page","&page")
                if settings.getSetting('nextpagetop') == 'true':
                        main.addDir('[COLOR blue]Next Page %s/%s[/COLOR]' % (str(np[0]),str(lastpage[0])),next_page,'paradisehillIndex',artwork + '/main/next.png')
        if match:
            for x,url,name,thumbnail in match:
                name=name.encode('utf-8')
                url = base_url + url
                thumbnail="http://www.paradisehill.tv"  + thumbnail
                try: 
                    main.addDir(name,url,'paradisehillVideoLinks',thumbnail)
                except:
                    continue
        if len(np) > 0:
                if settings.getSetting('nextpagebottom') == 'true':
                        main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'paradisehillIndex',artwork + '/main/next.png')
        main.AUTOVIEW('movies')

def VIDEOLINKS(name,url,thumb):
        link = net.http_GET(url).content
        match=re.compile('films="(.+?)"', re.S).findall(link)
        if match:
            match1=re.compile('(http://.+?.mp4)').findall(match[0])
            if not match1:
                match1=re.compile('(http://.+?.flv)').findall(match[0])
            if match1:
                partcounter=1
                for url in match1:
                        disc = re.compile('.+?cd(\d+).+?', re.S|re.I).findall(url)
                        if disc:
                            discno = " CD " + disc[0]
                            cdname = name + discno
                        else:
                            if partcounter > 1:
                                discno=' Part' + str(partcounter)
                                cdname = name + discno
                                partcounter +=1
                            else:
                                discno=''
                                cdname=name
                                partcounter +=1

                        if main.resolvable(url):
                                try:
                                        main.addHDir(cdname,url,'resolve',thumb, disk=discno)
                                except:
                                        continue

def SEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = re.sub(' ','+', search)
                url = base_url + '/en/search_results.html?search=' + search
                INDEX(url)
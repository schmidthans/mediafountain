#TubePirate Module by o9r1sh October 2013
import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os,cgi
import urlresolver

from t0mm0.common.net import Net
net = Net()

artwork = main.artwork
base_url = 'http://botz.to'
settings = main.settings

def CATEGORIES():
        main.addDir('Genres','none','botzGenres',artwork + '/main/genres.png')
        main.addDir('Aktuell',base_url,'botzIndex',artwork + '/main/featured.png')
        main.addDir('Search',base_url +'/?cat=4362','botzSearch',artwork + '/main/search.png')

def GENRES():
	#url = base_url + '/en/'
	link = net.http_GET(base_url).content
	genre=re.compile('<li\sclass="cat-item.+?"><a\shref="(.+?)".+?>(.+?)</a>', re.S).findall(link)
	#print "eliinfo match", match[0]
	#genre=re.compile('<div\sclass="item_zag.+?<a\shref="(.+?)"\stitle="(.+?)".*?<img src="(.+?)".+?Films:(.+?)</div', re.S).findall(match[0])
	#parse = re.search('<h2>Categories</h2>(.*?)<div class="sep"></div>', data, re.S)
	#phCat = re.findall('<div\sclass="item_zag.*?<a\shref="(.*?)"\stitle="(.*?)".*?<img src="(.+?)".+?Films:(.*?)</div', parse.group(1), re.S)
	if genre:
		for (genreUrl, genreTitle) in genre:
			#url = base_url + phUrl
			#print "eliinfo ######### genre", genreUrl, genreTitle.encode('utf8')
			try: 
				main.addDir(genreTitle, genreUrl,'botzIndex',artwork + '/main/genres.png')
			except:
				continue

def INDEX(url):
		next_page = ''
		if re.match(".*?search", url):
			issearch=True
		else:
			issearch=False
		#print "eliinfo ######### INDEX(url)", url
		link = net.http_GET(url).content
		#print "eliinfo ############### INDEX link", re.compile('<(.+?)>',re.S).findall(link)
		match=re.compile('<div\sclass="entry">.+?href="(.+?)".+?src="(.+?)"\salt="(.+?)"',re.S).findall(link)
		#movies = re.findall('<div class="cat_item">.*?<a href="(.*?)"\s{0,2}title=".*?"\s{0,2}>(.*?)<.*?<img src="(.*?)"', data, re.S)
		#np=re.compile('<div\sclass="pagi">.+?<li><span>.+?<li><a href="\?page=(.+?)">', re.S).findall(link)
		np=re.compile('<a href="http://botz.to/.+?/page/(.+?)"', re.S).findall(link)
		
		#print "eliinfo ######### INDEX np", np
		if len(np) > 0:
				#npc = str(np[0]).replace('&#038;','&').replace('&amp;','&')
				ispage=re.compile('(.+?page/)\d').findall(url)
				#print "eliinfo ######### INDEX ispage", ispage
				if ispage:
					next_page = ispage[0] + str(np[0])
				else:
					next_page = url + "/page/" + str(np[0])
				#http://www.botz.tv/en/search_results.html?search=%s&page=%s
				#if issearch:
				#	print "eliinfo ######### INDEX search"
				#	next_page=next_page.replace("?page","&page")
				#print "eliinfo ######### INDEX next_page", next_page
				if settings.getSetting('nextpagetop') == 'true':
						main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'botzIndex',artwork + '/main/next.png')

		if match:
			#print "elinfo ############ INDEX match", match
			for url,thumbnail,name in match:
				name=name.encode('utf-8')
				#url = base_url + url
				#if issearch:
				#	thumbnail="http://www.botz.tv"  + thumbnail
					#print "eliinfo ######### INDEX thumbnail"
				#print "elinfo ############ INDEX url,name,thumbnail", url,name,thumbnail
				try: 
					main.addDir(name,url,'botzVideoLinks',thumbnail)
				except:
					continue
		if len(np) > 0:
				if settings.getSetting('nextpagebottom') == 'true':
						main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'botzIndex',artwork + '/main/next.png')

def VIDEOLINKS(name,url,thumb):
		#print "elinfo ############ VIDEOLINKS url", url
		link = net.http_GET(url).content
		#print "elinfo ############ VIDEOLINKS link", link
		
		match=re.compile('href="(http://(streamcloud|flashx|divxstage|movshare|mooshare|primeshare|played|vidstream|bitshare|www.sockshare|www.putlocker|xvidstage|filenuke|nowvideo).+?)"', re.S).findall(link)
		if match:
			print "elinfo ############ VIDEOLINKS match", match
			#partcounter=1
			for url,hoster in match:
				if main.resolvable(url):
					#print "VIDEOLINKS final ########url",cdname, url, thumb
					try:
							main.addHDir(name,url,'resolve',thumb)
					except:
							continue

def SEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = re.sub(' ','+', search)
                
                url = base_url + '/?s=' + search
                SEARCHINDEX(url)

def SEARCHINDEX(url):
		next_page = ''
		#print "eliinfo ######### SEARCH(url)", url
		link = net.http_GET(url).content
		#print "eliinfo ######### SEARCH it now"
		#print "eliinfo ############### INDEX link", re.compile('<(.+?)>',re.S).findall(link)
		#match=re.compile('<div\sclass="post".+?href="(.+?)".+?tag">(.+?)</a></div>.+?src="(.+?)".+?="(.+?)"',re.S).findall(link)
		match=re.compile('<div\sclass="post".+?href="(.+?)".+?"bookmark">(.+?)<.+?tag">(.+?)</a></div>.+?src="(.+?)"',re.S).findall(link)
		#print "eliinfo ######### SEARCH finish"
		#match=re.compile('<div\sclass="post".+?href="(.+?)".+?bookmark(.+?)<.+?tag">(.+?)</a></div>.+?src="(.+?)"',re.S).findall(link)
		
		#movies = re.findall('<div class="cat_item">.*?<a href="(.*?)"\s{0,2}title=".*?"\s{0,2}>(.*?)<.*?<img src="(.*?)"', data, re.S)
		#np=re.compile('<div\sclass="pagi">.+?<li><span>.+?<li><a href="\?page=(.+?)">', re.S).findall(link)
		np=re.compile('http://botz.to/.+?/page/(.+?)\?', re.S).findall(link)
		#http://botz.to/page/2?s=haus
		#print "eliinfo ######### SEARCH np", np
		if len(np) > 0:
				#npc = str(np[0]).replace('&#038;','&').replace('&amp;','&')
				ispage=re.compile('(.+?page/)\d').findall(url)
				searchstr=re.compile('s=(.+?)$').findall(url)
				#hauprint "eliinfo ######### INDEX ispage", ispage
				#http://botz.to/page/2?s=haus
				next_page = base_url + "/page/" + str(np[0]) + '?s=' + searchstr[0]
				#http://www.botz.tv/en/search_results.html?search=%s&page=%s
				#if issearch:
				#	print "eliinfo ######### INDEX search"
				#	next_page=next_page.replace("?page","&page")
				#print "eliinfo ######### INDEX next_page", next_page
				if settings.getSetting('nextpagetop') == 'true':
						main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'botzSearchindex',artwork + '/main/next.png')

		if match:
			#print "elinfo ############ SEARCH match", match
			for url,name,category,thumbnail in match:
				name=name.encode('utf-8')
				category=category.encode('utf-8')
				#thumbnail=thumbnail+".jpg"
				#url = base_url + url
				#if issearch:
				#	thumbnail="http://www.botz.tv"  + thumbnail
					#print "eliinfo ######### INDEX thumbnail"
				#print "elinfo ############ SEARCH url,name,thumbnail", url,name,category,thumbnail
				try: 
					main.addDir(name,url,'botzVideoLinks',thumbnail)
				except:
					continue
		if len(np) > 0:
				if settings.getSetting('nextpagebottom') == 'true':
						main.addDir('[COLOR blue]Next Page[/COLOR]',next_page,'botzSearchindex',artwork + '/main/next.png')
#Videocloud Module by o9r1sh October 2013

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmcaddon,sys,main,xbmc,os
import urlresolver

artwork = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.mediaroot/resources/artwork/', ''))
base_url = 'http://videocloud.in'

def CATEGORIES():
        main.addDir('Action',base_url +'/category/action/',49,artwork + 'action.png')
        main.addDir('Adventure',base_url +'/category/adventure/',49,artwork + 'adventure.png')
        main.addDir('Comedy',base_url +'/category/comedy/',49,artwork + 'comedy.png')
        main.addDir('Crime',base_url +'/category/crime/',49,artwork + 'crime.png')
        main.addDir('Drama',base_url +'/category/drama/',49,artwork + 'drama.png')
        main.addDir('Family',base_url +'/category/family/',49,artwork + 'family.png')
        main.addDir('Fantasy',base_url +'/category/fantasy/',49,artwork + 'fantasy.png')
        main.addDir('Horror',base_url +'/category/horror/',49,artwork + 'horror.png')
        main.addDir('Mystery',base_url +'/category/mystery/',49,artwork + 'mystery.png')
        main.addDir('Others',base_url +'/category/others/',49,artwork + 'others.png')
        main.addDir('Romance',base_url +'/category/romance/',49,artwork + 'romance.png')
        main.addDir('Sci-Fi',base_url +'/category/sci-fi/',49,artwork + 'sci-fi.png')
        main.addDir('Thriller',base_url +'/category/thriller/',49,artwork + 'thriller.png')
        main.addDir('War',base_url +'/category/war/',49,artwork + 'war.png')
        main.addDir('Western',base_url +'/category/western/',49,artwork + 'western.png')

def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<a href=".+?" title=".+?">(.+?)</a></h1>\n\t\t\n\t\t\n\t</header>\n\n\t<div class=".+?">\n\t\t<a href="(.+?)"><img src="(.+?)" alt=".+?" width=".+?" height=".+?" class=".+?" /></a>').findall(link)
        np=re.compile('<strong>.+?</strong><a href="(.+?)">').findall(link)
        if len(np) > 0:
                next_page = np[0]
                main.addDir('Next Page',next_page,49,artwork + 'next.png')
        for name,url,thumbnail in match:
                if len(match) > 0:
                        head, sep, tail = name.partition(')')
                        name = head[:-5]
                        year = head[-5:] + sep

                        try:
                                req = urllib2.Request(url)
                                req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
                                response = urllib2.urlopen(req)
                                links=response.read()
                                response.close()
                                vid_link=re.compile('<source src="(.+?)"').findall(links)
                        except:
                                continue
                        try:       
                                main.addMDir(name,vid_link[0],9,thumbnail,year)
                        except:
                                continue

        main.AUTOVIEW('movies')


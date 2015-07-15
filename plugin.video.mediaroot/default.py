#mediaroot addon by MediaFountain

import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,urlresolver,xbmcaddon,os
from resources.modules import main
from resources.modules import mykino
from resources.modules import freeomovie, pornhive,pornmvz,paradisehill,spankbang

addon_id = 'plugin.video.mediaroot'
from t0mm0.common.addon import Addon
addon = main.addon
#myaddon = Addon('script.module.mediaroot')


settings = xbmcaddon.Addon(id=addon_id)
artwork = main.artwork

def CATEGORIES():
        if settings.getSetting('adult') == 'true':
                text_file = None
                if not os.path.exists(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.mediaroot/")):
                        os.makedirs(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.mediaroot/"))

                if not os.path.exists(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.mediaroot/sec.0")):
                        pin = ''
                        notice = xbmcgui.Dialog().yesno('Would You Like To Set A Password','Would you like to set a password for the adult section?','','')
                        if notice:
                                print "#### errorrrrrrrrrrrr"
                                keyboard = xbmc.Keyboard(pin,'Please Choose A New Password')
                                keyboard.doModal()
                                if keyboard.isConfirmed():
                                        pin = keyboard.getText()
                                text_file = open(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.mediaroot/sec.0"), "w")
                                text_file.write(pin)
                                text_file.close()
                        else:
                                text_file = open(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.mediaroot/sec.0"), "w")
                                text_file.write(pin)
                                text_file.close()
                                
                main.addDir('Adults Only','none','adultSections',artwork + '/main/adult.png')
        if settings.getSetting('movies') == 'true':
                main.addDir('Movies','none','movieSections',artwork + '/main/movie.png')
        if settings.getSetting('hdmovies') == 'true':
                main.addDir('HD Movies','none','hdSections',artwork + '/main/hdmovie.png')
        if settings.getSetting('shows') == 'true':        
                main.addDir('TV Shows','none','tvSections',artwork + '/main/tvshows.png')
        if settings.getSetting('docs') == 'true':
                main.addDir('Documentaries','none','docSections',artwork + '/main/docs.png')
        if settings.getSetting('cartoons') == 'true':
                main.addDir('Cartoons','none','cartoonSections',artwork + '/main/cartoons.png')
        if settings.getSetting('anime') == 'true':
                main.addDir('Anime','none','animeSections',artwork + '/main/anime.png')
        if settings.getSetting('favorites') == 'true':
                main.addDir('Favorites','none','favorites',artwork + '/main/favorites.png')
        if settings.getSetting('search') == 'true':
                main.addDir('Master Search','none','masterSearch',artwork + '/main/search.png')
        if settings.getSetting('resolver') == 'true':
                main.addDir('Resolver Settings','none','resolverSettings',artwork + '/main/resolver.png')

def MOVIESECTIONS():
        if settings.getSetting('mykinomovie') == 'true':
                main.addDir('MyKino Movie','none','mykinoCategories',artwork + '/movies/mykino.png')

def HDMOVIESECTIONS():
        pass

def TVSECTIONS():
        if settings.getSetting('mykinoseries') == 'true':
                main.addDir('MyKino Series','none','mykinoSeries',artwork + '/movies/mykino.png')

def DOCSECTIONS():
        pass

def CARTOONSECTIONS():
        pass

def ANIMESECTIONS():
        pass

def ADULT():
        text_file = open(xbmc.translatePath("special://home/userdata/addon_data/plugin.video.mediaroot/sec.0"), "r")
        line = file.readline(text_file)
        pin = ''
        if not line == '':
                keyboard = xbmc.Keyboard(pin,'Please Enter Your Password')
                keyboard.doModal()
                if keyboard.isConfirmed():
                        pin = keyboard.getText()
        if pin == line:
                if settings.getSetting('search') == 'true':
                        main.addDir('Master Porn Search','none','masterPornSearch',artwork + '/main/search.png')
                if settings.getSetting('freeomovie') == 'true':
                        main.addDir('FreeoMovie','none','freeOMovieCategories',artwork + '/adult/freeomovie.png')
                if settings.getSetting('pornmvz') == 'true':
                        main.addDir('Pornmvz','none','pornmvzCategories',artwork + '/adult/pornmvz.png')
                if settings.getSetting('pornhive') == 'true':
                        main.addDir('Pornhive','none','pornhiveCategories',artwork + '/adult/pornhive.png')
                if settings.getSetting('paradisehill') == 'true':
                        main.addDir('Paradisehill','none','paradisehillCategories',artwork + '/adult/paradisehill.png')
                if settings.getSetting('spankbang') == 'true':
                        main.addDir('Spankbang','none','spankbangCategories',artwork + '/adult/spankbang.png')
        else:
                notice = xbmcgui.Dialog().ok('Wrong Password','The password you entered is incorrect')

def MASTERSEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = search.replace(' ','+')
        threads = []
        if settings.getSetting('mykino') == 'true':
                print "#### masterseach mykino"
                try:
                        threads.append(main.Thread(mykino.MASTERSEARCH(search)))
                except:
                        pass
        [i.start() for i in threads]
        [i.join() for i in threads]

def MASTERPORNSEARCH():
        search = ''
        keyboard = xbmc.Keyboard(search,'Search')
        keyboard.doModal()
        if keyboard.isConfirmed():
                search = keyboard.getText()
                search = search.replace(' ','+')
        threads = []
        if settings.getSetting('pornmvz') == 'true':
                print "#### masterseach pornmvz", search
                try:
                        threads.append(main.Thread(pornmvz.MASTERSEARCH(search)))
                except:
                        pass
        if settings.getSetting('pornhive') == 'true':
                print "#### masterseach pornhive", search
                try:
                        threads.append(main.Thread(pornhive.MASTERSEARCH(search)))
                except:
                        pass
        [i.start() for i in threads]
        [i.join() for i in threads]

def COLLECTIVESEARCH(name):
        threads = []
#         if settings.getSetting('mmline') == 'true':
#                 try:
#                         threads.append(main.Thread(mmline.MASTERSEARCH(name)))
#                 except:
#                         pass
#         if settings.getSetting('wwmf') == 'true':
#                 try:
#                         threads.append(main.Thread(wwmf.MASTERSEARCH(name)))
#                 except:
#                         pass
#         if settings.getSetting('channelcut') == 'true':
#                 try:
#                         threads.append(main.Thread(channelcut.MASTERSEARCH(name)))
#                 except:
#                         pass
#         if settings.getSetting('wsoeu') == 'true':
#                 try:
#                         threads.append(main.Thread(wsoeu.MASTERSEARCH(name)))
#                 except:
#                         pass
        if settings.getSetting('pornhive') == 'true':
                print "#### masterseach pornhive"
                try:
                        threads.append(main.Thread(pornhive.MASTERSEARCH(name)))
                except:
                        pass
        [i.start() for i in threads]
        [i.join() for i in threads]

def FAVORITES():
        if settings.getSetting('movies') == 'true':
                main.addDir('Movies','movie','getFavorites',artwork + '/main/movie.png')
        if settings.getSetting('shows') == 'true':
                main.addDir('TV Shows','tvshow','getFavorites',artwork + '/main/tv.png')
        if settings.getSetting('cartoons') == 'true':
                main.addDir('Cartoons','cartoon','getFavorites',artwork + '/main/cartoons.png')
        if settings.getSetting('anime') == 'true':
                main.addDir('Anime','anime','getFavorites',artwork + '/main/anime.png')
      
mode = addon.queries['mode']
url = addon.queries.get('url', '')
name = addon.queries.get('name', '')
thumb = addon.queries.get('thumb', '')
year = addon.queries.get('year', '')
season = addon.queries.get('season', '')
episode = addon.queries.get('episode', '')
show = addon.queries.get('show', '')
types = addon.queries.get('types', '')

print "Mode is: "+str(mode)
print "URL is: "+str(url)
print "Name is: "+str(name)
print "Thumb is: "+str(thumb)
print "Year is: "+str(year)
print "Season is: "+str(season)
print "Episode is: "+str(episode)
print "Show is: "+str(show)
print "Type is: "+str(types)

#Default modes__________________________________________________________________
if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()

elif mode=='addFavorite':
        print ""+url
        main.addFavorite()

elif mode=='removeFavorite':
        print ""+url
        main.removeFavorite()


elif mode=='getFavorites':
        print ""+url
        main.getFavorites(url)

elif mode=='favorites':
        print ""+url
        FAVORITES()
        
elif mode=='movieSections':
        print ""+url
        MOVIESECTIONS()

elif mode=='tvSections':
        print ""+url
        TVSECTIONS()

elif mode=='docSections':
        print ""+url
        DOCSECTIONS()

elif mode=='hdSections':
        print ""+url
        HDMOVIESECTIONS()

elif mode=='masterSearch':
        print ""+url
        MASTERSEARCH()

elif mode=='collectiveSearch':
        print ""+url
        COLLECTIVESEARCH(name)

elif mode=='masterPornSearch':
#        print "####### masterPornSearch"
        print ""+url
        MASTERPORNSEARCH()

elif mode=='adultSections':
        print ""+url
        ADULT()

elif mode=='resolverSettings':
        print ""+url
        urlresolver.display_settings()

elif mode=='cartoonSections':
        print ""+url
        CARTOONSECTIONS()

elif mode=='animeSections':
        print ""+url
        ANIMESECTIONS()

#Main modes_____________________________________________________________________
elif mode=='resolve':
        print "####resolve "+url
        main.RESOLVE(name,url,thumb)

# mykino modules
elif mode=='mykinoCategories':
        print ""+url
        mykino.CATEGORIES()

elif mode=='mykinoIndex':
        print "xxxxxxxxxxxxxxxxxxxx"+url
        mykino.INDEX(url)

elif mode=='mykinoGenres':
        print ""+url
        mykino.GENRES()

elif mode=='mykinoFilter':
        print ""+url
        mykino.FILTER(url)

elif mode=='mykinoSearch':
        print ""+url
        mykino.SEARCH()

elif mode=='mykinoVideoLinks':
        print ""+url
        mykino.VIDEOLINKS(name,url,thumb)

elif mode=='mykinoSeries':
        print ""+url
        mykino.SERIES()

elif mode=='mykinoSeriesGenres':
        print ""+url
        mykino.SERIESGENRES()

elif mode=='mykinoSeriesIndex':
        print ""+url
        mykino.SERIESINDEX(url)

elif mode=='mykinoSeriesSeason':
        print ""+url
        mykino.SERIESSEASON(url,thumb)

elif mode=='mykinoSeriesSeries':
        print ""+url
        mykino.SERIESSERIES(name,url,thumb)

elif mode=='mykinoSeriesLinks':
        print ""+url
        mykino.SERIESLINKS(name, url,thumb)

#FreeOMovie Modes_______________________________________________________________
elif mode=='freeOMovieCategories':
        print ""+url
        freeomovie.CATEGORIES()

elif mode=='freeOMovieGenres':
        print ""+url
        freeomovie.GENRES()

elif mode=='freeOMovieSearch':
        print ""+url
        freeomovie.SEARCH()

elif mode=='freeOMovieIndex':
        print ""+url
        freeomovie.INDEX(url)

elif mode=='freeOMovieVideoLinks':
        print ""+url
        freeomovie.VIDEOLINKS(name,url,thumb)

#pornhive
elif mode=='pornhiveCategories':
        print ""+url
        pornhive.CATEGORIES()
elif mode=='pornhiveIndex':
        print ""+url
        pornhive.INDEX(url)
elif mode=='pornhiveVideoLinks':
        print ""+url
        pornhive.VIDEOLINKS(name,url,thumb)
elif mode=='pornhivePlayLinks':
        print ""+url
        pornhive.PLAYLINKS(name,url,thumb)
elif mode=='pornhiveSearch':
        print ""+url
        pornhive.SEARCH()
        
# spankbang
elif mode=='spankbangCategories':
        print ""+url
        spankbang.CATEGORIES()

elif mode=='spankbangIndex':
        print "xxxxxxxxxxxxxxxxxxxx"+url
        spankbang.INDEX(url)

elif mode=='spankbangGenres':
        print ""+url
        spankbang.GENRES()

elif mode=='spankbangFilter':
        print ""+url
        spankbang.FILTER(url)

elif mode=='spankbangSearch':
        print ""+url
        spankbang.SEARCH()

elif mode=='spankbangVideoLinks':
        print ""+url
        spankbang.VIDEOLINKS(name,url,thumb)
#Pornmvz Modes_______________________________________________________________
elif mode=='pornmvzCategories':
        print ""+url
        pornmvz.CATEGORIES()

elif mode=='pornmvzAll':
        print ""+url
        pornmvz.CATEGORIES()

elif mode=='pornmvzIndex':
        print ""+url
        pornmvz.INDEX(url)

elif mode=='pornmvzAsian':
        print ""+url
        pornmvz.CATEGORIES(url)

elif mode=='pornmvzEnglish':
        print ""+url
        pornmvz.CATEGORIES()

elif mode=='pornmvzFrench':
        print ""+url
        pornmvz.CATEGORIES()

elif mode=='pornmvzGerman':
        print ""+url
        pornmvz.CATEGORIES()

elif mode=='pornmvzItalian':
        print ""+url
        pornmvz.CATEGORIES()

elif mode=='pornmvzVideoLinks':
        print ""+url
        pornmvz.VIDEOLINKS(name,url,thumb)
elif mode=='pornmvzSearch':
        print ""+url
        pornmvz.SEARCH()
#paradisehill modes__________________________________________________________________
elif mode=='paradisehillCategories':
        print ""+url
        paradisehill.CATEGORIES()

elif mode=='paradisehillIndex':
        print ""+url
        paradisehill.INDEX(url)

elif mode=='paradisehillGenres':
        print ""+url
        paradisehill.GENRES()

elif mode=='paradisehillSearch':
        print ""+url
        paradisehill.SEARCH()

elif mode=='paradisehillVideoLinks':
        print ""+url
        paradisehill.VIDEOLINKS(name,url,thumb)








xbmcplugin.endOfDirectory(int(sys.argv[1]))

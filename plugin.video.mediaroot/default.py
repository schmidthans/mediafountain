#mediaroot addon by MediaFountain

import urllib,urllib2,re,xbmcplugin,xbmcgui,sys,xbmc,urlresolver,xbmcaddon,os
from resources.modules import main,mooviemaniac,wsoeu,fma,zmovie,wwmf,iwo,freeomovie,tubepirate
from resources.modules import mykino
from resources.modules import channelcut,filmikz,epornik,fullepisode,toonjet,pornhive,pornmvz,paradisehill,botz,spankbang

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

        if settings.getSetting('freemoviesaddict') == 'true':
                main.addDir('FreeMoviesAddict','none','fmaCategories',artwork + '/main/fma.png')

        if settings.getSetting('iwatchonlinemovies') == 'true':
                main.addDir('I-WatchOnline','none','iwoCategories',artwork + '/main/iwatchonline.png')

        if settings.getSetting('mooviemaniac') == 'true':
                main.addDir('MoovieManiac','none','moovieManiacCategories',artwork + '/main/mmaniac.png')

        if settings.getSetting('zmovie') == 'true':
                main.addDir('Watch-Movies / Z-Movie','none','zmovieCategories',artwork + '/main/zmovie.png')

        if settings.getSetting('wwmf') == 'true':
                main.addDir('WeWatchMoviesFree','none','wwmfCategories',artwork + '/main/wwmf.png')

        if settings.getSetting('botz') == 'true':
                main.addDir('BoTz','none','botzCategories',artwork + '/main/wwmf.png')

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
                if settings.getSetting('epornik') == 'true':
                        main.addDir('Epornik','none','epornikCategories',artwork + '/adult/epornik.png')
                if settings.getSetting('filmikz') == 'true':
                        main.addDir('Filmikz','none','filmikzAdultCategories',artwork + '/adult/filmikz.png')
                if settings.getSetting('freeomovie') == 'true':
                        main.addDir('FreeoMovie','none','freeOMovieCategories',artwork + '/adult/freeomovie.png')
                if settings.getSetting('tubepirate') == 'true':
                        main.addDir('TubePirate','none','tubePirateCategories',artwork + '/adult/tubepirate.png')
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
        if settings.getSetting('wwmf') == 'true':
                try:
                        threads.append(main.Thread(wwmf.MASTERSEARCH(search)))
                except:
                        pass
        if settings.getSetting('channelcut') == 'true':
                try:
                        threads.append(main.Thread(channelcut.MASTERSEARCH(search)))
                except:
                        pass
        if settings.getSetting('wsoeu') == 'true':
                try:
                        threads.append(main.Thread(wsoeu.MASTERSEARCH(search)))
                except:
                        pass
        if settings.getSetting('fullepisode') == 'true':
                try:
                        threads.append(main.Thread(fullepisode.MASTERSEARCH(search)))
                except:
                        pass
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
        if settings.getSetting('mmline') == 'true':
                try:
                        threads.append(main.Thread(mmline.MASTERSEARCH(name)))
                except:
                        pass
        if settings.getSetting('wwmf') == 'true':
                try:
                        threads.append(main.Thread(wwmf.MASTERSEARCH(name)))
                except:
                        pass
        if settings.getSetting('channelcut') == 'true':
                try:
                        threads.append(main.Thread(channelcut.MASTERSEARCH(name)))
                except:
                        pass
        if settings.getSetting('wsoeu') == 'true':
                try:
                        threads.append(main.Thread(wsoeu.MASTERSEARCH(name)))
                except:
                        pass
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
        print "####### masterPornSearch"
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

#MoovieManic modes______________________________________________________________
elif mode=='moovieManiacCategories':
        print ""+url
        mooviemaniac.CATEGORIES()

elif mode=='moovieManiacIndex':
        print ""+url
        mooviemaniac.INDEX(url)
#WatchSeries-Online modes_______________________________________________________
elif mode=='watchSeriesOnlineCategories':
        print ""+url
        wsoeu.CATEGORIES()

elif mode=='watchSeriesOnlineSeriesIndex':
        print ""+url
        wsoeu.INDEXSHOWS(url)

elif mode=='watchSeriesOnlineEpisodesIndex':
        print ""+url
        wsoeu.INDEXEPS(url,name)

elif mode=='watchSeriesOnlineVideoLinks':
        print ""+url
        wsoeu.VIDEOLINKS(url,name,thumb)

elif mode=='watchSeriesOnlineSearch':
        print ""+url
        wsoeu.SEARCH()

elif mode=='watchSeriesOnlineLetters':
        print ""+url
        wsoeu.LETTERS()

elif mode=='watchSeriesOnlineRecentEpisodes':
        print ""+url
        wsoeu.RECENTEPS(url)

#Free Movies Addict modes_______________________________________________________
elif mode=='fmaCategories':
        print ""+url
        fma.CATEGORIES()

elif mode=='fmaIndex':
        print ""+url
        fma.INDEX(url)

elif mode=='fmaVideoLinks':
        print ""+url
        fma.VIDEOLINKS(name,url,thumb)

elif mode=='fmaGenres':
        print ""+url
        fma.GENRES()

elif mode=='fmaYears':
        print ""+url
        fma.YEARS()

elif mode=='fmaLetters':
        print ""+url
        fma.LETTERS()
#Z-Movie modes__________________________________________________________________
elif mode=='zmovieIndex':
        print ""+url
        zmovie.INDEX(url)

elif mode=='zmovieLetters':
        print ""+url
        zmovie.LETTERS()

elif mode=='zmovieGenres':
        print ""+url
        zmovie.GENRES()

elif mode=='zmovieCategories':
        print ""+url
        zmovie.CATEGORIES()

elif mode=='zmovieVideoLinks':
        print ""+url
        zmovie.VIDEOLINKS(name,url,thumb)
#We Watch Movies Free___________________________________________________________
elif mode=='wwmfCategories':
        print ""+url
        wwmf.CATEGORIES()
        
elif mode=='wwmfIndex':
        print ""+url
        wwmf.INDEX(url)

elif mode=='wwmfLetters':
        print ""+url
        wwmf.LETTERS()

elif mode=='wwmfGenres':
        print ""+url
        wwmf.GENRES()

elif mode=='wwmfSearch':
        print ""+url
        wwmf.SEARCH()

elif mode=='wwmfVideoLinks':
        print ""+url
        wwmf.VIDEOLINKS(name,url,thumb)
#I-WatchOnline modes____________________________________________________________
elif mode=='iwoCategories':
        print ""+url
        iwo.MOVIE_CATEGORIES()

elif mode=='iwoSeriesCategories':
        print ""+url
        iwo.SERIES_CATEGORIES()

elif mode=='iwoSeriesGenres':
        print ""+url
        iwo.SERIES_GENRES()

elif mode=='iwoSeriesLetters':
        print ""+url
        iwo.SERIES_LETTERS()

elif mode=='iwoIndex':
        print ""+url
        iwo.MOVIE_INDEX(url)

elif mode=='iwoSeriesIndex':
        print ""+url
        iwo.SERIES_INDEX(url)

elif mode=='iwoEpisodesIndex':
        print ""+url
        iwo.EPISODES_INDEX(url,name)

elif mode=='iwoVideoLinks':
        print ""+url
        iwo.VIDEOLINKS(name,url,thumb)

elif mode=='iwoHDMovies':
        print ""+url
        iwo.HD_MOVIES()

elif mode=='iwoLetters':
        print ""+url
        iwo.LETTERS()

elif mode=='iwoHDLetters':
        print ""+url
        iwo.HD_LETTERS()

elif mode=='iwoGenres':
        print ""+url
        iwo.GENRES()

elif mode=='iwoHDGenres':
        print ""+url
        iwo.HD_GENRES()

elif mode=='iwoAction':
        print ""+url
        iwo.ACTION()

elif mode=='iwoAdventure':
        print ""+url
        iwo.ADVENTURE()

elif mode=='iwoAnimation':
        print ""+url
        iwo.ANIMATION()

elif mode=='iwoBiography':
        print ""+url
        iwo.BIOGRAPHY()

elif mode=='iwoComedy':
        print ""+url
        iwo.COMEDY()

elif mode=='iwoCrime':
        print ""+url
        iwo.CRIME()

elif mode=='iwoDocumentary':
        print ""+url
        iwo.DOCUMENTARY()

elif mode=='iwoDrama':
        print ""+url
        iwo.DRAMA()

elif mode=='iwoFamily':
        print ""+url
        iwo.FAMILY()

elif mode=='iwoFantasy':
        print ""+url
        iwo.FANTASY()

elif mode=='iwoFilmNoir':
        print ""+url
        iwo.FILMNOIR()

elif mode=='iwoHistory':
        print ""+url
        iwo.HISTORY()

elif mode=='iwoHorror':
        print ""+url
        iwo.HORROR()

elif mode=='iwoMusic':
        print ""+url
        iwo.MUSIC()

elif mode=='iwoMusical':
        print ""+url
        iwo.MUSICAL()

elif mode=='iwoMystery':
        print ""+url
        iwo.MYSTERY()

elif mode=='iwoNews':
        print ""+url
        iwo.NEWS()

elif mode=='iwoRomance':
        print ""+url
        iwo.ROMANCE()

elif mode=='iwoSciFi':
        print ""+url
        iwo.SCIFI()

elif mode=='iwoShort':
        print ""+url
        iwo.SHORT()

elif mode=='iwoSport':
        print ""+url
        iwo.SPORT()

elif mode=='iwoThriller':
        print ""+url
        iwo.THRILLER()

elif mode=='iwoWar':
        print ""+url
        iwo.WAR()

elif mode=='iwoWestern':
        print ""+url
        iwo.WESTERN()


elif mode=='iwoHDAction':
        print ""+url
        iwo.HD_ACTION()

elif mode=='iwoHDAdventure':
        print ""+url
        iwo.HD_ADVENTURE()

elif mode=='iwoHDAnimation':
        print ""+url
        iwo.HD_ANIMATION()

elif mode=='iwoHDBiography':
        print ""+url
        iwo.HD_BIOGRAPHY()

elif mode=='iwoHDComedy':
        print ""+url
        iwo.HD_COMEDY()

elif mode=='iwoHDCrime':
        print ""+url
        iwo.HD_CRIME()

elif mode=='iwoHDDocumentary':
        print ""+url
        iwo.HD_DOCUMENTARY()

elif mode=='iwoHDDrama':
        print ""+url
        iwo.HD_DRAMA()

elif mode=='iwoHDFamily':
        print ""+url
        iwo.HD_FAMILY()

elif mode=='iwoHDFantasy':
        print ""+url
        iwo.HD_FANTASY()

elif mode=='iwoHDFilmNoir':
        print ""+url
        iwo.HD_FILMNOIR()

elif mode=='iwoHDHistory':
        print ""+url
        iwo.HD_HISTORY()

elif mode=='iwoHDHorror':
        print ""+url
        iwo.HD_HORROR()

elif mode=='iwoHDMusic':
        print ""+url
        iwo.HD_MUSIC()

elif mode=='iwoHDMusical':
        print ""+url
        iwo.HD_MUSICAL()

elif mode=='iwoHDMystery':
        print ""+url
        iwo.HD_MYSTERY()

elif mode=='iwoHDNews':
        print ""+url
        iwo.HD_NEWS()

elif mode=='IwoHDRomance':
        print ""+url
        iwo.HD_ROMANCE()

elif mode=='iwoHDSciFi':
        print ""+url
        iwo.HD_SCIFI()

elif mode=='iwoHDShort':
        print ""+url
        iwo.HD_SHORT()

elif mode=='iwoHDSport':
        print ""+url
        iwo.HD_SPORT()

elif mode=='iwoHDThriller':
        print ""+url
        iwo.HD_THRILLER()

elif mode=='iwoHDWar':
        print ""+url
        iwo.HD_WAR()

elif mode=='iwoHDWestern':
        print ""+url
        iwo.HD_WESTERN()

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
#TubePirate Modes_______________________________________________________________
elif mode=='tubePirateCategories':
        print ""+url
        tubepirate.CATEGORIES()

elif mode=='tubePirateIndex':
        print ""+url
        tubepirate.INDEX(url)

elif mode=='tubePirateMostViewed':
        print ""+url
        tubepirate.MOST_VIEWED()

elif mode=='tubePirateTopRated':
        print ""+url
        tubepirate.TOP_RATED()

elif mode=='tubePirateActors':
        print ""+url
        tubepirate.ACTORS()

elif mode=='tubePirateLetters':
        print ""+url
        tubepirate.LETTERS()

elif mode=='tubePirateTopRatedActors':
        print ""+url
        tubepirate.TOP_RATED_ACTORS()

elif mode=='tubePirateMostViewedActors':
        print ""+url
        tubepirate.MOST_VIEWED_ACTORS()

elif mode=='tubePirateMostActorIndex':
        print ""+url
        tubepirate.ACTOR_INDEX(url)

elif mode=='tubePirateGenres':
        print ""+url
        tubepirate.GENRES()
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


#ChannelCut Modes_______________________________________________________________
elif mode=='channelCutIndex':
        print ""+url
        channelcut.INDEX(url)

elif mode=='channelCutCategories':
        print ""+url
        channelcut.CATEGORIES()

elif mode=='channelCutLetters':
        print ""+url
        channelcut.LETTERS()

elif mode=='channelCutEpisodes':
        print ""+url
        channelcut.EPISODES(url)

elif mode=='channelCutRecentEpisodes':
        print ""+url
        channelcut.RECENTEPISODES(url)

elif mode=='channelCutVideoLinks':
        print ""+url
        channelcut.VIDEOLINKS(name,url)

elif mode=='channelCutNum':
        print ""+url
        channelcut.NUM()

elif mode=='channelCutA':
        print ""+url
        channelcut.A()

elif mode=='channelCutB':
        print ""+url
        channelcut.B()

elif mode=='channelCutC':
        print ""+url
        channelcut.C()

elif mode=='channelCutD':
        print ""+url
        channelcut.D()

elif mode=='channelCutE':
        print ""+url
        channelcut.E()

elif mode=='channelCutF':
        print ""+url
        channelcut.F()

elif mode=='channelCutG':
        print ""+url
        channelcut.G()

elif mode=='channelCutH':
        print ""+url
        channelcut.H()

elif mode=='channelCutI':
        print ""+url
        channelcut.I()

elif mode=='channelCutJ':
        print ""+url
        channelcut.J()

elif mode=='channelCutK':
        print ""+url
        channelcut.K()

elif mode=='channelCutL':
        print ""+url
        channelcut.L()

elif mode=='channelCutM':
        print ""+url
        channelcut.M()

elif mode=='channelCutN':
        print ""+url
        channelcut.N()

elif mode=='channelCutO':
        print ""+url
        channelcut.O()

elif mode=='channelCutP':
        print ""+url
        channelcut.P()

elif mode=='channelCutQ':
        print ""+url
        channelcut.Q()

elif mode=='channelCutR':
        print ""+url
        channelcut.R()

elif mode=='channelCutS':
        print ""+url
        channelcut.S()

elif mode=='channelCutT':
        print ""+url
        channelcut.T()

elif mode=='channelCutU':
        print ""+url
        channelcut.U()

elif mode=='channelCutV':
        print ""+url
        channelcut.V()

elif mode=='channelCutW':
        print ""+url
        channelcut.W()

elif mode=='channelCutX':
        print ""+url
        channelcut.X()

elif mode=='channelCutY':
        print ""+url
        channelcut.Y()

elif mode=='channelCutZ':
        print ""+url
        channelcut.Z()

elif mode=='channelCutSearch':
        print ""+url
        channelcut.SEARCH()

#Filmikz Modes____________________________________________________________________
elif mode=='filmikzAdultCategories':
        print ""+url
        filmikz.ADULT_CATEGORIES()

elif mode=='filmikzAdultIndex':
        print ""+url
        filmikz.ADULT_INDEX(url)

elif mode=='filmikzVideoLinks':
        print ""+url
        filmikz.VIDEOLINKS(url,name,thumb)

elif mode=='filmikzAdultSearch':
        print ""+url
        filmikz.ADULT_SEARCH()
#Epornik Modes__________________________________________________________________
elif mode=='epornikCategories':
        print ""+url
        epornik.CATEGORIES()

elif mode=='epornikIndex':
        print ""+url
        epornik.INDEX(url)

elif mode=='epornikSearch':
        print ""+url
        epornik.SEARCH()

#Full Episode Modes___________________________________________________________
elif mode=='fullEpisodeCategories':
        print ""+url
        fullepisode.CATEGORIES()

elif mode=='fullEpisodeIndex':
        print ""+url
        fullepisode.INDEX(url)

elif mode=='fullEpisodeVideoLinks':
        print ""+url
        fullepisode.VIDEOLINKS(url,name,thumb)

elif mode=='fullEpisodeSearch':
        print ""+url
        fullepisode.SEARCH()
#ToonJet Modes_________________________________________________________________
elif mode=='toonJetCategories':
        print ""+url
        toonjet.CATEGORIES()

elif mode=='toonJetIndex':
        print ""+url
        toonjet.INDEX(url)

#botz modes__________________________________________________________________
#botz modes__________________________________________________________________
elif mode=='botzCategories':
        print ""+url
        botz.CATEGORIES()

elif mode=='botzIndex':
        print ""+url
        botz.INDEX(url)

elif mode=='botzGenres':
        print ""+url
        botz.GENRES()

elif mode=='botzSearch':
        print ""+url
        botz.SEARCH()

elif mode=='botzSearchindex':
        print ""+url
        botz.SEARCHINDEX(url)

elif mode=='botzVideoLinks':
        print ""+url
        botz.VIDEOLINKS(name,url,thumb)

xbmcplugin.endOfDirectory(int(sys.argv[1]))

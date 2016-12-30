import sys,os
import xbmc
import xbmcplugin
import xbmcaddon
from resources.modules import common

PLUGIN_NAME = "mediaroot"

__settings__ = xbmcaddon.Addon(id="plugin.video." + PLUGIN_NAME)
__language__ = __settings__.getLocalizedString

class cConfig:

    def __check(self):
        try:
            import xbmcaddon           
            self.__bIsDharma = True            
        except ImportError:
            self.__bIsDharma = False

    def __init__(self):
        self.__check()

        if (self.__bIsDharma):
            import xbmcaddon
            self.__oSettings = xbmcaddon.Addon(common.addonID)
            self.__aLanguage = self.__oSettings.getLocalizedString


    def isDharma(self):
        return self.__bIsDharma
        

    def showSettingsWindow(self):
        if (self.__bIsDharma):
            self.__oSettings.openSettings()
        else:
            try:		
                xbmcplugin.openSettings( sys.argv[ 0 ] )
            except:
                pass

    def getSetting(self, sName):
        if (self.__bIsDharma):
            return self.__oSettings.getSetting(sName)
        else:
            try:                
                return xbmcplugin.getSetting(sName)
            except:
                return ''

    def getLocalizedString(self, sCode):
        if (self.__bIsDharma):
            return self.__aLanguage(sCode)
        else:
            try:		
                 return xbmc.getLocalizedString(sCode)
            except:
                return ''

def get_data_path():
    dev = xbmc.translatePath(__settings__.getAddonInfo('Profile'))

    if not os.path.exists(dev):
        os.makedirs(dev)

    return dev
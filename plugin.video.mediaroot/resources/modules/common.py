import xbmcaddon

addonID = 'plugin.video.mediaroot'
addon = xbmcaddon.Addon(id = addonID)
addonPath = addon.getAddonInfo('path')
profilePath = addon.getAddonInfo('profile')
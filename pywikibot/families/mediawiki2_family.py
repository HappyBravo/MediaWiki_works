# THIS IS JUST AN EXAMPLE
# CHECKOUT https://www.mediawiki.org/wiki/Manual:Pywikibot/Use_on_third-party_wikis FOR MORE DETAILS

 # -*- coding: utf-8  -*-

from pywikibot import family

# The official Mozilla Wiki. #Put a short project description here.

class Family(family.Family):

    name = 'mediawiki2' # Set the family name; this should be the same as in the filename.
    langs = {
        'en': 'localhost', # Put the hostname here.
    }

    def version(self, code):
        return "1.39.3"  # The MediaWiki version used.
                        # Not very important in most cases. Needed for older versions

    def scriptpath(self, code):
        return '' # The relative path of index.php, api.php : look at your wiki address.
# This line may need to be changed to /wiki or /w,
# depending on the folder where your mediawiki program is located.
# Note: Do not _include_ index.php, etc.

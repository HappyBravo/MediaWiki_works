# MediaWiki_works
An attempt to make uploaded PDFs searchable on MediaWiki.

----

## REQUIREMENTS
- [CirrusSearch](https://www.mediawiki.org/wiki/Extension:CirrusSearch)
  - [Setup Instructions](https://github.com/wikimedia/mediawiki-extensions-CirrusSearch)
- [PDFHandler](https://www.mediawiki.org/wiki/Extension:PdfHandler)
- [OCRmyPDF](https://pypi.org/project/ocrmypdf/)
- [pywikibot](https://github.com/wikimedia/pywikibot)
- [watchdog](https://pypi.org/project/watchdog/)

---

Run [```watcher.py```](watcher.py) to automatically upload files on the server.

---

Configure [this](https://github.com/HappyBravo/MediaWiki_works/blob/main/MW_pybot.py#L36) according to your wiki site before using.

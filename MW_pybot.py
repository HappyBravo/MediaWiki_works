# IMPORTING LIBRARIES

import os
from pathlib import Path
import pywikibot
from OCR_worker.pdftotext import convert_pdf_to_text, extract_text # IMPORTING PYTHON SCRIPTs WHICH ADDS A TEXT LAYER

# DEFINING FUNCTIONS

def check_MIME_pdf(file_name):
    '''
    FOR HANDLING ERROR FOR FILENAMES LIKE  "OO_No._45_dt._09.05.2023.pdf"  
    GIVES ERROR >>> "verification-error: File extension ".2023" does not match the detected MIME type of the file (application/pdf)."
    '''
    _file_name = ''
    isChanged = False

    _file_name = file_name[:-4]  # EXCLUDING '.pdf' EXTENSION 
    _file_name = _file_name.replace('.', '')
    _file_name = _file_name+'.pdf'
    isChanged = _file_name != file_name

    return (_file_name, isChanged)


def upload_pdf_files(file_path, wiki_url, username, password, addSummary = False, summary=' '):
    '''
    UPLOADS ALL PDF FILES FROM A DIRECTORY
    TO MEDIAWIKI WITH AN OCR TEXT LAYER

    IF addSummary is True,
        if USER PROVIDES SOME SUMMARY THEN IT ADDS THAT IN THE COMMENT SECION,
        ELSE, IT SCRAPS THE TEXT FROM PDF   AND ADDS THE TEXT IN THE COMMENT SECTION
    '''

    site = pywikibot.Site(user=username, code="en", fam="mediawiki2") # DEPENDING ON HOW YOU HAVE CONFIGURED YOUR MEDIAWIKI, 'code' AND 'fam' CAN TAKE DIFFERENT VALUES
                                                                     # VISIT : https://www.mediawiki.org/wiki/Manual:Pywikibot/Use_on_third-party_wikis
                                                                     # GENERALLY THE CUSTOM WIKI FOLDER IS AT ~/[PYWIKIBOT INSTALL PATH]pywikibot/pywikibot/families ON THE DEVICE

    if password == None:
        site.login() # IN THIS METHOD PASSWORD IS ASKED BY PYWIKIBOT DURING RUNTIME. 
    else:
        logg = pywikibot.login.LoginManager(password = password, site = site, user = username)
        # print(logg)
        # input()

    for file_name in os.listdir(file_path):
        if file_name.endswith('.pdf'):
            (new_file_name, isChanged) = check_MIME_pdf(file_name)
            
            print("processing ", {file_name})

            _file_path = file_path
            ffile_path = os.path.join(file_path, file_name)

            if isChanged:
                file_name = new_file_name

            output_file = "new/ocr_"+file_name     # SAVES FILE IS new DIRECTORY
            output_file_path = os.path.join(_file_path, output_file)
            
            convert_pdf_to_text(pdf_file=ffile_path, output_file=output_file_path)

            print("Text Layer Added")

            page_name = file_name[:-4]  # Remove the '.pdf' extension from the file name

            
            if addSummary:
                if len(summary) < 2:
                    textt = extract_text(output_file_path)
                    summary = " \n ".join([textt[page] for page in range(len(textt))])
                    
                print(f"Summary = \n{summary}")

            page = pywikibot.FilePage(site, page_name)
            
            try:
                page.upload(output_file_path, ignore_warnings=True, comment=summary)
            except Exception as e:
                print(e)
    site.logout()
    

# REQUIRED INFO FOR LOGIN AND FILE PATH
# Provide the necessary information here
## DEFAULTS
file_path = './PDFs'  # Path to the folder containing PDF files
wiki_url = 'http://localhost'  # URL of your local MediaWiki server
username = 'YOUR USERNAME'  # Your MediaWiki username
password = None         # YOUR PASSWORD 

def main_uploader(
        file_path = file_path, 
        wiki_url = wiki_url, 
        username = username, 
        password = password,
        addSummary = False, 
        summary = ' ' 
        ):
    
    # summary_buffer = "TESTINF SUMMARY. SOme random text for summary."
    # add_summ = True
    # summary_buffer = ''
    # add_summ = False
    
    # UPLOAD
    upload_pdf_files(file_path = file_path, wiki_url = wiki_url, username = username,password = password, addSummary = addSummary, summary = summary)



if __name__ ==  '__main__':
    main_uploader()
    print("Done")

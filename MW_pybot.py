# IMPORTING LIBRARIES

import os
from pathlib import Path
import pywikibot
# from pywikibot.data.api import LoginManager
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

    site = pywikibot.Site(user=username,fam="mediawiki2", code="en") # DEPENDING ON HOW YOU HAVE CONFIGURED YOUR MEDIAWIKI, 'code' AND 'fam' CAN TAKE DIFFERENT VALUES
                                                                     # VISIT : https://www.mediawiki.org/wiki/Manual:Pywikibot/Use_on_third-party_wikis
                                                                     # GENERALLY THE CUSTOM WIKI FOLDER IS AT ~/[PYWIKIBOT INSTALL PATH]pywikibot/pywikibot/families ON THE DEVICE
    print("Trying to Login")
    if password == None:
        message = "Password will be asked by pywikibot as an Input"
        print(message)
        try :
            site.login() # IN THIS METHOD PASSWORD IS ASKED BY PYWIKIBOT DURING RUNTIME. 
        except Exception as e:
            print("Login error 1 :", e)
    else:
        try :
            logg = pywikibot.login.LoginManager(password = password, site = site, user = username)
            # logg.login()
        except Exception as e:
            print("Login error 2 :", e)
    
        # print(logg)
        # input()

    print("Checking if correctly logged in")
    login_flagg = 0 # if login_flagg == 3, IT MEANS USER IS LOGGED IN, IS NOT None AND HAS RIGHT TO UPLOAD.
    print(site.logged_in())
    # input()

    if site.logged_in():
        print("User is logged in\nChecking info ...")
        login_flagg += 1

        u_info = site.userinfo
        # print(u_info['name'])
        # print(u_info['rights'])

        mess_str = ""
        if u_info['name'] != None :
            mess_str += f"{u_info['name']} is logged in, "
            login_flagg += 1
            if 'upload' in u_info['rights']:
                mess_str += "and has right to upload."
                login_flagg += 1
            else:
                mess_str += "but does not has right to upload."
        else:
            mess_str += f"Not logged in as correct user. It is logged in as {u_info['name']}."
        
        print(mess_str)
 
    # input()
    if login_flagg != 3:
        '''
        NOT TO INITIATE THE PROCESSING AND UPLOADING TASK IF NOT CORRECTLY LOGGED IN
        '''

        print("Something is wrong with login !!! \n Try again !!!")
        return 0 
    
    for file_name in os.listdir(file_path):
        if file_name.endswith('.pdf'): # ONLY UPLOAD PDFs FROM THIS SCRIPT
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
                print("Error while uploading on MediaWiki, \n --- with Error :", e)
    
    # site.logout()
    return 1
    

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
    # print("Username: ", username)
    # print("Password: ", password)

    return upload_pdf_files(file_path = file_path, wiki_url = wiki_url, username = username,password = password, addSummary = addSummary, summary = summary)



if __name__ ==  '__main__':
    main_uploader()
    print("Done")

import ocrmypdf
import PyPDF2

def convert_pdf_to_text(pdf_file, output_file): 
    '''
    PERFORMS OCR 
    AND ADDS A TEXT LAYER

    TAKES - INPUT FILE LOCATION/NAME, OUTPUT PDF FILE LOCATION/NAME
    '''
    ocrmypdf.ocr(pdf_file, output_file, skip_text= True)

def extract_text(pdf_obj):
    '''
    EXTRACTS THE TEXT FROM THE PDF,
    THIS FUNCTION DO NOT DO OCR !

    RETURNS THE TEXT EXTRACTED FROM THE PDF
    '''
    pdfObj = open(pdf_obj, "rb")
    pdfReader = PyPDF2.PdfReader(pdfObj)
    textt = {} # PAGENO : TEXT IN THAT PAGE
    for i in range(len(pdfReader.pages)):
        textt[i] = pdfReader.pages[i].extract_text()
    return textt


    ###############
    ### TESTING ###
    ###############

if __name__ == "__main__":
    normal_pdf = "./test_pdf.pdf" # NORMAL PDF
    normal_out_pdf = "normal_converted.pdf"

    image_pdf = "./3.pdf" # IMAGE IN PDF, NEED OCR
    image_out_pdf = "image_comverted.pdf" # IMAGE IN PDF, CONVERTED

    oo_pdf = "./OfficeOrder_example.pdf" # IMAGE IN PDF, NEED OCR
    oo_out_pdf = "oo_converted.pdf" # OFFICE ORDER CONVERTED

    convert_pdf_to_text(normal_pdf, normal_out_pdf)
    print(extract_text(normal_out_pdf)[0])

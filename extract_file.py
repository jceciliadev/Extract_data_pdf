import pytesseract
from pytesseract import image_to_string
from PIL import Image
from io import StringIO
from tika import parser
from PIL.ExifTags import TAGS
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

path_img = "/home/shanks/Documentos/AppZurich/Docs/Traducir/IMG_Traducir/preview.jpg"
path_pdfs = '../data_pdf/data'
image_list = []
def load_data_img(path_img):
    '''Metodo de carga de IMG para extraer datos de una IMG
    @path_img : parametro de entrada de la img.
    '''
    image = Image.open(path_img)
    exifdata = image.getexif()
    for tag_id in exifdata:
        # get the tag name, instead of human unreadable tag id
        print(tag_id)
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        # decode bytes
        if isinstance(data, bytes):
            data = data.decode()
        print(f"{tag:25}: {data}")



def load_data_pytesseract():
    pytesseract.pytesseract.tesseract_cmd = r'/home/shanks/Documentos/AppZurich/Docs/Traducir/IMG_Traducir'
    texts = [pytesseract.image_to_string('/home/shanks/Documentos/AppZurich/Docs/Traducir/IMG_Traducir/*.jpeg',lang = 'eng',
                                         config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789') for img in image_list]
    for text in texts:
        print(text)


def load_data_pdf(path_pdfs):

    file = path_pdfs
    file_data = parser.from_file(file)
    text = file_data['content']


def convert_pdf_to_string(file_path):
    output_string = StringIO()
    with open(file_path, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

    return (output_string.getvalue())


def convert_title_to_filename(title):
    filename = title.lower()
    filename = filename.replace(' ', '_')
    return filename


def split_to_title_and_pagenum(table_of_contents_entry):
    title_and_pagenum = table_of_contents_entry.strip()

    title = None
    pagenum = None

    if len(title_and_pagenum) > 0:
        if title_and_pagenum[-1].isdigit():
            i = -2
            while title_and_pagenum[i].isdigit():
                i -= 1

            title = title_and_pagenum[:i].strip()
            pagenum = int(title_and_pagenum[i:].strip())

    return title, pagenum
#print(pytesseract.image_to_string(r'/home/shanks/Documentos/AppZurich/Docs/Traducir/IMG_Traducir/preview.jpg'))


